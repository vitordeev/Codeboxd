from pathlib import Path
p=Path('Codeboxd_main/services/catalog.py')
s=p.read_text(encoding='utf8').replace('import asyncio\n','import asyncio\nimport copy\nimport json\nimport logging\nimport time\nfrom collections import OrderedDict\n')
s=s.replace("'Explore os destaques do MyAnimeList.', 'top/anime'", "'Explore os destaques da Kitsu.', '-averageRating'")
s=s.replace("TYPES =", "logger = logging.getLogger(__name__)\nKITSU_URL = 'https://kitsu.app/api/edge'\n_kitsu_cache: OrderedDict = OrderedDict()\n\n\nTYPES =",1)
s=s.replace("    except (httpx.HTTPError, ValueError) as exc:\n        raise APIError('A fonte de catálogo está indisponível no momento.') from exc", '''    except (httpx.HTTPError, ValueError) as exc:
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
        raise APIError(message, status) from exc''')
start=s.index('def anime_item(')
end=s.index('\n\nasync def recommendations',start)
s=s[:start]+'''async def kitsu_fetch(path: str, **params) -> dict:
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
''' + s[end:]
s=s.replace("    if source == 'jikan' and kind == 'anime' and identifier.isdigit():\n        payload=await fetch(f'https://api.jikan.moe/v4/anime/{identifier}/recommendations')\n        return [anime_item(row['entry']) for row in payload.get('data',[])[:limit] if isinstance(row.get('entry'),dict)]", '''    if source in ('kitsu', 'jikan') and kind == 'anime' and identifier.isdigit():
        kitsu_id = await kitsu_identifier(item)
        payload = await kitsu_fetch(f'/anime/{kitsu_id}/media-relationships', **{
            'include': 'destination', 'page[limit]': min(20, limit)})
        related_ids = {str(target['id']) for row in payload.get('data', [])
            if (target := ((row.get('relationships') or {}).get('destination') or {}).get('data'))
            and target.get('type') == 'anime'}
        return [kitsu_item(row) for row in payload.get('included', [])
                if kitsu_safe(row) and str(row['id']) in related_ids and str(row['id']) != kitsu_id][:limit]''')
start=s.index("    if source == 'jikan' and kind == 'anime'",s.index('async def reviews'))
end=s.index('    return []',start)
s=s[:start]+'''    if source in ('kitsu', 'jikan') and kind == 'anime' and identifier.isdigit():
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
''' + s[end:]
s=s.replace("    if source != 'tmdb' or kind not in ('movie', 'series') or not identifier.isdigit():", '''    if source in ('kitsu', 'jikan') and kind == 'anime' and identifier.isdigit():
        video = str((item.get('details') or {}).get('YouTube ID') or '')
        if not video:
            kitsu_id = await kitsu_identifier(item)
            payload = await kitsu_fetch('/anime/' + kitsu_id)
            video = str((payload['data'].get('attributes') or {}).get('youtubeVideoId') or '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{6,20}', video): return []
        return [dict(title='Trailer', embed_url='https://www.youtube-nocookie.com/embed/' + video,
                     watch_url='https://www.youtube.com/watch?v=' + video)][:limit]
    if source != 'tmdb' or kind not in ('movie', 'series') or not identifier.isdigit():''')
s=s.replace("        payload = await fetch('https://api.jikan.moe/v4/' + selection, params={'limit': 20, 'sfw': 'true'})\n        items = [anime_item(item) for item in payload.get('data', [])]", "        payload = await kitsu_fetch('/anime', **{'sort': selection, 'page[limit]': 20, 'include': 'mappings'})\n        items = kitsu_items(payload)")
s=s.replace("        payload = await fetch('https://api.jikan.moe/v4/anime', params={'q':query,'page':page,'limit':12,'sfw':'true'})\n        return [anime_item(item) for item in payload.get('data',[])]", "        payload = await kitsu_fetch('/anime', **{\n            **({'filter[text]': query} if query else {'sort': '-userCount'}),\n            'page[limit]': 12, 'page[offset]': (max(1, page) - 1) * 12, 'include': 'mappings'})\n        return kitsu_items(payload)")
s=s.replace("'jikan': ('anime',), 'openlibrary'", "'jikan': ('anime',), 'kitsu': ('anime',), 'openlibrary'")
s=s.replace("    if source == 'jikan':\n        if not identifier.isdigit(): raise APIError('Identificador inválido.')\n        return anime_item((await fetch(f'https://api.jikan.moe/v4/anime/{identifier}/full'))['data'])", '''    if source in ('kitsu', 'jikan'):
        kitsu_id = await kitsu_identifier(item)
        payload = await kitsu_fetch('/anime/' + kitsu_id, include='categories,mappings')
        if not isinstance(payload['data'], dict) or not kitsu_safe(payload['data']):
            raise APIError('Anime não disponível neste catálogo.', 404)
        result = kitsu_item(payload['data'], payload.get('included'))
        if source == 'jikan':
            # Preserve saved library links while refreshing metadata through Kitsu.
            result.update(external_source=source, external_id=identifier,
                          identity_key=f'jikan:anime:{identifier}', id=item.get('id', 0))
        return result''')
p.write_text(s,encoding='utf8')
