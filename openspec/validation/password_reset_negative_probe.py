"""Check invalid reset codes without sending email or changing any password (P.6)."""
import argparse
import json
import os
import secrets
from pathlib import Path

import httpx
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--account-file', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / '.env')
    auth = os.getenv('XANO_AUTH_URL', '').rstrip('/')
    if not auth.startswith('https://'):
        parser.error('XANO_AUTH_URL must use HTTPS')
    account = json.loads(args.account_file.read_text(encoding='utf-8'))[0]
    with httpx.Client(timeout=20) as client:
        invalid = client.post(auth + '/reset/magic-link-login',
                              json={'email': account['email'],
                                    'magic_token': 'invalid-' + secrets.token_urlsafe(32)})
        login = client.post(auth + '/auth/login',
                            json={key: account[key] for key in ('email', 'password')})
    report = {'layer': 'remote_negative_test', 'pending_id': 'P.6',
              'email_sent': False, 'password_update_requested': False,
              'invalid_code_status': invalid.status_code,
              'invalid_code_rejected': invalid.status_code in (400, 401, 403, 422),
              'original_password_login_status': login.status_code,
              'original_password_still_works': login.status_code == 200,
              'email_delivery_and_full_reset': 'not_tested'}
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if report['invalid_code_rejected'] and report['original_password_still_works'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
