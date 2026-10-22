"""Bounded real-API rejection checks; credentials and records stay in memory.

Run with --session-file pointing to private JSON containing authToken.
Only rejected submissions are attempted; no automatic retry or cleanup writes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]


def interactive_login(auth):
    """Ask the user locally; never expose input through logs or artifacts."""
    import tkinter as tk
    from tkinter import ttk

    window = tk.Tk()
    window.title("Codeboxd — validação de conta de teste")
    window.geometry("460x280")
    window.resizable(False, False)
    frame = ttk.Frame(window, padding=20)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Entre com uma conta de teste do Codeboxd.").pack(anchor="w")
    ttk.Label(frame, text="Senha e sessão ficam somente na memória.").pack(anchor="w")
    ttk.Label(frame, text="E-mail").pack(anchor="w", pady=(12, 0))
    email = ttk.Entry(frame, width=55)
    email.pack()
    ttk.Label(frame, text="Senha").pack(anchor="w")
    password = ttk.Entry(frame, show="*", width=55)
    password.pack()
    notice = ttk.Label(frame, text="")
    notice.pack(pady=8)
    result = {}

    def submit():
        button.configure(state="disabled")
        notice.configure(text="Autenticando…")
        window.update_idletasks()
        try:
            with httpx.Client(timeout=20, follow_redirects=False) as client:
                response = client.post(auth + "/auth/login", json={
                    "email": email.get().strip(), "password": password.get()})
            password.delete(0, "end")
            if response.status_code != 200:
                notice.configure(text=f"Login rejeitado (HTTP {response.status_code}).")
                return
            result["token"] = response.json()["authToken"]
            window.destroy()
        except Exception as error:
            notice.configure(text="Falha de acesso: " + type(error).__name__)
        finally:
            if "token" not in result:
                button.configure(state="normal")

    button = ttk.Button(frame, text="Entrar e executar validação", command=submit)
    button.pack()
    window.bind("<Return>", lambda event: submit())
    window.after(600000, window.destroy)
    email.focus_set()
    print("READY_FOR_USER_LOGIN: use a janela local Codeboxd; não envie senha pelo chat.", flush=True)
    window.mainloop()
    if "token" not in result:
        raise RuntimeError("interactive_login_cancelled_or_expired")
    return result["token"]


def checked(response):
    if response.status_code != 200:
        raise RuntimeError(f"read_http_{response.status_code}")
    return response.json()


def snapshot(client, base, headers, table_id):
    """Hash every record in memory, following bounded metadata pagination."""
    rows = {}
    page = 1
    seen = set()
    while page is not None:
        if page in seen or len(seen) >= 100:
            raise RuntimeError("snapshot_pagination_limit")
        seen.add(page)
        data = checked(client.get(f"{base}/table/{table_id}/content",
                                 headers=headers, params={"page": page, "per_page": 100}))
        for row in data["items"]:
            key = str(row["id"])
            if key in rows:
                raise RuntimeError("snapshot_duplicate_id")
            rows[key] = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
        page = data["nextPage"]
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    login = parser.add_mutually_exclusive_group(required=True)
    login.add_argument("--session-file", type=Path)
    login.add_argument("--interactive-login", action="store_true")
    args = parser.parse_args()
    output = ROOT / "openspec/changes/archive/2026-10-21-exigir-texto-denuncias-avaliacoes/validation/api-real-2026-10-21.json"
    report = {"layer": "authenticated_real_api", "checks": [], "passed": False,
              "started_at": datetime.now(timezone.utc).isoformat()}
    try:
        config = dotenv_values(ROOT / ".env")
        auth = config["XANO_AUTH_URL"].rstrip("/")
        social = config["XANO_SOCIAL_URL"].rstrip("/")
        token = (interactive_login(auth) if args.interactive_login else
                 json.loads(args.session_file.read_text(encoding="utf-8-sig"))["authToken"])
        if not isinstance(token, str) or not token.strip():
            raise RuntimeError("invalid_session_file")
        origin = urlsplit(auth)
        meta = f"{origin.scheme}://{origin.netloc}/api:meta/workspace/147717"
        raw = (Path.home() / ".xano/credentials.yaml").read_text(encoding="utf-8")
        tokens = re.findall(r"^\s*access_token:\s*(.*?)\s*$", raw, re.M)
        if len(tokens) != 1:
            raise RuntimeError("metadata_profile_ambiguous")
        meta_headers = {"Authorization": "Bearer " + tokens[0].strip().strip("'\"")}
        headers = {"Authorization": "Bearer " + token}
        with httpx.Client(timeout=20, follow_redirects=False) as client:
            identity = checked(client.get(auth + "/auth/me", headers=headers))
            if not identity.get("id") or identity.get("account_status") == "disabled":
                raise RuntimeError("active_identity_required")
            tables = checked(client.get(meta + "/table", headers=meta_headers))
            tables = tables["items"] if isinstance(tables, dict) else tables
            ids = {t["name"]: t["id"] for t in tables}
            targets = ("report", "user_media_interaction")
            before = {name: snapshot(client, meta, meta_headers, ids[name]) for name in targets}
            media = checked(client.get(social + "/media", params={"per_page": 1}))
            items = media["items"] if isinstance(media, dict) else media
            media_id = items[0]["id"]
            try:
                for endpoint, method, field, payload in (
                    ("/reports", "POST", "description", {"target_type": "media", "target_id": str(media_id), "reason": "other"}),
                    ("/interactions", "PUT", "review", {"media_id": media_id, "status": "completed", "rating": 4.5}),
                ):
                    for label, value in (("absent", None), ("null", None), ("empty", ""), ("whitespace", " \t\n ")):
                        body = dict(payload)
                        if label != "absent":
                            body[field] = value
                        response = client.request(method, social + endpoint, headers=headers, json=body)
                        try:
                            error = response.json()
                        except ValueError:
                            error = {}
                        expected = (response.status_code == 400 and error.get("code") == "ERROR_CODE_INPUT_ERROR"
                                    and (field in str(error).lower() or
                                         (field == "review" and "Escreva sua avaliação" in str(error))))
                        report["checks"].append({"endpoint": endpoint, "case": label,
                                                 "status": response.status_code, "passed": expected})
                        if not expected:
                            raise RuntimeError("unexpected_rejection_response")
                        time.sleep(1)
            finally:
                after = {name: snapshot(client, meta, meta_headers, ids[name]) for name in targets}
                report["storage_unchanged"] = {name: before[name] == after[name] for name in targets}
            report["passed"] = len(report["checks"]) == 8 and all(report["storage_unchanged"].values())
    except Exception as error:
        # Exceptions may contain private URLs, payloads or tokens: retain only type.
        report["failure_type"] = type(error).__name__
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
