"""Read-only checks of published administrative APIs; never creates accounts.

Run with .venv/Scripts/python.exe from the repository root. Optional tokens come
from ADMIN_PROBE_ADMIN_TOKEN, ADMIN_PROBE_MEMBER_TOKEN and
ADMIN_PROBE_DISABLED_TOKEN. Output contains status codes only, never responses,
tokens or the server URL. Missing credentials are reported as skipped.
"""
import argparse
import json
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv


ENDPOINTS = (
    ("/admin/dashboard", {}),
    ("/admin/users", {"search": "", "page": 1, "per_page": 1}),
    ("/admin/catalog", {"media_type": "movie", "page": 1, "per_page": 1}),
    ("/admin/reports", {"page": 1, "per_page": 1}),
)


def classify(status: int, role: str) -> str:
    if status == 404:
        return "unavailable"
    if role == "admin":
        return "passed" if status == 200 else "failed"
    return "passed" if status in (401, 403) else "failed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--member-account-file", type=Path,
                        help="Private JSON array of existing test accounts; uses only the first")
    parser.add_argument("--guest-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[4]
    load_dotenv(root / ".env")
    base = os.getenv("XANO_SOCIAL_URL", "").strip().rstrip("/")
    if not base.startswith("https://"):
        parser.error("XANO_SOCIAL_URL must be configured with HTTPS")
    results = []
    with httpx.Client(timeout=15, follow_redirects=False) as client:
        member_token = ""
        if args.member_account_file:
            accounts = json.loads(args.member_account_file.read_text(encoding="utf-8"))
            account = accounts[0]
            auth_base = os.getenv("XANO_AUTH_URL", "").strip().rstrip("/")
            if not auth_base.startswith("https://"):
                parser.error("XANO_AUTH_URL must be configured with HTTPS")
            login = client.post(auth_base + "/auth/login",
                                json={key: account[key] for key in ("email", "password")})
            if login.status_code != 200:
                parser.error(f"Test account login failed with HTTP {login.status_code}")
            member_token = login.json()["authToken"]
            identity = client.get(auth_base + "/auth/me",
                                  headers={"Authorization": "Bearer " + member_token})
            if identity.status_code != 200 or identity.json().get("role") != "member":
                parser.error("Test account must have a server-verified member role")
        roles = ("guest",) if args.guest_only else ("guest", "member", "disabled", "admin")
        for role in roles:
            token = os.getenv(f"ADMIN_PROBE_{role.upper()}_TOKEN", "")
            if role == "member" and member_token:
                token = member_token
            if role != "guest" and not token:
                results.append({"role": role, "result": "skipped_missing_token"})
                continue
            headers = {"Accept": "application/json"}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            for path, params in ENDPOINTS:
                try:
                    for attempt in range(3):
                        response = client.get(base + path, params=params, headers=headers)
                        if response.status_code != 429 or attempt == 2:
                            break
                        time.sleep(20)
                    status = response.status_code
                    outcome = classify(status, role)
                except httpx.RequestError:
                    status, outcome = None, "network_error"
                results.append({"role": role, "endpoint": path,
                                "status": status, "result": outcome})
    report = {"layer": "remote_read_only", "mutations": False,
              "scope": "GET only; does not verify mutations, counts or audit persistence",
              "results": results}
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all(row["result"] == "passed" for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
