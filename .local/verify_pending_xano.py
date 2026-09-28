"""Verify optional post media and cross-list reuse using existing Xano media."""
import json
from pathlib import Path

import httpx
from dotenv import dotenv_values

config = dotenv_values('.env')
auth = config['XANO_AUTH_URL'].rstrip('/')
social = config.get('XANO_SOCIAL_URL', '').rstrip('/') or auth.split('/api:')[0] + '/api:codeboxd'
accounts = json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
client = httpx.Client(timeout=30)
created_lists = []
created_posts = []


def request(method, base, path, token='', data=None, expected=(200,)):
    response = client.request(method, base + path, json=data,
        headers={'Authorization': 'Bearer ' + token} if token else {})
    if response.status_code not in expected:
        raise AssertionError(f'{method} {path} returned HTTP {response.status_code}: {response.text[:200]}')
    return response.json() if response.content else None


try:
    login = request('POST', auth, '/auth/login', data={
        'email': accounts[0]['email'], 'password': accounts[0]['password']})
    token = login['authToken']
    media = request('GET', social, '/media', token=token)
    if isinstance(media, dict):
        media = media.get('items', media.get('media', []))
    existing = next((row for row in media if row.get('media_type') == 'movie'), None)
    if not existing:
        raise AssertionError('No existing movie record is available for safe checks')
    media_id = int(existing['id'])

    first = request('POST', social, '/lists', token=token,
        data={'title': 'Verificação temporária A', 'description': '', 'is_public': False})
    second = request('POST', social, '/lists', token=token,
        data={'title': 'Verificação temporária B', 'description': '', 'is_public': False})
    created_lists.extend([int(first['id']), int(second['id'])])
    for collection in (first, second):
        request('POST', social, f"/lists/{collection['id']}/items", token=token,
            data={'media_id': media_id})
        items = request('GET', social, f"/lists/{collection['id']}/items", token=token)
        if not any(int(row['media_id']) == media_id for row in items):
            raise AssertionError('Media did not persist in both separate lists')
    print('PASS same existing media can be added to two different lists', flush=True)

    without = request('POST', social, '/posts', token=token,
        data={'body': 'Temporary post without media'})
    with_media = request('POST', social, '/posts', token=token,
        data={'body': 'Temporary post with media', 'media_id': media_id})
    created_posts.extend([int(without['id']), int(with_media['id'])])
    if int(without.get('media_id') or 0) != 0 or int(with_media.get('media_id') or 0) != media_id:
        raise AssertionError('Optional media association did not persist as expected')
    print('PASS posts persist with and without media association', flush=True)
finally:
    for post_id in reversed(created_posts):
        try:
            request('DELETE', social, f'/posts/{post_id}', token=token, expected=(200, 204, 404))
        except Exception:
            pass
    for list_id in reversed(created_lists):
        try:
            request('DELETE', social, f'/lists/{list_id}', token=token, expected=(200, 204, 404))
        except Exception:
            pass
    client.close()
