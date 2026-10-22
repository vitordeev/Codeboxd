"""Interactive real-mail recovery check; secrets remain only in process memory."""
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import secrets

import httpx
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "openspec/changes/recuperar-senha-codigo-6-digitos/validation/email-real-resend-2026-10-22.json"


class Probe:
    def __init__(self, client, base):
        self.client = client
        self.base = base.rstrip("/")
        self.report = {"layer": "real_api_and_user_received_email", "passed": False,
                       "started_at": datetime.now(timezone.utc).isoformat(), "checks": []}
        self.stage = "not_started"
        self.restoration_needed = False

    def record(self, name, passed, response=None):
        check = {"scenario": name, "passed": bool(passed)}
        if response is not None:
            check["http_status"] = response.status_code
        self.report["checks"].append(check)
        self.save()
        if not passed:
            raise RuntimeError(name)

    def save(self):
        OUTPUT.write_text(json.dumps(self.report, indent=2) + "\n", encoding="utf-8")

    def login(self, email, password):
        return self.client.post(self.base + "/auth/login", json={"email": email, "password": password})

    def request(self, email, password):
        self.stage = "initial_login"
        response = self.login(email, password)
        self.record("controlled_account_login", response.status_code == 200, response)
        session = response.json()
        token, user_id = session["authToken"], session["user_id"]
        self.stage = "request_email"
        response = self.client.get(self.base + "/reset/request-reset-link", params={"email": email})
        self.record("request_accepted_not_delivery_proof", response.status_code == 200, response)
        return token, user_id

    def update(self, token, password):
        return self.client.post(self.base + "/reset/update_password",
                                headers={"Authorization": "Bearer " + token},
                                json={"password": password, "confirm_password": password})

    def complete(self, email, original, code, original_token, user_id):
        changed_possible = False
        self.stage = "received_code"
        self.record("user_received_email_with_six_ascii_digits", bool(re.fullmatch(r"[0-9]{6}", code)))
        temporary = "CbTest!" + secrets.token_urlsafe(28)
        try:
            self.stage = "consume_code"
            response = self.client.post(self.base + "/reset/magic-link-login",
                                        json={"email": email, "magic_token": code})
            self.record("received_code_accepted", response.status_code == 200, response)
            session = response.json()
            self.record("reset_identity_matches", session.get("user_id") == user_id)
            self.stage = "temporary_password_update"
            # A timeout may hide a committed update: always attempt restoration.
            changed_possible = True
            self.restoration_needed = True
            response = self.update(session["authToken"], temporary)
            self.record("temporary_password_saved", response.status_code == 200, response)
            self.stage = "new_password_login"
            response = self.login(email, temporary)
            self.record("new_password_login", response.status_code == 200
                        and response.json().get("user_id") == user_id, response)
            self.stage = "old_password_rejected"
            response = self.login(email, original)
            self.record("old_password_rejected", response.status_code in (401, 403), response)
            self.stage = "reuse_code"
            response = self.client.post(self.base + "/reset/magic-link-login",
                                        json={"email": email, "magic_token": code})
            self.record("used_code_rejected", response.status_code == 401
                        and response.json().get("code") == "ERROR_CODE_UNAUTHORIZED", response)
        finally:
            if changed_possible:
                self.stage = "restore_original_password"
                response = self.update(original_token, original)
                self.record("original_password_restored", response.status_code == 200, response)
                response = self.login(email, original)
                self.record("restored_password_login", response.status_code == 200
                            and response.json().get("user_id") == user_id, response)
                self.restoration_needed = False
        self.report["passed"] = all(check["passed"] for check in self.report["checks"])
        self.stage = "complete"
        self.save()


def main():
    import tkinter as tk
    from tkinter import ttk

    config = dotenv_values(ROOT / ".env")
    client = httpx.Client(timeout=25, follow_redirects=False)
    probe = Probe(client, config["XANO_AUTH_URL"])
    window = tk.Tk()
    window.title("Codeboxd — recuperação de senha com Resend")
    window.geometry("580x550")
    frame = ttk.Frame(window, padding=20)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Use uma conta de teste cuja caixa de e-mail você acessa.").pack(anchor="w")
    ttk.Label(frame, text="A senha original será restaurada após o teste.").pack(anchor="w")
    ttk.Label(frame, text="Não feche o processo durante a troca/restauração.").pack(anchor="w")
    ttk.Label(frame, text="E-mail cadastrado", padding=(0, 12, 0, 0)).pack(anchor="w")
    email = ttk.Entry(frame, width=65)
    email.pack()
    ttk.Label(frame, text="Senha atual do CODEBOXD (não é a senha do Resend)").pack(anchor="w")
    password = ttk.Entry(frame, show="*", width=65)
    password.pack()
    ttk.Label(frame, text="Código recebido neste e-mail (preencha após solicitar)").pack(anchor="w", pady=(12, 0))
    code = ttk.Entry(frame, show="*", width=20)
    code.pack(anchor="w")
    notice = ttk.Label(frame, text="", wraplength=510)
    notice.pack(pady=10)
    state = {}

    def fail(error):
        probe.report["failure_stage"] = probe.stage
        probe.report["failure_type"] = type(error).__name__
        probe.save()
        notice.configure(text="Verificação interrompida em " + probe.stage + ". Resultado registrado sem dados privados.")
        print("CHECK_INTERRUPTED: " + probe.stage + " " + type(error).__name__, flush=True)
        if probe.restoration_needed:
            restore_button.configure(state="normal")
            notice.configure(text="A restauração ainda não foi confirmada. Use Restaurar senha original antes de fechar.")
        elif probe.stage == "initial_login":
            request_button.configure(state="normal")
            notice.configure(text="Login Codeboxd rejeitado. Confira o e-mail e a senha do Codeboxd, não os do Resend, e tente novamente.")

    def restore():
        restore_button.configure(state="disabled")
        try:
            probe.stage = "manual_restore_original_password"
            response = probe.update(state["token"], state["original"])
            probe.record("manual_original_password_restored", response.status_code == 200, response)
            response = probe.login(state["email"], state["original"])
            probe.record("manual_restored_password_login", response.status_code == 200
                         and response.json().get("user_id") == state["user_id"], response)
            probe.restoration_needed = False
            notice.configure(text="Senha original restaurada. O teste incompleto permanece registrado.")
        except Exception as error:
            fail(error)

    def request():
        if not email.get().strip() or not password.get():
            notice.configure(text="Informe e-mail e senha atual da conta de teste.")
            return
        if probe.report["checks"]:
            previous = {"checks": probe.report["checks"], "failure_stage": probe.report.get("failure_stage")}
            probe.report.setdefault("previous_attempts", []).append(previous)
            probe.report["checks"] = []
            probe.report.pop("failure_stage", None)
            probe.report.pop("failure_type", None)
            if len(probe.report["previous_attempts"]) >= 3:
                notice.configure(text="Três tentativas registradas. Confira as credenciais antes de reiniciar o teste.")
                request_button.configure(state="disabled")
                return
        request_button.configure(state="disabled")
        notice.configure(text="Validando a conta e solicitando um único e-mail…")
        window.update_idletasks()
        try:
            state["email"], state["original"] = email.get().strip(), password.get()
            state["token"], state["user_id"] = probe.request(state["email"], state["original"])
            password.delete(0, "end")
            email.configure(state="disabled")
            password.configure(state="disabled")
            complete_button.configure(state="normal")
            notice.configure(text="Solicitação aceita. Abra a caixa de entrada/spam e informe o código recebido. A resposta da API ainda não comprova a entrega.")
            code.focus_set()
            print("WAITING_FOR_EMAIL_CODE: informe na janela o código recebido no e-mail.", flush=True)
        except Exception as error:
            fail(error)

    def complete():
        if not re.fullmatch(r"[0-9]{6}", code.get().strip()):
            notice.configure(text="Informe os seis dígitos do e-mail recebido agora.")
            return
        complete_button.configure(state="disabled")
        notice.configure(text="Executando troca, login, rejeição de reutilização e restauração…")
        window.update_idletasks()
        try:
            probe.complete(state["email"], state["original"], code.get().strip(), state["token"], state["user_id"])
            code.delete(0, "end")
            state.clear()
            notice.configure(text="Concluído. Senha original restaurada e login confirmado.")
            print("RECOVERY_COMPLETE: " + json.dumps(probe.report), flush=True)
            window.after(2000, window.destroy)
        except Exception as error:
            fail(error)

    request_button = ttk.Button(frame, text="Validar conta e enviar código por e-mail", command=request)
    request_button.pack(pady=4)
    complete_button = ttk.Button(frame, text="Confirmar recebimento e executar teste", command=complete, state="disabled")
    complete_button.pack(pady=4)
    restore_button = ttk.Button(frame, text="Restaurar senha original", command=restore, state="disabled")
    restore_button.pack(pady=4)
    def close():
        if probe.restoration_needed:
            notice.configure(text="Restaure a senha original pelo botão antes de fechar.")
            return
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", close)
    email.focus_set()
    print("READY_FOR_RECOVERY_LOGIN: use a janela local; nunca envie senha/código no chat.", flush=True)
    try:
        window.mainloop()
    finally:
        if not probe.report["passed"]:
            probe.report["incomplete"] = True
            probe.save()
        client.close()
    return 0 if probe.report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
