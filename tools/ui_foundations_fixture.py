"""Test entry point: real Codeboxd UI, deterministic fictional reads, no remote APIs."""
import httpx

# Fail closed even if an unmocked service path is reached by a fixture.
async def deny_external(self, request):
    raise RuntimeError('ui_fixture_forbids_outbound_http')

httpx.AsyncClient._send_single_request = deny_external

from Codeboxd_main.services import catalog
from Codeboxd_main.state import social


def items(kind='movie'):
    return [catalog.media('tmdb' if kind in ('movie', 'series') else kind, kind, str(i),
        f'Obra de teste {i:02} — uma história com título longo para verificar a leitura',
        cover_url='https://ui-fixture.invalid/cover.png', year=2020+i % 5,
        description='Conteúdo fictício para verificar layout e navegação.') for i in range(1, 13)]


async def search(query='', kind='all', page=1):
    return items('movie' if kind == 'all' else kind), []


async def highlights():
    return items('series')


async def collection(key):
    return items(catalog.HOME_COLLECTIONS[key][0])


async def detail(item):
    return dict(items(item['media_type'])[0], external_id=item['external_id'])


async def recommendations(item, **kwargs):
    return items(item['media_type'])


async def empty(*args, **kwargs):
    return []


async def request(method, path, **kwargs):
    if method != 'GET':
        raise RuntimeError('ui_fixture_forbids_mutations')
    if path == '/media':
        return []
    return []


catalog.search = search
catalog.series_highlights = highlights
catalog.home_collection = collection
catalog.detail = detail
catalog.recommendations = recommendations
catalog.trailers = empty
catalog.reviews = empty
catalog.availability = empty
social.request = request

from Codeboxd_main.Codeboxd_main import app  # noqa: E402,F401
