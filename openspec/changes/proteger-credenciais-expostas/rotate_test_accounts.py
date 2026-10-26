"""Rotate only historical test passwords via existing app APIs; never print secrets."""
import argparse
import json
from pathlib import Path
import secrets
import time
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

from audit_inventory import ROOT, HERE, git


def historical_accounts():
    inventory = json.loads((HERE / 'inventory.json').read_text(encoding='utf-8'))
    accounts, seen = [], set()

    def walk(value):
        if isinstance(value, dict):
            if isinstance(value.get('email'), str) and isinstance(value.get('password'), str):
                accounts.append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for row in inventory['findings']:
        if row['scope'] == 'history' and row['path'].startswith('.local/') and row['path'].endswith('.json') and row['object'] not in seen:
            seen.add(row['object'])
            walk(json.loads(git('cat-file', 'blob', row['object'])))
    if len(accounts) != 5 or len({a['email'].strip().lower() for a in accounts}) != 5:
        raise RuntimeError('Unexpected account scope')
    return accounts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    base = dotenv_values(ROOT / '.env').get('XANO_AUTH_URL', '').rstrip('/')
    parsed = urlsplit(base)
    if parsed.scheme != 'https' or not parsed.hostname or not parsed.hostname.endswith('.xano.io') or parsed.username or parsed.password:
        raise RuntimeError('Unexpected origin')
    report = {'applied': args.apply, 'accounts': [], 'historical_tokens': []}
    private_dir = ROOT / '.local' / 'credential-rotation'
    private_dir.mkdir(parents=True, exist_ok=True)
    output = HERE / ('account-rotation.json' if args.apply else 'account-preview.json')
    previous = json.loads(output.read_text(encoding='utf-8')) if args.apply and output.exists() else {}
    completed = {r['account']: r for r in previous.get('accounts', [])
                 if r.get('password_changed') and r.get('new_identity_matches')
                 and r.get('old_login_after_change_status') in (401, 403)}
    if previous:
        # Keep previous sanitized attempts; never overwrite evidence on resume.
        number = 1
        while (HERE / f'account-rotation-attempt-{number}.json').exists():
            number += 1
        (HERE / f'account-rotation-attempt-{number}.json').write_text(json.dumps(previous, indent=2) + '\n', encoding='utf-8')

    def save():
        output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    class PacedClient(httpx.Client):
        def request(self, *request_args, **kwargs):
            time.sleep(2)
            response = super().request(*request_args, **kwargs)
            if response.status_code == 429:
                retry = response.headers.get('Retry-After', '')
                report['rate_limited'] = True
                report['retry_after_seconds'] = int(retry) if retry.isdigit() else 60
                save()
                raise RuntimeError('Rate limited; no automatic mutation retry')
            return response

    with PacedClient(timeout=20, follow_redirects=False) as client:
        accounts = historical_accounts()
        for index, account in enumerate(accounts, 1):
            if f'A.{index:02}' in completed:
                report['accounts'].append(completed[f'A.{index:02}'])
                save()
                continue
            row = {'account': f'A.{index:02}', 'password_changed': False}
            report['accounts'].append(row)
            save()
            login = client.post(base + '/auth/login', json={'email': account['email'], 'password': account['password']})
            row['old_login_status'] = login.status_code
            if login.status_code != 200:
                row['limitation'] = 'Historical login rejected or unavailable; no password change attempted'
                save()
                continue
            token = login.json().get('authToken')
            if not isinstance(token, str) or not token:
                raise RuntimeError('Unexpected login response')
            headers = {'Authorization': 'Bearer ' + token}
            identity = client.get(base + '/auth/me', headers=headers)
            row['identity_status'] = identity.status_code
            if identity.status_code != 200:
                save()
                continue
            user = identity.json()
            matched = str(user.get('email', '')).strip().lower() == account['email'].strip().lower()
            row['identity_matches_history'] = matched
            row['role'] = user.get('role') if user.get('role') in ('member', 'admin', 'moderator') else 'unknown'
            if not matched or row['role'] != 'member' or user.get('account_status') != 'active':
                row['limitation'] = 'Identity, role or status requires review; no change attempted'
                save()
                continue
            if args.apply:
                # Preserve replacement privately BEFORE attempting the remote mutation.
                secret_file = private_dir / f'account-{index:02}.json'
                if secret_file.exists():
                    saved = json.loads(secret_file.read_text(encoding='utf-8'))
                    if saved.get('email') != account['email'] or saved.get('user_id') != user['id']:
                        raise RuntimeError('Private replacement identity mismatch')
                    replacement = saved['password']
                else:
                    replacement = 'Cbx9!' + secrets.token_urlsafe(32)
                    with secret_file.open('x', encoding='utf-8') as stream:
                        json.dump({'email': account['email'], 'user_id': user['id'], 'password': replacement}, stream)
                changed = client.post(base + '/reset/update_password', headers=headers,
                                      json={'password': replacement, 'confirm_password': replacement})
                row['password_change_status'] = changed.status_code
                row['password_changed'] = changed.status_code == 200
                save()
                if changed.status_code != 200:
                    continue
                fresh = client.post(base + '/auth/login', json={'email': account['email'], 'password': replacement})
                row['new_login_status'] = fresh.status_code
                fresh_token = fresh.json().get('authToken') if fresh.status_code == 200 else None
                if fresh_token:
                    verified = client.get(base + '/auth/me', headers={'Authorization': 'Bearer ' + fresh_token})
                    row['new_identity_status'] = verified.status_code
                    row['new_identity_matches'] = verified.status_code == 200 and verified.json().get('id') == user['id']
                old = client.post(base + '/auth/login', json={'email': account['email'], 'password': account['password']})
                row['old_login_after_change_status'] = old.status_code
                previous = client.get(base + '/auth/me', headers=headers)
                row['prechange_session_after_change_status'] = previous.status_code
                row['prechange_session_rejected'] = previous.status_code in (401, 403)
            save()
        # Test exposed stored tokens, never persist or print their values.
        for index, account in enumerate(accounts, 1):
            token = next((account[k] for k in ('authToken', 'auth_token', 'token', 'access_token')
                          if isinstance(account.get(k), str) and account[k]), None)
            if token:
                response = client.get(base + '/auth/me', headers={'Authorization': 'Bearer ' + token})
                report['historical_tokens'].append({'account': f'A.{index:02}', 'status': response.status_code,
                                                    'rejected': response.status_code in (401, 403)})
                save()
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except httpx.RequestError:
        raise SystemExit('Network unavailable; inspect sanitized report and private replacement state before resuming') from None
    except Exception as exc:
        raise SystemExit('Account operation stopped (' + type(exc).__name__ + '); private details suppressed') from None
