"""Interactive, read-only admin API checks; credentials and payloads stay in memory."""
import argparse
import asyncio
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from html import escape
from pathlib import Path
import secrets
import threading
import time
from urllib.parse import parse_qs

import httpx
from dotenv import dotenv_values
from tools.performance_probe import safe_endpoint
from Codeboxd_main.services.api import retry_after_seconds

ROOT = Path(__file__).resolve().parents[1]
USER_FIELDS = {'id', 'username', 'name', 'role', 'account_status', 'created_at'}
SECRET_KEYS = {'password', 'password_hash', 'authtoken', 'auth_token', 'access_token',
               'refresh_token', 'token', 'secret', 'email'}


def no_secrets(value):
    if isinstance(value, dict):
        return not (set(str(k).lower() for k in value) & SECRET_KEYS) and all(
            no_secrets(v) for v in value.values())
    return not isinstance(value, list) or all(no_secrets(v) for v in value)


def page_contract(data, page=1, per_page=1):
    return (isinstance(data, dict) and isinstance(data.get('items'), list)
            and type(data.get('total')) is int and data['total'] >= 0
            and data.get('page') == page and data.get('per_page') == per_page
            and len(data['items']) <= per_page
            and data['total'] >= len(data['items'])
            and (data.get('next_page') is None or
                 (type(data['next_page']) is int and data['next_page'] > page)))


class Probe:
    def __init__(self, client, auth, social, output, pause=1.2):
        self.client, self.auth, self.social = client, auth.rstrip('/'), social.rstrip('/')
        self.output, self.pause = output, pause
        self.token = None
        self.calls = 0
        self.report = dict(layer='real_admin_api_reads', passed=False,
                           started_at=datetime.now(timezone.utc).isoformat(), checks=[], requests=[])

    def save(self):
        self.output.write_text(json.dumps(self.report, indent=2)+'\n', encoding='utf-8')

    def request(self, method, base, path, **kwargs):
        if self.calls >= 60:
            raise RuntimeError('request_budget')
        if self.calls:
            time.sleep(self.pause)
        self.calls += 1
        started = time.perf_counter()
        response = self.client.request(method, base+path, **kwargs)
        self.report['requests'].append(dict(method=method, endpoint=safe_endpoint(path),
            status=response.status_code, duration_ms=round((time.perf_counter()-started)*1000, 3)))
        self.save()
        if response.status_code == 429:
            self.report['retry_after_seconds'] = retry_after_seconds(response.headers.get('Retry-After', ''))
            self.save()
            raise RuntimeError('remote_rate_limit')
        return response

    def check(self, name, passed, status=None):
        row = dict(scenario=name, passed=bool(passed))
        if status is not None:
            row['http_status'] = status
        self.report['checks'].append(row)
        self.save()
        if not passed:
            raise RuntimeError('contract_check_failed')

    def authenticate(self, email, password):
        response = self.request('POST', self.auth, '/auth/login',
                                json=dict(email=email, password=password))
        if response.status_code != 200:
            return False
        token = response.json().get('authToken')
        if not isinstance(token, str) or not token:
            return False
        me = self.request('GET', self.auth, '/auth/me',
                          headers={'Authorization': 'Bearer '+token})
        user = me.json() if me.status_code == 200 else {}
        allowed = (user.get('id') == 14 and user.get('role') == 'admin'
                   and user.get('account_status') == 'active')
        if allowed:
            self.token = token
        return allowed

    def get(self, name, path, params):
        response = self.request('GET', self.social, path, params=params,
                                headers={'Authorization': 'Bearer '+self.token})
        self.check(name+'_http', response.status_code == 200, response.status_code)
        return response.json()

    def paged(self, name, path, filters=None):
        params = dict(filters or {}, page=1, per_page=1)
        data = self.get(name, path, params)
        self.check(name+'_page', page_contract(data) and no_secrets(data))
        if data['next_page'] is not None:
            next_page = data['next_page']
            following = self.get(name+'_next', path, dict(params, page=next_page))
            self.check(name+'_continuation', page_contract(following, next_page)
                       and no_secrets(following) and following['total'] == data['total']
                       and not ({x['id'] for x in data['items']} &
                                {x['id'] for x in following['items']}))
        return data

    def user_filters(self, own):
        """Exercise real search/filter contracts without exporting account values."""
        row = own['items'][0]
        for field in ('username', 'name'):
            value = row.get(field)
            self.check('users_'+field+'_available', isinstance(value, str) and bool(value.strip()))
            value = value.strip()
            data = self.paged('users_search_'+field, '/admin/users', {'search': value})
            self.check('users_search_'+field+'_matches', data['total'] > 0 and all(
                value.casefold() in str(item.get('username', '')).casefold()
                or value.casefold() in str(item.get('name', '')).casefold()
                for item in data['items']))
        for status in ('active', 'disabled'):
            data = self.paged('users_status_'+status, '/admin/users', {'account_status': status})
            self.check('users_status_'+status+'_matches', all(
                item.get('account_status') == status for item in data['items']))
        combined = self.paged('users_combined', '/admin/users', {
            'user_id': 14, 'role': 'admin', 'account_status': 'active'})
        self.check('users_combined_matches', combined['total'] == 1
                   and combined['items'][0].get('id') == 14
                   and combined['items'][0].get('role') == 'admin'
                   and combined['items'][0].get('account_status') == 'active')
        for field in ('role', 'account_status'):
            response = self.request('GET', self.social, '/admin/users',
                params={field: 'invalid'}, headers={'Authorization': 'Bearer '+self.token})
            self.check('users_invalid_'+field, response.status_code == 400, response.status_code)

    def run(self):
        if not self.token:
            raise RuntimeError('admin_session_required')
        dashboard = self.get('dashboard', '/admin/dashboard', {'per_page': 1})
        self.check('dashboard_totals', no_secrets(dashboard) and all(
            type(dashboard.get(k)) is int and dashboard[k] >= 0
            for k in ('users_total', 'posts_total', 'media_total', 'reports_pending')))
        users = self.paged('users', '/admin/users')
        self.check('users_fields', all(set(row) <= USER_FIELDS for row in users['items']))
        own = self.paged('users_exact_id', '/admin/users', {'user_id': 14})
        self.check('users_exact_match', own['total'] == 1 and own['items'][0]['id'] == 14)
        self.user_filters(own)
        for role in ('member', 'admin'):
            data = self.paged('users_role_'+role, '/admin/users', {'role': role})
            self.check('users_role_'+role+'_matches', all(x['role'] == role for x in data['items']))
        marker = 'cbnomatch_'+secrets.token_hex(16)
        empty = self.paged('users_empty', '/admin/users', {'search': marker})
        self.check('users_empty_result', empty['total'] == 0 and not empty['items'])
        for kind in ('movie', 'series', 'anime', 'book'):
            data = self.paged('catalog_'+kind, '/admin/catalog', {'media_type': kind})
            self.check('catalog_'+kind+'_matches', all(x['media_type'] == kind for x in data['items']))
        self.paged('reports', '/admin/reports')
        for field, value in (('status', 'pending'), ('target_type', 'message'), ('reason', 'spam')):
            data = self.paged('reports_'+field, '/admin/reports', {field: value})
            self.check('reports_'+field+'_matches', all(x[field] == value for x in data['items']))
        self.report['passed'] = True
        self.save()


def login_server(probe, role_label='admin aprovada'):
    path = '/'+secrets.token_urlsafe(32)
    ready = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        attempts = 0

        def log_message(self, *args):
            pass

        def reply(self, status, body):
            payload = body.encode('utf-8')
            try:
                self.send_response(status)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(payload)))
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Content-Security-Policy', "default-src 'none'; form-action 'self'; frame-ancestors 'none'")
                self.end_headers()
                self.wfile.write(payload)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                # The browser may navigate away after submitting valid credentials.
                # Losing that page is independent of the upstream login result.
                pass

        def allowed(self):
            origin = 'http://'+self.server.server_address[0]+':'+str(self.server.server_port)
            return (self.path == path and self.headers.get('Host') == origin[7:]
                    and self.headers.get('Origin', origin) == origin)

        def do_GET(self):
            if not self.allowed():
                self.reply(403, 'Acesso recusado.')
                return
            self.reply(200, '''<!doctype html><meta charset="utf-8"><title>Validação Codeboxd</title>
                <h1>Validação Codeboxd</h1>
                <p>Use a conta ROLE_LABEL. As consultas não alteram dados.</p>
                <form method="post"><label>Email <input name="email" type="email" required></label>
                <label>Senha <input name="password" type="password" autocomplete="off" required></label>
                <button>Entrar e validar consultas</button></form>'''.replace('ROLE_LABEL', escape(role_label)))

        def do_POST(self):
            if not self.allowed() or Handler.attempts >= 3 or ready.is_set():
                self.reply(403, 'Acesso recusado.')
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 8192:
                    self.reply(400, 'Formulário inválido.')
                    return
                Handler.attempts += 1
                fields = parse_qs(self.rfile.read(length).decode('utf-8'))
                authenticated = probe.authenticate(fields['email'][0], fields['password'][0])
                fields.clear()
                if authenticated:
                    ready.set()
                    self.reply(200, '<h1>Login confirmado. Validação em andamento.</h1>')
                else:
                    self.reply(403, '<p>Conta não autorizada. Volte e tente novamente.</p>')
            except Exception:
                probe.report['failure_type'] = 'login_failed'
                probe.save()
                self.reply(502, 'Não foi possível autenticar. Encerre e tente depois.')
                ready.set()

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    server.timeout = 1
    return server, path, ready


async def main(output, pause=3.0, probe_type=Probe, role_label='admin aprovada'):
    from playwright.async_api import async_playwright
    if output.exists():
        raise RuntimeError('output_already_exists')
    output.parent.mkdir(parents=True, exist_ok=True)
    config = dotenv_values(ROOT/'.env')
    with httpx.Client(timeout=25, follow_redirects=False) as client:
        probe = probe_type(client, config['XANO_AUTH_URL'], config['XANO_SOCIAL_URL'], output, pause=pause)
        server, path, ready = login_server(probe, role_label)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(channel='msedge', headless=False)
                try:
                    page = await browser.new_page()
                    await page.goto(f'http://127.0.0.1:{server.server_port}'+path)
                    print('Aguardando login local da conta '+role_label+' (até 10 minutos).', flush=True)
                    deadline = time.monotonic()+600
                    while not ready.is_set() and time.monotonic() < deadline:
                        await asyncio.sleep(1)
                    if not probe.token:
                        raise RuntimeError('admin_session_unavailable')
                    await asyncio.to_thread(probe.run)
                finally:
                    await browser.close()
        except Exception as error:
            probe.report['failure_type'] = type(error).__name__
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)
            probe.token = None
            probe.report['request_count'] = probe.calls
            probe.save()
        print(json.dumps({'passed': probe.report['passed'], 'checks': len(probe.report['checks'])}))
        return 0 if probe.report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pause', type=float, default=3.0)
    args = parser.parse_args()
    if not 1.2 <= args.pause <= 10:
        parser.error('Use an interval between 1.2 and 10 seconds')
    raise SystemExit(asyncio.run(main(args.output, args.pause)))
