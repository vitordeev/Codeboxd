"""Real controlled-account validation. Secrets stay under ignored .local only."""
import argparse
import json
import secrets
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

from tools.session_revocation import ROOT, CHANGE, PRIVATE, metadata_config


class PacedClient(httpx.Client):
    def request(self, *args, **kwargs):
        time.sleep(3)
        response = super().request(*args, **kwargs)
        if response.status_code == 429:
            retry = response.headers.get('Retry-After', '')
            (CHANGE / 'rate-limit.json').write_text(json.dumps({'http_status': 429,
                'retry_after_seconds': int(retry) if retry.isdigit() else 60,
                'mutation_automatically_retried': False}, indent=2) + '\n', encoding='utf-8')
            raise RuntimeError('Rate limited; no automatic retry')
        return response


def login(client, base, account):
    response = client.post(base + '/auth/login', json={'email': account['email'], 'password': account['password']})
    if response.status_code != 200 or not response.json().get('authToken'):
        raise RuntimeError('Controlled account login failed')
    return response.json()['authToken']


def private_accounts():
    return [(index, json.loads((ROOT / '.local/credential-rotation' / f'account-{index:02}.json').read_text(encoding='utf-8')))
            for index in (1, 3, 4, 5)]


def verify(client, config, meta, meta_headers):
    auth = config['XANO_AUTH_URL'].rstrip('/')
    social = config['XANO_SOCIAL_URL'].rstrip('/')
    if urlsplit(social).hostname != urlsplit(auth).hostname:
        raise RuntimeError('Unexpected social origin')
    report = {'layer': 'real-xano-api', 'passed': False, 'checks': []}

    def check(name, passed, response=None):
        row = {'scenario': name, 'passed': bool(passed)}
        if response is not None:
            row['http_status'] = response.status_code
        report['checks'].append(row)
        (CHANGE / 'remote-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        if not passed:
            raise RuntimeError('Validation assertion failed; see sanitized report')

    def get(base, path, token):
        return client.get(base + path, headers={'Authorization': 'Bearer ' + token})

    legacy = json.loads((PRIVATE / 'legacy-sessions.json').read_text(encoding='utf-8'))
    for old in legacy:
        response = get(auth, '/auth/me', old['token'])
        check(f'legacy_A{old["account"]:02}_rejected', response.status_code == 401, response)
    response = get(social, '/library', legacy[0]['token'])
    check('legacy_direct_social_read_rejected', response.status_code == 401, response)
    response = client.delete(social + '/posts/0', headers={'Authorization': 'Bearer ' + legacy[0]['token']})
    check('legacy_direct_mutation_rejected', response.status_code == 401, response)

    accounts = dict(private_accounts())
    account, other = accounts[1], accounts[3]
    session, other_session = login(client, auth, account), login(client, auth, other)
    response = get(auth, '/auth/me', session)
    check('fresh_login_identity', response.status_code == 200 and response.json().get('id') == account['user_id'], response)
    response = get(social, '/library', session)
    check('fresh_direct_social_read', response.status_code == 200, response)
    response = get(social, '/admin/dashboard', session)
    check('member_still_denied_admin', response.status_code == 403, response)

    # Two genuinely concurrent attempts with one version; preserve both candidates first.
    candidates = ['Cbx9!' + secrets.token_urlsafe(32), 'Cbx9!' + secrets.token_urlsafe(32)]
    pending = PRIVATE / 'password-race.json'
    if pending.exists():
        raise RuntimeError('Preserve previous race evidence; do not replay mutations blindly')
    pending.write_text(json.dumps({'email': account['email'], 'user_id': account['user_id'], 'candidates': candidates}), encoding='utf-8')

    def change(candidate, token=session):
        return client.post(auth + '/reset/update_password', headers={'Authorization': 'Bearer ' + token},
                           json={'password': candidate, 'confirm_password': candidate})

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(change, candidates))
    successful = [i for i, response in enumerate(outcomes) if response.status_code == 200]
    if len(successful) == 1:
        replacement = candidates[successful[0]]
        previous_password = account['password']
        account['password'] = replacement
        # Durable private canonical replacement, before more verification requests.
        canonical = ROOT / '.local/credential-rotation/account-01.json'
        temporary = canonical.with_suffix('.tmp')
        temporary.write_text(json.dumps(account), encoding='utf-8')
        temporary.replace(canonical)
    check('concurrent_password_change_one_success', len(successful) == 1)
    check('concurrent_reuse_rejected', sorted(r.status_code for r in outcomes) == [200, 401])
    response = get(auth, '/auth/me', session)
    check('prechange_session_rejected', response.status_code == 401, response)
    response = get(social, '/library', session)
    check('prechange_social_read_rejected', response.status_code == 401, response)
    response = client.delete(social + '/posts/0', headers={'Authorization': 'Bearer ' + session})
    check('prechange_social_mutation_rejected', response.status_code == 401, response)
    response = client.post(auth + '/auth/login', json={'email': account['email'], 'password': previous_password})
    check('prechange_password_rejected', response.status_code in (401, 403), response)
    current = login(client, auth, account)
    response = get(auth, '/auth/me', current)
    check('new_password_and_identity', response.status_code == 200 and response.json().get('id') == account['user_id'], response)
    response = get(auth, '/auth/me', other_session)
    check('other_account_session_preserved', response.status_code == 200 and response.json().get('id') == other['user_id'], response)

    # Invoke the existing private code generator, not the email endpoint.
    generated = client.post(meta + '/function/run', headers=meta_headers,
                            json={'name': 'Quick Start/generate_magic_link', 'input': {'email': account['email']},
                                  'middleware': False, 'trace': False})
    check('private_recovery_generator_without_email', generated.status_code == 200, generated)
    codes = []

    def find_code(value):
        if isinstance(value, dict):
            token = value.get('token')
            if isinstance(token, str) and len(token) == 6 and token.isascii() and token.isdigit():
                codes.append(token)
            for child in value.values():
                find_code(child)
        elif isinstance(value, list):
            for child in value:
                find_code(child)
    find_code(generated.json())
    check('private_recovery_code_received', len(set(codes)) == 1)
    response = client.post(auth + '/reset/magic-link-login', json={'email': account['email'], 'magic_token': codes[0]})
    check('recovery_credential_issued', response.status_code == 200 and response.json().get('user_id') == account['user_id'], response)
    reset = response.json()['authToken']
    for base, path, label in ((auth, '/auth/me', 'identity'), (social, '/library', 'social'), (social, '/admin/dashboard', 'admin')):
        response = get(base, path, reset)
        check('recovery_cannot_access_' + label, response.status_code == 401, response)
    response = client.delete(social + '/posts/0', headers={'Authorization': 'Bearer ' + reset})
    check('recovery_cannot_mutate_social', response.status_code == 401, response)
    response = change(account['password'], reset)
    check('recovery_password_change_allowed', response.status_code == 200, response)
    response = change(account['password'], reset)
    check('recovery_credential_reuse_rejected', response.status_code == 401, response)
    response = get(auth, '/auth/me', current)
    check('recovery_revokes_previous_normal_session', response.status_code == 401, response)
    response = get(auth, '/auth/me', other_session)
    check('recovery_preserves_other_account', response.status_code == 200, response)
    final_session = login(client, auth, account)
    response = get(auth, '/auth/me', final_session)
    check('final_account_access_preserved', response.status_code == 200, response)
    report['passed'] = all(row['passed'] for row in report['checks'])
    (CHANGE / 'remote-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': report['passed'], 'checks': len(report['checks'])}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', action='store_true')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--schema', action='store_true')
    parser.add_argument('--audit-unusable-account', action='store_true')
    args = parser.parse_args()
    config = dotenv_values(ROOT / '.env')
    auth = config['XANO_AUTH_URL'].rstrip('/')
    meta, headers = metadata_config()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    with PacedClient(timeout=30, follow_redirects=False) as client:
        if args.audit_unusable_account:
            raw = subprocess.run(['git', 'cat-file', 'blob', '5d1872467de17388404040bb5129262d163358d2'],
                                 cwd=ROOT, capture_output=True, check=True).stdout
            historical = json.loads(raw)
            tables_response = client.get(meta + '/table', headers=headers)
            if tables_response.status_code != 200:
                raise RuntimeError('Metadata table lookup unavailable')
            tables = tables_response.json()
            tables = tables.get('items', []) if isinstance(tables, dict) else tables
            table = next(t for t in tables if t.get('name') == 'user')
            found, page = [], 1
            while True:
                response = client.get(meta + f'/table/{int(table["id"])}/content', headers=headers,
                                      params={'page': page, 'per_page': 100})
                if response.status_code != 200:
                    raise RuntimeError('Metadata account inspection unavailable')
                data = response.json()
                if not isinstance(data, dict) or not isinstance(data.get('items'), list):
                    raise RuntimeError('Unexpected metadata pagination')
                found.extend(row for row in data['items'] if str(row.get('email', '')).strip().lower()
                             == historical['email'].strip().lower())
                if not data.get('nextPage'):
                    break
                page = int(data['nextPage'])
                if page > 10:
                    raise RuntimeError('Account inspection exceeded bounded coverage')
            report = {'account': 'A.02', 'exists': bool(found), 'matched_records': len(found),
                      'complete_scan': True, 'pages_examined': page}
            if len(found) > 1:
                raise RuntimeError('Ambiguous historical identity')
            if found:
                report['role'] = found[0].get('role') if found[0].get('role') in ('admin', 'member', 'moderator') else 'unknown'
                report['account_status'] = found[0].get('account_status') if found[0].get('account_status') in ('active', 'disabled') else 'unknown'
                response = client.post(auth + '/auth/login', json={'email': historical['email'], 'password': historical['password']})
                report['historical_login_status'] = response.status_code
                report['resolved'] = report['account_status'] == 'active' and response.status_code in (401, 403)
            else:
                report['resolved'] = True
            (CHANGE / 'unusable-account-inspection.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(report))
        if args.schema:
            origin = urlsplit(auth)
            response = client.get(f'{origin.scheme}://{origin.netloc}/apispec:meta', params={'type': 'json'}, headers=headers)
            report = {'schema_status': response.status_code}
            if response.status_code == 200:
                schema = response.json()
                (PRIVATE / 'metadata-schema.json').write_text(json.dumps(schema), encoding='utf-8')
                report['function_run_paths'] = [path for path in schema.get('paths', {}) if 'function' in path and ('run' in path or 'debug' in path)]
            print(json.dumps(report))
        if args.capture:
            target = PRIVATE / 'legacy-sessions.json'
            if target.exists():
                raise RuntimeError('Preserve existing legacy session capture')
            captured = []
            for index, account in private_accounts():
                token = login(client, auth, account)
                response = client.get(auth + '/auth/me', headers={'Authorization': 'Bearer ' + token})
                if response.status_code != 200 or response.json().get('id') != account['user_id']:
                    raise RuntimeError('Capture identity mismatch')
                captured.append({'account': index, 'token': token})
                target.write_text(json.dumps(captured), encoding='utf-8')
            report = {'captured_accounts': len(captured), 'layer': 'real-api-before-policy', 'passed': len(captured) == 4}
            (CHANGE / 'legacy-capture.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(report))
        if args.verify:
            verify(client, config, meta, headers)


if __name__ == '__main__':
    try:
        main()
    except httpx.RequestError:
        raise SystemExit('Validation network unavailable; private details suppressed') from None
    except RuntimeError as exc:
        known = ('Rate limited; no automatic retry', 'Validation assertion failed; see sanitized report',
                 'Preserve previous race evidence; do not replay mutations blindly', 'Controlled account login failed')
        raise SystemExit(str(exc) if str(exc) in known else 'Validation stopped; private details suppressed') from None
    except Exception as exc:
        raise SystemExit('Validation stopped (' + type(exc).__name__ + '); private details suppressed') from None
