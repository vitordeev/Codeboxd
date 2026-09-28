"""Verify movie, series, anime and book items in a real Xano list."""
import asyncio
import json
import sys
from pathlib import Path

import httpx
from dotenv import dotenv_values

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Codeboxd_main.services.catalog import detail, media

config = dotenv_values('.env')
auth = config['XANO_AUTH_URL'].rstrip('/')
social = config.get('XANO_SOCIAL_URL', '').rstrip('/') or auth.split('/api:')[0] + '/api:codeboxd'
accounts = json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
client = httpx.Client(timeout=30)
token = ''
list_id = 0


def call(method, base, path, data=None, params=None, expected=(200,)):
    response = client.request(method, base + path, json=data, params=params,
        headers={'Authorization': 'Bearer ' + token} if token else {})
    if response.status_code not in expected:
        raise AssertionError(f'{method} {path} returned HTTP {response.status_code}: {response.text[:200]}')
    return response.json() if response.content else None


try:
    login = call('POST', auth, '/auth/login', {'email': accounts[0]['email'], 'password': accounts[0]['password']})
    token = login['authToken']
    catalog_rows = call('GET', social, '/media', params={'page': 1, 'per_page': 100})
    if isinstance(catalog_rows, dict):
        catalog_rows = catalog_rows.get('items', catalog_rows.get('media', []))
    by_kind = {kind: next((row for row in catalog_rows if row.get('media_type') == kind), None)
               for kind in ('movie', 'series', 'book')}
    if any(row is None for row in by_kind.values()):
        raise AssertionError('Existing movie, series and book records are required')

    anime_item = media('jikan', 'anime', '1', 'Cowboy Bebop')
    anime = next((row for row in catalog_rows if row.get('identity_key') == anime_item['identity_key']), None)
    if anime is None:
        anime_item = asyncio.run(detail(anime_item))
        payload = {key: anime_item.get(key) for key in (
            'external_source', 'external_id', 'media_type', 'title', 'description',
            'cover_url', 'year', 'details')}
        anime = call('POST', social, '/media', payload)
    by_kind['anime'] = anime
    ids = {kind: int(row['id']) for kind, row in by_kind.items()}

    collection = call('POST', social, '/lists', data={
        'title': 'Validação temporária das categorias', 'description': '', 'is_public': False})
    list_id = int(collection['id'])
    for kind, media_id in ids.items():
        call('POST', social, f'/lists/{list_id}/items', {'media_id': media_id})
    listed = call('GET', social, f'/lists/{list_id}/items')
    actual_ids = {int(row['media_id']) for row in listed}
    if actual_ids != set(ids.values()):
        raise AssertionError(f'Expected all four media records; got {len(actual_ids)} list items')
    print('PASS one Xano list stores and returns movie, series, anime and book media', flush=True)
    print('Anime catalog record:', anime.get('title', 'Cowboy Bebop'), 'source:', anime.get('external_source', 'jikan'), flush=True)
finally:
    if list_id:
        try:
            call('DELETE', social, f'/lists/{list_id}', expected=(200, 204, 404))
        except Exception:
            pass
    client.close()
