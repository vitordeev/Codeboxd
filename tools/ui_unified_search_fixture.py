"""Fixture for unified search UI acceptance; all rows are fictional."""
import json
import os
from pathlib import Path

import tools.ui_foundations_fixture as base
from Codeboxd_main.services import catalog
from Codeboxd_main.state import social

_original_search = base.search
_root = Path(__file__).resolve().parents[1]
_log_path = Path(os.environ['UI_FIXTURE_REQUEST_LOG']).resolve() if os.environ.get(
    'UI_FIXTURE_REQUEST_LOG') else None
_detail_media = []
for _media_id in range(1, 22):
    _media = catalog.media(
        'tmdb', 'movie', str(_media_id), f'Obra de lista {_media_id}',
        year=2020, description='Obra fictícia para testar detalhes de lista.')
    _media['id'] = _media_id
    _detail_media.append(_media)


def _record(kind, **values):
    if _log_path is None:
        return
    if not _log_path.is_relative_to(_root / '.local'):
        raise RuntimeError('ui_fixture_log_must_stay_local')
    _log_path.parent.mkdir(parents=True, exist_ok=True)
    with _log_path.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps({'kind': kind, **values}, ensure_ascii=False) + '\n')


async def search(query='', kind='all', page=1):
    if not query:
        return await _original_search(query, kind, page)
    _record('catalog', query=query, scope=kind, page=page)
    result = base.items('movie' if kind == 'all' else kind)
    return result[:1], []


async def request(method, path, **kwargs):
    if method != 'GET':
        raise RuntimeError('ui_fixture_forbids_mutations')
    params = kwargs.get('params') or {}
    _record('api', method=method, path=path, params=params)
    page = int(params.get('page', 1))
    if path == '/profiles' and params.get('q'):
        return {
            'items': [{
                'user_id': 41, 'username': 'joana_fixture',
                'display_name': 'Joana Fixture', 'avatar_url': '',
            }] if page == 1 else [],
            'total': 1, 'page': page, 'per_page': 20, 'next_page': None,
        }
    if path == '/lists/public' and params.get('q'):
        return {
            'items': [{
                'id': 51, 'title': 'Lista pública de Joana',
                'description': 'Coleção fictícia para validar a busca.',
                'items_count': 3,
                'creator': {
                    'user_id': 41, 'username': 'joana_fixture',
                    'display_name': 'Joana Fixture', 'avatar_url': '',
                },
            } if page == 1 else {
                'id': 52, 'title': 'Outra lista pública de Joana',
                'description': 'Segunda página fictícia.',
                'items_count': 1,
                'creator': {
                    'user_id': 41, 'username': 'joana_fixture',
                    'display_name': 'Joana Fixture', 'avatar_url': '',
                },
            }],
            'total': 21, 'page': page, 'per_page': 20,
            'next_page': 2 if page == 1 else None,
        }
    if path == '/lists/public/51':
        return {
            'id': 51, 'user_id': 41, 'title': 'Lista pública de Joana',
            'description': 'Coleção fictícia para validar a busca.',
            'is_public': True,
            'creator': {
                'user_id': 41, 'username': 'joana_fixture',
                'display_name': 'Joana Fixture', 'avatar_url': '',
            },
        }
    if path == '/lists/public/53':
        return {
            'id': 53, 'user_id': 41, 'title': 'Lista vazia',
            'description': '', 'is_public': True,
            'creator': {
                'user_id': 41, 'username': 'joana_fixture',
                'display_name': 'Joana Fixture', 'avatar_url': '',
            },
        }
    if path in ('/lists/public/51/items', '/lists/public/53/items'):
        if path.endswith('/53/items'):
            return []
        start = (page - 1) * 20
        return [{'id': start + offset + 1, 'list_id': 51, 'media_id': start + offset + 1}
                for offset in range(20 if page == 1 else 1)]
    if path == '/media':
        return _detail_media
    return []


catalog.search = search
social.request = request

from Codeboxd_main.Codeboxd_main import app  # noqa: E402,F401
