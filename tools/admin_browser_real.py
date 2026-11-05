"""Read-only real admin UI acceptance with legitimate login and an isolated server."""
import argparse
import asyncio
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time

import httpx
from dotenv import dotenv_values
from playwright.async_api import async_playwright, expect

from tools.admin_reads_remote import Probe, main
from tools.real_login_measurement import stop_process_tree
from tools.performance_probe import safe_endpoint

ROOT = Path(__file__).resolve().parents[1]


async def validate(probe):
    expect.set_options(timeout=90000)
    private = ROOT / '.local/admin-browser-20261104'
    private.mkdir(exist_ok=True)
    config = dotenv_values(ROOT / '.env')
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 3035))
    stats = {'requests': [], 'injected_failures': 0, 'rate_limits': 0}
    fault = [False]
    slot, last = threading.Lock(), [0.0]

    class Proxy(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            group = self.path.split('/')[1]
            if group not in ('auth', 'social'):
                self.send_error(404)
                return
            path = self.path[len('/' + group):]
            if path.split('?')[0] not in ('/auth/me', '/admin/dashboard', '/admin/users', '/admin/catalog', '/admin/reports'):
                self.send_error(403)
                return
            if self.headers.get('Authorization') != 'Bearer ' + probe.token:
                self.send_error(403)
                return
            with slot:
                time.sleep(max(0, 3.1 - (time.monotonic() - last[0])))
                last[0] = time.monotonic()
                if fault[0] and path.split('?')[0] == '/admin/dashboard':
                    fault[0] = False
                    stats['injected_failures'] += 1
                    status, content = 503, b'{"message":"Servico indisponivel no ensaio controlado."}'
                else:
                    base = config['XANO_AUTH_URL' if group == 'auth' else 'XANO_SOCIAL_URL'].rstrip('/')
                    with httpx.Client(timeout=30, follow_redirects=False) as client:
                        response = client.get(base + path, headers={'Authorization': 'Bearer ' + probe.token})
                    status, content = response.status_code, response.content
                    stats['rate_limits'] += status == 429
                stats['requests'].append({'endpoint': safe_endpoint(path), 'status': status})
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            try:
                self.wfile.write(content)
            except OSError:
                pass

    proxy = ThreadingHTTPServer(('127.0.0.1', 0), Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    frontend = ROOT / '.local/frontends/status-real-15580'
    env = dict(os.environ, XANO_AUTH_URL=f'http://127.0.0.1:{proxy.server_port}/auth',
               XANO_SOCIAL_URL=f'http://127.0.0.1:{proxy.server_port}/social',
               REFLEX_WEB_WORKDIR=str(frontend), REFLEX_USE_NPM='true',
               REFLEX_STATE_MANAGER_MODE='memory', COOKIE_SECURE='false',
               REFLEX_APP_MODULE_IMPORT='tools.list_status_browser_app')
    process = None
    probe.report.update(layer='real_admin_browser_paced_read_only_proxy', cases=[],
                        proxy_min_interval_seconds=3.1, normal_server_modified=False)
    probe.save()
    try:
        with (private / 'server.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen([sys.executable, '-m', 'reflex', 'run', '--env', 'prod', '--single-port',
                '--frontend-port', '3035', '--backend-port', '3035'], cwd=ROOT, env=env,
                stdout=log, stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            for _ in range(240):
                if process.poll() is not None:
                    raise RuntimeError('Isolated production startup failed')
                try:
                    async with httpx.AsyncClient(timeout=1) as client:
                        response = await client.get('http://127.0.0.1:3035/admin/login/')
                    if response.status_code == 200:
                        break
                except httpx.RequestError:
                    pass
                await asyncio.sleep(1)
            else:
                raise TimeoutError('Isolated server readiness')
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(channel='msedge', headless=True)
                try:
                    for width in (1440, 390):
                        context = await browser.new_context(viewport={'width': width, 'height': 900})
                        try:
                            await context.add_cookies([{'name': 'codeboxd_auth', 'value': probe.token,
                                'url': 'http://localhost:3035', 'sameSite': 'Lax'}])
                            page = await context.new_page()
                            errors = []
                            page.on('pageerror', lambda error: errors.append(type(error).__name__))
                            await page.goto('http://localhost:3035/admin/')
                            await expect(page.get_by_role('heading', name='Dashboard', exact=True)).to_be_visible()
                            await expect(page.locator('.admin-metric-value').first).to_have_text(__import__('re').compile(r'\d+'))
                            values = await page.locator('.admin-metric-value').all_text_contents()
                            fault[0] = True
                            await page.get_by_role('button', name='Atualizar', exact=True).click()
                            await expect(page.get_by_role('alert')).to_be_visible()
                            if await page.locator('.admin-metric-value').all_text_contents() != values:
                                raise AssertionError('Dashboard discarded confirmed totals on failure')
                            for label, loading in [('Usuários', 'Carregando usuários…'), ('Filmes', 'Carregando catálogo…'),
                                                   ('Séries', 'Carregando catálogo…'), ('Livros', 'Carregando catálogo…'),
                                                   ('Animes', 'Carregando catálogo…'), ('Reports', 'Carregando reports…')]:
                                probe.report['phase'] = label + '_' + str(width)
                                probe.save()
                                await page.locator('.admin-sidebar').get_by_role('link', name=label, exact=True).click()
                                await expect(page.get_by_role('heading', name=label, exact=True)).to_be_visible()
                                if label in ('Filmes', 'Séries', 'Livros', 'Animes'):
                                    search_button = page.get_by_role('button', name='Pesquisar', exact=True)
                                    await expect(search_button).to_be_disabled()
                                    await expect(search_button).to_be_enabled()
                                if label == 'Usuários':
                                    search = page.get_by_label('Buscar por nome, usuário ou ID')
                                    await search.fill('cb_absent_20261104_7fa56e31')
                                    await page.get_by_role('button', name='Pesquisar', exact=True).click()
                                    await expect(page.get_by_text('Nenhuma conta encontrada para esta pesquisa.', exact=True)).to_be_visible()
                                elif label in ('Filmes', 'Séries', 'Livros', 'Animes'):
                                    await page.get_by_label('Pesquisar título').fill('cb_absent_20261104_7fa56e31')
                                    await page.get_by_role('button', name='Pesquisar', exact=True).click()
                                    await expect(page.get_by_text('Nenhuma obra encontrada para esta pesquisa.', exact=True)).to_be_visible()
                                else:
                                    await expect(page.get_by_text(loading, exact=True)).not_to_be_visible()
                                if await page.evaluate('document.documentElement.scrollWidth > innerWidth'):
                                    raise AssertionError('Horizontal overflow')
                            if errors:
                                raise AssertionError('JavaScript errors')
                            await page.screenshot(path=str(private / f'admin-{width}.png'), full_page=True)
                            probe.report['cases'].append({'width': width, 'passed': True,
                                'sections': 7, 'empty_searches': 5, 'injected_dashboard_error_preserved_values': True})
                            probe.save()
                        except Exception as exc:
                            try:
                                await page.screenshot(path=str(private / f'failure-{width}.png'), full_page=True)
                                (private / 'failure.txt').write_text(str(exc) + '\n' + await page.locator('body').inner_text(), encoding='utf-8')
                            except Exception:
                                pass
                            raise
                        finally:
                            await context.close()
                finally:
                    await browser.close()
        probe.report['passed'] = len(probe.report['cases']) == 2 and stats['rate_limits'] == 0
    finally:
        if process is not None:
            stop_process_tree(process)
        proxy.shutdown()
        proxy.server_close()
        probe.report.update(stats)
        probe.save()


class BrowserProbe(Probe):
    login_notice = 'Valida a interface administrativa real em desktop/celular. Somente leituras; falha de dashboard injetada localmente.'

    def run(self):
        self.paged('reports_queue', '/admin/reports')
        asyncio.run(validate(self))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.output, probe_type=BrowserProbe)))
