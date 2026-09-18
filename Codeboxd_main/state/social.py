"""Social UI state backed by Xano endpoints."""
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
        source=m.get('external_source',''),external_id=m.get('external_id',''),
        details=' · '.join(f'{k}: {v}' for k,v in details.items()) if isinstance(details,dict) else '').items()}


class SocialState(SessionState):
    notice: str = ''
    busy: bool = False
    search_term: str = ''
    search_type: str = 'all'
    search_page: int = 1
    search_results: list[dict[str,str]] = []
    catalog_items: list[dict[str,str]] = []
    selected: dict[str,str] = {'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':''}
    selected_status: str = 'planned'
    selected_rating: str = '0'
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
        self.library=[]; self.posts=[]; self.comments=[]; self.lists=[]; self.list_items=[]
        self.following_ids=[]; self.liked_posts=[]; self.selected_post=''
        self.edit_post_id=''; self.edit_post_body=''; self.edit_post_media='0'; self.edit_post_spoiler=False
        self.edit_comment_id=''; self.edit_comment_body=''
        self.selected_review=''; self.selected_rating='0'; self.selected_status='planned'; self.selected_spoiler=False
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

    async def _call(self, method, path, data=None, params=None):
        result=await request(method,path,token=self._token(),data=data,params=params)
        if method!='GET': return result
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
        self.notice=self.error_message or 'Entre na sua conta para continuar.'
        return False

    async def _load_reference(self):
        self._media={str(m['id']):m for m in rows(await self._call('GET','/media'))}
        self.catalog_items=[present_media(m) for m in self._media.values()]
        self._profiles={str(p['user_id']):p for p in rows(await self._call('GET','/profiles'))}
        self.people=[self._person(uid) for uid in self._profiles]

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
        await self._validate_session()
        try: await self._load_reference()
        except APIError as exc: self._failure(exc)

    @rx.event
    async def search(self, form: dict):
        if self.busy: return
        self.busy=True; self.notice=''; self.search_page=1
        self.search_term=str(form.get('query','')).strip(); self.search_type=str(form.get('kind','all'))
        yield
        try:
            found,errors=await catalog.search(self.search_term,self.search_type)
            self._results={m['identity_key']:m for m in found}
            for m in self._media.values():
                if self.search_term.casefold() in m['title'].casefold() and self.search_type in ('all',m['media_type']):
                    self._results[m['identity_key']]=m
            self.search_results=[present_media(m) for m in self._results.values()]
            self.notice=' '.join(errors) or ('Nenhum resultado encontrado.' if not self.search_results else '')
        finally: self.busy=False

    @rx.event
    async def more_results(self):
        if self.busy: return
        self.busy=True; yield
        try:
            found,errors=await catalog.search(self.search_term,self.search_type,self.search_page+1)
            self._results.update({m['identity_key']:m for m in found})
            self.search_results=[present_media(m) for m in self._results.values()]; self.search_page+=1
            self.notice=' '.join(errors) or ('Não há mais resultados.' if not found else '')
        finally: self.busy=False

    @rx.event
    async def open_result(self, key: str):
        item=self._results.get(key)
        if not item: return
        if item.get('id'): return rx.redirect('/obra/'+str(item['id']))
        return rx.redirect('/obra?'+urlencode({k:item[k] for k in ('external_source','external_id','media_type')}))

    @rx.event
    async def load_external_media(self):
        self.notice=''; self._selected_raw={}
        self.selected={'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':''}
        await self._validate_session()
        self.selected_status='planned'; self.selected_rating='0'; self.selected_review=''; self.selected_spoiler=False
        params=self.router.page.params
        item=catalog.media(str(params.get('external_source','')),str(params.get('media_type','')),
                           str(params.get('external_id','')),'Sem título')
        try:
            existing=rows(await self._call('GET','/media',params={'identity_key':item['identity_key']}))
            if existing: return rx.redirect('/obra/'+str(existing[0]['id']))
        except APIError:
            pass
        try:
            self._selected_raw=await catalog.detail(item)
            self.selected=present_media(self._selected_raw)
        except APIError as exc: self._failure(exc)

    @rx.event
    async def load_media(self):
        identifier=self.router.page.params.get('media_id','')
        self._selected_raw={}
        self.selected={'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':''}
        if not str(identifier).isdigit(): return
        self.notice=''; self.selected_status='planned'; self.selected_rating='0'; self.selected_review=''; self.selected_spoiler=False
        try:
            self._selected_raw=await self._call('GET',f'/media/{identifier}'); self.selected=present_media(self._selected_raw)
            if await self._validate_session():
                for i in rows(await self._call('GET','/interactions')):
                    if i['media_id']==int(identifier):
                        self.selected_status=i['status']; self.selected_rating=str(i.get('rating') or 0)
                        self.selected_review=str(i.get('review') or ''); self.selected_spoiler=bool(i.get('spoiler'))
        except APIError as exc:
            self.selected={'id':'','title':'','kind':'','year':'','cover':'','description':'','details':'','source':'','external_id':''}; self._failure(exc)

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
            await self._call('PUT','/interactions',dict(media_id=mid,status=form.get('status','planned'),
                rating=rating,review=str(form.get('review','')).strip(),spoiler=form.get('spoiler')=='on'))
            self.notice='Sua experiência foi salva.'
            return rx.redirect('/obra/'+str(mid))
        except ValueError: self.notice='Escolha uma nota de 0,5 a 5, em passos de 0,5.'
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
        uid=str(self.router.page.params.get('profile_id') or self.user_id)
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
        self.liked_posts=[str(i['post_id']) for i in rows(await self._call('GET','/likes'))]
        data=rows(await self._call('GET','/feed'))
        own=rows(await self._call('GET','/posts',params={'user_id':self.user_id}))
        combined={str(p['id']):p for p in data+own}; self.posts=[]
        for p in sorted(combined.values(),key=lambda x:x.get('created_at',0),reverse=True):
            person=self._person(p['user_id']); m=self._media.get(str(p.get('media_id')), {})
            self.posts.append(dict(id=str(p['id']),user_id=str(p['user_id']),author=person['display_name'],
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
                self.edit_post_id=pid; self.edit_post_body=p['body']; self.edit_post_media=p['media_id']; self.edit_post_spoiler=p['spoiler']=='True'

    @rx.event
    def cancel_post(self):
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
            await self.discussion(pid)
            await self._call('DELETE' if pid in self.liked_posts else 'PUT',f'/posts/{int(pid)}/like')
            await self.discussion(pid)
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
            await self.load_lists(); await self.open_list(str(result['id'])); self.notice='Lista salva.'
        except APIError as exc: self._failure(exc)

    @rx.event
    async def remove_list(self):
        if not await self._require_user(): return rx.redirect('/login')
        try:
            await self._call('DELETE','/lists/'+str(int(self.selected_list['id'])))
            self.new_list(); await self.load_lists(); self.notice='Lista removida.'
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
