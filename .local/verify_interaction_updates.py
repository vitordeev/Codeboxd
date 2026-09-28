"""Verify interaction updates and cross-session persistence, restoring old values."""
import json
from pathlib import Path

import httpx
from dotenv import dotenv_values

config = dotenv_values('.env')
auth = config['XANO_AUTH_URL'].rstrip('/')
social = config.get('XANO_SOCIAL_URL', '').rstrip('/') or auth.split('/api:')[0] + '/api:codeboxd'
accounts = json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
client = httpx.Client(timeout=30)
tokens = []
snapshots = []


def request(method, base, path, token='', data=None, expected=(200,)):
    response = client.request(method, base + path, json=data,
        headers={'Authorization': 'Bearer ' + token} if token else {})
    if response.status_code not in expected:
        raise AssertionError(f'{method} {path} returned HTTP {response.status_code}: {response.text[:200]}')
    return response.json() if response.content else None


def current_interaction(token, media_id):
    return next(row for row in request('GET', social, '/interactions', token=token)
                if int(row['media_id']) == media_id)


try:
    for account in accounts[:2]:
        login = request('POST', auth, '/auth/login', data={
            'email': account['email'], 'password': account['password']})
        tokens.append(login['authToken'])
    user_a, user_b = tokens
    rows_a = request('GET', social, '/interactions', token=user_a)
    rows_b = request('GET', social, '/interactions', token=user_b)
    shared = next(int(row['media_id']) for row in rows_a
                  if any(int(other['media_id']) == int(row['media_id']) for other in rows_b))
    for token, rows in ((user_a, rows_a), (user_b, rows_b)):
        row = next(item for item in rows if int(item['media_id']) == shared)
        snapshots.append((token, {'media_id': shared, 'status': row['status'],
            'rating': float(row.get('rating') or 0), 'review': str(row.get('review') or ''),
            'spoiler': bool(row.get('spoiler'))}))

    request('PUT', social, '/interactions', token=user_a, data={
        'media_id': shared, 'status': 'in_progress', 'rating': 3,
        'review': 'Temporary first review', 'spoiler': False})
    request('PUT', social, '/interactions', token=user_a, data={
        'media_id': shared, 'status': 'dropped', 'rating': 4.5,
        'review': 'Temporary edited review', 'spoiler': False})
    renewed = request('POST', auth, '/auth/login', data={
        'email': accounts[0]['email'], 'password': accounts[0]['password']})['authToken']
    a_after = current_interaction(renewed, shared)
    b_after = current_interaction(user_b, shared)
    if (a_after['status'], float(a_after['rating']), a_after['review']) != ('dropped', 4.5, 'Temporary edited review'):
        raise AssertionError('Updated interaction did not persist across a new login')
    original_b = snapshots[1][1]
    if (b_after['status'], float(b_after.get('rating') or 0), str(b_after.get('review') or '')) != (
            original_b['status'], original_b['rating'], original_b['review']):
        raise AssertionError('Updating one user changed the other user interaction')
    print('PASS in-progress/dropped status, rating and review updates persist after relogin and preserve user isolation', flush=True)
finally:
    for token, old in snapshots:
        try:
            request('PUT', social, '/interactions', token=token, data=old)
        except Exception:
            pass
    client.close()
