"""Supervised two-code recovery acceptance. Real execution needs specific approval."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import secrets
import time
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]


class CheckStopped(RuntimeError):
    """Only fixed, non-private messages may reach the operator."""


class Probe:
    def __init__(self, client, base, output, *, approval_reference,
                 clock=time.monotonic, sleep=time.sleep):
        origin = urlsplit(base)
        synthetic = type(client._transport) is httpx.MockTransport
        if (origin.scheme != 'https' or not origin.hostname or origin.username or
                origin.password or origin.query or origin.fragment or
                not (origin.hostname.endswith('.xano.io') or
                     synthetic and origin.hostname.endswith('.invalid'))):
            raise CheckStopped('invalid_destination')
        if not approval_reference.strip():
            raise CheckStopped('specific_approval_reference_required')
        self.client, self.base, self.output = client, base.rstrip('/'), Path(output)
        self.clock, self.sleep = clock, sleep
        self.phase, self.restoration_needed = 'new', False
        self.email = self.original = self.initial_token = ''
        self.user_id = None
        self.mail_requests = 0
        self.requests = 0
        self.login_rejections = 0
        self.last_call = None
        self.requested_at = None
        self.pending_request = False
        self.report = {'layer': 'simulated_transport' if synthetic else 'supervised_real_api',
                       'started_at': datetime.now(timezone.utc).isoformat(),
                       'approval_reference_sha256': hashlib.sha256(approval_reference.encode()).hexdigest(),
                       'passed': False, 'restoration_needed': False, 'checks': []}
        with self.output.open('x', encoding='utf-8') as stream:
            json.dump(self.report, stream, indent=2)

    def save(self):
        self.report.update(phase=self.phase, restoration_needed=self.restoration_needed,
                           mail_requests_attempted=self.mail_requests, requests_attempted=self.requests)
        temporary = self.output.with_suffix(self.output.suffix + '.tmp')
        temporary.write_text(json.dumps(self.report, indent=2) + '\n', encoding='utf-8')
        temporary.replace(self.output)

    def resume_pending(self, path):
        """Reuse an unconsumed request after a closed window; never send it again."""
        self.require('new')
        raw = Path(path).read_bytes()
        previous = json.loads(raw)
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(previous['started_at'])).total_seconds()
        if (previous.get('phase') != 'awaiting_first_code' or previous.get('restoration_needed') is not False
                or previous.get('mail_requests_attempted') != 1 or not 0 <= age < 900
                or previous.get('layer') != self.report['layer']
                or previous.get('approval_reference_sha256') != self.report['approval_reference_sha256']
                or not any(row.get('scenario') == 'request_accepted_not_delivery_proof' and row.get('passed') is True
                           for row in previous.get('checks', []))):
            raise CheckStopped('pending_request_cannot_be_resumed')
        self.pending_request = True
        self.mail_requests = 1
        self.requests = previous['requests_attempted']
        self.requested_at = self.clock()  # Conservative new cooldown after restart.
        self.report['resumed_evidence_sha256'] = hashlib.sha256(raw).hexdigest()
        self.report['operator_observation_unavailable_on_resume'] = True
        self.save()

    def check(self, name, passed):
        self.report['checks'].append({'scenario': name, 'passed': bool(passed)})
        self.save()
        if not passed:
            raise CheckStopped(name)

    def require(self, phase):
        if self.phase != phase:
            raise CheckStopped('operation_not_available')

    def call(self, method, path, **kwargs):
        if self.requests >= 24:
            raise CheckStopped('request_budget_exhausted_manual_recovery_required')
        if self.last_call is not None:
            self.sleep(max(0, 2.2 - (self.clock() - self.last_call)))
        self.last_call = self.clock()
        self.requests += 1
        self.save()
        try:
            response = self.client.request(method, self.base + path, **kwargs)
        except httpx.RequestError:
            raise CheckStopped('network_result_uncertain_no_retry') from None
        self.report['last_http_status'] = response.status_code
        self.save()
        return response

    def session(self, response):
        try:
            body = response.json()
            if (response.status_code != 200 or not isinstance(body, dict) or
                    type(body.get('user_id')) is not int or body['user_id'] <= 0 or
                    not isinstance(body.get('authToken'), str) or not body['authToken']):
                raise ValueError()
            return body['authToken'], body['user_id']
        except (ValueError, KeyError, TypeError):
            raise CheckStopped('invalid_session_response') from None

    def login(self, password):
        return self.call('POST', '/auth/login', json={'email': self.email, 'password': password})

    def send(self):
        if self.mail_requests >= 2:
            raise CheckStopped('mail_budget_exhausted')
        if self.requested_at is not None and self.clock() - self.requested_at < 61:
            raise CheckStopped('wait_for_backend_cooldown')
        self.mail_requests += 1
        self.requested_at = self.clock()
        self.save()
        response = self.call('GET', '/reset/request-reset-link', params={'email': self.email})
        self.requested_at = self.clock()  # Wait a full cooldown after the response.
        self.check('request_accepted_not_delivery_proof', response.status_code == 200)

    def begin(self, email, original):
        self.require('new')
        if self.login_rejections >= 3:
            raise CheckStopped('initial_login_attempt_limit')
        if not email.strip() or not original:
            raise CheckStopped('private_account_details_required')
        self.email, self.original = email.strip(), original
        self.phase = 'initial_login'
        self.save()
        response = self.login(original)
        if response.status_code in (401, 403):
            self.login_rejections += 1
            self.report['initial_login_rejections'] = self.login_rejections
            self.phase = 'new'
            self.email = self.original = ''
            self.save()
            raise CheckStopped('login_rejected_check_current_codeboxd_password')
        self.initial_token, self.user_id = self.session(response)
        self.check('controlled_account_login', True)
        self.phase = 'initial_request'
        if not self.pending_request:
            self.send()
        self.phase = 'awaiting_first_code'
        self.save()

    def consume(self, code):
        token, user_id = self.session(self.call('POST', '/reset/magic-link-login',
                                               json={'email': self.email, 'magic_token': code}))
        self.check('reset_identity_matches', user_id == self.user_id)
        return token

    def update(self, reset_token, password):
        return self.call('POST', '/reset/update_password',
                         headers={'Authorization': 'Bearer ' + reset_token},
                         json={'password': password, 'confirm_password': password})

    def first_code(self, code):
        self.require('awaiting_first_code')
        if not re.fullmatch(r'[0-9]{6}', code):
            raise CheckStopped('six_ascii_digits_required')
        self.phase = 'first_code_attempted'
        if not self.pending_request:
            self.report['operator_observation_seconds'] = round(self.clock() - self.requested_at, 3)
        self.check('operator_reports_first_code_received', True)
        token = self.consume(code)
        temporary = 'Cb9!' + secrets.token_urlsafe(28)
        self.restoration_needed = True
        self.phase = 'password_write_attempted'
        self.save()
        response = self.update(token, temporary)
        self.check('temporary_password_saved', response.status_code == 200)
        _, user_id = self.session(self.login(temporary))
        self.check('new_password_login', user_id == self.user_id)
        response = self.login(self.original)
        self.check('old_password_rejected', response.status_code in (401, 403))
        response = self.call('POST', '/reset/magic-link-login',
                             json={'email': self.email, 'magic_token': code})
        self.check('used_code_rejected', response.status_code == 401)
        response = self.call('GET', '/auth/me', headers={'Authorization': 'Bearer ' + self.initial_token})
        self.check('previous_session_revoked', response.status_code in (401, 403))
        self.phase = 'ready_for_restoration'
        self.save()

    def confirm_original(self):
        """Reconcile after an uncertain write without changing a password."""
        if not self.restoration_needed:
            raise CheckStopped('restoration_not_pending')
        response = self.login(self.original)
        if response.status_code in (401, 403):
            return False
        _, user_id = self.session(response)
        self.check('original_password_login_confirmed', user_id == self.user_id)
        self.restoration_needed = False
        self.phase = 'restored'
        self.report['passed'] = all(row['passed'] for row in self.report['checks']) and all(
            any(row['scenario'] == name and row['passed'] for row in self.report['checks'])
            for name in ('temporary_password_saved', 'new_password_login', 'old_password_rejected',
                         'used_code_rejected', 'previous_session_revoked', 'original_password_saved'))
        self.save()
        self.email = self.original = self.initial_token = ''
        return True

    def request_restoration(self):
        if not self.restoration_needed or self.phase in ('restoration_request_attempted', 'awaiting_restore_code',
                                                        'restoration_write_attempted', 'restored'):
            raise CheckStopped('restoration_request_not_available')
        if self.requested_at is not None and self.clock() - self.requested_at < 61:
            raise CheckStopped('wait_for_backend_cooldown')
        self.phase = 'restoration_request_attempted'
        self.send()
        self.phase = 'awaiting_restore_code'
        self.save()

    def restore_code(self, code):
        self.require('awaiting_restore_code')
        if not re.fullmatch(r'[0-9]{6}', code):
            raise CheckStopped('six_ascii_digits_required')
        self.phase = 'restoration_code_attempted'
        self.check('operator_reports_second_code_received', True)
        token = self.consume(code)
        self.phase = 'restoration_write_attempted'
        self.save()
        response = self.update(token, self.original)
        self.check('original_password_saved', response.status_code == 200)
        self.check('restored_password_login', self.confirm_original())


def available_actions(probe):
    """UI availability follows the same phases as the transport guards."""
    actions = set()
    if probe.phase == 'new' and probe.login_rejections < 3:
        actions.add('begin')
    if probe.phase == 'awaiting_first_code':
        actions.add('first')
    if probe.phase == 'awaiting_restore_code':
        actions.add('restore')
    if probe.restoration_needed:
        actions.add('confirm')
        if (probe.mail_requests < 2 and probe.phase not in ('restoration_request_attempted',
                'awaiting_restore_code', 'restoration_write_attempted', 'restored')
                and probe.clock() - probe.requested_at >= 61):
            actions.add('request_restore')
    return actions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--approval-reference')
    parser.add_argument('--config', type=Path, default=ROOT / '.env')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--pending-request', type=Path)
    args = parser.parse_args(argv)
    if not args.execute or not args.approval_reference or not args.approval_reference.strip():
        parser.error('Specific approval, --execute and --approval-reference are required before any network call.')
    if args.output.exists():
        parser.error('Preserve existing evidence; use a new output.')
    config = dotenv_values(args.config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    import tkinter as tk
    from tkinter import ttk
    with httpx.Client(timeout=25, follow_redirects=False, trust_env=False) as client:
        probe = Probe(client, config.get('XANO_AUTH_URL', ''), args.output,
                      approval_reference=args.approval_reference)
        if args.pending_request:
            probe.resume_pending(args.pending_request)
        window = tk.Tk()
        window.title('Codeboxd — aceite supervisionado de recuperação')
        frame = ttk.Frame(window, padding=18)
        frame.pack()
        ttk.Label(frame, text='Conta de teste autorizada. Dois e-mails; restauração usa um novo código.').pack()
        ttk.Label(frame, text='E-mail Codeboxd').pack()
        email = ttk.Entry(frame, width=60)
        email.pack()
        ttk.Label(frame, text='Senha atual Codeboxd (somente nesta janela)').pack()
        password = ttk.Entry(frame, width=60, show='*')
        password.pack()
        ttk.Label(frame, text='Código recebido da solicitação atual').pack()
        code = ttk.Entry(frame, width=20, show='*')
        code.pack()
        notice = ttk.Label(frame, text='Nenhuma operação iniciada.', wraplength=530)
        notice.pack(pady=12)
        instruction = ttk.Label(frame, text='', wraplength=530)
        instruction.pack(pady=8)
        buttons = {}

        def refresh():
            allowed = available_actions(probe)
            for name, button in buttons.items():
                button.configure(state='normal' if name in allowed else 'disabled')
            email.configure(state='normal' if 'begin' in allowed else 'disabled')
            password.configure(state='normal' if 'begin' in allowed else 'disabled')
            code.configure(state='normal' if allowed & {'first', 'restore'} else 'disabled')
            messages = {
                'new': 'Informe a MESMA conta de teste. ' + ('O código anterior será usado; nenhum novo e-mail será solicitado.' if probe.pending_request else 'Use o botão 1 para solicitar o código.'),
                'awaiting_first_code': 'Login confirmado. Abra o e-mail já solicitado, preencha o código de seis dígitos e use SOMENTE o botão 2.',
                'awaiting_restore_code': 'Abra o segundo e-mail, informe o código de restauração e use SOMENTE o botão 4.',
                'restored': 'Senha original confirmada. Você pode fechar a janela.',
            }
            remaining = max(0, int(62 - (probe.clock() - probe.requested_at))) if probe.requested_at is not None else 0
            instruction.configure(text=messages.get(probe.phase, 'Etapa: ' + probe.phase + '. Restauração pendente: ' + str(probe.restoration_needed))
                                  + (f' Aguarde {remaining}s para solicitar restauração.' if probe.restoration_needed and probe.mail_requests < 2 and remaining else ''))

        def tick():
            refresh()
            window.after(1000, tick)

        def action(operation):
            phase_before = probe.phase
            try:
                operation()
                notice.configure(text='Etapa: ' + probe.phase + '. Restauração pendente: ' + str(probe.restoration_needed))
            except Exception as error:
                probe.report['passed'] = False
                probe.report['interrupted'] = True
                probe.report['failure_type'] = type(error).__name__
                if isinstance(error, CheckStopped):
                    probe.report['failure_reason'] = str(error)
                probe.save()
                if isinstance(error, CheckStopped) and str(error) == 'login_rejected_check_current_codeboxd_password':
                    notice.configure(text='Login rejeitado pelo servidor. Confira o e-mail e a senha ATUAL do Codeboxd (não a senha da caixa de e-mail). Nenhum código enviado ou senha alterada. Preencha novamente e use o botão 1; limite de três tentativas.')
                else:
                    notice.configure(text=('Interrompido: ' + str(error) if isinstance(error, CheckStopped) else 'Interrompido sem detalhes privados.')
                                     + ' Etapa: ' + probe.phase + '. Não repita escritas. Confirme a senha original ou use nova recuperação.')
            finally:
                password.configure(state='normal')
                password.delete(0, 'end')
                if probe.phase != phase_before:
                    code.configure(state='normal')
                    code.delete(0, 'end')
                refresh()

        for name, title, operation in (
            ('begin', '1. Validar conta e continuar' if probe.pending_request else '1. Login e solicitar primeiro código', lambda: probe.begin(email.get(), password.get())),
            ('first', '2. Confirmar primeiro código e testar troca', lambda: probe.first_code(code.get())),
            ('request_restore', '3. Solicitar código de restauração (após 61s)', probe.request_restoration),
            ('restore', '4. Restaurar com segundo código', lambda: probe.restore_code(code.get())),
            ('confirm', 'Conferir senha original após resultado incerto', probe.confirm_original),
        ):
            button = ttk.Button(frame, text=title, command=lambda op=operation: action(op))
            button.pack(pady=3)
            buttons[name] = button

        def close():
            if probe.restoration_needed:
                notice.configure(text='Restauração não confirmada. Preserve esta janela e conclua a recuperação; não há restauração automática.')
                return
            window.destroy()

        window.protocol('WM_DELETE_WINDOW', close)
        tick()
        window.mainloop()
        return 0 if probe.report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
