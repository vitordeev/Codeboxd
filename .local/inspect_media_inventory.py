import json
from pathlib import Path

import httpx
from dotenv import dotenv_values

config = dotenv_values('.env')
base = config['XANO_AUTH_URL'].rstrip('/')
social = config.get('XANO_SOCIAL_URL', '').rstrip('/') or base.split('/api:')[0] + '/api:codeboxd'
accounts = json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
with httpx.Client(timeout=30) as client:
    login = client.post(base + '/auth/login', json={
        'email': accounts[0]['email'], 'password': accounts[0]['password']})
    login.raise_for_status()
    token = login.json()['authToken']
    response = client.get(social + '/media', headers={'Authorization': 'Bearer ' + token}, params={'page': 1, 'per_page': 100})
    response.raise_for_status()
    records = response.json()
    if isinstance(records, dict):
        records = records.get('items', records.get('media', []))
    counts = {}
    examples = {}
    for row in records:
        kind = row.get('media_type', 'unknown')
        counts[kind] = counts.get(kind, 0) + 1
        examples.setdefault(kind, row.get('id'))
    print(json.dumps({'counts': counts, 'example_ids': examples}, sort_keys=True))
