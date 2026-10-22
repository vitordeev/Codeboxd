"""Social UI state backed by Xano endpoints."""
import asyncio
import json
import os
import re
import uuid
import time
import math
import hashlib
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import reflex as rx
from reflex.constants import Endpoint
from .session import SessionState
from ..services import catalog
from ..services.api import APIError, base_url, request, rows
from ..services.uploads import upload_file

DEFAULT_MEDIA_LISTS = (
    ('Quero ver / ler', 'Obras para descobrir depois.'),
    ('Já assisti / li', 'Obras que você já terminou.'),
)
BROKEN_DEFAULT_LISTS = {
    'jã¡ assisti / li': ('Já assisti / li', 'Obras que você já terminou.'),
}

# Tasks stay outside Reflex state: they cannot be pickled. Keys contain only
# a session-local nonce, cache generation and a digest of the request.
_NAVIGATION_IN_FLIGHT: dict[tuple, asyncio.Task] = {}


async def shared_navigation_read(key, read):
    task = _NAVIGATION_IN_FLIGHT.get(key)
    if task is None:
        task = asyncio.create_task(read())
        _NAVIGATION_IN_FLIGHT[key] = task

        def finished(done):
            if _NAVIGATION_IN_FLIGHT.get(key) is done:
                del _NAVIGATION_IN_FLIGHT[key]
            # A cancelled waiter must not leave an unobserved task exception.
            if not done.cancelled(): done.exception()

        task.add_done_callback(finished)
    # Cancelling one consumer must not cancel another consumer's request.
    return deepcopy(await asyncio.shield(task))


def normalize_rating(value) -> str:
    """Accept either decimal separator, keeping the existing half-star scale."""
    try:
        rating = Decimal(str(value if value is not None else 0).strip().replace(',', '.'))
    except InvalidOperation as exc:
        raise ValueError('Invalid rating') from exc
    if not rating.is_finite() or not 0 <= rating <= 5 or (rating * 2) % 1:
        raise ValueError('Invalid rating')
    return '0' if rating == 0 else format(rating.normalize(), 'f')


def present_media(m: dict) -> dict[str,str]:
    details=m.get('details') or {}
    return {k:str(v or '') for k,v in dict(id=m.get('id',0),key=m.get('identity_key',''),
        title=m.get('title','Sem título'),kind=catalog.TYPES.get(m.get('media_type'),'Mídia'),
        year=m.get('year',''),cover=catalog.safe_url(m.get('cover_url')),description=m.get('description',''),
        backdrop=catalog.safe_url(m.get('backdrop_url')),
        source=m.get('external_source',''),external_id=m.get('external_id',''),
        details=' · '.join(f'{k}: {v}' for k,v in details.items()
            if k not in {'Kitsu ID', 'MyAnimeList ID', 'YouTube ID'}) if isinstance(details,dict) else '').items()}


class SocialState(SessionState):
    notice: str = ''
    busy: bool = False
    media_details_loading: bool = False
    media_interaction_loading: bool = False
    media_details_error: str = ''
    _media_generation: int = 0
    _profile_generation: int = 0
    _visit_generation: int = 0
    _interaction_generation: int = 0
    search_term: str = ''
    search_type: str = 'all'
    submitted_query: str = ''
    search_active: bool = False
    has_more_results: bool = True
    failed_covers: list[str] = []
    search_page: int = 1
    search_results: list[dict[str,str]] = []
    featured_items: list[dict[str,str]] = []
    popular_movies: list[dict[str,str]] = []
    popular_series: list[dict[str,str]] = []
    home_collections: dict[str,list[dict[str,str]]] = {key: [] for key in catalog.HOME_COLLECTIONS}
    home_collection_errors: list[str] = []
    home_loaded: bool = False
    popular_exhausted: list[str] = []
    _popular_pages: dict[str,int] = {'movie':1, 'series':1}
    _popular_loaded: list[str] = []
    catalog_items: list[dict[str,str]] = []
    selected: dict[str,str] = {'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':'','backdrop':''}
    recommendations: list[dict[str,str]] = []
    availability: list[dict[str,str]] = []
    community_reviews: list[dict[str,str]] = []
    selected_status: str = 'planned'
    selected_rating: str = '0'
    guest_ratings: str = rx.LocalStorage('{}', name='codeboxd_guest_ratings', sync=True)
    trailers: list[dict[str,str]] = []
    selected_review: str = ''
    selected_spoiler: bool = False
    interaction_saving: bool = False
    interaction_saved: bool = False
    review_editor_open: bool = True
    _saved_interaction: dict = {}
    library: list[dict[str,str]] = []
    library_paginated: bool = False
    library_loading: bool = False
    library_has_more: bool = False
    library_error: str = ''
    _library_cursor: int = 0
    _library_generation: int = 0
    _library_owner: str = ''
    _library_retry_at: float = 0.0
    people: list[dict[str,str]] = []
    profile: dict[str,str] = {'user_id':'','username':'','display_name':'','bio':'','avatar_url':'','banner_url':''}
    profile_stats: str = ''
    profile_activity_loading: bool = False
    profile_people_loading: bool = False
    profile_activity_error: str = ''
    profile_people_error: str = ''
    profile_counts: dict[str,int] = {'followers':0,'following':0,'activities':0}
    profile_activity: list[dict[str,str]] = []
    followers: list[dict[str,str]] = []
    following: list[dict[str,str]] = []
    following_ids: list[str] = []
    posts: list[dict[str,str]] = []
    comments: list[dict[str,str]] = []
    selected_post: str = ''
    liked_posts: list[str] = []
    edit_post_id: str = ''
    post_editor_token: str = ''
    edit_post_body: str = ''
    edit_post_media: str = '0'
    edit_post_spoiler: bool = False
    post_media_query: str = ''
    post_media_searching: bool = False
    post_media_results: list[dict[str,str]] = []
    post_media_selected: dict[str,str] = {'id':'','key':'','title':'','cover':''}
    post_image_filename: str = ''
    post_image_mime: str = ''
    post_existing_image_url: str = ''
    edit_comment_id: str = ''
    edit_comment_body: str = ''
    lists: list[dict[str,str]] = []
    quick_lists: list[dict[str,str]] = []
    list_items: list[dict[str,str]] = []
    selected_list: dict[str,str] = {'id':'','title':'','description':'','user_id':'','is_public':'True'}
    list_media_query: str = ''
    list_media_results: list[dict[str,str]] = []
    list_media_searching: bool = False
    list_media_error: str = ''
    list_item_saving: bool = False
    media_list_open: bool = False
    media_list_loading: bool = False
    media_list_options: list[dict[str,str]] = []
    media_list_target: str = ''
    media_list_error: str = ''
    _list_search_generation: int = 0
    _list_media_candidates: dict[str,dict] = {}
    _media: dict[str,dict] = {}
    _results: dict[str,dict] = {}
    _selected_raw: dict = {}
    _profiles: dict[str,dict] = {}
    _post_media_candidates: dict[str,dict] = {}
    _post_media_raw: dict = {}
    _post_image_path: str = ''
    _identity: int = 0
    _navigation_reads: dict = {}
    _navigation_generation: int = 0
    _navigation_scope: str = ''
    visible_count: int = 20
    post_editor_open: bool = False
    post_saving: bool = False
    list_editor_open: bool = False
    report_dialog_open: bool = False
    report_target_type: str = ''
    report_target_id: str = ''
    report_reason: str = 'spam'
    report_description: str = ''
    report_sending: bool = False
    report_error: str = ''
    _report_retry_at: float = 0.0

    @rx.event
    def set_post_editor_open(self, value: bool):
        if self.post_saving: return
        if not value:
            self.cancel_post()
        elif self.is_authenticated:
            self.post_editor_open = True
        else:
            return rx.redirect('/login')

    @rx.event
    def set_list_editor_open(self, value: bool):
        self.list_editor_open = value

    @rx.event
    def update_search_term(self, value: str):
        self.search_term=value[:200]

    @rx.event
    def set_selected_status(self, value: str):
        if value in ('planned','in_progress','completed','dropped'):
            self.selected_status=value

    @rx.event
    def set_selected_rating(self, value: str):
        try:
            value = normalize_rating(value)
        except ValueError:
            return
        self.selected_rating=value
        if not self.is_authenticated and self.selected.get('key'):
            try: ratings=json.loads(self.guest_ratings or '{}')
            except (TypeError,ValueError): ratings={}
            if not isinstance(ratings,dict): ratings={}
            ratings[self.selected['key']]=value
            self.guest_ratings=json.dumps(ratings,separators=(',',':'))
            self.notice='Nota salva somente neste navegador. Entre para publicar uma crítica e organizar suas obras.'

    @rx.var
    def selected_rating_value(self) -> float:
        try:
            return float(normalize_rating(self.selected_rating))
        except ValueError:
            return 0.0

    def _restore_guest_rating(self):
        if self.is_authenticated or not self.selected.get('key'): return
        try: ratings=json.loads(self.guest_ratings or '{}')
        except (TypeError,ValueError): return
        value=ratings.get(self.selected['key']) if isinstance(ratings,dict) else None
        if value is not None:
            try: self.selected_rating=normalize_rating(value)
            except ValueError: pass

    async def _load_trailers(self):
        stamp=self._media_stamp(); item=deepcopy(self._selected_raw)
        self.trailers=[]
        try:
            result=await catalog.trailers(item)
            if stamp==self._media_stamp(): self.trailers=result
        except APIError as exc:
            if stamp==self._media_stamp(): self.media_details_error=str(exc)

    async def _load_availability(self):
        stamp=self._media_stamp(); item=deepcopy(self._selected_raw)
        self.availability=[]
        try:
            result=await catalog.availability(item)
            if stamp==self._media_stamp(): self.availability=result
        except APIError as exc:
            if stamp==self._media_stamp(): self.media_details_error=str(exc)

    def _route_stamp(self):
        return (self._visit_generation,self.router.url.path,
                tuple(sorted(self.router.url.query_parameters.items())),self._token())

    def _media_stamp(self):
        return (self._media_generation,self._route_stamp(),
                self._selected_raw.get('identity_key') or self._selected_raw.get('id'))

    def _search_stamp(self):
        return (self._route_stamp(),self.submitted_query,self.search_type,self.search_active)

    @rx.event
    def new_post(self):
        if self.post_saving: return
        if not self.is_authenticated: return rx.redirect('/login')
        self.cancel_post()
        self.post_editor_token=uuid.uuid4().hex
        self.post_editor_open = True

    @rx.event
    def update_post_media_query(self, value: str):
        self.post_media_query=value[:160]

    @rx.event
    async def search_post_media(self):
        query=self.post_media_query.strip()
        self.post_media_results=[]
        self._post_media_candidates={}
        if not query:
            self.notice='Digite o nome de uma obra para pesquisar.'
            return
        self.post_media_searching=True
        yield
        try:
            found,errors=await catalog.search(query,'all')
            candidates={str(item.get('identity_key') or ''):item for item in found
                        if item.get('identity_key')}
            for item in self._media.values():
                if catalog.title_score(query,item)>0:
                    candidates[str(item.get('identity_key') or '')]=item
            candidates.pop('',None)
            self._post_media_candidates=candidates
            ranked=catalog.relevant_results(query,list(candidates.values()))
            self.post_media_results=[present_media(item) for item in ranked[:12]]
            self.notice=' '.join(errors) or ('Nenhuma obra encontrada.' if not self.post_media_results else '')
        except APIError as exc:
            self.notice=str(exc)
        finally:
            self.post_media_searching=False

    @rx.event
    def select_post_media(self, key: str):
        item=self._post_media_candidates.get(key)
        if not item: return
        self._post_media_raw=item
        selected=present_media(item)
        self.post_media_selected={k:selected[k] for k in ('id','key','title','cover')}
        self.edit_post_media=str(item.get('id') or '0')
        self.post_media_results=[]

    @rx.event
    def clear_post_media(self):
        self._post_media_raw={}
        self.post_media_selected={'id':'','key':'','title':'','cover':''}
        self.edit_post_media='0'

    async def _persist_post_media(self) -> int:
        if not self._post_media_raw:
            return 0
        try:
            media_id=int(self._post_media_raw.get('id') or 0)
        except (TypeError,ValueError):
            media_id=0
        if media_id:
            return media_id
        payload={key:self._post_media_raw[key] for key in
                 ('external_source','external_id','media_type','title','description','cover_url','year','details')}
        result=await self._call('POST','/media',payload)
        self._post_media_raw=result
        selected=present_media(result)
        self.post_media_selected={k:selected[k] for k in ('id','key','title','cover')}
        return int(result['id'])

    @rx.event
    async def stage_post_image(self, files: list[rx.UploadFile]):
        if not await self._require_user(): return rx.redirect('/login')
        if len(files)!=1:
            self.notice='Selecione uma imagem.'
            return
        content=await files[0].read()
        if len(content)>5*1024*1024:
            self.notice='A imagem deve ter no m\u00e1ximo 5 MB.'
            return
        signatures=((b'\x89PNG\r\n\x1a\n','png','image/png'),
            (b'\xff\xd8\xff','jpg','image/jpeg'),(b'GIF87a','gif','image/gif'),
            (b'GIF89a','gif','image/gif'),(b'RIFF','webp','image/webp'))
        match=next(((ext,mime) for signature,ext,mime in signatures if content.startswith(signature)),None)
        if match and match[0]=='webp' and content[8:12]!=b'WEBP': match=None
        if not match:
            self.notice='Envie uma imagem PNG, JPG, WEBP ou GIF v\u00e1lida.'
            return
        self._discard_post_upload()
        extension,mime=match
        relative=f'posts/staged-{uuid.uuid4().hex}.{extension}'
        path=rx.get_upload_dir()/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(content)
        self._post_image_path=str(path)
        self.post_image_filename=relative
        self.post_image_mime=mime
        self.notice='Imagem carregada. Ela ser\u00e1 salva junto com a publica\u00e7\u00e3o.'

    def _discard_post_upload(self):
        if self._post_image_path:
            Path(self._post_image_path).unlink(missing_ok=True)
        self._post_image_path=''
        self.post_image_filename=''
        self.post_image_mime=''

    @rx.event
    def remove_post_image(self):
        self._discard_post_upload()
        self.notice='Imagem removida do rascunho.'

    @rx.var
    def suggested_people(self) -> list[dict[str,str]]:
        return [p for p in self.people if p['user_id'] != str(self.user_id)][:5]

    @rx.var
    def visible_library(self) -> list[dict[str,str]]:
        return self.library if self.library_paginated else self.library[:self.visible_count]

    @rx.var
    def visible_people(self) -> list[dict[str,str]]:
        return self.people[:self.visible_count]

    @rx.var
    def visible_posts(self) -> list[dict[str,str]]:
        return self.posts[:self.visible_count]

    @rx.var
    def visible_lists(self) -> list[dict[str,str]]:
        return self.lists[:self.visible_count]

    @rx.event
    def show_more(self):
        self.visible_count+=20

    @rx.event
    async def visit(self, section: str):
        self._visit_generation+=1
        generation=self._visit_generation
        self.visible_count=20; self.busy=True; self.notice=''
        yield
        try:
            if section == 'home':
                async for _ in self._home_updates():
                    yield
                return
            if section == 'profile':
                async for event in self._profile_updates():
                    yield event
                return
            if section in ('media','external'):
                async for event in self._media_updates(section=='external'):
                    yield event
                return
            loaders={'home':self.load_home,'library':self.load_library,'community':self.load_community,
                     'profile':self.load_profile,'feed':self.load_feed,'lists':self.load_lists,
                     'media':self.load_media,'external':self.load_external_media}
            if section in loaders:
                result=await loaders[section]()
                if result: yield result
        finally:
            if generation==self._visit_generation: self.busy=False

    def _reset_personal(self):
        self._library_generation+=1
        self._library_cursor=0; self._library_owner=''; self._library_retry_at=0.0
        self.library_loading=False; self.library_has_more=False; self.library_error=''
        self._navigation_reads={}
        self._navigation_generation+=1
        self.profile_activity_loading=False; self.profile_people_loading=False
        self.profile_activity_error=''; self.profile_people_error=''
        self.profile_counts={'followers':0,'following':0,'activities':0}
        self._saved_interaction = {}
        self.interaction_saved = False
        self.review_editor_open = True
        self._discard_post_upload()
        self.post_editor_open=False; self.list_editor_open=False
        self.report_dialog_open=False; self.report_target_type=''; self.report_target_id=''
        self.report_reason='spam'; self.report_description=''; self.report_sending=False
        self.report_error=''; self._report_retry_at=0.0
        self.library=[]; self.posts=[]; self.comments=[]; self.lists=[]; self.quick_lists=[]; self.list_items=[]
        self.following_ids=[]; self.liked_posts=[]; self.selected_post=''
        self.edit_post_id=''; self.edit_post_body=''; self.edit_post_media='0'; self.edit_post_spoiler=False
        self.post_editor_token=''
        self.post_media_query=''; self.post_media_results=[]; self._post_media_candidates={}; self._post_media_raw={}
        self.post_media_selected={'id':'','key':'','title':'','cover':''}
        self.post_existing_image_url=''
        self.edit_comment_id=''; self.edit_comment_body=''
        self.selected_review=''; self.selected_rating='0'; self.selected_status='planned'; self.selected_spoiler=False
        self.trailers=[]
        self.selected_list={'id':'','title':'','description':'','user_id':'','is_public':'True'}
        self._reset_list_search()
        self.media_list_open=False; self.media_list_options=[]; self.media_list_target=''; self.media_list_error=''
        self.profile={'user_id':'','username':'','display_name':'','bio':'','avatar_url':'','banner_url':''}
        self.profile_activity=[]; self.profile_stats=''; self.followers=[]; self.following=[]

    async def _validate_session(self) -> bool:
        valid = await super()._validate_session()
        # A transient provider error leaves the cached identity intact. Preserve
        # its draft; an identity change or rejected session must still clear it.
        if self._identity != self.user_id or (not valid and not self.is_authenticated):
            self._reset_personal()
        self._identity = self.user_id
        return valid

    async def _validate_navigation_session(self) -> bool:
        valid=await super()._validate_navigation_session()
        if self._identity!=self.user_id or (not valid and not self.is_authenticated):
            self._reset_personal()
        self._identity=self.user_id
        return valid

    @rx.event
    def logout_social(self):
        self._reset_personal()
        self._identity=0
        return self.logout()

    @rx.var
    def owns_profile(self) -> bool:
        return self.user_id > 0 and self.profile.get('user_id') == str(self.user_id)

    @rx.var
    def owns_list(self) -> bool:
        return self.user_id > 0 and self.selected_list.get('user_id') == str(self.user_id)

    def _failure(self, exc: APIError):
        self.notice=str(exc)
        if exc.status==401:
            self._clear_session(); self._reset_personal(); self._identity=0

    async def _call(self, method, path, data=None, params=None, *, paginate=True):
        cacheable=method=='GET' and (path in ('/media','/profiles','/lists','/interactions')
                                   or re.fullmatch(r'/profiles/[0-9]+',path) is not None)
        key=hashlib.sha256(json.dumps([self._token(),path,params,data,paginate],sort_keys=True).encode()).hexdigest()
        if method!='GET':
            self._navigation_reads={}; self._navigation_generation+=1
        generation=self._navigation_generation
        token=self._token()
        cached=self._navigation_reads.get(key) if cacheable else None
        if cached and cached[0]>time.monotonic():
            return deepcopy(cached[1])
        try:
            if cacheable:
                if not self._navigation_scope: self._navigation_scope=uuid.uuid4().hex
                inflight_key=(self._navigation_scope,generation,key)
                result=await shared_navigation_read(inflight_key,
                    lambda: self._request_pages(method,path,data,params,paginate=paginate,expected_token=token))
            else:
                result=await self._request_pages(method,path,data,params,paginate=paginate)
        except APIError as exc:
            if token!=self._token():
                raise APIError('Sessão alterada. Atualize a página.',409) from exc
            if exc.status in (401,403):
                self._navigation_reads={}; self._navigation_generation+=1
                self._forget_navigation_validation()
            raise
        finally:
            # Also discard reads started while a write was in flight.
            if method!='GET':
                self._navigation_reads={}; self._navigation_generation+=1
        if cacheable and generation==self._navigation_generation and token==self._token():
            now=time.monotonic()
            self._navigation_reads={k:v for k,v in self._navigation_reads.items() if v[0]>now}
            if len(self._navigation_reads)>=32:
                self._navigation_reads.pop(next(iter(self._navigation_reads)))
            self._navigation_reads[key]=(now+15,deepcopy(result))
        return result

    async def _request_pages(self, method, path, data=None, params=None, *, paginate=True, expected_token=None):
        token=self._token() if expected_token is None else expected_token
        if self._token()!=token: raise APIError('Sessão alterada. Atualize a página.',409)
        result=await request(method,path,token=token,data=data,params=params)
        if self._token()!=token: raise APIError('Sessão alterada. Atualize a página.',409)
        if method!='GET' or not paginate: return result
        # Read bounded API pages without truncating references or profile statistics.
        keys=[key for key,value in result.items() if isinstance(value,list)] if isinstance(result,dict) else []
        page=1
        while (isinstance(result,list) and len(result)==page*100) or any(len(result[key])==page*100 for key in keys):
            page+=1
            if page>100: raise APIError('Há muitos registros para esta consulta. Tente novamente mais tarde.')
            batch=await request(method,path,token=token,params={**(params or {}),'page':page,'per_page':100})
            if self._token()!=token: raise APIError('Sessão alterada. Atualize a página.',409)
            if isinstance(result,list): result.extend(rows(batch))
            else:
                for key in keys: result[key].extend(rows(batch[key]))
        return result

    async def _require_user(self, *, navigation=False) -> bool:
        valid=await self._validate_navigation_session() if navigation else await self._validate_session()
        if valid: return True
        # A transient auth-service failure is not a logout. Keep the current
        # navigation usable; any protected write is still authorized by Xano.
        if self.user_id > 0 and self._token(): return True
        self.notice=self.error_message or 'Entre na sua conta para continuar.'
        return False

    async def _load_media(self, per_page: int | None = None):
        stamp=self._route_stamp()
        params={'per_page':per_page} if per_page else None
        result=await self._call('GET','/media',params=params)
        if stamp!=self._route_stamp(): return
        self._media={str(m['id']):m for m in rows(result)}
        self.catalog_items=[present_media(m) for m in self._media.values()]

    async def _load_people(self):
        stamp=self._route_stamp()
        result=await self._call('GET','/profiles')
        if stamp!=self._route_stamp(): return
        self._profiles={str(p['user_id']):p for p in rows(result)}
        self.people=[self._person(uid) for uid in self._profiles]

    async def _load_reference(self):
        await asyncio.gather(self._load_media(),self._load_people())

    def _person(self, uid) -> dict[str,str]:
        p=self._profiles.get(str(uid),{})
        return dict(user_id=str(uid),username=str(p.get('username') or 'usuário'),
            display_name=str(p.get('display_name') or 'Usuário'),avatar_url=catalog.safe_url(p.get('avatar_url')),bio=str(p.get('bio') or ''))

    def _interaction(self, i: dict) -> dict[str,str]:
        result=present_media(self._media.get(str(i['media_id']),{'id':i['media_id']}))
        result.update(status={'planned':'Quero ver / ler','in_progress':'Em andamento','completed':'Concluído','dropped':'Abandonado'}.get(i['status'],i['status']),
            rating=str(i.get('rating') or 'Sem nota').replace('.',','),review=str(i.get('review') or ''),spoiler=str(bool(i.get('spoiler'))))
        return result

    @rx.event
    async def load_home(self):
        async for _ in self._home_updates():
            pass

    async def _home_updates(self):
        stamp=self._route_stamp()
        self.notice=''
        async def popular(kind):
            attribute = 'popular_movies' if kind == 'movie' else 'popular_series'
            if getattr(self, attribute) and kind in self._popular_loaded and kind != 'series': return
            items, errors = await catalog.search('', kind)
            if kind == 'series':
                highlights = await catalog.series_highlights()
                items = list({item['identity_key']: item for item in [*highlights, *items]}.values())
            if stamp!=self._route_stamp(): return
            if items:
                setattr(self, attribute, [present_media(m) for m in items])
                self._popular_loaded = [*self._popular_loaded, kind] if kind not in self._popular_loaded else self._popular_loaded
                self._popular_pages[kind] = 1
                self.popular_exhausted = [value for value in self.popular_exhausted if value != kind]
            if errors: self.notice = ' '.join(filter(None, [self.notice, *errors]))

        async def community():
            try: await self._load_media(per_page=20)
            except APIError as exc: self._failure(exc)

        pending = {asyncio.create_task(job) for job in (
            self._validate_navigation_session(), community(), popular('movie'), popular('series'), self._load_home_collections())}
        previous = None
        try:
            while pending:
                done, pending = await asyncio.wait(pending, timeout=0.15, return_when=asyncio.FIRST_COMPLETED)
                for job in done:
                    job.result()
                if stamp!=self._route_stamp(): return
                snapshot = (len(self.popular_movies), len(self.popular_series),
                            tuple(len(items) for items in self.home_collections.values()),
                            tuple(self.home_collection_errors))
                if done or snapshot != previous:
                    previous = snapshot
                    self.featured_items = (self.home_collections.get('movies_now') or self.popular_movies)[:2]
                    yield
        finally:
            for job in pending:
                job.cancel()
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
        for kind, attribute in [('movie', 'popular_movies'), ('series', 'popular_series')]:
            if not getattr(self, attribute):
                setattr(self, attribute, [present_media(m) for m in self._media.values()
                                         if m.get('media_type') == kind][:12])
        self.featured_items = (self.home_collections.get('movies_now') or self.popular_movies)[:2]
        self.home_loaded=True
        yield

    async def _load_home_collections(self):
        stamp=self._route_stamp()
        # Bound requests so one slow or unavailable provider cannot erase other shelves.
        slots={provider: asyncio.Semaphore(limit) for provider, limit in
               [('tmdb', 2), ('book', 2), ('anime', 1)]}
        async def load(key):
            if self.home_collections.get(key): return
            kind = catalog.HOME_COLLECTIONS[key][0]
            async with slots['tmdb' if kind in ('movie', 'series') else kind]:
                try:
                    items=await catalog.home_collection(key)
                    if stamp!=self._route_stamp(): return
                    self.home_collections[key]=[present_media(m) for m in items]
                    self.home_collection_errors=[value for value in self.home_collection_errors if value != key]
                except (APIError, KeyError, TypeError, ValueError):
                    if stamp!=self._route_stamp(): return
                    if key not in self.home_collection_errors:
                        self.home_collection_errors=[*self.home_collection_errors,key]
        await asyncio.gather(*(load(key) for key in catalog.HOME_COLLECTIONS))

    @rx.event
    async def retry_home_collections(self):
        if self.busy: return
        self.busy=True
        yield
        try:
            async for _ in self._home_updates():
                yield
        finally:
            self.busy=False

    @rx.event
    def show_home_catalog(self):
        self.search_active=False
        self.search_term=''
        self.submitted_query=''
        self.notice=''

    @rx.event
    async def more_popular(self, kind: str):
        if self.busy or kind not in ('movie', 'series') or kind in self.popular_exhausted: return
        self.busy=True
        yield
        try:
            page=self._popular_pages[kind]+1 if kind in self._popular_loaded else 1
            found,errors=await catalog.search('',kind,page)
            attribute='popular_movies' if kind=='movie' else 'popular_series'
            existing={item['key']:item for item in getattr(self,attribute)} if page > 1 or not found else {}
            existing.update({item['identity_key']:present_media(item) for item in found})
            setattr(self,attribute,list(existing.values()))
            if found and kind not in self._popular_loaded: self._popular_loaded=[*self._popular_loaded,kind]
            if found or not errors: self._popular_pages[kind]=page
            if not found and not errors: self.popular_exhausted=[*self.popular_exhausted,kind]
            self.notice=' '.join(errors)
        finally:
            self.busy=False

    @rx.event
    def cover_failed(self, url: str):
        if url and url not in self.failed_covers:
            self.failed_covers = [*self.failed_covers, url]

    @rx.event
    async def browse_category(self, kind: str):
        if kind not in catalog.TYPES and kind != 'all': return
        async for event in self.search({'query': '', 'kind': kind}):
            yield event

    @rx.event
    def open_featured(self, source: str, identifier: str, kind: str):
        return rx.redirect('/obra?'+urlencode({'external_source':source,'external_id':identifier,'media_type':kind}))

    @rx.event
    def open_recommendation(self, source: str, identifier: str):
        kind=str(self._selected_raw.get('media_type',''))
        return rx.redirect('/obra?'+urlencode({'external_source':source,'external_id':identifier,'media_type':kind}))

    @rx.event
    async def search(self, form: dict):
        if self.busy: return
        self.busy=True; self.notice=''; self.search_page=1
        self.search_term=str(form.get('query',self.search_term)).strip()[:200]
        self.submitted_query=self.search_term
        self.search_type='all' if self.submitted_query else str(form.get('kind','all'))
        if self.search_type not in ('all', *catalog.TYPES): self.search_type='all'
        self.search_active=True; self.has_more_results=True
        self._results={}; self.search_results=[]
        stamp=self._search_stamp()
        yield
        try:
            found,errors=await catalog.search(self.search_term,self.search_type)
            if stamp!=self._search_stamp(): return
            if errors:
                try:
                    cached=await self._call('GET','/media',params={'per_page':50},paginate=False)
                    if stamp!=self._search_stamp(): return
                    query=self.submitted_query
                    found.extend(item for item in rows(cached)
                        if (not query or catalog.title_score(query,item) > 0)
                        and self.search_type in ('all',item.get('media_type')))
                except APIError:
                    pass
            self._results={m['identity_key']:m for m in found}
            for m in self._media.values():
                if (not self.submitted_query or catalog.title_score(self.submitted_query,m) > 0) and self.search_type in ('all',m['media_type']):
                    self._results[m['identity_key']]=m
            self.search_results=[present_media(m) for m in catalog.relevant_results(self.submitted_query,list(self._results.values()))]
            self.has_more_results=bool(found) or bool(errors)
            self.notice=' '.join(errors) or ('Nenhum resultado encontrado.' if not self.search_results else '')
        finally:
            if stamp==self._search_stamp(): self.busy=False

    @rx.event
    async def more_results(self):
        if self.busy: return
        stamp=self._search_stamp()
        self.busy=True; yield
        try:
            found,errors=await catalog.search(self.submitted_query,self.search_type,self.search_page+1)
            if stamp!=self._search_stamp(): return
            self._results.update({m['identity_key']:m for m in found})
            self.search_results=[present_media(m) for m in catalog.relevant_results(self.submitted_query,list(self._results.values()))]
            if found or not errors: self.search_page+=1
            self.has_more_results=bool(found) or bool(errors)
            self.notice=' '.join(errors) or ('Não há mais resultados.' if not found else '')
        finally:
            if stamp==self._search_stamp(): self.busy=False

    @rx.event
    async def open_result(self, key: str):
        item=self._results.get(key)
        if not item: return
        try:
            internal_id=int(item.get('id') or 0)
        except (TypeError,ValueError):
            internal_id=0
        if internal_id>0: return rx.redirect('/obra/'+str(internal_id))
        return rx.redirect('/obra?'+urlencode({k:item[k] for k in ('external_source','external_id','media_type')}))

    @rx.event
    async def load_external_media(self):
        async for _ in self._media_updates(True): pass

    @rx.event
    async def load_media(self):
        async for _ in self._media_updates(False): pass

    async def _media_updates(self, external: bool):
        self._media_generation+=1
        generation=self._media_generation; route=self._route_stamp()
        def current():
            return generation==self._media_generation and route==self._route_stamp()
        self._saved_interaction={}
        self.interaction_saved=False; self.review_editor_open=True
        self.media_details_loading=False; self.media_interaction_loading=False; self.media_details_error=''
        self.notice=''; self._selected_raw={}
        self.recommendations=[]
        self.availability=[]
        self.community_reviews=[]
        self.selected={'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':'','backdrop':''}
        self.selected_status='planned'; self.selected_rating='0'; self.selected_review=''; self.selected_spoiler=False
        self.trailers=[]
        if external:
            params=self.router.url.query_parameters
            item=catalog.media(str(params.get('external_source','')),str(params.get('media_type','')),
                               str(params.get('external_id','')),'Sem título')
            detail=catalog.detail(item)
        else:
            identifier=self.router.url.path.rstrip('/').rsplit('/',1)[-1]
            if not identifier.isdigit(): return
            detail=self._call('GET',f'/media/{identifier}')
        try:
            detail_result,authenticated=await asyncio.gather(detail,self._validate_navigation_session(),return_exceptions=True)
            if not current(): return
            if isinstance(detail_result,APIError): raise detail_result
            if isinstance(detail_result,Exception):
                raise APIError('A fonte de catálogo está indisponível no momento.') from detail_result
            self._selected_raw=detail_result
            self.selected=present_media(self._selected_raw)
            self._restore_guest_rating()
            self.media_details_loading=True
            self.media_interaction_loading=authenticated is True
            yield
            async def personal():
                try:
                    if external: await self._load_external_interaction(authenticated is True)
                    else: await self._load_personal_interaction(str(identifier),authenticated is True)
                finally:
                    if current(): self.media_interaction_loading=False
            jobs={asyncio.create_task(job) for job in (
                personal(),
                self._prepare_default_lists(authenticated is True),self._load_trailers(),
                self._load_availability(),self._load_recommendations(),self._load_community_reviews())}
            try:
                while jobs:
                    done,jobs=await asyncio.wait(jobs,return_when=asyncio.FIRST_COMPLETED)
                    for job in done:
                        try: job.result()
                        except APIError as exc:
                            if current(): self.media_details_error=str(exc)
                    if not current(): return
                    yield
            finally:
                for job in jobs: job.cancel()
                if jobs: await asyncio.gather(*jobs,return_exceptions=True)
                if current(): self.media_details_loading=False
        except APIError as exc:
            if current(): self._failure(exc)

    async def _load_personal_interaction(self, identifier: str, authenticated: bool):
        stamp=self._media_stamp(); owner=self.user_id
        generation=self._interaction_generation
        self.selected_status='planned'; self.selected_rating='0'
        self.selected_review=''; self.selected_spoiler=False
        self.interaction_saved=False; self.review_editor_open=True
        self._saved_interaction={}
        if not authenticated:
            self._restore_guest_rating()
            return
        result=await self._call('GET','/interactions')
        if (stamp!=self._media_stamp() or owner!=self.user_id
                or generation!=self._interaction_generation): return
        for interaction in rows(result):
            if interaction.get('media_id')==int(identifier):
                self.selected_status=interaction['status']
                self.selected_rating=normalize_rating(interaction.get('rating') or 0)
                self.selected_review=str(interaction.get('review') or '')
                self.selected_spoiler=bool(interaction.get('spoiler'))
                self.interaction_saved=True
                self.review_editor_open=False
                self._saved_interaction=dict(user_id=self.user_id, media_id=int(identifier),
                    status=self.selected_status, rating=float(self.selected_rating),
                    review=self.selected_review, spoiler=self.selected_spoiler)
                break

    async def _load_external_interaction(self, authenticated: bool):
        if not authenticated:
            return
        self.selected_status='planned'; self.selected_rating='0'
        self.selected_review=''; self.selected_spoiler=False
        self.interaction_saved=False; self.review_editor_open=True
        self._saved_interaction={}
        stamp=self._media_stamp(); identity=self._selected_raw['identity_key']
        found=rows(await self._call('GET','/media',params={'identity_key':identity}))
        if stamp!=self._media_stamp():
            return
        matching=next((item for item in found if item.get('identity_key')==identity),None)
        if matching:
            mid=int(matching['id'])
            self._selected_raw['id']=mid
            self.selected['id']=str(mid)
            await self._load_personal_interaction(str(mid),True)

    async def _load_recommendations(self):
        stamp=self._media_stamp(); item=deepcopy(self._selected_raw)
        if not self._selected_raw.get('external_source'):
            self.recommendations=[]
            return
        try:
            result=[present_media(row) for row in await catalog.recommendations(item)]
            if stamp==self._media_stamp(): self.recommendations=result
        except APIError as exc:
            if stamp==self._media_stamp():
                self.recommendations=[]; self.media_details_error=str(exc)

    async def _load_community_reviews(self):
        stamp=self._media_stamp(); item=deepcopy(self._selected_raw)
        try:
            result=await catalog.reviews(item)
            if stamp==self._media_stamp(): self.community_reviews=result
        except APIError as exc:
            if stamp==self._media_stamp():
                self.community_reviews=[]; self.media_details_error=str(exc)

    async def _persist_selected(self) -> int:
        if not self._selected_raw: raise APIError('Escolha uma obra no catálogo.')
        stamp=self._media_stamp(); item=deepcopy(self._selected_raw)
        if self._selected_raw.get('id'):
            mid=int(self._selected_raw['id'])
            identity=self._selected_raw.get('identity_key')
            if not identity:
                return mid
            record=await self._call('GET',f'/media/{mid}')
            if stamp!=self._media_stamp(): raise APIError('A obra mudou. Confira a ficha novamente.',409)
            if not isinstance(record,dict): raise APIError('Não foi possível confirmar a identidade da obra.')
            if record.get('identity_key')==identity:
                return mid
            self._selected_raw['id']=0
            self.selected['id']=''
        payload={k:item[k] for k in ('external_source','external_id','media_type','title','description','cover_url','year','details')}
        result=await self._call('POST','/media',payload)
        if stamp!=self._media_stamp(): raise APIError('A obra mudou. Confira a ficha novamente.',409)
        self._selected_raw=result; self.selected=present_media(result)
        return int(result['id'])

    async def _ensure_default_lists(self):
        """Repair and create default lists when an account accesses its lists."""
        stamp=self._route_stamp()
        def check():
            if stamp!=self._route_stamp(): raise APIError('A página mudou. Atualize suas listas.',409)
        existing=rows(await self._call('GET','/lists'))
        check()
        by_title={str(item.get('title') or '').casefold():item for item in existing}
        for old in existing:
            old_title=str(old.get('title') or '').casefold()
            repair=BROKEN_DEFAULT_LISTS.get(old_title)
            if repair:
                check()
                title,description=repair
                result=await self._call('PUT',f"/lists/{int(old['id'])}",dict(
                    title=title,description=description,
                    is_public=old.get('is_public',True)))
                check()
                if not isinstance(result,dict) or not result.get('id'):
                    raise APIError('Não foi possível corrigir suas listas padrão.')
                by_title.pop(old_title,None)
                by_title[title.casefold()]=result
        for title,description in DEFAULT_MEDIA_LISTS:
            check()
            if title.casefold() not in by_title:
                result=await self._call('POST','/lists',dict(
                    title=title,description=description,is_public=True))
                check()
                if not isinstance(result,dict) or not result.get('id'):
                    raise APIError('Não foi possível preparar suas listas padrão.')
                by_title[title.casefold()]=result
        self.quick_lists=[dict(id=str(by_title[title.casefold()]['id']),title=title)
                          for title,_ in DEFAULT_MEDIA_LISTS]

    async def _prepare_default_lists(self, authenticated: bool):
        stamp=self._route_stamp()
        self.quick_lists=[]
        if not authenticated and not (self.user_id>0 and self._token()):
            return
        try:
            await self._ensure_default_lists()
        except APIError as exc:
            if stamp==self._route_stamp(): self._failure(exc)

    @rx.event
    async def save_interaction(self, form: dict):
        if self.interaction_saving: return
        self.interaction_saving=True
        try:
            return await self._save_interaction(form)
        finally:
            self.interaction_saving=False

    @rx.event
    async def submit_interaction(self, form: dict):
        if self.interaction_saving: return
        self.interaction_saving=True
        try:
            yield
            result=await self._save_interaction(form)
            if result: yield result
        finally:
            self.interaction_saving=False

    @rx.event
    def edit_interaction(self):
        if not self.interaction_saving:
            self.review_editor_open=True
            self.notice=''

    async def _save_interaction(self, form: dict):
        stamp=self._media_stamp()
        try:
            if form.get('media_key') is not None and form['media_key']!=self._selected_raw.get('identity_key'):
                self.notice='A obra mudou. Confira a ficha antes de enviar a avaliação.'
                return
            rating=float(normalize_rating(form.get('rating') or 0))
            status=form.get('status',self.selected_status)
            if status not in ('planned','in_progress','completed','dropped'):
                self.notice='Escolha um status válido.'; return
            payload=dict(media_id=int(self._selected_raw.get('id') or 0), status=status,
                rating=rating,review=str(form.get('review') or '').strip(),
                spoiler=form.get('spoiler') in ('on','true',True))
            if not payload['review']:
                self.notice='Escreva sua avaliação antes de enviar.'
                return
            if dict(user_id=self.user_id,**payload)==self._saved_interaction:
                self.selected_status=status; self.selected_rating=normalize_rating(rating)
                self.selected_review=payload['review']; self.selected_spoiler=payload['spoiler']
                self.interaction_saved=True; self.review_editor_open=False
                self.notice='Sua avaliação já está salva.'
                return
            if not await self._require_user(): return rx.redirect('/login')
            if stamp!=self._media_stamp(): return
            self.selected_status=status; self.selected_rating=normalize_rating(rating)
            self.selected_review=payload['review']; self.selected_spoiler=payload['spoiler']
            self._interaction_generation+=1
            mid=await self._persist_selected()
            if stamp!=self._media_stamp(): return
            payload['media_id']=mid
            try: await self._call('PUT','/interactions',payload)
            finally: self._interaction_generation+=1
            if stamp!=self._media_stamp(): return
            self._saved_interaction=dict(user_id=self.user_id,**payload)
            self.interaction_saved=True; self.review_editor_open=False
            self.notice='Sua avaliação foi salva com sucesso.'
        except ValueError:
            if stamp==self._media_stamp(): self.notice='Escolha uma nota de 0,5 a 5, em passos de 0,5, ou 0 para remover a nota.'
        except APIError as exc:
            if stamp==self._media_stamp(): self._failure(exc)

    @rx.event
    async def quick_add(self, status: str, rating: float = 0, list_title: str = ''):
        stamp=self._media_stamp()
        if not await self._require_user(): return rx.redirect('/login')
        if stamp!=self._media_stamp(): return
        try: rating=float(normalize_rating(rating))
        except ValueError:
            self.notice='Escolha uma nota em passos de 0,5.'
            return
        if status not in ('planned','completed') or not 0<=rating<=5:
            self.notice='Ação inválida.'
            return
        if rating>0 and not self.selected_review.strip():
            self.notice='Escreva sua avaliação antes de enviar uma nota.'
            return
        if list_title not in {title for title,_ in DEFAULT_MEDIA_LISTS}:
            self.notice='Escolha uma lista válida.'
            return
        try:
            await self._ensure_default_lists()
            if stamp!=self._media_stamp(): return
            mid=await self._persist_selected()
            if stamp!=self._media_stamp(): return
            await self._call('PUT','/interactions',dict(media_id=mid,status=status,rating=rating,
                review=self.selected_review,spoiler=self.selected_spoiler))
            if stamp!=self._media_stamp(): return
            self._saved_interaction={}
            target=next(item for item in self.quick_lists if item['title']==list_title)
            await self._call('POST',f"/lists/{int(target['id'])}/items",{'media_id':mid})
            if stamp!=self._media_stamp(): return
            self.selected_status=status
            if rating: self.selected_rating=normalize_rating(rating)
            self.notice=f'“{self.selected["title"]}” adicionada à lista {list_title}.'
        except APIError as exc:
            if stamp==self._media_stamp(): self._failure(exc)

    @rx.event
    async def load_library(self):
        self.library=[]; self.notice=''
        self._library_generation+=1
        self._library_cursor=0; self.library_error=''; self.library_has_more=False
        self.library_loading=False; self._library_retry_at=0.0
        self.library_paginated=os.getenv('LIBRARY_PAGINATION_ENABLED','false').lower()=='true'
        if not await self._require_user(navigation=True): return rx.redirect('/login')
        stamp=self._route_stamp()
        self._library_owner=self._token()
        if self.library_paginated:
            self.library_has_more=True
            await self._load_library_page()
            return
        try:
            await self._load_media()
            if stamp!=self._route_stamp(): return
            result=await self._call('GET','/interactions')
            if stamp==self._route_stamp(): self.library=[self._interaction(i) for i in rows(result)]
        except APIError as exc:
            if stamp==self._route_stamp(): self._failure(exc)

    async def _load_library_page(self):
        if self.library_loading or not self.library_has_more:
            return
        if self._token()!=self._library_owner or self.router.url.path.rstrip('/')!='/biblioteca':
            return
        if time.monotonic()<self._library_retry_at:
            return
        generation=self._library_generation
        token=self._token(); owner=self.user_id; cursor=self._library_cursor
        route=self.router.url.path
        def current():
            return (generation==self._library_generation and token==self._token()
                    and owner==self.user_id and route==self.router.url.path)
        self.library_loading=True; self.library_error=''
        try:
            data=await self._call('GET','/library',params={'after_id':cursor},paginate=False)
            if not current(): return
            if (not isinstance(data,dict) or not isinstance(data.get('items'),list)
                    or type(data.get('has_more')) is not bool or len(data['items'])>20):
                raise ValueError('Invalid library page')
            page=data['items']; previous=cursor; additions=[]
            seen={item['id'] for item in self.library}
            for item in page:
                if (not isinstance(item,dict) or type(item.get('id')) is not int
                        or item['id']<=previous or item.get('user_id')!=owner
                        or type(item.get('media_id')) is not int or item['media_id']<=0
                        or item.get('status') not in ('planned','in_progress','completed','dropped')):
                    raise ValueError('Invalid library item')
                previous=item['id']
                media=present_media({'id':item['media_id'],'title':item.get('media_title') or 'Obra indisponível',
                                     'media_type':item.get('media_type'),'cover_url':item.get('media_cover_url'),
                                     'year':item.get('media_year')})
                media.update(status={'planned':'Quero ver / ler','in_progress':'Em andamento',
                    'completed':'Concluído','dropped':'Abandonado'}[item['status']],
                    rating=str(item.get('rating') or 'Sem nota').replace('.',','),
                    review=str(item.get('review') or ''),spoiler=str(bool(item.get('spoiler'))))
                if media['id'] not in seen:
                    additions.append(media); seen.add(media['id'])
            if data['has_more'] and len(page)!=20:
                raise ValueError('Invalid library continuation')
            self.library=self.library+additions
            self._library_cursor=previous; self.library_has_more=data['has_more']
        except (ValueError,TypeError):
            if current(): self.library_error='Não foi possível carregar a biblioteca. Tente novamente.'
        except APIError as exc:
            if current():
                if exc.status in (401,403):
                    self._reset_personal()
                    self._failure(exc)
                else:
                    self.library_error=str(exc)
                    if exc.status==429:
                        self._library_retry_at=time.monotonic()+max(1,exc.retry_after or 30)
        finally:
            if generation==self._library_generation: self.library_loading=False

    @rx.event
    async def show_more_library(self):
        if not self.library_paginated:
            self.visible_count+=20
            return
        if self.library_loading: return
        # Yield feedback before doing the bounded read, keeping existing cards usable.
        self.library_loading=True
        yield
        self.library_loading=False
        await self._load_library_page()

    @rx.event
    async def load_community(self):
        stamp=self._route_stamp()
        self.following_ids=[]
        self.notice=''
        await self._validate_navigation_session()
        if stamp!=self._route_stamp(): return
        try: await self._load_people()
        except APIError as exc:
            if stamp==self._route_stamp(): self._failure(exc)
        if stamp!=self._route_stamp(): return
        if self.user_id:
            try:
                data=await self._call('GET',f'/profiles/{self.user_id}')
                if stamp!=self._route_stamp(): return
                self.following_ids=[str(f['followed_id']) for f in data['following']]
            except APIError as exc:
                if exc.status!=404: self._failure(exc)

    @rx.event
    async def load_profile(self):
        async for event in self._profile_updates():
            if event is not None: return event

    async def _profile_updates(self):
        self._profile_generation+=1
        generation=self._profile_generation
        self.notice=''; self.profile_activity=[]; self.followers=[]; self.following=[]
        self.profile_stats=''; self.following_ids=[]
        self.profile_counts={'followers':0,'following':0,'activities':0}
        self.profile_activity_error=''; self.profile_people_error=''
        self.profile_activity_loading=False; self.profile_people_loading=False
        self.profile={'user_id':'','username':'','display_name':'','bio':'','avatar_url':'','banner_url':''}
        await self._validate_navigation_session()
        if generation!=self._profile_generation: return
        route_id=self.router.url.path.rstrip('/').rsplit('/',1)[-1]
        uid=str(route_id if route_id.isdigit() else self.user_id)
        if not uid.isdigit() or int(uid)==0:
            yield rx.redirect('/login')
            return
        route=self.router.url.path
        token=self._token()
        def current():
            return (generation==self._profile_generation
                    and self.router.url.path==route and self._token()==token)
        self.profile={'user_id':uid,'username':'','display_name':'','bio':'','avatar_url':'','banner_url':''}
        try:
            data=await self._call('GET',f'/profiles/{uid}')
            if not current(): return
            self.profile={k:str(v or '') for k,v in data['profile'].items()}
            self.profile_counts={'followers':len(data['followers']),'following':len(data['following']),
                                 'activities':len(data['interactions'])}
            if int(uid)==self.user_id:
                self.following_ids=[str(f['followed_id']) for f in data['following']]
            completed=sum(i['status']=='completed' for i in data['interactions'])
            self.profile_stats=f"{completed} obras concluídas · {len(data['followers'])} seguidores · {len(data['following'])} seguindo"
        except APIError as exc:
            if not current(): return
            if exc.status==404 and int(uid)==self.user_id: self.notice='Complete seu perfil para participar da comunidade.'
            else: self._failure(exc)
            return
        self.profile_activity_loading=True; self.profile_people_loading=True
        # Publish identity and exact counts before requesting optional references.
        yield

        async def people():
            profiles=rows(await self._call('GET','/profiles'))
            own=data if int(uid)==self.user_id or not self.user_id else await self._call('GET',f'/profiles/{self.user_id}')
            return profiles,own

        jobs={asyncio.create_task(self._call('GET','/media')):'activity',
              asyncio.create_task(people()):'people'}
        try:
            while jobs:
                done,_=await asyncio.wait(jobs,return_when=asyncio.FIRST_COMPLETED)
                for job in done:
                    section=jobs.pop(job)
                    try:
                        result=job.result()
                        if not current(): continue
                        if section=='activity':
                            self._media={str(m['id']):m for m in rows(result)}
                            self.profile_activity=[self._interaction(i) for i in data['interactions']]
                        else:
                            profiles,own=result
                            self._profiles={str(p['user_id']):p for p in profiles}
                            self.followers=[self._person(i['follower_id']) for i in data['followers']]
                            self.following=[self._person(i['followed_id']) for i in data['following']]
                            self.following_ids=[str(f['followed_id']) for f in own['following']] if self.user_id else []
                    except APIError as exc:
                        if current():
                            if section=='activity': self.profile_activity_error=str(exc)
                            else: self.profile_people_error=str(exc)
                            if exc.status in (401,403): self._failure(exc)
                    finally:
                        if current():
                            if section=='activity': self.profile_activity_loading=False
                            else: self.profile_people_loading=False
                if current(): yield
        finally:
            for job in jobs: job.cancel()
            if jobs: await asyncio.gather(*jobs,return_exceptions=True)
            if current():
                self.profile_activity_loading=False; self.profile_people_loading=False

    @rx.event
    async def save_profile(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        username=str(form.get('username','')).strip().lower()
        if not re.fullmatch(r'[a-z0-9_]{3,30}',username): self.notice='Nome de usuário inválido.'; return
        avatar=str(form.get('avatar_url','')).strip()
        if avatar and not catalog.safe_url(avatar): self.notice='Use uma URL HTTPS para a foto.'; return
        try:
            result=await self._call('PUT','/profile',dict(username=username,display_name=str(form.get('display_name','')).strip(),
                bio=str(form.get('bio','')).strip(),avatar_url=avatar,banner_url=self.profile.get('banner_url','')))
            self.profile={k:str(v or '') for k,v in result.items()}; self.user_name=username; self.notice='Perfil atualizado.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def upload_profile_banner(self, files: list[rx.UploadFile]):
        """Save a validated profile banner and persist its public upload URL."""
        if not await self._require_user(): return rx.redirect('/login')
        if not self.owns_profile:
            self.notice='Somente o dono do perfil pode trocar o banner.'; return
        if len(files) != 1:
            self.notice='Selecione uma imagem para o banner.'; return
        file=files[0]
        content=await file.read()
        if len(content)>5*1024*1024:
            self.notice='A imagem deve ter no máximo 5 MB.'; return
        signatures=((b'\x89PNG\r\n\x1a\n','png'),(b'\xff\xd8\xff','jpg'),
                    (b'RIFF','webp'),(b'GIF87a','gif'),(b'GIF89a','gif'))
        extension=next((ext for signature,ext in signatures if content.startswith(signature)),None)
        if extension=='webp' and content[8:12]!=b'WEBP': extension=None
        if not extension:
            self.notice='Envie uma imagem PNG, JPG, WEBP ou GIF válida.'; return
        relative=f'profiles/{self.user_id}/banner-{uuid.uuid4().hex}.{extension}'
        path=rx.get_upload_dir()/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(content)
        banner_url=Endpoint.UPLOAD.get_url().rstrip('/')+'/'+relative
        try:
            result=await self._call('PUT','/profile',dict(username=self.profile['username'],
                display_name=self.profile['display_name'],bio=self.profile['bio'],
                avatar_url=self.profile['avatar_url'],banner_url=banner_url))
            self.profile={k:str(v or '') for k,v in result.items()}
            self.notice='Banner atualizado.'
        except APIError as exc:
            path.unlink(missing_ok=True)
            self._failure(exc)

    @rx.event
    async def follow(self, uid: str):
        if not await self._require_user(): return rx.redirect('/login')
        if uid==str(self.user_id): self.notice='Este é o seu perfil.'; return
        try:
            if uid in self.following_ids:
                await self._call('DELETE',f'/follows/{int(uid)}'); self.following_ids.remove(uid)
            else:
                await self._call('PUT',f'/follows/{int(uid)}'); self.following_ids.append(uid)
            self.notice='Conexões atualizadas.'
        except APIError as exc: self._failure(exc)

    async def _refresh_posts(self):
        stamp=self._route_stamp()
        data=rows(await self._call('GET','/feed',params={'per_page':20}))
        if stamp!=self._route_stamp(): return
        own=rows(await self._call('GET','/posts',params={'user_id':self.user_id,'per_page':20}))
        if stamp!=self._route_stamp(): return
        combined={str(p['id']):p for p in data+own}
        try:
            liked=[str(i['post_id']) for i in rows(await self._call('GET','/likes'))]
        except APIError as exc:
            if exc.status != 404:
                raise
            # Older workspaces have no /likes route. Resolve like state only
            # when a user opens a discussion or taps its like button.
            liked=[]
        if stamp!=self._route_stamp(): return
        self.liked_posts=liked; self.posts=[]
        def post_timestamp(post):
            value=post.get('created_at') or 0
            try:
                return float(value.timestamp()) if hasattr(value,'timestamp') else float(value)
            except (TypeError,ValueError):
                return 0.0
        for p in sorted(combined.values(),key=post_timestamp,reverse=True):
            person=self._person(p['user_id']); m=self._media.get(str(p.get('media_id')), {})
            timestamp=post_timestamp(p)
            # Xano timestamps are milliseconds; accept seconds from legacy fixtures/workspaces too.
            published=datetime.fromtimestamp(timestamp / (1000 if timestamp > 10_000_000_000 else 1),tz=timezone.utc)
            image=p.get('image') or p.get('image_url') or p.get('image_file') or ''
            if isinstance(image,dict):
                image=image.get('url') or image.get('path') or image.get('file') or ''
                if isinstance(image,dict):
                    image=image.get('url') or image.get('path') or ''
            if isinstance(image,str) and (image.startswith('/') or image.startswith('vault/')):
                endpoint=urlsplit(base_url('social'))
                image=f'{endpoint.scheme}://{endpoint.netloc}/'+image.lstrip('/')
            self.posts.append(dict(id=str(p['id']),user_id=str(p['user_id']),author=person['display_name'],
                avatar=person['avatar_url'],media_cover=catalog.safe_url(m.get('cover_url')),
                body=str(p.get('body') or ''),published_at=published.strftime('%d/%m/%Y'),spoiler=str(bool(p.get('spoiler'))),media_id=str(p.get('media_id') or 0),media_title=m.get('title',''),
                image_url=catalog.safe_url(image),likes_count=str(p.get('likes_count','')),comments_count=str(p.get('comments_count',''))))

    @rx.event
    async def load_feed(self):
        stamp=self._route_stamp()
        self.posts=[]; self.comments=[]; self.notice=''
        if not await self._require_user(navigation=True): return rx.redirect('/login')
        if stamp!=self._route_stamp(): return
        try:
            await self._load_reference()
            if stamp==self._route_stamp(): await self._refresh_posts()
        except APIError as exc:
            if stamp==self._route_stamp(): self._failure(exc)

    @rx.event
    def edit_post(self, pid: str):
        if self.post_saving: return
        for p in self.posts:
            if p['id']==pid and p['user_id']==str(self.user_id):
                self.post_editor_token=uuid.uuid4().hex
                self.post_editor_open=True
                self.edit_post_id=pid; self.edit_post_body=p['body']; self.edit_post_media=p['media_id']; self.edit_post_spoiler=p['spoiler']=='True'
                self._post_media_raw=deepcopy(self._media.get(p['media_id'],
                    {'id':int(p['media_id']),'title':p.get('media_title','')})) if p['media_id']!='0' else {}
                if self._post_media_raw:
                    item=present_media(self._post_media_raw)
                    self.post_media_selected={k:item[k] for k in ('id','key','title','cover')}
                else:
                    self.post_media_selected={'id':'','key':'','title':'','cover':''}
                self.post_existing_image_url=p.get('image_url','')

    @rx.event
    def cancel_post(self):
        self.post_editor_open=False
        self.edit_post_id=''; self.edit_post_body=''; self.edit_post_media='0'; self.edit_post_spoiler=False
        self.post_editor_token=''
        self.post_media_query=''; self.post_media_results=[]; self.post_media_searching=False
        self._post_media_candidates={}; self._post_media_raw={}
        self.post_media_selected={'id':'','key':'','title':'','cover':''}
        self.post_existing_image_url=''
        self._discard_post_upload()

    @rx.event
    async def save_post(self, form: dict):
        if self.post_saving: return
        post_id=str(form.get('post_id',self.edit_post_id)).strip()
        editor_token=str(form.get('editor_token',self.post_editor_token))
        if post_id!=self.edit_post_id or editor_token!=self.post_editor_token:
            self.notice='A publicação mudou. Abra a edição novamente.'
            return
        owner=self.user_id; token=self._token()
        self.post_saving=True
        yield
        try:
            if not await self._require_user():
                yield rx.redirect('/login')
                return
            if self.user_id!=owner or self._token()!=token or self.edit_post_id!=post_id or self.post_editor_token!=editor_token:
                self.notice='A sessão ou a publicação mudou. Abra o editor novamente.'
                return
            media_id=await self._persist_post_media()
            if self.user_id!=owner or self._token()!=token or self.edit_post_id!=post_id or self.post_editor_token!=editor_token:
                self.notice='A sessão ou a publicação mudou. Abra o editor novamente.'
                return
            method='PUT' if post_id else 'POST'
            path='/posts'+('/'+post_id if post_id else '')
            payload=dict(body=str(form.get('body','')).strip(),media_id=media_id,spoiler=form.get('spoiler')=='on')
            if self._post_image_path:
                image_path=Path(self._post_image_path)
                form_data={key:str(value).lower() if isinstance(value,bool) else str(value)
                           for key,value in payload.items()}
                await upload_file(path,method=method,token=self._token(),data=form_data,field='image_upload',
                    filename=image_path.name,content=image_path.read_bytes(),mime=self.post_image_mime)
            else:
                await self._call(method,path,payload)
            self.cancel_post(); await self._refresh_posts(); self.notice='Publicação salva.'
        except (ValueError,TypeError): self.notice='Selecione uma obra válida.'
        except APIError as exc: self._failure(exc)
        finally: self.post_saving=False

    @rx.event
    async def remove_post(self, pid: str):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            await self._call('DELETE',f'/posts/{int(pid)}'); self.comments=[]; self.selected_post=''
            await self._refresh_posts(); self.notice='Publicação removida.'
        except APIError as exc: self._failure(exc)

    @rx.event
    def open_report(self, target_type: str, target_id: str):
        if not self.is_authenticated:
            return rx.redirect('/login')
        target_id = str(target_id).strip()
        external_media = target_type == 'media' and bool(self._selected_raw)
        if target_type not in ('post', 'comment', 'profile', 'media') or (not target_id and not external_media):
            self.notice = 'Este conteúdo não pode ser denunciado.'
            return
        self.report_target_type = target_type
        self.report_target_id = target_id or '0'
        self.report_reason = 'spam'
        self.report_description = ''
        self.report_error = ''
        self.report_dialog_open = True

    @rx.event
    def close_report(self):
        if not self.report_sending:
            self.report_dialog_open = False
            self.report_target_type = ''
            self.report_target_id = ''
            self.report_description = ''
            self.report_error = ''

    @rx.event
    def set_report_reason(self, value: str):
        if value in ('spam', 'harassment', 'inappropriate', 'other'):
            self.report_reason = value

    @rx.event
    def set_report_description(self, value: str):
        self.report_description = value[:2000]

    @rx.event
    async def submit_report(self, form: dict):
        if self.report_sending or not self.report_target_type or not self.report_target_id:
            return
        remaining = math.ceil(self._report_retry_at - time.monotonic())
        if remaining > 0:
            self.report_error = f'Aguarde {remaining} segundos antes de tentar enviar novamente.'
            return
        reason = str(form.get('reason', self.report_reason))
        description = str(form.get('description', self.report_description) or '').strip()[:2000]
        self.report_description = description
        if not description:
            self.report_error = 'Escreva os detalhes da denúncia antes de enviar.'
            return
        if reason not in ('spam', 'harassment', 'inappropriate', 'other'):
            self.report_error = 'Selecione um motivo válido.'
            return
        self.report_reason = reason
        self.report_sending = True
        self.report_error = ''
        self.notice = ''
        yield
        try:
            # The protected POST validates the session in Xano. Avoid an extra
            # auth/me request for an already identified member at every submission.
            if not self.is_authenticated:
                yield rx.redirect('/login')
                return
            if self.report_target_type == 'media' and self.report_target_id in ('0', ''):
                self.report_target_id = str(await self._persist_selected())
            await self._call('POST', '/reports', data={
                'target_type': self.report_target_type,
                'target_id': self.report_target_id,
                'reason': reason,
                'description': description,
            }, paginate=False)
            self.report_sending = False
            self.close_report()
            self.notice = 'Report enviado para análise. O conteúdo não foi alterado.'
        except APIError as exc:
            if exc.status == 429:
                wait = max(1, exc.retry_after or 30)
                self._report_retry_at = time.monotonic() + wait
                self.report_error = f'Muitas solicitações. Aguarde {wait} segundos para reenviar. Seus dados foram mantidos.'
            else:
                self.report_error = str(exc)
            self._failure(exc)
        finally:
            self.report_sending = False

    @rx.event
    async def discussion(self, pid: str):
        if self.selected_post!=pid:
            self.edit_comment_id=''; self.edit_comment_body=''
        self.comments=[]
        try:
            data=await self._call('GET',f'/posts/{int(pid)}/discussion'); self.selected_post=pid
            self.comments=[dict(id=str(c['id']),user_id=str(c['user_id']),body=c['body'],author=self._person(c['user_id'])['display_name']) for c in data['comments']]
            self._set_post_counts(pid, len(data['likes']), len(data['comments']))
            if any(l['user_id']==self.user_id for l in data['likes']):
                if pid not in self.liked_posts: self.liked_posts.append(pid)
            elif pid in self.liked_posts: self.liked_posts.remove(pid)
            self.notice=f"{len(data['likes'])} curtidas · {len(data['comments'])} comentários"
        except APIError as exc: self._failure(exc)

    def _set_post_counts(self, pid: str, likes: int, comments: int):
        self.posts=[dict(post, likes_count=str(likes), comments_count=str(comments))
                    if post['id']==pid else post for post in self.posts]

    @rx.event
    def close_discussion(self):
        self.selected_post=''
        self.comments=[]
        self.edit_comment_id=''
        self.edit_comment_body=''

    @rx.event
    async def like(self, pid: str):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            data=await self._call('GET',f'/posts/{int(pid)}/discussion')
            already_liked=any(like.get('user_id')==self.user_id for like in data['likes'])
            await self._call('DELETE' if already_liked else 'PUT',f'/posts/{int(pid)}/like')
            if already_liked:
                if pid in self.liked_posts: self.liked_posts.remove(pid)
            elif pid not in self.liked_posts:
                self.liked_posts.append(pid)
            count=len(data['likes'])-int(already_liked)+int(not already_liked)
            self._set_post_counts(pid, count, len(data['comments']))
            self.notice=f'{count} curtidas Â· {len(data["comments"])} comentÃ¡rios'
        except APIError as exc: self._failure(exc)

    @rx.event
    def edit_comment(self, cid: str):
        for c in self.comments:
            if c['id']==cid and c['user_id']==str(self.user_id): self.edit_comment_id=cid; self.edit_comment_body=c['body']

    @rx.event
    async def save_comment(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        body=str(form.get('body','')).strip()
        if not body:
            self.notice='Escreva um comentÃ¡rio antes de salvar.'
            return
        try:
            await self._call('PUT' if self.edit_comment_id else 'POST','/comments'+('/'+self.edit_comment_id if self.edit_comment_id else ''),
                dict(post_id=int(self.selected_post),body=body))
            self.edit_comment_id=''; self.edit_comment_body=''; await self.discussion(self.selected_post)
        except (ValueError,TypeError): self.notice='Escolha uma publicação.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def remove_comment(self, cid: str):
        if not await self._require_user(): return rx.redirect('/login')
        try: await self._call('DELETE',f'/comments/{int(cid)}'); await self.discussion(self.selected_post)
        except APIError as exc: self._failure(exc)

    @rx.event
    async def load_lists(self):
        stamp=self._route_stamp()
        self.notice=''; self.lists=[]; self.list_items=[]
        self.selected_list={'id':'','title':'','description':'','user_id':'','is_public':'True'}
        await self._validate_navigation_session()
        if stamp!=self._route_stamp(): return
        try:
            await self._load_media()
            if stamp!=self._route_stamp(): return
            if self.user_id: await self._ensure_default_lists()
            if stamp!=self._route_stamp(): return
            public=rows(await self._call('GET','/lists/public'))
            if stamp!=self._route_stamp(): return
            own=rows(await self._call('GET','/lists')) if self.user_id else []
            if stamp!=self._route_stamp(): return
            combined={str(i['id']):i for i in public+own}
            self.lists=[{k:str(v if v is not None else '') for k,v in i.items()} for i in combined.values()]
        except APIError as exc:
            if stamp==self._route_stamp(): self._failure(exc)

    @rx.event
    def new_list(self):
        self._reset_list_search()
        self.list_editor_open=True
        self.selected_list=dict(id='',title='',description='',user_id=str(self.user_id),is_public='True'); self.list_items=[]

    @rx.event
    async def open_list(self, lid: str):
        self._reset_list_search()
        stamp=self._route_stamp()
        self.list_items=[]; item=next((i for i in self.lists if i['id']==lid),None)
        if not item: return
        self.selected_list=item
        try:
            path=f'/lists/{int(lid)}/items' if self.user_id else f'/lists/public/{int(lid)}/items'
            items=rows(await self._call('GET',path))
            if stamp!=self._route_stamp() or self.selected_list.get('id')!=lid: return
            self.list_items=[present_media(self._media.get(str(i['media_id']),{'id':i['media_id']})) for i in items]
        except APIError as exc:
            if stamp==self._route_stamp() and self.selected_list.get('id')==lid: self._failure(exc)

    @rx.event
    async def save_list(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        if not str(form.get('title','')).strip(): self.notice='Informe um título para a lista.'; return
        lid=self.selected_list.get('id','')
        try:
            result=await self._call('PUT' if lid else 'POST','/lists'+('/'+lid if lid else ''),dict(
                title=str(form.get('title','')).strip(),description=str(form.get('description','')).strip(),is_public=form.get('is_public')=='on'))
            await self.load_lists(); await self.open_list(str(result['id'])); self.notice='Lista salva.'; self.list_editor_open=False
        except APIError as exc: self._failure(exc)

    @rx.event
    async def remove_list(self):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            await self._call('DELETE','/lists/'+str(int(self.selected_list['id'])))
            self.new_list(); await self.load_lists(); self.notice='Lista removida.'; self.list_editor_open=False
        except (ValueError,KeyError): self.notice='Escolha uma lista.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def add_list_item(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        if not self.owns_list:
            self.notice='Escolha uma lista sua.'
            return
        try:
            lid=str(int(self.selected_list['id']))
            await self._call('POST',f'/lists/{lid}/items',{'media_id':int(form.get('media_id') or 0)})
            await self.open_list(lid); self.notice='Obra adicionada.'
        except (ValueError,KeyError): self.notice='Salve a lista e escolha uma obra.'
        except APIError as exc: self._failure(exc)

    def _reset_list_search(self):
        self._list_search_generation+=1
        self.list_media_query=''; self.list_media_results=[]; self._list_media_candidates={}
        self.list_media_searching=False; self.list_media_error=''

    @rx.event
    def update_list_media_query(self, value: str):
        self._list_search_generation+=1
        self.list_media_query=value[:160]
        self.list_media_results=[]; self._list_media_candidates={}; self.list_media_error=''
        self.list_media_searching=False

    @rx.event
    async def search_list_media(self):
        if not self.owns_list: return
        query=self.list_media_query.strip()
        if not query:
            self.list_media_error='Digite o nome de uma obra para pesquisar.'
            return
        self._list_search_generation+=1
        generation=self._list_search_generation
        context=(self._route_stamp(),self.selected_list.get('id'),self.user_id)
        self.list_media_searching=True; self.list_media_error=''; self.list_media_results=[]
        self._list_media_candidates={}
        yield
        def current():
            return generation==self._list_search_generation and context==(self._route_stamp(),self.selected_list.get('id'),self.user_id)
        try:
            found,errors=await catalog.search(query,'all')
            if not current(): return
            candidates={str(m.get('identity_key') or 'local:'+str(m['id'])):deepcopy(m)
                        for m in found+list(self._media.values())
                        if (m.get('identity_key') or m.get('id')) and catalog.title_score(query,m)>0}
            ranked=catalog.relevant_results(query,list(candidates.values()))[:24]
            self._list_media_candidates={str(m.get('identity_key') or 'local:'+str(m['id'])):m for m in ranked}
            self.list_media_results=[]
            for key,item in self._list_media_candidates.items():
                shown=present_media(item); shown['key']=key
                self.list_media_results.append(shown)
            self.list_media_error=' '.join(errors) or ('Nenhuma obra encontrada.' if not ranked else '')
        except APIError as exc:
            if current(): self.list_media_error=str(exc)
        finally:
            if current(): self.list_media_searching=False

    async def _persist_list_candidate(self, item: dict) -> dict:
        item=deepcopy(item)
        if item.get('id'): return item
        payload={k:item[k] for k in ('external_source','external_id','media_type','title','description','cover_url','year','details') if k in item}
        result=await self._call('POST','/media',payload)
        if not isinstance(result,dict) or not result.get('id'):
            raise APIError('Não foi possível identificar a obra.')
        if item.get('identity_key') and result.get('identity_key')!=item['identity_key']:
            raise APIError('A identidade da obra não corresponde ao resultado.',409)
        return result

    @rx.event
    async def add_list_result(self, key: str):
        if self.list_item_saving or not self.owns_list: return
        item=deepcopy(self._list_media_candidates.get(key) or {})
        if not item: return
        lid=self.selected_list.get('id'); owner=self.user_id; token=self._token()
        generation=self._list_search_generation
        self.list_item_saving=True
        yield
        def current():
            return owner==self.user_id and token==self._token() and lid==self.selected_list.get('id') and generation==self._list_search_generation and self.owns_list
        try:
            if not await self._require_user():
                yield rx.redirect('/login'); return
            if not current(): return
            record=await self._persist_list_candidate(item)
            if not current(): return
            mid=str(record['id'])
            if any(row['id']==mid for row in self.list_items):
                self.notice='Esta obra já está na lista.'; return
            await self._call('POST',f'/lists/{int(lid)}/items',{'media_id':int(mid)})
            if not current(): return
            self._media[mid]=record
            self._list_media_candidates[key]=record
            self.list_items=[*self.list_items,present_media(record)]
            self.notice='Obra adicionada à lista.'
        except (ValueError,KeyError):
            if current(): self.list_media_error='Selecione uma obra e uma lista válidas.'
        except APIError as exc:
            if current(): self.list_media_error=str(exc); self._failure(exc)
        finally:
            self.list_item_saving=False

    @rx.event
    def close_media_lists(self):
        if not self.list_item_saving:
            self.media_list_open=False; self.media_list_options=[]; self.media_list_target=''; self.media_list_error=''

    @rx.event
    def select_media_list(self, value: str):
        if not self.list_item_saving and any(row['id']==value for row in self.media_list_options):
            self.media_list_target=value

    @rx.event
    async def open_media_lists(self):
        stamp=self._media_stamp()
        if not await self._require_user():
            yield rx.redirect('/login'); return
        if stamp!=self._media_stamp(): return
        self.media_list_open=True; self.media_list_loading=True
        self.media_list_options=[]; self.media_list_target=''; self.media_list_error=''
        yield
        try:
            found=rows(await self._call('GET','/lists'))
            if stamp!=self._media_stamp() or not self.media_list_open: return
            self.media_list_options=[{'id':str(row['id']),'title':str(row['title']),
                                      'is_public':str(bool(row.get('is_public')))}
                                     for row in found if str(row.get('user_id'))==str(self.user_id)]
            if not self.media_list_options: self.media_list_error='Você ainda não tem listas. Crie uma em Minhas listas.'
        except APIError as exc:
            if stamp==self._media_stamp(): self.media_list_error=str(exc)
        finally:
            if stamp==self._media_stamp(): self.media_list_loading=False

    @rx.event
    async def add_current_media_to_list(self):
        if self.list_item_saving: return
        lid=self.media_list_target
        if not any(row['id']==lid for row in self.media_list_options):
            self.media_list_error='Escolha uma lista sua.'; return
        stamp=self._media_stamp(); owner=self.user_id
        self.list_item_saving=True
        yield
        def current():
            return stamp==self._media_stamp() and owner==self.user_id and self.media_list_open and self.media_list_target==lid
        try:
            if not await self._require_user():
                yield rx.redirect('/login'); return
            if not current(): return
            mid=await self._persist_selected()
            if not current(): return
            await self._call('POST',f'/lists/{int(lid)}/items',{'media_id':mid})
            if not current(): return
            self.notice='Obra adicionada à lista.'
            self.media_list_open=False
        except (ValueError,KeyError):
            if current(): self.media_list_error='Escolha uma lista válida.'
        except APIError as exc:
            if current(): self.media_list_error=str(exc); self._failure(exc)
        finally:
            self.list_item_saving=False

    @rx.event
    async def remove_list_item(self, mid: str):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            lid=str(int(self.selected_list['id']))
            await self._call('DELETE',f'/lists/{lid}/items/{int(mid)}'); await self.open_list(lid)
        except APIError as exc: self._failure(exc)
