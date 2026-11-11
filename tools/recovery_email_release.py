"""Validate recovery mail without delivery; preview/apply only its Xano endpoint."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import httpx
from dotenv import dotenv_values
from tools.build_recovery_email import TEMPLATE, TEXT, ENDPOINT
from tools.session_revocation import metadata_config, export_workspace, blocks, identity

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / '.local/recovery-email-release'
GUID = 'f3THZ4ZNIuWXhP86ujrorYTZZPs'


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--change', default='melhorar-email-recuperacao')
    parser.add_argument('--endpoint', choices=('request', 'update'), default='request')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.change):
        parser.error('Invalid change name')
    report_dir = ROOT / 'openspec/changes' / args.change
    if not (report_dir / 'proposal.md').is_file():
        parser.error('An active planned change is required')
    private = PRIVATE if args.change == 'melhorar-email-recuperacao' else ROOT / '.local' / args.change
    endpoint_path = ENDPOINT if args.endpoint == 'request' else ROOT / 'xano/api/authentication/reset/update_password_POST.xs'
    target_guid = GUID if args.endpoint == 'request' else 'uu3mbalHPafTRIy10GtGBdmRrrI'
    report = {'passed': False, 'published': False, 'emails_delivered_by_validation': 0}
    try:
        base, headers = metadata_config()
        endpoint = endpoint_path.read_text(encoding='utf-8')
        config = dotenv_values(ROOT / '.env')
        with httpx.Client(timeout=40, follow_redirects=False) as client:
            if not args.apply and args.endpoint == 'request':
                # Sandbox does not deliver, generate reset records or consume codes.
                payload = {
                    'from': {'email': config['SENDGRID_FROM'], 'name': 'Codeboxd'},
                    'personalizations': [{'to': [{'email': config['SENDGRID_FROM']}]}],
                    'subject': 'Seu código de 6 dígitos para recuperar a senha do Codeboxd',
                    'content': [{'type': 'text/plain', 'value': TEXT.replace('{{code}}', '482619')},
                                {'type': 'text/html', 'value': TEMPLATE.read_text(encoding='utf-8').replace('{{code}}', '482619')}],
                    'tracking_settings': {'click_tracking': {'enable': False, 'enable_text': False},
                                          'open_tracking': {'enable': False}, 'subscription_tracking': {'enable': False}},
                    'mail_settings': {'sandbox_mode': {'enable': True}},
                }
                response = client.post('https://api.sendgrid.com/v3/mail/send',
                    headers={'Authorization': 'Bearer ' + config['SENDGRID_API_KEY']}, json=payload)
                report['sandbox_http_status'] = response.status_code
                if response.status_code != 200:
                    raise RuntimeError('sandbox_failed')
            before = export_workspace(client, base, headers)
            params = {'partial': 'true', 'env': 'false', 'records': 'false', 'delete': 'false'}
            response = client.post(base + '/multidoc/dry-run', headers={**headers, 'Content-Type': 'text/x-xanoscript'},
                                   params=params, content=endpoint.encode())
            report['preview_http_status'] = response.status_code
            response.raise_for_status()
            data = response.json()
            operations = data.get('operations', [])
            report['operations'] = [{k: r.get(k) for k in ('type', 'name', 'action')} for r in operations]
            if (data.get('has_env') or data.get('has_records') or len(operations) != 1
                or operations[0].get('type') != 'query'
                or 'parse error' in str(operations[0].get('details', '')).lower()):
                raise RuntimeError('unexpected_preview')
            private.mkdir(parents=True, exist_ok=True)
            signature = {'before': sha(before), 'endpoint': sha(endpoint)}
            if not args.apply:
                (private / 'preview.json').write_text(json.dumps(signature), encoding='utf-8')
            else:
                approved = json.loads((private / 'preview.json').read_text())
                if approved != signature:
                    raise RuntimeError('preview_changed')
                backup = private / 'before-without-secrets.xs'
                if backup.exists():
                    raise RuntimeError('backup_already_exists')
                backup.write_text(before, encoding='utf-8')
                response = client.post(base + '/multidoc', headers={**headers, 'Content-Type': 'text/x-xanoscript'},
                                       params=params, content=endpoint.encode())
                report['push_http_status'] = response.status_code
                response.raise_for_status()
                report['published'] = True
                after = export_workspace(client, base, headers)
                left = {identity(b): b for b in blocks(before)}
                right = {identity(b): b for b in blocks(after)}
                changed = {k for k in left.keys() | right.keys() if left.get(k) != right.get(k)}
                if changed != {target_guid}:
                    raise RuntimeError('unexpected_remote_delta')
                report['only_recovery_endpoint_changed'] = True
            report['passed'] = True
    except Exception as error:
        report['failure_type'] = type(error).__name__
    name = 'deployment.json' if args.apply else 'preview.json'
    (report_dir / name).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
