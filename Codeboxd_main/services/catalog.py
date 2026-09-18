"""Media providers called on the Python server; provider keys stay off the client."""
import asyncio
import os
import re
from urllib.parse import urlsplit
from typing import Any

import httpx

from .api import APIError

TYPES = {'movie': 'Filme', 'series': 'Série', 'anime': 'Anime', 'book': 'Livro'}


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
                year=int(extra.get('year') or 0), details=extra.get('details') or {})


async def fetch(url: str, **kwargs) -> dict:
    try:
        async with httpx.AsyncClient(timeout=15, headers={'User-Agent': 'Codeboxd/1.0'}) as client:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            value = response.json()
            if not isinstance(value, dict):
                raise ValueError('Expected object')
            return value
    except (httpx.HTTPError, ValueError) as exc:
        raise APIError('A fonte de catálogo está indisponível no momento.') from exc


def year(value) -> int:
    match = re.match(r'\d{4}', str(value or ''))
    return int(match[0]) if match else 0


def tmdb_item(item: dict, kind: str) -> dict:
    details = {}
    for label, key in [('Duração (min)', 'runtime'), ('Temporadas', 'number_of_seasons'), ('Episódios', 'number_of_episodes')]:
        if item.get(key): details[label] = str(item[key])
    if item.get('genres'): details['Gêneros'] = ', '.join(g['name'] for g in item['genres'])
    return media('tmdb', kind, str(item['id']), item.get('title') or item.get('name'),
                 description=item.get('overview'), year=year(item.get('release_date') or item.get('first_air_date')),
                 cover_url=('https://image.tmdb.org/t/p/w500'+item['poster_path']) if item.get('poster_path') else '', details=details)


def anime_item(item: dict) -> dict:
    return media('jikan','anime',str(item['mal_id']),item.get('title'),description=item.get('synopsis'),
                 year=item.get('year'), cover_url=item.get('images',{}).get('jpg',{}).get('image_url'),
                 details={'Episódios':str(item.get('episodes') or 'Não informado'),
                          'Estúdios':', '.join(s['name'] for s in item.get('studios',[]))})


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
        payload = await fetch('https://api.jikan.moe/v4/anime', params={'q':query,'page':page,'limit':12,'sfw':'true'})
        return [anime_item(item) for item in payload.get('data',[])]
    payload = await fetch('https://openlibrary.org/search.json',params={
        'q':query or 'fiction','page':page,'limit':12,'fields':'key,title,author_name,first_publish_year,cover_i,number_of_pages_median'})
    return [media('openlibrary','book',str(item['key']).split('/')[-1],item.get('title'),
                  year=item.get('first_publish_year'),
                  cover_url=f"https://covers.openlibrary.org/b/id/{item['cover_i']}-M.jpg" if item.get('cover_i') else '',
                  details={'Autores':', '.join(item.get('author_name',[])), 'Páginas':str(item.get('number_of_pages_median') or 'Não informado')})
            for item in payload.get('docs',[])]


async def search(query: str, kind: str = 'all', page: int = 1) -> tuple[list[dict], list[str]]:
    kinds = list(TYPES) if kind == 'all' else [kind]
    if any(k not in TYPES for k in kinds): raise ValueError('Unknown media type')
    results = await asyncio.gather(*(search_one(query.strip()[:200],k,page) for k in kinds), return_exceptions=True)
    items, errors = [], []
    for k,result in zip(kinds,results):
        if isinstance(result,Exception): errors.append(f'{TYPES[k]}: {result if isinstance(result,APIError) else "Fonte indisponível."}')
        else: items.extend(result)
    return items, errors


async def detail(item: dict) -> dict:
    source, identifier = item['external_source'], str(item['external_id'])
    allowed = {'tmdb': ('movie', 'series'), 'jikan': ('anime',), 'openlibrary': ('book',)}
    if item.get('media_type') not in allowed.get(source, ()):
        raise APIError('Fonte ou categoria inválida.')
    if source == 'tmdb':
        if not identifier.isdigit(): raise APIError('Identificador inválido.')
        category='movie' if item['media_type']=='movie' else 'tv'
        payload=await fetch(f'https://api.themoviedb.org/3/{category}/{identifier}',params={'language':'pt-BR'},
                            headers={'Authorization':'Bearer '+os.getenv('TMDB_READ_TOKEN','')})
        return tmdb_item(payload,item['media_type'])
    if source == 'jikan':
        if not identifier.isdigit(): raise APIError('Identificador inválido.')
        return anime_item((await fetch(f'https://api.jikan.moe/v4/anime/{identifier}/full'))['data'])
    if source == 'openlibrary':
        if not re.fullmatch(r'OL\d+W',identifier): raise APIError('Identificador inválido.')
        payload=await fetch(f'https://openlibrary.org/works/{identifier}.json')
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
