"""Real browser acceptance using disposable users and the actual Xano backend."""
import asyncio
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import socket
import sys
import threading
import time
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values
from playwright.async_api import async_playwright, expect

from tools.isolated_frontend import prepare_frontend
from tools.list_status_migration import PRIVATE
from tools.real_login_measurement import stop_process_tree

ROOT = Path(__file__).resolve().parents[1]


async def main(frontend_workdir=None, private_dir=None, output=None):
    expect.set_options(timeout=120000)
    private = private_dir.resolve() if private_dir else PRIVATE
    if not private.is_relative_to((ROOT / '.local').resolve()):
        raise ValueError('Private artifacts must stay under .local')
    with socket.socket() as port_check:
        port_check.bind(('127.0.0.1', 3035))
    config = dotenv_values(ROOT / '.env')
    journal = json.loads((private / 'live-journal.json').read_text(encoding='utf-8'))
    users = journal['test_users']
    if len(users) != 2 or not (journal.get('real-final_passed') or journal.get('browser_fixture_ready')):
        raise ValueError('Final API acceptance and two disposable sessions required')
    a, b = users
    mid = journal['fixture_media_ids'][0]
    allowed_tokens = {user['token'] for user in users}
    slot = threading.Lock()
    last_call = [0.0]
    stats = {'requests': 0, 'rate_limits': 0, 'responses': []}

    class Proxy(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def do_GET(self): self.forward()
        def do_POST(self): self.forward()
        def do_PUT(self): self.forward()
        def do_DELETE(self): self.forward()

        def forward(self):
            group = self.path.split('/')[1]
            if group not in ('auth', 'social'):
                self.send_error(404)
                return
            token = self.headers.get('Authorization', '').removeprefix('Bearer ')
            base = config['XANO_AUTH_URL' if group == 'auth' else 'XANO_SOCIAL_URL'].rstrip('/')
            path = self.path[len('/' + group):]
            body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            fixture_login = False
            if group == 'auth' and path == '/auth/login' and self.command == 'POST':
                submitted = json.loads(body)
                fixture_login = any(submitted.get('email') == u['email'] and submitted.get('password') == u['password'] for u in users)
            if self.command != 'GET' and token not in allowed_tokens and not fixture_login:
                self.send_error(403)
                return
            headers = {key: self.headers[key] for key in ('Authorization', 'Content-Type', 'Accept') if key in self.headers}
            with slot:
                time.sleep(max(0, 2.4 - (time.monotonic() - last_call[0])))
                last_call[0] = time.monotonic()
                with httpx.Client(timeout=30, follow_redirects=False) as client:
                    response = client.request(self.command, base + path, headers=headers, content=body)
                if fixture_login and response.status_code == 200:
                    new_token = response.json().get('authToken')
                    if isinstance(new_token, str) and new_token:
                        allowed_tokens.add(new_token)
                stats['requests'] += 1
                stats['rate_limits'] += response.status_code == 429
                stats['responses'].append({'method': self.command, 'path': path.split('?')[0], 'status': response.status_code})
            self.send_response(response.status_code)
            self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
            self.send_header('Content-Length', str(len(response.content)))
            self.end_headers()
            try: self.wfile.write(response.content)
            except OSError: pass

    proxy = ThreadingHTTPServer(('127.0.0.1', 0), Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    if frontend_workdir:
        frontend = frontend_workdir.resolve()
        if not frontend.is_relative_to((ROOT/'.local/frontends').resolve()) or not frontend.is_dir():
            raise ValueError('Use only an isolated frontend under this workspace')
    else:
        frontend = prepare_frontend('status-real-' + str(os.getpid()))
    env = dict(os.environ, XANO_AUTH_URL=f'http://127.0.0.1:{proxy.server_port}/auth',
               XANO_SOCIAL_URL=f'http://127.0.0.1:{proxy.server_port}/social',
               REFLEX_WEB_WORKDIR=str(frontend), REFLEX_USE_NPM='true',
               REFLEX_STATE_MANAGER_MODE='memory', COOKIE_SECURE='false',
               DEFAULT_LIST_IDENTITY_ENABLED='true',
               REFLEX_APP_MODULE_IMPORT='tools.list_status_browser_app',
               TMDB_READ_TOKEN='', DEEPL_API_KEY='')
    report = {'layer': 'browser_real_xano_paced_proxy', 'passed': False, 'cases': [],
              'transport_timeout_seconds': 60, 'proxy_min_interval_seconds': 2.4,
              'normal_server_modified': False}
    output = output or ROOT / 'openspec/changes/corrigir-conexoes-feed-listas/validation/browser-real-2026-11-03.json'
    if output.exists():
        raise FileExistsError('Preserve previous browser evidence; choose a new output')
    process = None
    with (private / 'browser-server.log').open('w', encoding='utf-8') as log:
        try:
            process = subprocess.Popen([sys.executable, '-m', 'reflex', 'run', '--env', 'prod', '--single-port',
                '--frontend-port', '3035', '--backend-port', '3035'], cwd=ROOT, env=env,
                stdout=log, stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            print('STARTING_ISOLATED_PRODUCTION_3035', flush=True)
            for _ in range(240):
                if process.poll() is not None:
                    raise RuntimeError('Production process exited')
                try:
                    async with httpx.AsyncClient(timeout=1) as client:
                        response = await client.get('http://127.0.0.1:3035/login/')
                    if response.status_code == 200: break
                except httpx.RequestError: pass
                await asyncio.sleep(1)
            else: raise TimeoutError('Production startup')
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(channel='msedge', headless=True)
                try:
                    for width in (1440, 390):
                        context = await browser.new_context(viewport={'width': width, 'height': 900})
                        page = await context.new_page()
                        errors = []
                        error_messages = []
                        page.on('pageerror', lambda err: errors.append(type(err).__name__))
                        page.on('pageerror', lambda err: error_messages.append(str(err)))
                        local_failures = []
                        page.on('response', lambda response: local_failures.append({'path':urlsplit(response.url).path,'status':response.status}) if response.status>=400 else None)
                        page.set_default_timeout(120000)
                        report['phase'] = 'fixture_login_' + str(width)
                        await page.goto('http://localhost:3035/login/')
                        await page.locator('input[name=email]').fill(a['email'])
                        await page.locator('input[name=password]').fill(a['password'])
                        await page.get_by_role('button',name='Entrar',exact=True).click()
                        await page.wait_for_url('**/conta*',timeout=120000)
                        await expect(page.locator('.profile-identity h2')).to_be_visible()
                        if width == 1440:
                            report['phase'] = 'profile_follow'
                            await page.locator('a[href="/comunidade"]').first.click()
                            await page.locator(f"a[href='/perfil/{b['id']}']").first.click()
                            follow = page.get_by_role('button', name='Seguir', exact=True)
                            await expect(follow).to_be_enabled()
                            await follow.click()
                            await expect(page.get_by_role('button', name='Deixar de seguir', exact=True)).to_be_enabled()
                            await page.locator('a[href="/feed"]').first.click()
                            report['phase'] = 'followed_feed'
                            await expect(page.locator('.post-card').first).to_be_visible()
                            report['cases'].append({'case': 'new_reader_follow_and_feed', 'width': width, 'passed': True})
                            print(json.dumps(report['cases'][-1]), flush=True)
                        report['phase'] = 'media_' + str(width)
                        await page.locator('a[href="/conta"]').first.click()
                        await page.locator(f'a[href="/obra/{mid}"]').first.click()
                        planned = page.locator('.media-list-link').filter(has_text='Quero ver / ler')
                        watched = page.locator('.media-list-link').filter(has_text='Já assisti / li')
                        await expect(planned).to_be_enabled()
                        await expect(watched).to_be_enabled()
                        report['phase'] = 'toggle_' + str(width)
                        await planned.click()
                        await expect(planned).to_have_attribute('aria-pressed', 'true')
                        await watched.click()
                        await expect(watched).to_have_attribute('aria-pressed', 'true')
                        await expect(planned).to_have_attribute('aria-pressed', 'false')
                        await watched.click()
                        await expect(watched).to_have_attribute('aria-pressed', 'false')
                        await page.locator('a[href="/conta"]').first.click()
                        await expect(page.locator('.profile-identity h2')).to_be_visible()
                        await page.reload()
                        await page.locator(f'a[href="/obra/{mid}"]').first.click()
                        report['phase'] = 'reload_' + str(width)
                        await expect(watched).to_be_enabled()
                        await expect(watched).to_have_attribute('aria-pressed', 'false')
                        await expect(planned).to_have_attribute('aria-pressed', 'false')
                        if await page.evaluate('document.documentElement.scrollWidth > innerWidth'):
                            raise AssertionError('Horizontal overflow')
                        if errors: raise AssertionError('Browser JavaScript error')
                        await page.screenshot(path=str(private / f'browser-status-{width}.png'), full_page=True)
                        report['cases'].append({'case': 'exclusive_toggle_static_reload_and_revisit', 'width': width, 'passed': True})
                        print(json.dumps(report['cases'][-1]), flush=True)
                        await context.close()
                except Exception:
                    try:
                        await page.screenshot(path=str(private/'browser-failure.png'),full_page=True)
                        (private/'browser-failure.txt').write_text(await page.locator('body').inner_text(),encoding='utf-8')
                        (private/'browser-diagnostics.json').write_text(json.dumps({'page_errors':error_messages,'responses':local_failures,'url_path':urlsplit(page.url).path}),encoding='utf-8')
                    except Exception: pass
                    raise
                finally: await browser.close()
            report['passed'] = len(report['cases']) == 3 and stats['rate_limits'] == 0
        except Exception as exc:
            report['failure_type'] = type(exc).__name__
        finally:
            if process is not None: stop_process_tree(process)
            proxy.shutdown()
            proxy.server_close()
            report.update(stats)
            output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frontend-workdir',type=Path)
    parser.add_argument('--private-dir', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.frontend_workdir, args.private_dir, args.output)))
