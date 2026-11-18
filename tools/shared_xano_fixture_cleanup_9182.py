"""Reconcile only the approved interrupted Xano pilot fixtures 48/49 and 119/120."""
import argparse
import json
from datetime import datetime, timezone
import getpass
from pathlib import Path
import time
import tkinter as tk
from tkinter import ttk

import httpx
from dotenv import dotenv_values

from tools.shared_xano_acceptance import digest
from tools.session_revocation import ROOT, metadata_config

RUN = 'cbshared_9182bcbf0edb'
CHANGE = ROOT/'openspec/changes/reconciliar-fixtures-piloto-xano-9182bcbf0edb'
OUTPUT = CHANGE/'reconciliation-execution.json'
USER_TABLE, LIST_TABLE, ITEM_TABLE = 881681, 895415, 895416
USERS = {48: RUN+'_a', 49: RUN+'_b'}
LISTS = {119: (48, RUN+' public', True), 120: (48, RUN+' private', False)}
MIN_INTERVAL = 10.0


class Stop(RuntimeError):
    pass


def save(state):
    tmp = OUTPUT.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(state, indent=2)+'\n', encoding='utf-8')
    tmp.replace(OUTPUT)


def rows(client, base, headers, table_id):
    result, page, total, seen = [], 1, None, set()
    while True:
        if page in seen or len(seen) >= 20:
            raise Stop('pagination_loop_or_budget')
        seen.add(page)
        response = client.get(f'{base}/table/{table_id}/content',
            headers={**headers, 'x-data-source': 'live'}, params={'page': page, 'per_page': 100})
        if response.status_code != 200:
            raise Stop('inventory_read_http_'+str(response.status_code))
        body = response.json()
        if not isinstance(body, dict) or not isinstance(body.get('items'), list) or type(body.get('itemsTotal')) is not int:
            raise Stop('inventory_shape_unknown')
        if total is None:
            total = body['itemsTotal']
        elif total != body['itemsTotal']:
            raise Stop('inventory_changed_during_read')
        result.extend(body['items'])
        next_page = body.get('nextPage')
        if next_page in (None, False, 0):
            break
        if type(next_page) is not int or next_page <= page:
            raise Stop('invalid_next_page')
        page = next_page
    if len(result) != total:
        raise Stop('incomplete_inventory')
    if any(not isinstance(row, dict) or type(row.get('id')) is not int for row in result):
        raise Stop('invalid_row_identity')
    return result


def public_ids(client, social):
    response = client.get(social+'/lists/public', headers={'x-data-source': 'live'},
                          params={'page': 1, 'per_page': 100})
    if response.status_code != 200:
        raise Stop('public_lists_read_http_'+str(response.status_code))
    value = response.json()
    if isinstance(value, dict):
        value = value.get('items')
    if not isinstance(value, list):
        raise Stop('public_lists_shape_unknown')
    return {row.get('id') for row in value if isinstance(row, dict)}


def login_window(client, auth, social, state):
    result = {}
    window = tk.Tk()
    window.title('Reconciliar fixtures autorizadas no Xano')
    frame = ttk.Frame(window, padding=18); frame.pack()
    ttk.Label(frame, text='Confirme o admin Codeboxd (ID 14). A limpeza só começa após todas as leituras e esta confirmação.').pack()
    fields = []
    for label, masked in [('E-mail do administrador', False), ('Senha do administrador', True)]:
        ttk.Label(frame, text=label).pack()
        field = ttk.Entry(frame, width=56, show='*' if masked else '')
        field.pack(pady=4); fields.append(field)
    status = tk.StringVar(value='Nenhuma escrita executada.')
    ttk.Label(frame, textvariable=status, wraplength=520).pack(pady=8)
    button = ttk.Button(frame, text='Validar admin e executar reconciliação')

    def start():
        button.configure(state='disabled')
        email, secret = fields[0].get().strip(), fields[1].get()
        fields[1].delete(0, 'end')
        try:
            response = client.post(auth+'/auth/login', headers={'x-data-source': 'live'},
                                   json={'email': email, 'password': secret})
            if response.status_code != 200:
                raise Stop('admin_login_rejected_before_writes')
            body = response.json(); token = body.get('authToken')
            if body.get('user_id') != 14 or not isinstance(token, str):
                raise Stop('expected_admin_identity_mismatch')
            headers = {'Authorization': 'Bearer '+token, 'x-data-source': 'live'}
            me = client.get(auth+'/auth/me', headers=headers)
            actor = me.json() if me.status_code == 200 else {}
            if (actor.get('id') != 14 or actor.get('role') != 'admin'
                    or actor.get('account_status') != 'active'
                    or str(actor.get('email', '')).casefold() != email.casefold()):
                raise Stop('active_admin_confirmation_failed')
            state['admin_confirmed'] = True
            state['phase'] = 'mutating'
            save(state)
            result['token'] = token
            status.set('Admin confirmado; reconciliação executada. Revise o recibo local.')
            window.quit()
        except Exception as exc:
            state['failure_reason'] = str(exc) if isinstance(exc, Stop) else type(exc).__name__
            save(state)
            status.set('Interrompido: '+state['failure_reason']+'. Sem repetição automática.')
            button.configure(state='normal')
    button.configure(command=start); button.pack(pady=8)
    window.mainloop()
    window.destroy()
    return result.get('token')


def login_console(client, auth, state):
    """Prompt locally; getpass masks the admin password and nothing is persisted."""
    email = input('E-mail do administrador Codeboxd (ID 14): ').strip()
    secret = getpass.getpass('Senha do administrador (entrada oculta): ')
    response = client.post(auth+'/auth/login', headers={'x-data-source': 'live'},
                           json={'email': email, 'password': secret})
    secret = None
    if response.status_code != 200:
        raise Stop('admin_login_rejected_before_writes')
    body = response.json(); token = body.get('authToken')
    if body.get('user_id') != 14 or not isinstance(token, str):
        raise Stop('expected_admin_identity_mismatch')
    headers = {'Authorization': 'Bearer '+token, 'x-data-source': 'live'}
    me = client.get(auth+'/auth/me', headers=headers)
    actor = me.json() if me.status_code == 200 else {}
    if (actor.get('id') != 14 or actor.get('role') != 'admin'
            or actor.get('account_status') != 'active'
            or str(actor.get('email', '')).casefold() != email.casefold()):
        raise Stop('active_admin_confirmation_failed')
    state['admin_confirmed'] = True
    state['phase'] = 'mutating'
    save(state)
    return token


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--console-login', action='store_true', required=True,
                        help='prompt for the admin login in this PowerShell window (password masked)')
    args = parser.parse_args()
    OUTPUT = args.output.resolve()
    if not OUTPUT.is_relative_to(CHANGE.resolve()):
        parser.error('Output must remain inside this OpenSpec change.')
    if OUTPUT.exists():
        raise Stop('receipt_already_exists_no_retry')
    config = dotenv_values(ROOT/'.env')
    auth, social = config['XANO_AUTH_URL'].rstrip('/'), config['XANO_SOCIAL_URL'].rstrip('/')
    base, meta_headers = metadata_config()
    state = {'layer': 'approved_fixture_reconciliation', 'workspace': 147717, 'run_id': RUN,
             'passed': False, 'remote_writes': 0, 'write_attempts': [], 'checks': [],
             'fixture_ids': {'users': [48, 49], 'lists': [119, 120]},
             'metadata_api_used_for_lists': True, 'phase': 'read_only_preflight'}
    save(state)
    last_write = None

    def write(client, method, url, headers, body, label, expected=(200, 204)):
        nonlocal last_write
        if last_write is not None:
            pause = max(0.0, MIN_INTERVAL-(time.monotonic()-last_write))
            if pause: time.sleep(pause)
        attempt = {'action': label, 'state': 'attempting',
                   'started_at': datetime.now(timezone.utc).isoformat()}
        state['write_attempts'].append(attempt); state['remote_writes'] += 1; save(state)
        try:
            response = client.request(method, url, headers=headers, json=body)
        except httpx.RequestError:
            attempt['state'] = 'uncertain_no_retry'; save(state)
            raise Stop(label+'_uncertain_no_retry') from None
        attempt.update(http_status=response.status_code,
                       finished_at=datetime.now(timezone.utc).isoformat())
        if response.status_code not in expected:
            attempt['state'] = 'rejected_no_retry'; save(state)
            raise Stop(label+'_rejected_'+str(response.status_code))
        attempt['state'] = 'accepted'; last_write = time.monotonic(); save(state)
        return response

    try:
        with httpx.Client(timeout=45, follow_redirects=False, trust_env=False) as client:
            users = rows(client, base, meta_headers, USER_TABLE)
            lists = rows(client, base, meta_headers, LIST_TABLE)
            items = rows(client, base, meta_headers, ITEM_TABLE)
            by_user = {row['id']: row for row in users}
            for user_id, username in USERS.items():
                row = by_user.get(user_id)
                if (not row or row.get('username') != username or row.get('role') != 'member'
                        or row.get('account_status') != 'active'):
                    raise Stop('fixture_user_identity_or_status_mismatch')
            by_list = {row['id']: row for row in lists}
            for list_id, (owner, title, public) in LISTS.items():
                row = by_list.get(list_id)
                if (not row or row.get('user_id') != owner or row.get('title') != title
                        or row.get('default_key') is not None or row.get('is_public') is not public):
                    raise Stop('fixture_list_identity_or_visibility_mismatch')
                refs = [entry.get('id') for entry in items if entry.get('list_id') == list_id]
                state.setdefault('references', {})[str(list_id)] = refs
                if refs:
                    raise Stop('fixture_list_has_references')
            exposed = public_ids(client, social)
            if 119 not in exposed or 120 in exposed:
                raise Stop('public_visibility_does_not_match_review')
            state['preflight'] = {'users': {str(i): digest(by_user[i]) for i in USERS},
                'lists': {str(i): digest(by_list[i]) for i in LISTS},
                'list_count': len(lists), 'item_count': len(items),
                'list_hashes': {str(row['id']): digest(row) for row in lists},
                'item_hashes': {str(row['id']): digest(row) for row in items},
                'public_exposed_fixture_ids': sorted(exposed.intersection(LISTS))}
            state['checks'].append({'check': 'fixture_identity_references_and_visibility_verified', 'passed': True})
            save(state)

            token = login_console(client, auth, state) if args.console_login else login_window(client, auth, social, state)
            if not token:
                raise Stop('admin_login_not_completed')
            admin_headers = {'Authorization': 'Bearer '+token, 'x-data-source': 'live'}

            # Make the only public custom fixture private and confirm the visitor endpoint hides it.
            write(client, 'PUT', f'{base}/table/{LIST_TABLE}/content/119',
                  {**meta_headers, 'x-data-source': 'live'}, {'is_public': False}, 'privatize_list_119')
            row = client.get(f'{base}/table/{LIST_TABLE}/content/119',
                headers={**meta_headers, 'x-data-source': 'live'})
            if row.status_code != 200 or row.json().get('is_public') is not False or 119 in public_ids(client, social):
                raise Stop('list_119_privacy_verification_failed')
            state['checks'].append({'check': 'list_119_private_and_hidden', 'passed': True}); save(state)

            for list_id, (owner, title, _was_public) in LISTS.items():
                current = client.get(f'{base}/table/{LIST_TABLE}/content/{list_id}',
                    headers={**meta_headers, 'x-data-source': 'live'})
                current_items = rows(client, base, meta_headers, ITEM_TABLE)
                if current.status_code != 200:
                    raise Stop('list_identity_recheck_failed')
                row = current.json()
                if (row.get('id') != list_id or row.get('user_id') != owner or row.get('title') != title
                        or row.get('is_public') is not False
                        or any(entry.get('list_id') == list_id for entry in current_items)):
                    raise Stop('list_identity_or_references_changed_before_delete')
                write(client, 'DELETE', f'{base}/table/{LIST_TABLE}/content/{list_id}',
                      {**meta_headers, 'x-data-source': 'live'}, None, 'delete_list_'+str(list_id))
                after_lists = rows(client, base, meta_headers, LIST_TABLE)
                after_items = rows(client, base, meta_headers, ITEM_TABLE)
                if any(entry.get('id') == list_id for entry in after_lists):
                    raise Stop('list_delete_not_verified')
                if {str(r['id']): digest(r) for r in after_items} != state['preflight']['item_hashes']:
                    raise Stop('list_items_changed_during_cleanup')
                state['checks'].append({'check': 'list_'+str(list_id)+'_deleted_and_items_preserved', 'passed': True})
                save(state)

            for user_id in (49, 48):
                lookup = client.get(social+'/admin/users', headers=admin_headers,
                    params={'search': USERS[user_id], 'page': 1, 'per_page': 25})
                values = lookup.json().get('items', []) if lookup.status_code == 200 else []
                matches = [r for r in values if r.get('id') == user_id and r.get('username') == USERS[user_id]]
                if len(matches) != 1 or matches[0].get('role') != 'member' or matches[0].get('account_status') != 'active':
                    if len(matches) == 1 and matches[0].get('account_status') == 'disabled':
                        state['checks'].append({'check': 'user_'+str(user_id)+'_already_disabled', 'passed': True})
                        save(state); continue
                    raise Stop('admin_fixture_identity_or_status_mismatch')
                write(client, 'PUT', social+f'/admin/users/{user_id}/status', admin_headers,
                      {'account_status': 'disabled', 'reason': RUN+' approved fixture cleanup'},
                      'disable_user_'+str(user_id), expected=(200,))
                verify = client.get(social+'/admin/users', headers=admin_headers,
                    params={'search': USERS[user_id], 'page': 1, 'per_page': 25})
                after = verify.json().get('items', []) if verify.status_code == 200 else []
                matches = [r for r in after if r.get('id') == user_id]
                if len(matches) != 1 or matches[0].get('account_status') != 'disabled':
                    raise Stop('user_disable_verification_failed')
                state['checks'].append({'check': 'user_'+str(user_id)+'_disabled', 'passed': True}); save(state)

            state['passed'] = True; state['phase'] = 'complete'
            state['completed_at'] = datetime.now(timezone.utc).isoformat(); save(state)
    except Exception as exc:
        state['failure_reason'] = str(exc) if isinstance(exc, Stop) else type(exc).__name__
        state['phase'] = 'interrupted'; save(state)
        raise


if __name__ == '__main__':
    main()
