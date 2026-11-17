"""Restore a supervised account without repeating the temporary-password trial."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import httpx
from dotenv import dotenv_values

from tools.password_recovery_remote import ROOT, Probe, CheckStopped


class Restoration(Probe):
    def begin_restore(self, email, password, confirmation, same_account):
        self.require('new')
        if (not same_account or not re.fullmatch(r'[^\s@]+@[^\s@]+', email.strip())
                or password != confirmation or not 8 <= len(password) <= 128
                or not re.search('[A-Za-z]', password) or not re.search('[0-9]', password)):
            raise CheckStopped('confirm_same_account_and_valid_matching_password')
        self.email, self.original = email.strip(), password
        self.restoration_needed = True
        self.phase = 'checking_existing_password'
        self.save()
        response = self.login(password)
        if response.status_code == 200:
            token, self.user_id = self.session(response)
            self.finish(token)
            return
        if response.status_code not in (401, 403):
            raise CheckStopped('initial_login_unexpected_no_mail_sent')
        self.phase = 'request_attempted'
        self.save()
        # Guard before the network call: never send again after uncertainty.
        self.mail_requests = 1
        response = self.call('GET', '/reset/request-reset-link', params={'email': self.email})
        self.check('single_request_accepted_not_delivery_proof', response.status_code == 200)
        self.phase = 'awaiting_restore_code'
        self.save()

    def restore(self, code):
        self.require('awaiting_restore_code')
        if not re.fullmatch('[0-9]{6}', code):
            raise CheckStopped('six_ascii_digits_required')
        self.phase = 'restore_code_attempted'
        self.check('operator_received_new_code', True)
        response = self.call('POST', '/reset/magic-link-login',
                             json={'email': self.email, 'magic_token': code})
        token, self.user_id = self.session(response)
        self.phase = 'restoration_write_attempted'
        self.save()
        response = self.update(token, self.original)
        self.check('original_password_saved', response.status_code == 200)
        self.phase = 'restoration_verification'
        self.save()
        token, user_id = self.session(self.login(self.original))
        self.check('restored_login_identity_matches', user_id == self.user_id)
        self.finish(token)

    def finish(self, token):
        response = self.call('GET', '/auth/me', headers={'Authorization': 'Bearer ' + token})
        try:
            body = response.json()
            matches = (response.status_code == 200 and type(body.get('id')) is int
                       and body['id'] == self.user_id
                       and isinstance(body.get('email'), str)
                       and body['email'].casefold() == self.email.casefold())
        except (ValueError, AttributeError, TypeError):
            matches = False
        self.check('controlled_account_identity_confirmed', matches)
        self.restoration_needed = False
        self.phase = 'restored'
        self.report['passed'] = True
        self.report['acceptance_scope'] = 'restoration_only_linked_to_previous_trial'
        self.save()
        self.email = self.original = self.initial_token = ''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--approval-reference', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if not args.execute or not args.approval_reference.strip() or args.output.exists():
        parser.error('Specific approval, execution flag and new evidence path required.')
    previous = ROOT / 'openspec/changes/recuperar-senha-codigo-6-digitos/validation/ciclo-controlado-retomada-2-2026-11-12.json'
    raw = previous.read_bytes()
    if json.loads(raw).get('restoration_needed') is not True:
        parser.error('Previous pending restoration evidence required.')
    import tkinter as tk
    from tkinter import ttk
    config = dotenv_values(ROOT / '.env')
    with httpx.Client(timeout=30, follow_redirects=False, trust_env=False) as client:
        probe = Restoration(client, config.get('XANO_AUTH_URL', ''), args.output,
                            approval_reference=args.approval_reference)
        probe.report['previous_trial_sha256'] = hashlib.sha256(raw).hexdigest()
        probe.save()
        window = tk.Tk()
        window.title('Codeboxd - restaurar conta controlada')
        frame = ttk.Frame(window, padding=18)
        frame.pack()
        fields = []
        for label, masked in [('E-mail da mesma conta do ensaio anterior', False),
                              ('Senha original que deseja restaurar', True),
                              ('Confirme essa senha', True), ('Novo codigo recebido (se solicitado)', True)]:
            ttk.Label(frame, text=label).pack()
            field = ttk.Entry(frame, width=58, show='*' if masked else '')
            field.pack(pady=4)
            fields.append(field)
        confirmed = tk.BooleanVar()
        ttk.Checkbutton(frame, text='Confirmo: mesma conta controlada do ensaio anterior', variable=confirmed).pack()
        status = tk.StringVar(value='Verifica a senha primeiro. No maximo um pedido novo; sem retries.')
        ttk.Label(frame, textvariable=status, wraplength=480).pack(pady=10)
        def action(restore=False):
            if restore:
                restore_button.configure(state='disabled')
            else:
                begin.configure(state='disabled')
            try:
                status.set('Operacao em andamento...')
                window.update_idletasks()
                if restore:
                    code = fields[3].get().strip()
                    fields[3].delete(0, 'end')
                    probe.restore(code)
                    code = ''
                else:
                    probe.begin_restore(fields[0].get(), fields[1].get(), fields[2].get(), confirmed.get())
                    for field in fields[:3]:
                        field.delete(0, 'end')
                        field.configure(state='disabled')
                if probe.phase == 'restored':
                    status.set('Senha e identidade confirmadas no login. Restauracao concluida; pode fechar.')
                else:
                    status.set('Pedido aceito. Informe somente o NOVO codigo nesta janela e clique Restaurar.')
                    restore_button.configure(state='normal')
            except CheckStopped as exc:
                probe.report['failure_reason'] = str(exc)
                probe.save()
                status.set('Interrompido: ' + str(exc) + '. Sem reenvio ou repeticao automatica.')
                if probe.phase == 'new':
                    begin.configure(state='normal')
                elif restore and probe.phase == 'awaiting_restore_code':
                    restore_button.configure(state='normal')
        begin = ttk.Button(frame, text='Verificar senha / solicitar um codigo', command=action)
        begin.pack(pady=6)
        restore_button = ttk.Button(frame, text='Restaurar e confirmar login', command=lambda: action(True), state='disabled')
        restore_button.pack(pady=6)
        window.mainloop()


if __name__ == '__main__':
    main()
