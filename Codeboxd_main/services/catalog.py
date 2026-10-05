"""Media providers called on the Python server; provider keys stay off the client."""
import asyncio
import copy
import json
import logging
import time
from collections import OrderedDict
import os
import re
import unicodedata
from urllib.parse import urlsplit
from typing import Any

import httpx

from .api import APIError

logger = logging.getLogger(__name__)
KITSU_URL = 'https://kitsu.app/api/edge'
_kitsu_cache: OrderedDict = OrderedDict()


TYPES = {'movie': 'Filme', 'series': 'Série', 'anime': 'Anime', 'book': 'Livro'}

# Each shelf has its own provider selection; do not repeat a search page under
# different editorial headings.
HOME_COLLECTIONS = {
    'movies_now': ('movie', 'Agora nos cinemas', 'Histórias que acabam de chegar à tela.', 'movie/now_playing'),
    'movies_rated': ('movie', 'Filmes muito bem avaliados', 'Favoritos do público no TMDB.', 'movie/top_rated'),
    'movies_upcoming': ('movie', 'No radar: próximos filmes', 'Para colocar na sua lista de desejos.', 'movie/upcoming'),
    'series_rated': ('series', 'Séries muito bem avaliadas', 'Uma boa história pede mais um episódio.', 'tv/top_rated'),
    'books_fiction': ('book', 'Sua próxima leitura', 'Explore histórias da literatura de ficção.', 'fiction'),
    'books_fantasy': ('book', 'Livros de fantasia', 'Outros mundos começam na primeira página.', 'fantasy'),
    'books_mystery': ('book', 'Mistérios entre páginas', 'Só mais um capítulo para descobrir.', 'mystery'),
    'books_popular': ('book', 'Livros conhecidos e populares', 'Clássicos e favoritos para começar bem.', 'titles:1984|Duna|Harry Potter|Sapiens|O Hobbit'),
    'books_game_theory': ('book', 'Teoria dos Jogos', 'Uma seleção específica para sua pesquisa.', 'title:Teoria dos Jogos'),
    'anime_rated': ('anime', 'Animes muito bem avaliados', 'Explore os destaques da Kitsu.', '-averageRating'),
    'anime_popular': ('anime', 'Animes populares', 'Os universos mais procurados pelos fãs.', '-userCount'),
    'anime_current': ('anime', 'Animes em destaque agora', 'Lançamentos e histórias que estão em alta.', '-startDate'),
}


def normalized_title(value: str) -> str:
    text = unicodedata.normalize('NFKD', str(value).casefold())
    return ' '.join(re.findall(r'[^\W_]+', ''.join(c for c in text if not unicodedata.combining(c))))


def search_query(value: str) -> str:
    # Common Portuguese misspelling; keep other words and the user's visible input intact.
    return re.sub(r'\bhomen\b', 'homem', value.strip()[:200], flags=re.IGNORECASE)


def title_score(query: str, item: dict) -> float:
    """Require every significant query word in a title, never in author/subject metadata."""
    query = normalized_title(search_query(query))
    if not query: return 1
    stopwords = {'a', 'o', 'as', 'os', 'de', 'da', 'do', 'das', 'dos', 'e', 'the', 'of', 'and'}
    terms = [word for word in query.split() if word not in stopwords] or query.split()
    best = 0.0
    titles = [item.get('title', ''), *(item.get('search_titles') or [])]
    for value in titles:
        title = normalized_title(value)
        words = title.split()
        if not words: continue
        # Providers also return loosely related matches. Require whole words so
        # similar spellings and prefixes cannot turn unrelated titles into hits.
        if not all(term in words for term in terms): continue
        score = 1.0
        if title == query: score += 2
        elif f' {query} ' in f' {title} ': score += 1
        best = max(best, score)
    return best


def relevant_results(query: str, items: list[dict]) -> list[dict]:
    scored = [(title_score(query, item), item) for item in items]
    result, seen_anime = [], set()
    for score, item in sorted(scored, key=lambda pair: pair[0], reverse=True):
        if score <= 0: continue
        mal_id = ''
        if item.get('media_type') == 'anime':
            if item.get('external_source') == 'jikan': mal_id = str(item.get('external_id') or '')
            elif item.get('external_source') == 'kitsu': mal_id = str((item.get('details') or {}).get('MyAnimeList ID') or '')
        if mal_id and mal_id in seen_anime: continue
        if mal_id: seen_anime.add(mal_id)
        result.append(item)
    return result


def safe_url(value: Any) -> str:
    value = str(value or '').strip()
    try:
        parsed = urlsplit(value)
        return value if parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password else ''
    except ValueError:
        return ''


def media(source: str, kind: str, identifier: str, title: str, **extra) -> dict:
    return dict(id=0, identity_key=f'{source}:{kind}:{identifier}', external_source=source,
                external_id=str(identifier), media_type=kind, title=title or 'Sem título',
                description=str(extra.get('description') or ''), cover_url=safe_url(extra.get('cover_url')),
                year=int(extra.get('year') or 0), details=extra.get('details') or {},
                backdrop_url=safe_url(extra.get('backdrop_url')), search_titles=extra.get('search_titles') or [])


async def fetch(url: str, **kwargs) -> dict:
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(8, connect=3), headers={'User-Agent': 'Codeboxd/1.0'}) as client:
            for attempt in range(3):
                try:
                    response = await client.get(url, **kwargs)
                    response.raise_for_status()
                    value = response.json()
                    if not isinstance(value, dict): raise ValueError('Expected object')
                    return value
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code not in (429,500,502,503,504) or attempt == 2: raise
                    retry_after=exc.response.headers.get('Retry-After','')
                    try: delay=max(0.5,float(retry_after))
                    except ValueError: delay=0.5*(2**attempt)
                    if delay > 5: raise  # Do not retry before the provider permits it.
                    await asyncio.sleep(delay)
    except (httpx.HTTPError, ValueError) as exc:
        provider = {'api.themoviedb.org': 'TMDB', 'api.jikan.moe': 'Jikan',
                    'openlibrary.org': 'Open Library', 'kitsu.app': 'Kitsu'}.get(urlsplit(url).hostname, 'Catálogo')
        status = exc.response.status_code if isinstance(exc, httpx.HTTPStatusError) else 0
        reason = type(exc).__name__
        if isinstance(exc, httpx.HTTPStatusError):
            try:
                body = exc.response.json()
                errors = body.get('errors') or []
                reason = body.get('message') or body.get('status_message') or (
                    errors[0].get('detail') if isinstance(errors, list) and errors and isinstance(errors[0], dict) else '') or exc.response.reason_phrase
            except (ValueError, AttributeError):
                reason = exc.response.reason_phrase
        # Log only the public endpoint and error, never request headers or queries.
        reason = str(reason)
        for header in (kwargs.get('headers') or {}).values():
            if header and header != 'application/vnd.api+json':
                reason = reason.replace(str(header), '[redacted]')
        token = os.getenv('TMDB_READ_TOKEN', '').strip()
        if token: reason = reason.replace(token, '[redacted]')
        logger.warning('catalog_failure provider=%s path=%s status=%s reason=%s',
                       provider, urlsplit(url).path, status or 'network/format', ' '.join(reason.split())[:300])
        if isinstance(exc, httpx.TimeoutException): message = f'{provider}: tempo de resposta esgotado.'
        elif status == 429: message = f'{provider}: limite de consultas atingido. Tente novamente em instantes.'
        elif status: message = f'{provider}: indisponível no momento (HTTP {status}).'
        elif isinstance(exc, ValueError): message = f'{provider}: resposta em formato inválido.'
        else: message = f'{provider}: não foi possível conectar.'
        raise APIError(message, status) from exc


def year(value) -> int:
    match = re.match(r'\d{4}', str(value or ''))
    return int(match[0]) if match else 0


def tmdb_item(item: dict, kind: str) -> dict:
    details = {}
    for label, key in [('Duração (min)', 'runtime'), ('Temporadas', 'number_of_seasons'), ('Episódios', 'number_of_episodes')]:
        if item.get(key): details[label] = str(item[key])
    if item.get('genres'): details['Gêneros'] = ', '.join(g['name'] for g in item['genres'])
    if item.get('vote_average'): details['Nota TMDB'] = f"{float(item['vote_average']):.1f}/10"
    if item.get('status'): details['Status'] = str(item['status'])
    if item.get('created_by'): details['Criação'] = ', '.join(p.get('name','') for p in item['created_by'][:5] if p.get('name'))
    return media('tmdb', kind, str(item['id']), item.get('title') or item.get('name'),
                 search_titles=[item.get('original_title') or item.get('original_name') or ''],
                 description=item.get('overview'), year=year(item.get('release_date') or item.get('first_air_date')),
                 cover_url=('https://image.tmdb.org/t/p/w500'+item['poster_path']) if item.get('poster_path') else '',
                 details=details, backdrop_url=('https://image.tmdb.org/t/p/w1280'+item['backdrop_path']) if item.get('backdrop_path') else '')


async def kitsu_fetch(path: str, **params) -> dict:
    """Small, short-lived cache for public Kitsu responses; failures are never cached."""
    key = (path, json.dumps(params, sort_keys=True))
    cached = _kitsu_cache.get(key)
    if cached and time.monotonic() - cached[0] < 300:
        _kitsu_cache.move_to_end(key)
        return copy.deepcopy(cached[1])
    payload = await fetch(KITSU_URL + path, params=params,
                          headers={'Accept': 'application/vnd.api+json'})
    if not isinstance(payload.get('data'), (list, dict)):
        logger.warning('catalog_failure provider=Kitsu path=%s status=format', path)
        raise APIError('Kitsu: resposta em formato inválido.')
    _kitsu_cache[key] = (time.monotonic(), copy.deepcopy(payload))
    _kitsu_cache.move_to_end(key)
    while len(_kitsu_cache) > 128: _kitsu_cache.popitem(last=False)
    return payload


def kitsu_safe(item: dict) -> bool:
    attrs = item.get('attributes') or {}
    return item.get('type') == 'anime' and not attrs.get('nsfw') and attrs.get('ageRating') != 'R18'


def kitsu_item(item: dict, included: list[dict] | None = None) -> dict:
    attrs = item.get('attributes') or {}
    titles = attrs.get('titles') or {}
    details = {'Fonte': 'Kitsu', 'Kitsu ID': str(item['id']),
               'Episódios': str(attrs.get('episodeCount') or 'Não informado'),
               'Formato': str(attrs.get('subtype') or ''), 'Status': str(attrs.get('status') or ''),
               'Duração (min)': str(attrs.get('episodeLength') or '')}
    if attrs.get('averageRating'): details['Nota Kitsu'] = str(attrs['averageRating']) + '/100'
    video = str(attrs.get('youtubeVideoId') or '')
    if re.fullmatch(r'[A-Za-z0-9_-]{6,20}', video): details['YouTube ID'] = video
    relationships = item.get('relationships') or {}
    category_ids = {str(row['id']) for row in (relationships.get('categories') or {}).get('data', [])}
    mapping_ids = {str(row['id']) for row in (relationships.get('mappings') or {}).get('data', [])}
    genres = []
    for row in included or []:
        values = row.get('attributes') or {}
        if row.get('type') == 'categories' and str(row['id']) in category_ids:
            if values.get('title'): genres.append(values['title'])
        if row.get('type') == 'mappings' and str(row['id']) in mapping_ids:
            external_id = str(values.get('externalId') or '')
            if values.get('externalSite') == 'myanimelist/anime' and external_id.isdigit():
                details['MyAnimeList ID'] = external_id
    if genres: details['Gêneros'] = ', '.join(genres)
    return media('kitsu', 'anime', str(item['id']), titles.get('pt_br') or attrs.get('canonicalTitle') or titles.get('en_jp') or titles.get('en'),
        description=attrs.get('synopsis') or attrs.get('description'), year=year(attrs.get('startDate')),
        search_titles=[value for value in [*titles.values(), *(attrs.get('abbreviatedTitles') or [])] if value],
        cover_url=(attrs.get('posterImage') or {}).get('large') or (attrs.get('posterImage') or {}).get('original'),
        backdrop_url=(attrs.get('coverImage') or {}).get('large'), details=details)


def kitsu_items(payload: dict) -> list[dict]:
    return [kitsu_item(item, payload.get('included')) for item in payload.get('data', []) if kitsu_safe(item)]


async def kitsu_identifier(item: dict) -> str:
    identifier = str(item.get('external_id', ''))
    if item.get('media_type') != 'anime' or not identifier.isdigit():
        raise APIError('Identificador de anime inválido.')
    if item.get('external_source') == 'kitsu': return identifier
    if item.get('external_source') != 'jikan': raise APIError('Fonte inválida.')
    # Old records contain MAL IDs, which must never be treated as Kitsu IDs.
    payload = await kitsu_fetch('/mappings', **{'filter[externalSite]': 'myanimelist/anime',
        'filter[externalId]': identifier, 'include': 'item', 'page[limit]': 20})
    for row in payload.get('data', []):
        attrs = row.get('attributes') or {}
        target = ((row.get('relationships') or {}).get('item') or {}).get('data') or {}
        if (attrs.get('externalSite') == 'myanimelist/anime' and str(attrs.get('externalId')) == identifier
                and target.get('type') == 'anime' and str(target.get('id', '')).isdigit()):
            return str(target['id'])
    raise APIError('Este anime antigo ainda não possui correspondência na Kitsu.', 404)


async def recommendations(item: dict, limit: int = 8) -> list[dict]:
    """Return related works supplied by the same public catalog provider."""
    source, kind, identifier = item.get('external_source'), item.get('media_type'), str(item.get('external_id',''))
    if source == 'tmdb' and kind in ('movie','series') and identifier.isdigit():
        token=os.getenv('TMDB_READ_TOKEN','').strip()
        if not token: return []
        category='movie' if kind=='movie' else 'tv'
        related='recommendations' if kind=='movie' else 'similar'
        payload=await fetch(f'https://api.themoviedb.org/3/{category}/{identifier}/{related}',
                            params={'language':'pt-BR','page':1},headers={'Authorization':'Bearer '+token})
        return [tmdb_item(value,kind) for value in payload.get('results',[])[:limit]]
    if source in ('kitsu', 'jikan') and kind == 'anime' and identifier.isdigit():
        kitsu_id = await kitsu_identifier(item)
        payload = await kitsu_fetch(f'/anime/{kitsu_id}/media-relationships', **{
            'include': 'destination', 'page[limit]': min(20, limit)})
        related_ids = {str(target['id']) for row in payload.get('data', [])
            if (target := ((row.get('relationships') or {}).get('destination') or {}).get('data'))
            and target.get('type') == 'anime'}
        return [kitsu_item(row) for row in payload.get('included', [])
                if kitsu_safe(row) and str(row['id']) in related_ids and str(row['id']) != kitsu_id][:limit]
    if source == 'openlibrary' and kind == 'book' and re.fullmatch(r'OL\d+W',identifier):
        subjects=[value.strip() for value in str((item.get('details') or {}).get('Temas','')).split(',') if value.strip()]
        if subjects:
            found=await fetch('https://openlibrary.org/search.json',params={'q':'subject:"'+subjects[0]+'"','limit':limit+1,
                'fields':'key,title,author_name,first_publish_year,cover_i'})
            return [media('openlibrary','book',str(row['key']).split('/')[-1],row.get('title'),year=row.get('first_publish_year'),
                cover_url=f"https://covers.openlibrary.org/b/id/{row['cover_i']}-M.jpg" if row.get('cover_i') else '',
                details={'Autores':', '.join(row.get('author_name',[]))}) for row in found.get('docs',[])
                if str(row.get('key','')).split('/')[-1]!=identifier][:limit]
    return []


async def reviews(item: dict, limit: int = 6) -> list[dict[str, str]]:
    """Fetch public reviews when the media provider exposes them."""
    source, kind, identifier = item.get('external_source'), item.get('media_type'), str(item.get('external_id',''))
    if source == 'tmdb' and kind in ('movie','series') and identifier.isdigit():
        token=os.getenv('TMDB_READ_TOKEN','').strip()
        if not token: return []
        category='movie' if kind=='movie' else 'tv'
        payload=await fetch(f'https://api.themoviedb.org/3/{category}/{identifier}/reviews',
                            params={'language':'pt-BR','page':1},headers={'Authorization':'Bearer '+token})
        return [dict(author=str(row.get('author') or 'Pessoa'),rating=str((row.get('author_details') or {}).get('rating') or ''),
            body=str(row.get('content') or ''),date=str(row.get('created_at') or '')[:10])
            for row in payload.get('results',[])[:limit] if row.get('content')]
    if source in ('kitsu', 'jikan') and kind == 'anime' and identifier.isdigit():
        kitsu_id = await kitsu_identifier(item)
        payload = await kitsu_fetch('/reviews', **{'filter[mediaType]': 'Anime',
            'filter[mediaId]': kitsu_id, 'include': 'user', 'page[limit]': min(20, limit)})
        users = {str(row['id']): (row.get('attributes') or {}).get('name', 'Pessoa')
                 for row in payload.get('included', []) if row.get('type') == 'users'}
        result = []
        for row in payload.get('data', []):
            attrs = row.get('attributes') or {}
            if not attrs.get('content') or attrs.get('spoiler'): continue
            user = ((row.get('relationships') or {}).get('user') or {}).get('data') or {}
            rating = attrs.get('rating')
            result.append(dict(author=users.get(str(user.get('id')), 'Pessoa'),
                rating=str(float(rating) / 2) if rating is not None else '',
                body=str(attrs['content']), date=str(attrs.get('createdAt') or '')[:10]))
        return result[:limit]
    return []


async def trailers(item: dict, limit: int = 3) -> list[dict[str, str]]:
    """Return safe YouTube trailer embeds for TMDB movies and series."""
    source, kind, identifier = item.get('external_source'), item.get('media_type'), str(item.get('external_id', ''))
    if source in ('kitsu', 'jikan') and kind == 'anime' and identifier.isdigit():
        video = str((item.get('details') or {}).get('YouTube ID') or '')
        if not video:
            kitsu_id = await kitsu_identifier(item)
            payload = await kitsu_fetch('/anime/' + kitsu_id)
            video = str((payload['data'].get('attributes') or {}).get('youtubeVideoId') or '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{6,20}', video): return []
        return [dict(title='Trailer', embed_url='https://www.youtube-nocookie.com/embed/' + video,
                     watch_url='https://www.youtube.com/watch?v=' + video)][:limit]
    if source != 'tmdb' or kind not in ('movie', 'series') or not identifier.isdigit():
        return []
    token = os.getenv('TMDB_READ_TOKEN', '').strip()
    if not token:
        return []
    category = 'movie' if kind == 'movie' else 'tv'
    payload = await fetch(f'https://api.themoviedb.org/3/{category}/{identifier}/videos',
                          params={'language': 'pt-BR'}, headers={'Authorization': 'Bearer ' + token})
    videos = payload.get('results', [])
    if not videos:
        payload = await fetch(f'https://api.themoviedb.org/3/{category}/{identifier}/videos',
                              params={'language': 'en-US'}, headers={'Authorization': 'Bearer ' + token})
        videos = payload.get('results', [])
    eligible = [video for video in videos if video.get('site') == 'YouTube'
                and video.get('type') in ('Trailer', 'Teaser')
                and re.fullmatch(r'[A-Za-z0-9_-]{6,20}', str(video.get('key', '')))]
    eligible.sort(key=lambda video: (video.get('type') != 'Trailer', not video.get('official', False)))
    return [dict(title=str(video.get('name') or 'Trailer'),
                 embed_url='https://www.youtube-nocookie.com/embed/' + video['key'],
                 watch_url='https://www.youtube.com/watch?v=' + video['key']) for video in eligible[:limit]]


def book_item(item: dict) -> dict:
    return media('openlibrary', 'book', str(item['key']).split('/')[-1], item.get('title'),
        year=item.get('first_publish_year'),
        search_titles=[edition.get('title', '') for edition in (item.get('editions') or {}).get('docs', [])],
        cover_url=f"https://covers.openlibrary.org/b/id/{item['cover_i']}-M.jpg" if item.get('cover_i') else '',
        details={'Autores': ', '.join(item.get('author_name', [])),
                 'Páginas': str(item.get('number_of_pages_median') or 'Não informado')})


async def home_collection(key: str) -> list[dict]:
    kind, _, _, selection = HOME_COLLECTIONS[key]
    if kind in ('movie', 'series'):
        token = os.getenv('TMDB_READ_TOKEN', '').strip()
        if not token: raise APIError('O catálogo de filmes e séries está indisponível.')
        payload = await fetch('https://api.themoviedb.org/3/' + selection,
            params={'language': 'pt-BR', 'page': 1, 'region': 'BR'},
            headers={'Authorization': f'Bearer {token}'})
        items = [tmdb_item(item, kind) for item in payload.get('results', []) if not item.get('adult')]
    elif kind == 'anime':
        payload = await kitsu_fetch('/anime', **{'sort': selection, 'page[limit]': 20, 'include': 'mappings'})
        items = kitsu_items(payload)
    else:
        if selection.startswith('title:'):
            payload = await fetch('https://openlibrary.org/search.json', params={
                'title': selection.removeprefix('title:'), 'lang': 'pt', 'limit': 20,
                'fields': 'key,title,author_name,first_publish_year,cover_i,number_of_pages_median,editions,editions.title'})
            items = [book_item(item) for item in payload.get('docs', [])]
        elif selection.startswith('titles:'):
            # Open Library is more reliable when each curated title is searched
            # independently than when several titles are combined in `q`.
            titles = [title.strip() for title in selection.removeprefix('titles:').split('|') if title.strip()]
            responses = await asyncio.gather(*(fetch('https://openlibrary.org/search.json', params={
                'title': title, 'lang': 'pt', 'limit': 4,
                'fields': 'key,title,author_name,first_publish_year,cover_i,number_of_pages_median,editions,editions.title'})
                for title in titles))
            items = [book_item(item) for payload in responses for item in payload.get('docs', [])]
        else:
            payload = await fetch('https://openlibrary.org/search.json', params={
                'q': f'subject:{selection}', 'lang': 'pt', 'limit': 20,
                'fields': 'key,title,author_name,first_publish_year,cover_i,number_of_pages_median,editions,editions.title'})
            items = [book_item(item) for item in payload.get('docs', [])]
    return list({item['identity_key']: item for item in items}.values())


async def search_one(query: str, kind: str, page: int = 1) -> list[dict]:
    if kind in ('movie','series'):
        token = os.getenv('TMDB_READ_TOKEN','').strip()
        if not token: raise APIError('A busca de filmes e séries ainda não está disponível.')
        category = 'movie' if kind == 'movie' else 'tv'
        path = f'search/{category}' if query else f'{category}/popular'
        payload = await fetch('https://api.themoviedb.org/3/'+path,
                              params={'query':query,'page':page,'language':'pt-BR','include_adult':'false'},
                              headers={'Authorization':f'Bearer {token}'})
        return [tmdb_item(item,kind) for item in payload.get('results',[])]
    if kind == 'anime':
        payload = await kitsu_fetch('/anime', **{
            **({'filter[text]': query} if query else {'sort': '-userCount'}),
            'page[limit]': 12, 'page[offset]': (max(1, page) - 1) * 12, 'include': 'mappings'})
        return kitsu_items(payload)
    payload = await fetch('https://openlibrary.org/search.json',params={
        **({'title':query} if query else {'q':'fiction'}), 'lang':'pt',
        'page':page,'limit':12,'fields':'key,title,author_name,first_publish_year,cover_i,number_of_pages_median,editions,editions.title'})
    return [book_item(item) for item in payload.get('docs',[])]


async def search(query: str, kind: str = 'all', page: int = 1) -> tuple[list[dict], list[str]]:
    kinds = list(TYPES) if kind == 'all' else [kind]
    if any(k not in TYPES for k in kinds): raise ValueError('Unknown media type')
    results = await asyncio.gather(*(search_one(search_query(query),k,page) for k in kinds), return_exceptions=True)
    items, errors = [], []
    for k,result in zip(kinds,results):
        if isinstance(result,Exception): errors.append(f'{TYPES[k]}: {result if isinstance(result,APIError) else "Fonte indisponível."}')
        else: items.extend(result)
    return relevant_results(query, items), errors


async def detail(item: dict) -> dict:
    source, identifier = item['external_source'], str(item['external_id'])
    allowed = {'tmdb': ('movie', 'series'), 'jikan': ('anime',), 'kitsu': ('anime',), 'openlibrary': ('book',)}
    if item.get('media_type') not in allowed.get(source, ()):
        raise APIError('Fonte ou categoria inválida.')
    if source == 'tmdb':
        if not identifier.isdigit(): raise APIError('Identificador inválido.')
        category='movie' if item['media_type']=='movie' else 'tv'
        headers={'Authorization':'Bearer '+os.getenv('TMDB_READ_TOKEN','')}
        payload,credits=await asyncio.gather(
            fetch(f'https://api.themoviedb.org/3/{category}/{identifier}',params={'language':'pt-BR'},headers=headers),
            fetch(f'https://api.themoviedb.org/3/{category}/{identifier}/credits',params={'language':'pt-BR'},headers=headers),
            return_exceptions=True)
        if isinstance(payload,BaseException): raise payload
        result=tmdb_item(payload,item['media_type'])
        if not isinstance(credits,BaseException):
            crew=credits.get('crew',[]); cast=credits.get('cast',[])
            label='Dire\u00e7\u00e3o' if category=='movie' else 'Cria\u00e7\u00e3o'
            people=[p.get('name','') for p in crew if p.get('job') in ('Director','Creator')][:3]
            if people: result['details'][label]=', '.join(people)
            if cast: result['details']['Elenco principal']=', '.join(p.get('name','') for p in cast[:8] if p.get('name'))
        return result
    if source in ('kitsu', 'jikan'):
        kitsu_id = await kitsu_identifier(item)
        payload = await kitsu_fetch('/anime/' + kitsu_id, include='categories,mappings')
        if not isinstance(payload['data'], dict) or not kitsu_safe(payload['data']):
            raise APIError('Anime não disponível neste catálogo.', 404)
        result = kitsu_item(payload['data'], payload.get('included'))
        if source == 'jikan':
            # Preserve saved library links while refreshing metadata through Kitsu.
            result.update(external_source=source, external_id=identifier,
                          identity_key=f'jikan:anime:{identifier}', id=item.get('id', 0))
        return result
    if source == 'openlibrary':
        if not re.fullmatch(r'OL\d+W',identifier): raise APIError('Identificador inválido.')
        payload=await fetch(f'https://openlibrary.org/works/{identifier}.json',params={'lang':'pt'})
        description=payload.get('description','')
        if isinstance(description,dict): description=description.get('value','')
        details=dict(item.get('details') or {})
        author_keys=[a.get('author',{}).get('key','') for a in payload.get('authors',[])[:5]]
        author_keys=[key for key in author_keys if re.fullmatch(r'/authors/OL\d+A',key)]
        if author_keys:
            authors=await asyncio.gather(*(fetch('https://openlibrary.org'+key+'.json') for key in author_keys),return_exceptions=True)
            names=[a.get('name','') for a in authors if isinstance(a,dict) and a.get('name')]
            if names: details['Autores']=', '.join(names)
        if payload.get('subjects'): details['Temas']=', '.join(str(s) for s in payload['subjects'][:8])
        covers=payload.get('covers') or []
        return {**item,'title':payload.get('title') or item['title'],'description':description,
                'year':year(payload.get('first_publish_date')) or item.get('year',0),'details':details,
                'cover_url':f'https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg' if covers and isinstance(covers[0],int) and covers[0]>0 else item.get('cover_url','')}
    return item


async def availability(item: dict, region: str = 'BR') -> list[dict[str, str]]:
    """Return legal viewing options reported by the catalog for a country."""
    source, identifier = item.get('external_source'), str(item.get('external_id', ''))
    kind = item.get('media_type')
    if source != 'tmdb' or kind not in ('movie', 'series') or not identifier.isdigit():
        return []
    category = 'movie' if kind == 'movie' else 'tv'
    headers = {'Authorization': 'Bearer ' + os.getenv('TMDB_READ_TOKEN', '')}
    payload = await fetch(f'https://api.themoviedb.org/3/{category}/{identifier}/watch/providers',
                          params={'watch_region': region.upper(), 'language': 'pt-BR'}, headers=headers)
    countries = payload.get('results') or {}
    country = countries.get(region.upper()) or {}
    result, seen = [], set()
    for bucket in ('flatrate', 'free', 'ads', 'rent', 'buy'):
        for provider in country.get(bucket, []) or []:
            name = str(provider.get('provider_name') or '').strip()
            link = safe_url(country.get('link'))
            if name and name not in seen:
                seen.add(name)
                result.append({'name': name, 'url': link, 'type': bucket})
    return result
