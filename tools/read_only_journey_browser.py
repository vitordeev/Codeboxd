"""Real-service browser navigation behind a write-blocking Xano proxy."""
import argparse
import asyncio
from collections import Counter, defaultdict
from http.cookiejar import CookieJar
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
import threading
import time
from urllib.parse import parse_qsl, unquote, urlsplit

from dotenv import dotenv_values
import httpx
import psutil
from playwright.async_api import async_playwright, expect

from Codeboxd_main.services.api import _NoCookies, retry_after_seconds
from tools.isolated_frontend import prepare_frontend
from tools.performance_probe import safe_endpoint
from tools.real_login_measurement import Measurement, VisitCycle, stop_process_tree

ROOT = Path(__file__).resolve().parents[1]


def require_free_port(port=3031):
    try:
        listeners = psutil.net_connections(kind='tcp')
    except (psutil.Error, OSError):
        raise RuntimeError('test_port_state_unknown') from None
    if any(item.laddr and item.laddr.port == port and item.status == psutil.CONN_LISTEN
           for item in listeners):
        raise RuntimeError('test_port_in_use')


def require_owned_listener(pid, port=3031):
    parent = psutil.Process(pid)
    owned = {pid, *(child.pid for child in parent.children(recursive=True))}
    listeners = {item.pid for item in psutil.net_connections(kind='tcp')
                 if item.laddr and item.laddr.port == port and item.status == psutil.CONN_LISTEN}
    if not listeners or not listeners <= owned:
        raise RuntimeError('test_server_owner_mismatch')


def allowed_read(method, path):
    parsed = urlsplit(path)
    if parsed.scheme or parsed.netloc or parsed.fragment:
        return False
    if method == 'POST':
        return parsed.path == '/auth/auth/login' and not parsed.query
    if method != 'GET' or not re.fullmatch(
            r'/(auth/auth/me|social/(media(?:/[0-9]+)?|profiles(?:/[0-9]+)?|library|'
            r'interactions|lists(?:/public|/[0-9]+/items)?|feed|posts|likes))', parsed.path):
        return False
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if key == 'identity_key':
            if not value or len(value) > 200 or any(c in value for c in '\r\n'):
                return False
        elif key not in ('page', 'per_page', 'after_id', 'user_id', 'media_id') or not value.isdigit():
            return False
    return True


def proxy_handler(measurement, bases, client):
    class Proxy(BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def log_message(self, *args):
            pass

        def reply(self, status, body, wait=0):
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            if wait:
                self.send_header('Retry-After', str(wait))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass

        def forward(self):
            if not allowed_read(self.command, self.path):
                measurement.stop_reason = 'blocked-non-read-request'
                self.close_connection = True
                self.reply(403, b'{}')
                return
            if not measurement.reserve(self.command):
                self.reply(429, b'{}', max(1, int(measurement.retry_until-time.monotonic())))
                return
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 <= length <= 8192:
                measurement.stop_reason = 'body-budget'
                self.reply(413, b'{}')
                return
            body = self.rfile.read(length) if length else None
            group, relative = self.path.lstrip('/').split('/', 1)
            headers = {key: self.headers[key] for key in ('Authorization', 'Content-Type', 'Accept')
                       if self.headers.get(key)}
            started = time.perf_counter()
            try:
                response = client.request(self.command, bases[group]+'/'+relative,
                                          headers=headers, content=body)
                wait = response.headers.get('Retry-After', '')
                measurement.record(self.command, self.path, response.status_code, started, wait)
                if (self.command == 'GET' and response.status_code not in (200, 204, 429)
                        and not (urlsplit(self.path).path == '/social/likes' and response.status_code == 404)):
                    measurement.stop_reason = 'remote-read-error'
                self.reply(response.status_code, response.content,
                           retry_after_seconds(wait) if response.status_code == 429 else 0)
            except httpx.RequestError:
                measurement.record(self.command, self.path, 0, started)
                measurement.stop_reason = 'proxy-network-error'
                self.reply(502, b'{}')

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = forward
    return Proxy


def preflight_data(user, lists, media):
    if not (isinstance(user, dict) and type(user.get('id')) is int and user['id'] > 0
            and user.get('role') == 'member' and user.get('account_status') == 'active'):
        raise RuntimeError('active_member_required')
    def rows(data):
        return data if isinstance(data, list) else data.get('items', [])
    owned = [row for row in rows(lists) if row.get('user_id') == user['id']]
    titles = {str(row.get('title', '')).casefold() for row in owned}
    if not {'quero ver / ler', 'já assisti / li'} <= titles or 'jã¡ assisti / li' in titles:
        raise RuntimeError('default_lists_need_repair')
    candidate = next((row for row in rows(media) if type(row.get('id')) is int and row['id'] > 0
                      and row.get('media_type') == 'movie' and row.get('title')), None)
    if candidate is None:
        raise RuntimeError('existing_movie_required')
    return candidate['id'], candidate['title']


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row['width'], row['step'])].append(row)
    return [dict(width=width, step=step, samples=len(values),
                 median_primary_ms=statistics.median(v['primary_ms'] for v in values),
                 median_finished_ms=statistics.median(v['finished_ms'] for v in values),
                 worst_finished_ms=max(v['finished_ms'] for v in values),
                 warnings=sum(v['warning_visible'] for v in values))
            for (width, step), values in groups.items()]


async def run(output, frontend, samples=5):
    if not 1 <= samples <= 5:
        raise ValueError('Use one to five samples')
    require_free_port()
    output.mkdir(parents=True, exist_ok=True)
    report_path = output/'result.json'
    if report_path.exists():
        raise FileExistsError('Preserve existing evidence')
    config = dotenv_values(ROOT/'.env')
    bases = {key: config[name].rstrip('/') for key, name in
             (('auth', 'XANO_AUTH_URL'), ('social', 'XANO_SOCIAL_URL'))}
    if not all(value.startswith('https://') for value in bases.values()):
        raise RuntimeError('real_https_services_required')
    report = dict(layer='real-browser-isolated-read-only-proxy', passed=False, steps=[],
                  samples_requested=samples, cache_controlled=False, normal_server_modified=False,
                  provider_python_requests_measured=False, screenshots_saved=False)
    measurement = Measurement(max_requests=400)
    wire = dict(sent_frames=0, received_frames=0, received_bytes=0, javascript_errors=0)
    cycle = VisitCycle()
    with httpx.Client(timeout=httpx.Timeout(10, connect=3), follow_redirects=False,
                      cookies=CookieJar(policy=_NoCookies())) as client:
        server = ThreadingHTTPServer(('127.0.0.1', 0), proxy_handler(measurement, bases, client))
        server.daemon_threads = True
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        proxy = f'http://127.0.0.1:{server.server_port}'
        env = dict(os.environ, XANO_AUTH_URL=proxy+'/auth', XANO_SOCIAL_URL=proxy+'/social',
                   REFLEX_WEB_WORKDIR=str(frontend.resolve()), REFLEX_USE_NPM='true',
                   COOKIE_SECURE='false', REFLEX_STATE_MANAGER_MODE='memory')
        env.pop('REFLEX_APP_MODULE_IMPORT', None)
        with (output/'server.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen([sys.executable, '-m', 'reflex', 'run', '--env', 'prod',
                '--single-port', '--frontend-port', '3031', '--backend-port', '3031'],
                cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            try:
                print('STARTING_ISOLATED_READ_ONLY_APP', flush=True)
                async with httpx.AsyncClient(timeout=2) as readiness:
                    for _ in range(240):
                        if process.poll() is not None:
                            raise RuntimeError('isolated_app_exited')
                        try:
                            response = await readiness.get('http://127.0.0.1:3031/login')
                            if response.status_code in (200, 307):
                                require_owned_listener(process.pid)
                                break
                        except httpx.RequestError:
                            pass
                        await asyncio.sleep(1)
                    else:
                        raise TimeoutError('isolated_startup')
                async with async_playwright() as pw:
                    browser = await pw.chromium.launch(channel='msedge', headless=False)
                    try:
                        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
                        page = await context.new_page()
                        page.on('pageerror', lambda _: wire.update(javascript_errors=wire['javascript_errors']+1))
                        def received(frame):
                            wire['received_frames'] += 1
                            wire['received_bytes'] += len(frame.encode() if isinstance(frame, str) else frame)
                            cycle.received(frame)
                        def socket(ws):
                            ws.on('framereceived', received)
                            ws.on('framesent', lambda _: wire.update(sent_frames=wire['sent_frames']+1))
                        page.on('websocket', socket)
                        base = 'http://127.0.0.1:3031'
                        await page.goto(base+'/login')
                        report['current_step'] = 'manual-member-login'
                        print('READY_FOR_MEMBER_LOGIN: use a conta de membro na janela de teste.', flush=True)
                        await page.wait_for_url('**/conta*', timeout=600000)
                        await expect(page.locator('.profile-identity h2')).to_be_visible(timeout=60000)
                        token = await page.evaluate("sessionStorage.getItem('codeboxd_session')")
                        if not token:
                            token = next((row['value'] for row in await context.cookies()
                                          if row['name'] == 'codeboxd_auth'), '')
                        token = unquote(token or '')
                        if token.startswith('"'):
                            token = json.loads(token)
                        report['current_step'] = 'read-only-preflight'
                        async with httpx.AsyncClient(timeout=20) as verify:
                            values = []
                            for path in ('/auth/auth/me', '/social/lists?per_page=100', '/social/media?per_page=20'):
                                await asyncio.sleep(3)
                                response = await verify.get(proxy+path, headers={'Authorization': 'Bearer '+token})
                                response.raise_for_status()
                                values.append(response.json())
                        mid, title = preflight_data(*values)
                        token = ''; values.clear()
                        async def step(name, action, primary, width, index, empty_heading=None):
                            await asyncio.sleep(3)
                            report['current_step'] = name
                            before = measurement.total
                            cycle.arm()
                            started = time.perf_counter()
                            await action()
                            deadline = time.monotonic()+60
                            while cycle.started_at is None:
                                if measurement.stop_reason or wire['javascript_errors']:
                                    raise RuntimeError('read_only_journey_stopped')
                                if time.monotonic() > deadline:
                                    raise TimeoutError('missing_loading_cycle')
                                await asyncio.sleep(.05)
                            if empty_heading:
                                while not await primary.is_visible():
                                    if measurement.stop_reason or wire['javascript_errors']:
                                        raise RuntimeError('read_only_journey_stopped')
                                    if cycle.finished_at is not None:
                                        await expect(page.locator('.site-main h1')).to_have_text(empty_heading)
                                        break
                                    if time.monotonic() > deadline:
                                        raise TimeoutError('missing_primary_content')
                                    await asyncio.sleep(.05)
                            else:
                                await expect(primary).to_be_visible(timeout=60000)
                            primary_ms = round((time.perf_counter()-started)*1000, 3)
                            while cycle.finished_at is None:
                                if measurement.stop_reason or wire['javascript_errors']:
                                    raise RuntimeError('read_only_journey_stopped')
                                if time.monotonic() > deadline:
                                    raise TimeoutError('unfinished_loading_cycle')
                                await asyncio.sleep(.05)
                            overflow = await page.evaluate('document.documentElement.scrollWidth > innerWidth')
                            if overflow or measurement.stop_reason or wire['javascript_errors']:
                                raise RuntimeError('journey_validation_failed')
                            warning = await page.locator('.site-main > [role="status"]').filter(
                                has_not_text=re.compile(r'^Carregando…$')).count()
                            warning += await page.get_by_role('alert').count()
                            report['steps'].append(dict(step=name, width=width, sample=index+1,
                                primary_ms=primary_ms, finished_ms=cycle.metrics()['cycle_total_ms'],
                                xano_calls=measurement.total-before, warning_visible=bool(warning)))
                            report_path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
                            print(json.dumps(dict(step=name, width=width, sample=index+1, passed=True)), flush=True)
                        for width in (1440, 390):
                            await page.set_viewport_size({'width': width, 'height': 900})
                            for index in range(samples):
                                routes = [('home', '/', '.spotlight-title', None),
                                          ('detail', '/obra/'+str(mid), '.media-detail-title', None),
                                          ('profile', '/conta', '.profile-identity h2', None),
                                          ('library', '/biblioteca', '.activity-card', 'Minha biblioteca'),
                                          ('lists', '/listas', '.list-row', None),
                                          ('feed', '/feed', '.feed-stream > article', 'Entre histórias'),
                                          ('community', '/comunidade', '.site-main article', 'Encontre sua comunidade')]
                                for name, path, selector, empty_heading in routes:
                                    await step(name, lambda path=path: page.goto(base+path, wait_until='domcontentloaded'),
                                               page.locator(selector).first, width, index, empty_heading)
                                    if name == 'home':
                                        async def search():
                                            await page.get_by_role('textbox', name='Buscar título').fill(title)
                                            await page.get_by_role('button', name='Buscar', exact=True).click()
                                            await expect(page.get_by_role('heading', name='Resultados da busca',
                                                                         exact=True)).to_be_visible()
                                        await step('search', search, page.locator('.media-card').first, width, index)
                                        # Reset only this temporary session's discovery view;
                                        # search context is otherwise intentionally kept on return.
                                        restore = page.get_by_role('button', name='Voltar aos destaques', exact=True)
                                        await restore.click()
                                        await expect(restore).not_to_be_visible()
                        report['summary'] = summarize(report['steps'])
                        report['passed'] = True
                    finally:
                        await browser.close()
            except Exception as error:
                report['failure_type'] = type(error).__name__
            finally:
                stop_process_tree(process)
                server.shutdown(); server.server_close(); worker.join(timeout=5)
                report.update(proxy=measurement.report(), wire=wire)
                report['summary'] = summarize(report['steps'])
                report_path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
                print(json.dumps(dict(passed=report['passed'], steps=len(report['steps']),
                                      failed_step=report.get('current_step'),
                                      stop_reason=measurement.stop_reason)), flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--samples', type=int, choices=range(1, 6), default=5)
    parser.add_argument('--frontend-workdir', type=Path)
    args = parser.parse_args()
    frontend = args.frontend_workdir or prepare_frontend('read-only-'+str(os.getpid()))
    frontend = frontend.resolve()
    if not frontend.is_relative_to((ROOT/'.local/frontends').resolve()) or not frontend.is_dir():
        parser.error('Use an isolated frontend directory')
    # Current normal frontend is explicitly reserved in CONTEXTO.md.
    if frontend.name == 'xano-pool-20261024':
        parser.error('The normal server frontend cannot be reused')
    raise SystemExit(asyncio.run(run(args.output, frontend, args.samples)))
