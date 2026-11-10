"""Verify the published reset API with one disposable member and no mail delivery."""
import json
from pathlib import Path
import secrets
import time
import uuid

import httpx
from dotenv import dotenv_values
from tools.default_list_integrity import read_table
from tools.session_revocation import metadata_config

ROOT = Path(__file__).resolve().parents[1]
CHANGE = ROOT / 'openspec/changes/reforcar-restricoes-redefinicao-senha'
PRIVATE = ROOT / '.local/reset-restrictions-fixture'


def main():
    output = CHANGE / 'remote-validation-api.json'
    if output.exists():
        raise SystemExit('Preserve previous evidence; inspect cleanup before another run.')
    report = {'passed': False, 'layer': 'published_api_disposable_member', 'emails_sent': 0,
              'real_accounts_modified': 0, 'fixture_removed': False, 'fixture_relations_removed': False, 'checks': []}
    PRIVATE.mkdir(parents=True, exist_ok=True)
    journal_path = PRIVATE / 'fixture.json'
    if journal_path.exists():
        journal = json.loads(journal_path.read_text())
    else:
        tag = uuid.uuid4().hex[:18]
        journal = {'email': 'reset-' + tag + '@example.invalid', 'username': 'cb_reset_' + tag}
        journal_path.write_text(json.dumps(journal), encoding='utf-8')
    email, username = journal['email'], journal['username']
    if not username.startswith('cb_reset_') or not email.endswith('@example.invalid'):
        raise SystemExit('Unexpected fixture identity')
    original = 'Cb9!' + secrets.token_urlsafe(24)
    replacement = 'Cb9!' + secrets.token_hex(30) + chr(233) * 64
    assert len(replacement) == 128
    config = dotenv_values(ROOT / '.env')
    auth = config['XANO_AUTH_URL'].rstrip('/')
    base, headers = metadata_config()
    meta_headers = {**headers, 'x-data-source': 'live'}

    class Client(httpx.Client):
        def request(self, method, url, **kwargs):
            if '/api:meta/' not in str(url):
                time.sleep(2.2)
            return super().request(method, url, **kwargs)

    with Client(timeout=40, follow_redirects=False) as client:
        response = client.get(base + '/table', headers=headers)
        response.raise_for_status()
        data = response.json()
        tables = {r['name']: r['id'] for r in (data.get('items', []) if isinstance(data, dict) else data)}

        def rows(table):
            return read_table(client, base, headers, tables[table])

        def matching_users():
            return [r for r in rows('user') if r.get('email') == email and r.get('username') == username]

        def url(table, ident):
            return base + '/table/' + str(tables[table]) + '/content/' + str(ident)

        def check(name, response, expected):
            passed = response.status_code in expected
            report['checks'].append({'scenario': name, 'http_status': response.status_code, 'passed': passed})
            print(json.dumps(report['checks'][-1]), flush=True)
            if not passed:
                raise RuntimeError('scenario_failed')

        def update(token, password, confirmation=None):
            return client.post(auth + '/reset/update_password', headers={'Authorization': 'Bearer ' + token} if token else {},
                               json={'password': password, 'confirm_password': password if confirmation is None else confirmation})

        try:
            if matching_users():
                raise RuntimeError('prior_fixture_requires_cleanup')
            response = client.post(auth + '/auth/signup', json={'name': 'Reset restrictions test', 'username': username,
                                                               'email': email, 'password': original})
            check('disposable_member_created', response, (200,))
            created = response.json()
            user_id, normal = created['user_id'], created['authToken']
            journal['user_id'] = user_id
            journal_path.write_text(json.dumps(journal), encoding='utf-8')
            generated = client.post(base + '/function/run', headers=headers,
                json={'name': 'Quick Start/generate_magic_link', 'input': {'email': email}, 'middleware': False, 'trace': False})
            check('private_generator_without_email', generated, (200,))
            codes = set()
            def find_codes(value):
                if isinstance(value, dict):
                    token = value.get('token')
                    if isinstance(token, str) and len(token) == 6 and token.isascii() and token.isdigit():
                        codes.add(token)
                    for child in value.values():
                        find_codes(child)
                elif isinstance(value, list):
                    for child in value:
                        find_codes(child)
            find_codes(generated.json())
            if len(codes) != 1:
                raise RuntimeError('private_code_not_found')
            response = client.post(auth + '/reset/magic-link-login', json={'email': email, 'magic_token': next(iter(codes))})
            check('recovery_credential_issued', response, (200,))
            reset = response.json()['authToken']
            check('missing_credential', update('', original), (401,))
            check('corrupt_credential', update('invalid-reset-credential', original), (401,))
            check('normal_session_denied', update(normal, original), (401,))
            for name, password in [('short', 'Ab12345'), ('letters_only', 'abcdefgh'), ('digits_only', '12345678'),
                                   ('over_128', 'A1' + 'x' * 127), ('non_ascii_digit_only', 'abcdefg' + chr(1633))]:
                check(name, update(reset, password), (400,))
            check('confirmation_mismatch', update(reset, replacement, 'different123'), (400,))
            check('current_password_reuse', update(reset, original), (400,))
            check('failed_attempts_preserve_version', client.get(auth + '/auth/me', headers={'Authorization': 'Bearer ' + normal}), (200,))
            check('valid_max_length_unicode_password', update(reset, replacement), (200,))
            check('reset_credential_replay_denied', update(reset, original), (401,))
            check('old_session_revoked', client.get(auth + '/auth/me', headers={'Authorization': 'Bearer ' + normal}), (401,))
            def login(password):
                return client.post(auth + '/auth/login', json={'email': email, 'password': password})
            check('new_password_login', login(replacement), (200,))
            check('old_password_denied', login(original), (401,403))
            check('last_character_not_truncated', login(replacement[:-1] + chr(234)), (401,403))
            report['passed'] = True
        except Exception as error:
            report['failure_type'] = type(error).__name__
        finally:
            try:
                matches = matching_users()
                if len(matches) > 1 or any(r.get('role') != 'member' for r in matches):
                    raise RuntimeError('fixture_identity_mismatch')
                for fixture in matches:
                    own_lists = [r for r in rows('user_list') if r.get('user_id') == fixture['id']]
                    own_ids = {r['id'] for r in own_lists}
                    if any(r.get('user_list_id', r.get('list_id')) in own_ids for r in rows('user_list_item')):
                        raise RuntimeError('fixture_lists_not_empty')
                    for listing in own_lists:
                        response = client.delete(url('user_list', listing['id']), headers=meta_headers)
                        response.raise_for_status()
                    for profile in rows('profile'):
                        if profile.get('user_id') == fixture['id']:
                            if profile.get('username') != username:
                                raise RuntimeError('profile_identity_mismatch')
                            response = client.delete(url('profile', profile['id']), headers=meta_headers)
                            response.raise_for_status()
                    response = client.delete(url('user', fixture['id']), headers=meta_headers)
                    response.raise_for_status()
                report['fixture_removed'] = not matching_users()
                fixture_id = journal.get('user_id')
                report['fixture_relations_removed'] = not any(r.get('user_id') == fixture_id for table in ('user_list', 'profile') for r in rows(table))
            except Exception as error:
                report['cleanup_failure_type'] = type(error).__name__
            report['passed'] = report['passed'] and report['fixture_removed'] and report['fixture_relations_removed']
            output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
