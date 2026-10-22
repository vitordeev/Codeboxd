"""Deploy only recovery endpoint and private Resend workspace variables.

Secrets are read from .env, sent directly to Xano and never printed or put in
tracked files. --apply requires a successful, reviewed --preview first.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

import httpx
from dotenv import dotenv_values
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / ".local/resend-deployment-2026-10-22"
REPORT = ROOT / "openspec/changes/recuperar-senha-codigo-6-digitos/validation/resend-deployment-2026-10-22.json"
GUID = "f3THZ4ZNIuWXhP86ujrorYTZZPs"


def blocks(text):
    return [part.strip() for part in re.split(r"(?m)^---\s*$", text) if part.strip()]


def identity(block):
    guid = re.search(r'guid\s*=\s*"([^"]+)"', block)
    if guid:
        return guid.group(1)
    lines = [line for line in block.splitlines() if line.strip() and not line.lstrip().startswith("//")]
    return lines[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    report = {"applied": False, "passed": False}
    config = dotenv_values(ROOT / ".env")
    key, sender = config.get("RESEND_API_KEY"), config.get("RESEND_FROM")
    if not key or not key.startswith("re_") or not sender:
        raise SystemExit("Private Resend configuration missing; no changes made.")
    origin = urlsplit(config["XANO_AUTH_URL"])
    base = f"{origin.scheme}://{origin.netloc}/api:meta/workspace/147717"
    raw = (Path.home() / ".xano/credentials.yaml").read_text(encoding="utf-8")
    tokens = re.findall(r"^\s*access_token:\s*(.*?)\s*$", raw, re.M)
    assert len(tokens) == 1
    headers = {"Authorization": "Bearer " + tokens[0].strip().strip("'\"")}
    BACKUP.mkdir(exist_ok=True, parents=True)
    try:
        with httpx.Client(timeout=40, follow_redirects=False) as client:
            def export(env=False):
                response = client.get(base + "/multidoc", headers=headers,
                                      params={"env": str(env).lower(), "records": "false"})
                response.raise_for_status()
                return response.text

            before = export()
            before_blocks = blocks(before)
            workspace = next(b for b in blocks(export(True)) if re.search(r"(?m)^workspace ", b))
            # Refuse replacing an existing env map without an explicit merge.
            if re.search(r"\benv\s*=", workspace):
                raise RuntimeError("existing_environment_requires_merge")
            env = "\n  env = {\n    RESEND_API_KEY: " + json.dumps(key) + "\n    RESEND_FROM: " + json.dumps(sender) + "\n  }\n"
            workspace = workspace.rstrip()[:-1] + env + "}"
            endpoint = (ROOT / "xano/api/authentication/reset/request_reset_link_GET.xs").read_text(encoding="utf-8")
            source = workspace + "\n---\n" + endpoint
            params = {"partial": "true", "env": "true", "records": "false", "delete": "false"}
            response = client.post(base + "/multidoc/dry-run", headers={**headers, "Content-Type": "text/x-xanoscript"},
                                   params=params, content=source.encode("utf-8"))
            report["preview_status"] = response.status_code
            response.raise_for_status()
            preview = response.json()
            report["summary"] = preview.get("summary")
            report["has_env"] = preview.get("has_env")
            operations = preview.get("operations", [])
            report["operations"] = [{k: row.get(k) for k in ("type", "name", "action")} for row in operations]
            if any("parse error" in str(row.get("details", "")).lower() for row in operations):
                raise RuntimeError("preview_parse_error")
            if not preview.get("has_env"):
                raise RuntimeError("environment_not_recognized")
            if not operations or any(row.get("type") not in ("workspace", "query") for row in operations):
                raise RuntimeError("unexpected_preview_scope")
            if len([row for row in operations if row.get("type") == "query"]) != 1:
                raise RuntimeError("unexpected_query_count")
            if not args.apply:
                (BACKUP / "preview-approved.json").write_text(json.dumps({
                    "before_hash": hashlib.sha256(before.encode()).hexdigest(),
                    "endpoint_hash": hashlib.sha256(endpoint.encode()).hexdigest()}), encoding="utf-8")
                report["passed"] = True
            else:
                approved = json.loads((BACKUP / "preview-approved.json").read_text())
                assert approved["before_hash"] == hashlib.sha256(before.encode()).hexdigest()
                assert approved["endpoint_hash"] == hashlib.sha256(endpoint.encode()).hexdigest()
                (BACKUP / "before-without-secrets.xs").write_text(before, encoding="utf-8")
                response = client.post(base + "/multidoc", headers={**headers, "Content-Type": "text/x-xanoscript"},
                                       params=params, content=source.encode("utf-8"))
                report["push_status"] = response.status_code
                response.raise_for_status()
                report["applied"] = True
                after_blocks = blocks(export())
                left = {identity(b): b for b in before_blocks}
                right = {identity(b): b for b in after_blocks}
                changed = [k for k in left.keys() | right.keys() if left.get(k) != right.get(k)]
                workspace_key = identity(next(b for b in before_blocks if re.search(r"(?m)^workspace ", b)))
                report["only_expected_definitions_changed"] = set(changed) <= {GUID, workspace_key} and GUID in changed
                after_workspace = next(b for b in blocks(export(True)) if re.search(r"(?m)^workspace ", b))
                report["private_variables_verified"] = key in after_workspace and sender in after_workspace
                report["passed"] = report["only_expected_definitions_changed"] and report["private_variables_verified"]
    except Exception as error:
        report["failure_type"] = type(error).__name__
        if isinstance(error, RuntimeError):
            report["failure_reason"] = str(error)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
