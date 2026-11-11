"""Preview/apply recovery mail configuration; never print secrets or provider bodies."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import httpx
from dotenv import dotenv_values
from tools.session_revocation import metadata_config, blocks, identity, export_workspace

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / '.local/sendgrid-recovery'
REPORT = ROOT / 'openspec/changes/integrar-sendgrid-recuperacao/deployment.json'
GUID = 'f3THZ4ZNIuWXhP86ujrorYTZZPs'


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    report = {'published': False, 'passed': False}
    try:
        config = dotenv_values(ROOT / '.env')
        key, sender = config.get('SENDGRID_API_KEY'), config.get('SENDGRID_FROM')
        if not key or not sender:
            raise RuntimeError('missing_configuration')
        base, headers = metadata_config()
        with httpx.Client(timeout=40, follow_redirects=False) as client:
            verified = client.get('https://api.sendgrid.com/v3/verified_senders', headers={'Authorization': 'Bearer ' + key})
            verified.raise_for_status()
            if not any(s.get('verified') is True and s.get('from_email', '').lower() == sender.lower()
                       for s in verified.json().get('results', [])):
                raise RuntimeError('sender_not_verified')
            report['sender_verified'] = True
            before = export_workspace(client, base, headers)
            remote = client.get(base + '/multidoc', headers=headers, params={'env': 'true', 'records': 'false'})
            remote.raise_for_status()
            workspace = next(b for b in blocks(remote.text) if re.search(r'(?m)^workspace ', b))
            env_match = re.search(r'\benv\s*=\s*\{([^{}]*)\}', workspace)
            if not env_match:
                raise RuntimeError('unexpected_environment_structure')
            # Preserve the exact existing map, replacing only our two entries.
            env = env_match.group(1)
            for name, value in [('SENDGRID_API_KEY', key), ('SENDGRID_FROM', sender)]:
                pattern = r'(?m)^\s*' + name + r'\s*:\s*"(?:[^"\\]|\\.)*"\s*$'
                env = re.sub(pattern, '', env)
                env += '\n    ' + name + ': ' + json.dumps(value) + '\n'
            merged = workspace[:env_match.start(1)] + env + workspace[env_match.end(1):]
            endpoint = (ROOT / 'xano/api/authentication/reset/request_reset_link_GET.xs').read_text(encoding='utf-8')
            source = merged + '\n---\n' + endpoint
            params = {'partial': 'true', 'env': 'true', 'records': 'false', 'delete': 'false'}
            response = client.post(base + '/multidoc/dry-run', headers={**headers, 'Content-Type': 'text/x-xanoscript'}, params=params, content=source.encode())
            report['preview_http_status'] = response.status_code
            response.raise_for_status()
            preview = response.json()
            operations = preview.get('operations', [])
            report['operations'] = [{k: row.get(k) for k in ('type', 'name', 'action')} for row in operations]
            if (not preview.get('has_env') or not operations
                or any(row.get('type') not in ('query', 'workspace') for row in operations)
                or len([r for r in operations if r.get('type') == 'query']) != 1
                or any('parse error' in str(r.get('details', '')).lower() for r in operations)):
                raise RuntimeError('unexpected_preview_scope')
            PRIVATE.mkdir(parents=True, exist_ok=True)
            signature = {'before': digest(before), 'workspace': digest(workspace), 'source': digest(source)}
            approval = PRIVATE / 'preview.json'
            if not args.apply:
                approval.write_text(json.dumps(signature), encoding='utf-8')
            else:
                if json.loads(approval.read_text()) != signature:
                    raise RuntimeError('preview_changed')
                backup = PRIVATE / 'before-without-secrets.xs'
                if backup.exists():
                    raise RuntimeError('backup_already_exists')
                backup.write_text(before, encoding='utf-8')
                response = client.post(base + '/multidoc', headers={**headers, 'Content-Type': 'text/x-xanoscript'}, params=params, content=source.encode())
                report['push_http_status'] = response.status_code
                response.raise_for_status()
                report['published'] = True
                after = export_workspace(client, base, headers)
                left = {identity(b): b for b in blocks(before)}
                right = {identity(b): b for b in blocks(after)}
                changed = {k for k in left.keys() | right.keys() if left.get(k) != right.get(k)}
                if changed != {GUID}:
                    raise RuntimeError('unexpected_post_publish_delta')
                report['only_recovery_endpoint_changed'] = True
                remote = client.get(base + '/multidoc', headers=headers, params={'env': 'true', 'records': 'false'})
                remote.raise_for_status()
                after_workspace = next(b for b in blocks(remote.text) if re.search(r'(?m)^workspace ', b))
                def values(w):
                    body = re.search(r'\benv\s*=\s*\{([^{}]*)\}', w).group(1)
                    return {m[1]: json.loads(m[2]) for m in re.finditer(r'(\w+)\s*:\s*("(?:[^"\\]|\\.)*")', body)}
                old, new = values(workspace), values(after_workspace)
                if any(new.get(k) != v for k, v in old.items() if k not in ('SENDGRID_API_KEY', 'SENDGRID_FROM')):
                    raise RuntimeError('existing_environment_changed')
                if new.get('SENDGRID_API_KEY') != key or new.get('SENDGRID_FROM') != sender:
                    raise RuntimeError('private_configuration_mismatch')
                report['private_configuration_verified'] = True
                report['existing_environment_preserved'] = True
            report['passed'] = True
    except Exception as error:
        report['failure_type'] = type(error).__name__
        # No exception message: it may contain HTTP payloads or secrets.
    REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
