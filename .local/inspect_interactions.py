import json
from pathlib import Path

import httpx
from dotenv import dotenv_values

config = dotenv_values('.env')
auth = config['XANO_AUTH_URL'].rstrip('/')
social = config.get('XANO_SOCIAL_URL', '').rstrip('/') or auth.split('/api:')[0] + '/api:codeboxd'
accounts = json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
with httpx.Client(timeout=30) as client:
    rows_by_user = []
    for account in accounts[:2]:
        login = client.post(auth + '/auth/login', json={'email': account['email'], 'password': account['password']})
        login.raise_for_status()
        token = login.json()['authToken']
        response = client.get(social + '/interactions', headers={'Authorization': 'Bearer ' + token})
        response.raise_for_status()
        rows_by_user.append(response.json())
    first = {int(row['media_id']) for row in rows_by_user[0]}
    second = {int(row['media_id']) for row in rows_by_user[1]}
    print(json.dumps({'counts': [len(rows) for rows in rows_by_user], 'shared_interaction': bool(first & second)}))
