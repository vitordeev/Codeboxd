"""Social UI state backed by Xano endpoints."""
import asyncio
import json
import re
from urllib.parse import urlencode
from datetime import datetime, timezone
import reflex as rx
from .session import SessionState
from ..services import catalog
from ..services.api import APIError, request, rows


def present_media(m: dict) -> dict[str,str]:
    details=m.get('details') or {}
    return {k:str(v or '') for k,v in dict(id=m.get('id',0),key=m.get('identity_key',''),
        title=m.get('title','Sem título'),kind=catalog.TYPES.get(m.get('media_type'),'Mídia'),
        year=m.get('year',''),cover=catalog.safe_url(m.get('cover_url')),description=m.get('description',''),
        backdrop=catalog.safe_url(m.get('backdrop_url')),
        source=m.get('external_source',''),external_id=m.get('external_id',''),
        details=' · '.join(f'{k}: {v}' for k,v in details.items()) if isinstance(details,dict) else '').items()}


class SocialState(SessionState):
    notice: str = ''
    busy: bool = False
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
    popular_exhausted: list[str] = []
    _popular_pages: dict[str,int] = {'movie':1, 'series':1}
    catalog_items: list[dict[str,str]] = []
    selected: dict[str,str] = {'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':'','backdrop':''}
    recommendations: list[dict[str,str]] = []
    community_reviews: list[dict[str,str]] = []
    selected_status: str = 'planned'
    selected_rating: str = '0'
    guest_ratings: str = rx.LocalStorage('{}', name='codeboxd_guest_ratings', sync=True)
    trailers: list[dict[str,str]] = []
    selected_review: str = ''
    selected_spoiler: bool = False
    library: list[dict[str,str]] = []
    people: list[dict[str,str]] = []
    profile: dict[str,str] = {'user_id':'','username':'','display_name':'','bio':'','avatar_url':''}
    profile_stats: str = ''
    profile_activity: list[dict[str,str]] = []
    followers: list[dict[str,str]] = []
    following: list[dict[str,str]] = []
    following_ids: list[str] = []
    posts: list[dict[str,str]] = []
    comments: list[dict[str,str]] = []
    selected_post: str = ''
    liked_posts: list[str] = []
    edit_post_id: str = ''
    edit_post_body: str = ''
    edit_post_media: str = '0'
    edit_post_spoiler: bool = False
    edit_comment_id: str = ''
    edit_comment_body: str = ''
    lists: list[dict[str,str]] = []
    list_items: list[dict[str,str]] = []
    selected_list: dict[str,str] = {'id':'','title':'','description':'','user_id':'','is_public':'True'}
    _media: dict[str,dict] = {}
    _results: dict[str,dict] = {}
    _selected_raw: dict = {}
    _profiles: dict[str,dict] = {}
    _identity: int = 0
    visible_count: int = 20
    post_editor_open: bool = False
    list_editor_open: bool = False

    @rx.event
    def set_post_editor_open(self, value: bool):
        if not value or self.is_authenticated:
            self.post_editor_open = value
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
        if value in ('1','2','3','4','5'):
            self.selected_rating=value
            if not self.is_authenticated and self.selected.get('key'):
                try: ratings=json.loads(self.guest_ratings or '{}')
                except (TypeError,ValueError): ratings={}
                if not isinstance(ratings,dict): ratings={}
                ratings[self.selected['key']]=value
                self.guest_ratings=json.dumps(ratings,separators=(',',':'))
                self.notice='Nota salva somente neste navegador. Entre para publicar uma crítica e organizar suas obras.'

    def _restore_guest_rating(self):
        if self.is_authenticated or not self.selected.get('key'): return
        try: ratings=json.loads(self.guest_ratings or '{}')
        except (TypeError,ValueError): return
        value=ratings.get(self.selected['key']) if isinstance(ratings,dict) else None
        if str(value) in ('1','2','3','4','5'): self.selected_rating=str(value)

    async def _load_trailers(self):
        self.trailers=[]
        try: self.trailers=await catalog.trailers(self._selected_raw)
        except APIError: pass

    @rx.event
    def new_post(self):
        if not self.is_authenticated: return rx.redirect('/login')
        self.cancel_post()
        self.post_editor_open = True

    @rx.var
    def suggested_people(self) -> list[dict[str,str]]:
        return [p for p in self.people if p['user_id'] != str(self.user_id)][:5]

    @rx.var
    def visible_library(self) -> list[dict[str,str]]:
        return self.library[:self.visible_count]

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
        self.visible_count=20; self.busy=True; self.notice=''
        yield
        try:
            loaders={'home':self.load_home,'library':self.load_library,'community':self.load_community,
                     'profile':self.load_profile,'feed':self.load_feed,'lists':self.load_lists,
                     'media':self.load_media,'external':self.load_external_media}
            if section in loaders:
                result=await loaders[section]()
                if result: yield result
        finally:
            self.busy=False

    def _reset_personal(self):
        self.post_editor_open=False; self.list_editor_open=False
        self.library=[]; self.posts=[]; self.comments=[]; self.lists=[]; self.list_items=[]
        self.following_ids=[]; self.liked_posts=[]; self.selected_post=''
        self.edit_post_id=''; self.edit_post_body=''; self.edit_post_media='0'; self.edit_post_spoiler=False
        self.edit_comment_id=''; self.edit_comment_body=''
        self.selected_review=''; self.selected_rating='0'; self.selected_status='planned'; self.selected_spoiler=False
        self.trailers=[]
        self.selected_list={'id':'','title':'','description':'','user_id':'','is_public':'True'}
        self.profile={'user_id':'','username':'','display_name':'','bio':'','avatar_url':''}
        self.profile_activity=[]; self.profile_stats=''; self.followers=[]; self.following=[]

    async def _validate_session(self) -> bool:
        valid = await super()._validate_session()
        if self._identity != self.user_id or not valid:
            self._reset_personal()
        self._identity = self.user_id
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
        result=await request(method,path,token=self._token(),data=data,params=params)
        if method!='GET' or not paginate: return result
        # Read bounded API pages without truncating references or profile statistics.
        keys=[key for key,value in result.items() if isinstance(value,list)] if isinstance(result,dict) else []
        page=1
        while (isinstance(result,list) and len(result)==page*100) or any(len(result[key])==page*100 for key in keys):
            page+=1
            if page>100: raise APIError('Há muitos registros para esta consulta. Tente novamente mais tarde.')
            batch=await request(method,path,token=self._token(),params={**(params or {}),'page':page,'per_page':100})
            if isinstance(result,list): result.extend(rows(batch))
            else:
                for key in keys: result[key].extend(rows(batch[key]))
        return result

    async def _require_user(self) -> bool:
        if await self._validate_session(): return True
        # A transient auth-service failure is not a logout. Keep the current
        # navigation usable; any protected write is still authorized by Xano.
        if self.user_id > 0 and self._token(): return True
        self.notice=self.error_message or 'Entre na sua conta para continuar.'
        return False

    async def _load_media(self, per_page: int | None = None):
        params={'per_page':per_page} if per_page else None
        self._media={str(m['id']):m for m in rows(await self._call('GET','/media',params=params))}
        self.catalog_items=[present_media(m) for m in self._media.values()]

    async def _load_people(self):
        self._profiles={str(p['user_id']):p for p in rows(await self._call('GET','/profiles'))}
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
            rating=str(i.get('rating') or 'Sem nota'),review=str(i.get('review') or ''),spoiler=str(bool(i.get('spoiler'))))
        return result

    @rx.event
    async def load_home(self):
        self.notice=''
        async def popular(kind):
            attribute = 'popular_movies' if kind == 'movie' else 'popular_series'
            if getattr(self, attribute): return
            items, errors = await catalog.search('', kind)
            setattr(self, attribute, [present_media(m) for m in items])
            if kind == 'movie': self.featured_items = self.popular_movies[:2]
            if errors: self.notice = ' '.join(filter(None, [self.notice, *errors]))

        async def community():
            try: await self._load_media(per_page=20)
            except APIError as exc: self._failure(exc)

        await asyncio.gather(self._validate_session(), community(), popular('movie'), popular('series'))

    @rx.event
    async def more_popular(self, kind: str):
        if self.busy or kind not in ('movie', 'series') or kind in self.popular_exhausted: return
        self.busy=True
        yield
        try:
            page=self._popular_pages[kind]+1
            found,errors=await catalog.search('',kind,page)
            attribute='popular_movies' if kind=='movie' else 'popular_series'
            existing={item['key']:item for item in getattr(self,attribute)}
            existing.update({item['identity_key']:present_media(item) for item in found})
            setattr(self,attribute,list(existing.values()))
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
        yield
        try:
            found,errors=await catalog.search(self.search_term,self.search_type)
            if errors and self.search_term:
                try:
                    cached=await self._call('GET','/media',params={'per_page':50},paginate=False)
                    query=self.submitted_query
                    found.extend(item for item in rows(cached)
                        if catalog.title_score(query,item) > 0
                        and self.search_type in ('all',item.get('media_type')))
                except APIError:
                    pass
            self._results={m['identity_key']:m for m in found}
            for m in self._media.values():
                if catalog.title_score(self.submitted_query,m) > 0 and self.search_type in ('all',m['media_type']):
                    self._results[m['identity_key']]=m
            self.search_results=[present_media(m) for m in catalog.relevant_results(self.submitted_query,list(self._results.values()))]
            self.has_more_results=bool(found) or bool(errors)
            self.notice=' '.join(errors) or ('Nenhum resultado encontrado.' if not self.search_results else '')
        finally: self.busy=False

    @rx.event
    async def more_results(self):
        if self.busy: return
        self.busy=True; yield
        try:
            found,errors=await catalog.search(self.submitted_query,self.search_type,self.search_page+1)
            self._results.update({m['identity_key']:m for m in found})
            self.search_results=[present_media(m) for m in catalog.relevant_results(self.submitted_query,list(self._results.values()))]
            if found or not errors: self.search_page+=1
            self.has_more_results=bool(found) or bool(errors)
            self.notice=' '.join(errors) or ('Não há mais resultados.' if not found else '')
        finally: self.busy=False

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
        self.notice=''; self._selected_raw={}
        self.recommendations=[]
        self.community_reviews=[]
        self.selected={'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':'','backdrop':''}
        self.selected_status='planned'; self.selected_rating='0'; self.selected_review=''; self.selected_spoiler=False
        self.trailers=[]
        params=self.router.url.query_parameters
        item=catalog.media(str(params.get('external_source','')),str(params.get('media_type','')),
                           str(params.get('external_id','')),'Sem título')
        try:
            detail_result,_=await asyncio.gather(catalog.detail(item),self._validate_session(),return_exceptions=True)
            if isinstance(detail_result,APIError): raise detail_result
            if isinstance(detail_result,Exception):
                raise APIError('A fonte de catálogo está indisponível no momento.') from detail_result
            self._selected_raw=detail_result
            self.selected=present_media(self._selected_raw)
            self._restore_guest_rating()
            await asyncio.gather(self._load_trailers(),self._load_recommendations(),self._load_community_reviews())
        except APIError as exc: self._failure(exc)

    @rx.event
    async def load_media(self):
        identifier=self.router.url.path.rstrip('/').rsplit('/',1)[-1]
        self._selected_raw={}
        self.recommendations=[]
        self.community_reviews=[]
        self.selected={'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':'','backdrop':''}
        if not str(identifier).isdigit(): return
        self.notice=''; self.selected_status='planned'; self.selected_rating='0'; self.selected_review=''; self.selected_spoiler=False
        self.trailers=[]
        try:
            self._selected_raw,authenticated=await asyncio.gather(
                self._call('GET',f'/media/{identifier}'),self._validate_session())
            self.selected=present_media(self._selected_raw)
            await asyncio.gather(self._load_trailers(),self._load_recommendations(),
                self._load_community_reviews(),self._load_personal_interaction(str(identifier),authenticated))
        except APIError as exc:
            self.selected={'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':'','backdrop':''}; self._failure(exc)

    async def _load_personal_interaction(self, identifier: str, authenticated: bool):
        if not authenticated:
            self._restore_guest_rating()
            return
        for interaction in rows(await self._call('GET','/interactions')):
            if interaction.get('media_id')==int(identifier):
                self.selected_status=interaction['status']
                self.selected_rating=str(interaction.get('rating') or 0)
                self.selected_review=str(interaction.get('review') or '')
                self.selected_spoiler=bool(interaction.get('spoiler'))
                break

    async def _load_recommendations(self):
        if not self._selected_raw.get('external_source'):
            self.recommendations=[]
            return
        try:
            self.recommendations=[present_media(item) for item in await catalog.recommendations(self._selected_raw)]
        except APIError:
            self.recommendations=[]

    async def _load_community_reviews(self):
        try:
            self.community_reviews=await catalog.reviews(self._selected_raw)
        except APIError:
            self.community_reviews=[]

    async def _persist_selected(self) -> int:
        if not self._selected_raw: raise APIError('Escolha uma obra no catálogo.')
        if self._selected_raw.get('id'): return int(self._selected_raw['id'])
        payload={k:self._selected_raw[k] for k in ('external_source','external_id','media_type','title','description','cover_url','year','details')}
        result=await self._call('POST','/media',payload)
        self._selected_raw=result; self.selected=present_media(result)
        return int(result['id'])

    @rx.event
    async def save_interaction(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            rating=float(form.get('rating') or 0)
            if not 0<=rating<=5 or rating*2!=int(rating*2): raise ValueError()
            if form.get('status','planned') not in ('planned','in_progress','completed','dropped'):
                self.notice='Escolha um status válido.'; return
            mid=await self._persist_selected()
            await self._call('PUT','/interactions',dict(media_id=mid,status=form.get('status',self.selected_status),
                rating=rating,review=str(form.get('review','')).strip(),spoiler=form.get('spoiler')=='on'))
            self.notice='Sua experiência foi salva.'
            return rx.redirect('/obra/'+str(mid))
        except ValueError: self.notice='Escolha uma nota de 0,5 a 5, em passos de 0,5.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def quick_add(self, status: str, rating: float = 0):
        if not await self._require_user(): return rx.redirect('/login')
        if status not in ('planned','completed') or not 0<=rating<=5:
            self.notice='Ação inválida.'
            return
        try:
            mid=await self._persist_selected()
            await self._call('PUT','/interactions',dict(media_id=mid,status=status,rating=rating,
                review=self.selected_review,spoiler=self.selected_spoiler))
            self.selected_status=status
            if rating: self.selected_rating=str(rating)
            self.notice='Obra adicionada à sua biblioteca.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def load_library(self):
        self.library=[]; self.notice=''
        if not await self._require_user(): return rx.redirect('/login')
        try:
            await self._load_reference()
            self.library=[self._interaction(i) for i in rows(await self._call('GET','/interactions'))]
        except APIError as exc: self._failure(exc)

    @rx.event
    async def load_community(self):
        self.following_ids=[]
        await self.load_home()
        try: await self._load_people()
        except APIError as exc: self._failure(exc)
        if self.user_id:
            try:
                data=await self._call('GET',f'/profiles/{self.user_id}')
                self.following_ids=[str(f['followed_id']) for f in data['following']]
            except APIError as exc:
                if exc.status!=404: self._failure(exc)

    @rx.event
    async def load_profile(self):
        self.notice=''; self.profile_activity=[]; self.followers=[]; self.following=[]
        await self._validate_session()
        route_id=self.router.url.path.rstrip('/').rsplit('/',1)[-1]
        uid=str(route_id if route_id.isdigit() else self.user_id)
        if not uid.isdigit() or int(uid)==0: return rx.redirect('/login')
        self.profile={'user_id':uid,'username':'','display_name':'','bio':'','avatar_url':''}
        try:
            await self._load_reference(); data=await self._call('GET',f'/profiles/{uid}')
            self.profile={k:str(v or '') for k,v in data['profile'].items()}
            self.profile_activity=[self._interaction(i) for i in data['interactions']]
            self.followers=[self._person(i['follower_id']) for i in data['followers']]
            self.following=[self._person(i['followed_id']) for i in data['following']]
            if self.user_id:
                own=data if int(uid)==self.user_id else await self._call('GET',f'/profiles/{self.user_id}')
                self.following_ids=[str(f['followed_id']) for f in own['following']]
            completed=sum(i['status']=='completed' for i in data['interactions'])
            self.profile_stats=f'{completed} obras concluídas · {len(self.followers)} seguidores · {len(self.following)} seguindo'
        except APIError as exc:
            self.profile_stats=''
            if exc.status==404 and int(uid)==self.user_id: self.notice='Complete seu perfil para participar da comunidade.'
            else: self._failure(exc)

    @rx.event
    async def save_profile(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        username=str(form.get('username','')).strip().lower()
        if not re.fullmatch(r'[a-z0-9_]{3,30}',username): self.notice='Nome de usuário inválido.'; return
        avatar=str(form.get('avatar_url','')).strip()
        if avatar and not catalog.safe_url(avatar): self.notice='Use uma URL HTTPS para a foto.'; return
        try:
            result=await self._call('PUT','/profile',dict(username=username,display_name=str(form.get('display_name','')).strip(),
                bio=str(form.get('bio','')).strip(),avatar_url=avatar))
            self.profile={k:str(v or '') for k,v in result.items()}; self.user_name=username; self.notice='Perfil atualizado.'
        except APIError as exc: self._failure(exc)

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
        data=rows(await self._call('GET','/feed',params={'per_page':20}))
        own=rows(await self._call('GET','/posts',params={'user_id':self.user_id,'per_page':20}))
        combined={str(p['id']):p for p in data+own}; self.posts=[]
        try:
            self.liked_posts=[str(i['post_id']) for i in rows(await self._call('GET','/likes'))]
        except APIError as exc:
            if exc.status != 404:
                raise
            # Older workspaces have no /likes route. Resolve like state only
            # when a user opens a discussion or taps its like button.
            self.liked_posts=[]
        for p in sorted(combined.values(),key=lambda x:x.get('created_at',0),reverse=True):
            person=self._person(p['user_id']); m=self._media.get(str(p.get('media_id')), {})
            self.posts.append(dict(id=str(p['id']),user_id=str(p['user_id']),author=person['display_name'],
                avatar=person['avatar_url'],media_cover=catalog.safe_url(m.get('cover_url')),
                body=p['body'],published_at=datetime.fromtimestamp(p.get('created_at',0)/1000,tz=timezone.utc).strftime('%d/%m/%Y'),spoiler=str(bool(p.get('spoiler'))),media_id=str(p.get('media_id') or 0),media_title=m.get('title','')))

    @rx.event
    async def load_feed(self):
        self.posts=[]; self.comments=[]; self.notice=''
        if not await self._require_user(): return rx.redirect('/login')
        try: await self._load_reference(); await self._refresh_posts()
        except APIError as exc: self._failure(exc)

    @rx.event
    def edit_post(self, pid: str):
        for p in self.posts:
            if p['id']==pid and p['user_id']==str(self.user_id):
                self.post_editor_open=True
                self.edit_post_id=pid; self.edit_post_body=p['body']; self.edit_post_media=p['media_id']; self.edit_post_spoiler=p['spoiler']=='True'

    @rx.event
    def cancel_post(self):
        self.post_editor_open=False
        self.edit_post_id=''; self.edit_post_body=''; self.edit_post_media='0'; self.edit_post_spoiler=False

    @rx.event
    async def save_post(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            payload=dict(body=str(form.get('body','')).strip(),media_id=int(form.get('media_id') or 0),spoiler=form.get('spoiler')=='on')
            await self._call('PUT' if self.edit_post_id else 'POST','/posts'+('/'+self.edit_post_id if self.edit_post_id else ''),payload)
            self.cancel_post(); await self._refresh_posts(); self.notice='Publicação salva.'
        except (ValueError,TypeError): self.notice='Selecione uma obra válida.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def remove_post(self, pid: str):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            await self._call('DELETE',f'/posts/{int(pid)}'); self.comments=[]; self.selected_post=''
            await self._refresh_posts(); self.notice='Publicação removida.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def discussion(self, pid: str):
        if self.selected_post!=pid:
            self.edit_comment_id=''; self.edit_comment_body=''
        self.comments=[]
        try:
            data=await self._call('GET',f'/posts/{int(pid)}/discussion'); self.selected_post=pid
            self.comments=[dict(id=str(c['id']),user_id=str(c['user_id']),body=c['body'],author=self._person(c['user_id'])['display_name']) for c in data['comments']]
            if any(l['user_id']==self.user_id for l in data['likes']):
                if pid not in self.liked_posts: self.liked_posts.append(pid)
            elif pid in self.liked_posts: self.liked_posts.remove(pid)
            self.notice=f"{len(data['likes'])} curtidas · {len(data['comments'])} comentários"
        except APIError as exc: self._failure(exc)

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
            self.notice=f'{count} curtidas Â· {len(data["comments"])} comentÃ¡rios'
        except APIError as exc: self._failure(exc)

    @rx.event
    def edit_comment(self, cid: str):
        for c in self.comments:
            if c['id']==cid and c['user_id']==str(self.user_id): self.edit_comment_id=cid; self.edit_comment_body=c['body']

    @rx.event
    async def save_comment(self, form: dict):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            await self._call('PUT' if self.edit_comment_id else 'POST','/comments'+('/'+self.edit_comment_id if self.edit_comment_id else ''),
                dict(post_id=int(self.selected_post),body=str(form.get('body','')).strip()))
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
        self.notice=''; self.lists=[]; self.list_items=[]
        self.selected_list={'id':'','title':'','description':'','user_id':'','is_public':'True'}
        await self._validate_session()
        try:
            await self._load_reference()
            public=rows(await self._call('GET','/lists/public'))
            own=rows(await self._call('GET','/lists')) if self.user_id else []
            combined={str(i['id']):i for i in public+own}
            self.lists=[{k:str(v if v is not None else '') for k,v in i.items()} for i in combined.values()]
        except APIError as exc: self._failure(exc)

    @rx.event
    def new_list(self):
        self.list_editor_open=True
        self.selected_list=dict(id='',title='',description='',user_id=str(self.user_id),is_public='True'); self.list_items=[]

    @rx.event
    async def open_list(self, lid: str):
        self.list_items=[]; item=next((i for i in self.lists if i['id']==lid),None)
        if not item: return
        self.selected_list=item
        try:
            path=f'/lists/{int(lid)}/items' if self.user_id else f'/lists/public/{int(lid)}/items'
            items=rows(await self._call('GET',path))
            self.list_items=[present_media(self._media.get(str(i['media_id']),{'id':i['media_id']})) for i in items]
        except APIError as exc: self._failure(exc)

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
        try:
            lid=str(int(self.selected_list['id']))
            await self._call('POST',f'/lists/{lid}/items',{'media_id':int(form.get('media_id') or 0)})
            await self.open_list(lid); self.notice='Obra adicionada.'
        except (ValueError,KeyError): self.notice='Salve a lista e escolha uma obra.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def remove_list_item(self, mid: str):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            lid=str(int(self.selected_list['id']))
            await self._call('DELETE',f'/lists/{lid}/items/{int(mid)}'); await self.open_list(lid)
        except APIError as exc: self._failure(exc)
