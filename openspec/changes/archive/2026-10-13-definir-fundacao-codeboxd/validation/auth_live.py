"""Opt-in live auth checks. Run from repository root; secrets stay in .local."""
import asyncio
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from Codeboxd_main.services.api import APIError, request
from Codeboxd_main.state.session import SessionState
import reflex as rx


async def main():
    suffix = secrets.token_hex(6)
    account = dict(name='Auth validation', username='auth_' + suffix,
                   email='auth_' + suffix + '@example.com',
                   password=secrets.token_urlsafe(24) + 'A1')
    local = ROOT / '.local' / ('auth-validation-' + suffix + '.json')
    local.write_text(json.dumps(account), encoding='utf8')
    results = []

    async def check(label, operation):
        try:
            await operation()
            results.append({'test': label, 'result': 'PASS'})
        except Exception as exc:
            results.append({'test': label, 'result': 'FAIL',
                            'error': type(exc).__name__,
                            'status': getattr(exc, 'status', None)})
        print(json.dumps(results[-1]), flush=True)

    async def rejected(path, data=None, token=''):
        try:
            await request('POST' if data is not None else 'GET', path,
                          group='auth', data=data, token=token)
        except APIError as exc:
            assert exc.status in (400, 401, 403, 409, 422), f'Unexpected HTTP {exc.status}'
        else:
            raise AssertionError('Invalid request accepted')

    async def signup():
        result = await request('POST', '/auth/signup', group='auth', data=account)
        token = result['authToken']
        user = await request('GET', '/auth/me', group='auth', token=token)
        assert user['id'] > 0
        account['id'] = user['id']
        local.write_text(json.dumps(account), encoding='utf8')

    async def login():
        state = rx.State(_reflex_internal_init=True).get_substate(SessionState.get_full_name().split('.'))
        async for _ in state._authenticate(dict(account, remember=True), False):
            pass
        assert state.is_authenticated and state.user_id == account['id']
        assert state.auth_token and not state.session_token and not state.is_loading
        assert await state._validate_session()
        state.logout()
        assert not state.is_authenticated and not state._token()

    await check('anonymous auth/me rejected', lambda: rejected('/auth/me'))
    await check('invalid login rejected', lambda: rejected('/auth/login', {
        'email': account['email'], 'password': 'invalid-password1'}))
    await check('new signup and auth/me', signup)
    if account.get('id'):
        await check('duplicate email rejected', lambda: rejected('/auth/signup',
            dict(account, username='other_' + suffix)))
        await check('duplicate username rejected', lambda: rejected('/auth/signup',
            dict(account, email='other_' + suffix + '@example.com')))
        await check('real login, session revalidation and local logout', login)
    output = Path(__file__).with_name('auth-live-results.json')
    output.write_text(json.dumps(results, indent=2) + '\n', encoding='utf8')
    return 1 if any(r['result'] == 'FAIL' for r in results) else 0


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
