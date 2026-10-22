"""Probe native Xano mail once, without reset codes or published changes."""
import json
from pathlib import Path
import re
import time
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "openspec/changes/recuperar-senha-codigo-6-digitos/validation/provedor-email-2026-10-22.json"
SCRIPT = '''function "diagnose_recovery_mail" {
  input {
    email email filters=trim|lower
  }
  stack {
    util.send_email {
      service_provider = "xano"
      to = $input.email
      subject = "Codeboxd - diagnostico de entrega"
      message = "Teste de entrega do Codeboxd. Esta mensagem nao contem codigo e nao altera sua senha."
    } as $delivery
  }
  response = $delivery
}'''


def safe(value):
    """Redact possible contact data, auth material and unbounded stack output."""
    if isinstance(value, dict):
        return {k: safe(v) for k, v in value.items()
                if not any(s in k.lower() for s in ("token", "password", "email", "input", "value_store", "stack", "header"))}
    if isinstance(value, list):
        return [safe(v) for v in value[:8]]
    if isinstance(value, str):
        value = re.sub(r"[\w.+-]+@[\w.-]+", "[redacted-email]", value)
        value = re.sub(r"https?://\S+", "[redacted-url]", value)
        return value[:1500]
    return value


def main():
    report = {"diagnostic": "native_mail_static_message", "published_changes": False}
    try:
        config = dotenv_values(ROOT / ".env")
        origin = urlsplit(config["XANO_AUTH_URL"])
        base = f"{origin.scheme}://{origin.netloc}/api:meta/workspace/147717"
        raw = (Path.home() / ".xano/credentials.yaml").read_text(encoding="utf-8")
        tokens = re.findall(r"^\s*access_token:\s*(.*?)\s*$", raw, re.M)
        assert len(tokens) == 1
        headers = {"Authorization": "Bearer " + tokens[0].strip().strip("'\"")}
        with httpx.Client(timeout=30, follow_redirects=False) as client:
            response = client.get(base + "/request_history", headers=headers, params={"per_page": 100})
            response.raise_for_status()
            history = response.json()
            rows = history.get("items", []) if isinstance(history, dict) else history
            row = next(x for x in rows if "request-reset-link" in str(x.get("uri", "")))
            email = row["input"]["email"]
            response = client.post(base + "/multidoc/debug", headers={**headers, "Content-Type": "text/x-xanoscript"},
                                   params={"entry_obj_type": "function", "entry_obj_name": "diagnose_recovery_mail",
                                           "input": json.dumps({"email": email})}, content=SCRIPT)
            report["start_status"] = response.status_code
            data = response.json()
            report["start_response"] = safe(data)
            debug_id = data.get("id") or data.get("debug_id")
            if debug_id and response.status_code == 200:
                for _ in range(12):
                    response = client.get(base + "/multidoc/debug/" + str(debug_id), headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    report["execution"] = safe(data)
                    if data.get("status") not in ("pending", "running", "queued"):
                        break
                    time.sleep(1)
    except Exception as error:
        report["failure_type"] = type(error).__name__
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
