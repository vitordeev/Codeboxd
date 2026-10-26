"""Controlled real API checks and scoped cleanup for default-list identity."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import secrets
import time
import uuid

import httpx
from dotenv import dotenv_values

from tools.default_list_deployment import PRIVATE
from tools.default_list_integrity import CHANGE, read_table
from tools.session_revocation import ROOT, metadata_config

JOURNAL = PRIVATE / 'test-account.json'
REPORT = CHANGE / 'validation/default-lists-remote.json'


def api_request(client, method, base, path, token=None, data=None):
    time.sleep(3.5)
    response = client.request(method, base + path,
        headers={'Authorization':'Bearer ' + token} if token else {}, json=data)
    if response.status_code == 429:
        wait = response.headers.get('Retry-After','')
        (CHANGE / 'validation/default-lists-rate-limit.json').write_text(json.dumps({
            'http_status':429, 'retry_after_seconds':int(wait) if wait.isdigit() else None,
            'mutation_retried_automatically':False}), encoding='utf-8')
        raise RuntimeError('Rate limited; no automatic mutation retry')
    return response


def verify():
    if JOURNAL.exists():
        cleaned = PRIVATE / 'test-account-cleaned.json'
        previous = json.loads(JOURNAL.read_text(encoding='utf-8'))
        if not cleaned.exists() or json.loads(cleaned.read_text(encoding='utf-8')).get('user_id') != previous.get('user_id'):
            raise RuntimeError('Test account journal exists; review before creating another')
        JOURNAL.rename(PRIVATE / ('test-account-' + previous['test_tag'] + '-cleaned.json'))
        if REPORT.exists(): REPORT.rename(REPORT.with_name('default-lists-remote-' + previous['test_tag'] + '.json'))
    config = dotenv_values(ROOT / '.env')
    auth, social = config['XANO_AUTH_URL'].rstrip('/'), config['XANO_SOCIAL_URL'].rstrip('/')
    tag = uuid.uuid4().hex[:10]
    account = dict(email=f'listcheck_{tag}@example.invalid', username='listcheck_' + tag,
                   password='Cbx9!' + secrets.token_urlsafe(24), name='Validação de listas', test_tag=tag)
    JOURNAL.write_text(json.dumps(account), encoding='utf-8')
    report = dict(layer='real_xano_api', checks=[], passed=False, cleanup_pending=True)
    def check(name, passed, response=None):
        row = dict(scenario=name, passed=bool(passed))
        if response is not None: row['http_status'] = response.status_code
        report['checks'].append(row)
        REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
        if not passed: raise RuntimeError('Check failed; inspect sanitized report: ' + name)
    with httpx.Client(timeout=30) as client:
        response = api_request(client, 'POST', auth, '/auth/signup', data={k:account[k] for k in ('name','username','email','password')})
        check('signup_succeeds', response.status_code == 200 and bool(response.json().get('authToken')), response)
        account['user_id'] = response.json()['user_id']
        JOURNAL.write_text(json.dumps(account), encoding='utf-8')
        token = response.json()['authToken']
        def get_lists():
            response = api_request(client, 'GET', social, '/lists', token)
            response.raise_for_status()
            data = response.json()
            return data['items'] if isinstance(data, dict) else data
        initial = get_lists()
        check('signup_two_default_keys', len(initial) == 2 and
              {r.get('default_key') for r in initial} == {f"{account['user_id']}:planned",f"{account['user_id']}:completed"})
        planned = next(row for row in initial if row['default_key'].endswith(':planned'))
        response = api_request(client, 'DELETE', social, f"/lists/{planned['id']}", token)
        check('remove_only_empty_disposable_default', response.status_code == 200, response)
        payload = dict(title='Quero ver / ler', default_kind='planned')
        def create():
            with httpx.Client(timeout=30) as other:
                return api_request(other, 'POST', social, '/lists', token, payload)
        with ThreadPoolExecutor(max_workers=3) as pool:
            responses = list(pool.map(lambda _:create(), range(3)))
        check('concurrent_defaults_return_same_record', all(r.status_code == 200 for r in responses)
              and len({r.json().get('id') for r in responses}) == 1)
        current = get_lists()
        check('concurrent_defaults_persist_only_two', len(current) == 2)
        planned = next(row for row in current if row['default_key'].endswith(':planned'))
        changed = dict(title='Padrão renomeado', description='Descrição preservada', is_public=False)
        response = api_request(client, 'PUT', social, f"/lists/{planned['id']}", token, changed)
        check('rename_default', response.status_code == 200, response)
        response = api_request(client, 'POST', social, '/lists', token, payload)
        check('preparation_preserves_renamed_private_default', response.status_code == 200
              and response.json().get('id') == planned['id'] and
              all(response.json().get(k) == v for k,v in changed.items()), response)
        response = api_request(client, 'PUT', social, f"/lists/{planned['id']}", token,
                               dict(title='Quero ver / ler', description='Obras para descobrir depois.', is_public=True))
        check('restore_disposable_default_metadata', response.status_code == 200, response)
        custom = [api_request(client, 'POST', social, '/lists', token, dict(title='Quero ver / ler',is_public=False)) for _ in range(2)]
        check('nullable_identity_allows_custom_homonyms', all(r.status_code == 200 and r.json().get('default_key') is None for r in custom)
              and len({r.json().get('id') for r in custom}) == 2)
        response = api_request(client, 'POST', social, '/lists', token, dict(title='Invalid',default_kind='invalid'))
        check('invalid_default_kind_rejected', response.status_code == 400, response)
        response = api_request(client, 'POST', social, '/lists', data=payload)
        check('visitor_cannot_create_default', response.status_code == 401, response)
        other_account = json.loads((ROOT / '.local/credential-rotation/account-03.json').read_text(encoding='utf-8'))
        response = api_request(client, 'POST', auth, '/auth/login', data={k:other_account[k] for k in ('email','password')})
        check('second_controlled_account_login', response.status_code == 200, response)
        other_token = response.json()['authToken']
        response = api_request(client, 'GET', social, '/lists', other_token)
        response.raise_for_status()
        data = response.json()
        other_lists = data['items'] if isinstance(data,dict) else data
        check('second_account_isolation', bool(other_lists) and all(r['user_id'] == other_account['user_id'] for r in other_lists)
              and all(r['user_id'] != account['user_id'] for r in other_lists))
        response = api_request(client, 'PUT', social, f"/lists/{other_lists[0]['id']}", token, dict(title='Forbidden'))
        check('cannot_mutate_other_account_list', response.status_code in (403,404), response)
        response = api_request(client, 'POST', social, '/lists', token,
                               dict(payload, user_id=other_account['user_id']))
        check('owner_comes_from_authenticated_session', response.status_code == 200 and
              response.json().get('user_id') == account['user_id'] and response.json().get('id') == planned['id'], response)
        title = 'Validação privada ' + tag
        response = api_request(client, 'POST', social, '/lists', token, dict(title=title, is_public=False))
        check('private_browser_destination_created', response.status_code == 200, response)
        account['browser_list_id'] = response.json()['id']
        account['browser_list_title'] = title
        backup = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
        if not backup['entries']: raise RuntimeError('No existing media available for browser validation')
        account['browser_media_id'] = backup['entries'][0]['media_id']
        JOURNAL.write_text(json.dumps(account), encoding='utf-8')
        base, headers = metadata_config()
        after = read_table(client, base, headers, 895415)
        lookup = {r['id']:r for r in after}
        check('preexisting_lists_unchanged', all({k:v for k,v in lookup[r['id']].items() if k != 'default_key'} == r for r in backup['lists']))
        check('preexisting_entries_unchanged', read_table(client, base, headers, 895416) == backup['entries'])
        report['passed'] = True
        REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(dict(passed=True, checks=len(report['checks']), disposable_account_ready_for_browser=True)))


def cleanup():
    account = json.loads(JOURNAL.read_text(encoding='utf-8'))
    base, headers = metadata_config()
    report = dict(layer='real_xano_cleanup', passed=False)
    with httpx.Client(timeout=30) as client:
        users = read_table(client, base, headers, 881681)
        matches = [r for r in users if r.get('email') == account['email']]
        if len(matches) != 1 or matches[0].get('username') != account['username'] or not account['username'].startswith('listcheck_'):
            raise RuntimeError('Disposable account identity not confirmed; no cleanup performed')
        uid = matches[0]['id']
        if account.get('user_id') not in (None,uid): raise RuntimeError('Disposable account ID mismatch')
        lists = [r for r in read_table(client, base, headers, 895415) if r['user_id'] == uid]
        ids = {r['id'] for r in lists}
        entries = [r for r in read_table(client, base, headers, 895416) if r['list_id'] in ids]
        # Profiles table ID is resolved by name from the workspace export below.
        response = client.get(base + '/table', headers=headers)
        response.raise_for_status()
        tables = response.json()
        if isinstance(tables,dict): tables=tables.get('items',tables.get('tables',[]))
        profile_table = next(t['id'] for t in tables if t['name']=='profile')
        profiles = [r for r in read_table(client, base, headers, profile_table) if r['user_id'] == uid]
        for table, records in ((895416,entries),(895415,lists),(profile_table,profiles),(881681,[matches[0]])):
            for row in records:
                response = client.delete(f"{base}/table/{table}/content/{row['id']}", headers={**headers,'x-data-source':'live'})
                response.raise_for_status()
                time.sleep(0.5)
        backup = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
        after_lists = read_table(client, base, headers, 895415)
        if [{k:v for k,v in row.items() if k != 'default_key'} for row in after_lists] != backup['lists']:
            raise RuntimeError('Existing list preservation mismatch after cleanup')
        if read_table(client, base, headers, 895416) != backup['entries']:
            raise RuntimeError('Existing items preservation mismatch after cleanup')
        if any(r['id']==uid for r in read_table(client, base, headers, 881681)):
            raise RuntimeError('Disposable account remains')
        report.update(passed=True, deleted_disposable_lists=len(lists), deleted_disposable_entries=len(entries),
                      deleted_disposable_profiles=len(profiles), deleted_disposable_accounts=1,
                      original_lists_preserved=len(after_lists), original_items_preserved=len(backup['entries']))
        (CHANGE / 'validation/default-lists-cleanup.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        if REPORT.exists():
            validation = json.loads(REPORT.read_text(encoding='utf-8'))
            validation['cleanup_pending'] = False
            REPORT.write_text(json.dumps(validation, indent=2), encoding='utf-8')
        (PRIVATE / 'test-account-cleaned.json').write_text(json.dumps({'cleaned':True,'user_id':uid}), encoding='utf-8')
        print(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('verify','cleanup'))
    args = parser.parse_args()
    try:
        verify() if args.action=='verify' else cleanup()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise SystemExit('Remote validation stopped (' + type(exc).__name__ + '); inspect journal before retry') from None
