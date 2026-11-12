"""Read-only admin route checks using existing local test accounts; no secrets printed."""
import asyncio
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


async def main():
    root = next(parent for parent in Path(__file__).resolve().parents if (parent / 'rxconfig.py').is_file())
    load_dotenv(root / '.env')
    accounts = json.loads((root / '.local/test-accounts.json').read_text(encoding='utf-8-sig'))
    endpoints = [
        ('/admin/dashboard', {}),
        ('/admin/users', {'search': '', 'user_id': 0, 'account_status': '', 'role': ''}),
        ('/admin/catalog', {'media_type': 'movie'}),
        ('/admin/reports', {'status': '', 'target_type': '', 'reason': ''}),
    ]
    results = []
    async with httpx.AsyncClient(timeout=20) as client:
        social = os.environ['XANO_SOCIAL_URL'].rstrip('/')
        auth = os.environ['XANO_AUTH_URL'].rstrip('/')

        async def reads(actor, headers):
            for path, params in endpoints:
                response = await client.get(social + path, params=params, headers=headers)
                row = {'actor': actor, 'path': path, 'status': response.status_code}
                results.append(row)
                print(json.dumps(row), flush=True)

        await reads('guest', {})
        for index, account in enumerate(accounts):
            response = await client.post(auth + '/auth/login', json={key: account[key] for key in ('email', 'password')})
            if response.status_code != 200:
                results.append({'account_index': index, 'login_status': response.status_code})
                continue
            headers = {'Authorization': 'Bearer ' + response.json()['authToken']}
            identity = await client.get(auth + '/auth/me', headers=headers)
            if identity.status_code != 200:
                results.append({'account_index': index, 'identity_status': identity.status_code})
                continue
            role = identity.json().get('role', 'unknown')
            await reads(role, headers)
    Path(__file__).with_name('backend-read-results-2026-10-19.json').write_text(
        json.dumps(results, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    asyncio.run(main())
