"""Supervised cleanup for the explicitly approved, rate-limited pilot run."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import tkinter as tk
from tkinter import ttk

import httpx
from dotenv import dotenv_values

from tools.session_revocation import ROOT

RUN = 'cbshared_35b8a42f44c4'
SOURCE = ROOT/'openspec/changes/validar-integracoes-xano-atual/pilot-execution-final-2026-11-18.json'
EXPECTED_USERS = {
    'a': {'id': 46, 'username': RUN+'_a'},
    'b': {'id': 47, 'username': RUN+'_b'},
}
DEFAULT_LIST_IDS = (111, 112, 113, 114)


class Stop(RuntimeError):
    pass


def rows(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get('items'), list):
        return value['items']
    raise Stop('response_shape_unknown')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text(encoding='utf-8'))
    if (source.get('run_id') != RUN or source.get('failure_reason') != 'write_rejected_429'
            or source.get('remote_writes') != 6 or args.output.exists()
            or not args.output.resolve().is_relative_to((ROOT/'openspec/changes/validar-integracoes-xano-atual').resolve())):
        parser.error('Source receipt or fresh change-local output rejected.')
    fixtures = source.get('fixtures', {})
    for key, expected in EXPECTED_USERS.items():
        actual = fixtures.get('user_'+key, {})
        if actual.get('id') != expected['id'] or actual.get('username') != expected['username']:
            parser.error('Fixture identity mismatch.')
    default_a = [row.get('id') for row in fixtures.get('defaults_a', [])]
    default_b = [row.get('id') for row in fixtures.get('defaults_b', [])]
    # The fourth list's write was rate-limited before its receipt could be saved;
    # independent read-only inventory confirmed it as B's 45:completed list.
    if sorted(default_a) != [111, 112] or sorted(default_b) != [113]:
        parser.error('Default list receipt mismatch.')

    config = dotenv_values(ROOT/'.env')
    auth_base = config['XANO_AUTH_URL'].rstrip('/')
    social_base = config['XANO_SOCIAL_URL'].rstrip('/')
    state = {'layer': 'supervised_xano_fixture_reconciliation', 'run_id': RUN,
             'passed': False, 'remote_writes': 0, 'checks': [], 'write_attempts': [],
             'fixture_ids': {'users': [46, 47], 'lists': list(DEFAULT_LIST_IDS)},
             'custom_lists_created': 0, 'phase': 'awaiting_admin_login'}

    def save():
        path = args.output.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(state, indent=2)+'\n', encoding='utf-8')
        tmp.replace(path)

    window = tk.Tk()
    window.title('Reconciliar piloto interrompido')
    frame = ttk.Frame(window, padding=18)
    frame.pack()
    ttk.Label(frame, text='Confirme o administrador do Codeboxd. O reconciliador só desativa as contas 46 e 47, depois de confirmar que as listas 111–114 estão privadas.').pack()
    fields = []
    for label, masked in [('E-mail do administrador', False), ('Senha do administrador', True)]:
        ttk.Label(frame, text=label).pack()
        field = ttk.Entry(frame, width=56, show='*' if masked else '')
        field.pack(pady=4)
        fields.append(field)
    status = tk.StringVar(value='Nenhuma escrita será feita antes das verificações.')
    ttk.Label(frame, textvariable=status, wraplength=540).pack(pady=8)
    button = ttk.Button(frame, text='Verificar e reconciliar contas de teste')

    def run():
        button.configure(state='disabled')
        email = fields[0].get().strip()
        secret = fields[1].get()
        fields[1].delete(0, 'end')
        try:
            state['phase'] = 'admin_login'
            save()
            with httpx.Client(timeout=90, follow_redirects=False, trust_env=False) as client:
                login = client.post(auth_base+'/auth/login', headers={'x-data-source': 'live'},
                                    json={'email': email, 'password': secret})
                if login.status_code != 200:
                    raise Stop('admin_login_rejected')
                body = login.json()
                token = body.get('authToken')
                if body.get('user_id') != 14 or not isinstance(token, str):
                    raise Stop('expected_admin_identity_mismatch')
                headers = {'Authorization': 'Bearer '+token, 'x-data-source': 'live'}
                me = client.get(auth_base+'/auth/me', headers=headers)
                actor = me.json() if me.status_code == 200 else {}
                if (actor.get('id') != 14 or actor.get('role') != 'admin'
                        or actor.get('account_status') != 'active'
                        or str(actor.get('email', '')).casefold() != email.casefold()):
                    raise Stop('active_admin_confirmation_failed')
                state['admin_confirmed'] = True
                state['phase'] = 'verify_lists_private'
                save()

                public = client.get(social_base+'/lists/public', headers={'x-data-source': 'live'},
                                    params={'page': 1, 'per_page': 100})
                if public.status_code != 200:
                    raise Stop('public_lists_read_failed')
                visible = {row.get('id') for row in rows(public.json())}
                if any(list_id in visible for list_id in DEFAULT_LIST_IDS):
                    state['public_fixture_lists_still_visible'] = sorted(visible.intersection(DEFAULT_LIST_IDS))
                    save()
                    raise Stop('fixture_default_list_still_public_manual_privacy_fix_required')
                state['checks'].append({'check': 'all_fixture_defaults_private', 'passed': True})
                state['phase'] = 'verify_fixture_identities'

                found_users = {}
                for key, expected in EXPECTED_USERS.items():
                    response = client.get(social_base+'/admin/users', headers=headers,
                                          params={'search': expected['username'], 'page': 1, 'per_page': 25})
                    if response.status_code != 200:
                        raise Stop('fixture_lookup_failed')
                    matches = [row for row in rows(response.json())
                               if row.get('id') == expected['id'] and row.get('username') == expected['username']]
                    if len(matches) != 1 or matches[0].get('role') != 'member':
                        raise Stop('fixture_identity_or_role_mismatch')
                    found_users[key] = matches[0]
                state['checks'].append({'check': 'fixture_identity_and_role_verified', 'passed': True})
                state['phase'] = 'disable_fixture_b'
                save()

                previous_write = 0.0
                for key in ('b', 'a'):
                    state['phase'] = 'disable_fixture_'+key
                    save()
                    user = found_users[key]
                    if user.get('account_status') == 'disabled':
                        state.setdefault('already_disabled', []).append(user['id'])
                        continue
                    if user.get('account_status') != 'active':
                        raise Stop('fixture_status_unexpected')
                    pause = max(0.0, 1.25-(time.monotonic()-previous_write)) if previous_write else 0.0
                    if pause:
                        time.sleep(pause)
                    attempt = {'action': 'disable_fixture_'+key, 'state': 'attempting',
                               'started_at': datetime.now(timezone.utc).isoformat()}
                    state['write_attempts'].append(attempt)
                    state['remote_writes'] += 1
                    save()
                    try:
                        response = client.put(social_base+f"/admin/users/{user['id']}/status",
                            headers=headers, json={'account_status': 'disabled',
                            'reason': RUN+' interrupted pilot cleanup'})
                    except httpx.RequestError:
                        attempt['state'] = 'uncertain_no_retry'
                        save()
                        raise Stop('cleanup_write_uncertain_no_retry') from None
                    attempt.update(state='response_received', http_status=response.status_code,
                                   finished_at=datetime.now(timezone.utc).isoformat())
                    save()
                    if response.status_code != 200:
                        attempt['state'] = 'rejected_no_retry'
                        save()
                        raise Stop('cleanup_write_rejected_'+str(response.status_code))
                    attempt['state'] = 'accepted'
                    previous_write = time.monotonic()
                    save()
                    verify = client.get(social_base+'/admin/users', headers=headers,
                                        params={'search': user['username'], 'page': 1, 'per_page': 25})
                    if verify.status_code != 200:
                        raise Stop('cleanup_verification_failed')
                    after = [row for row in rows(verify.json()) if row.get('id') == user['id']]
                    if len(after) != 1 or after[0].get('account_status') != 'disabled':
                        raise Stop('cleanup_verification_failed')
                    state.setdefault('disabled_users', []).append(user['id'])
                    state['checks'].append({'check': 'fixture_'+key+'_disabled', 'passed': True})
                    save()

                state['phase'] = 'partial_pilot_aborted_fixtures_disabled'
                state['passed'] = all(row['passed'] for row in state['checks'])
                save()
                status.set('Contas de teste desativadas. O piloto foi abortado; nenhuma fixture foi repetida ou criada de novo.')
        except Exception as exc:
            state['failure_reason'] = str(exc) if isinstance(exc, Stop) else type(exc).__name__
            save()
            status.set('Interrompido: '+state['failure_reason']+'. Sem repeticao automatica.')

    button.configure(command=run)
    button.pack(pady=8)
    window.mainloop()


if __name__ == '__main__':
    main()
