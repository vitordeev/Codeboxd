from pathlib import Path
p=Path('Codeboxd_main/state/social.py')
s=p.read_text(encoding='utf8')
s=s.replace('from urllib.parse import urlencode','from urllib.parse import urlencode\nfrom datetime import datetime, timezone')
s=s.replace("        try:\n            self._selected_raw=await catalog.detail(item)","        try:\n            existing=rows(await self._call('GET','/media',params={'identity_key':item['identity_key']}))\n            if existing: return rx.redirect('/obra/'+str(existing[0]['id']))\n        except APIError:\n            pass\n        try:\n            self._selected_raw=await catalog.detail(item)")
s=s.replace("            self.notice='Sua experiência foi salva.'", "            self.notice='Sua experiência foi salva.'\n            return rx.redirect('/obra/'+str(mid))")
s=s.replace("            completed=sum(i['status']=='completed' for i in data['interactions'])", "            if self.user_id:\n                own=data if int(uid)==self.user_id else await self._call('GET',f'/profiles/{self.user_id}')\n                self.following_ids=[str(f['followed_id']) for f in own['following']]\n            completed=sum(i['status']=='completed' for i in data['interactions'])")
s=s.replace("    async def _refresh_posts(self):\n        data=", "    async def _refresh_posts(self):\n        self.liked_posts=[str(i['post_id']) for i in rows(await self._call('GET','/likes'))]\n        data=")
s=s.replace("body=p['body'],spoiler=str(bool(p.get('spoiler'))),media_id=", "body=p['body'],published_at=datetime.fromtimestamp(p.get('created_at',0)/1000,tz=timezone.utc).strftime('%d/%m/%Y'),spoiler=str(bool(p.get('spoiler'))),media_id=")
p.write_text(s,encoding='utf8')
p=Path('Codeboxd_main/pages/social.py');s=p.read_text(encoding='utf8');s=s.replace("    return rx.el.article(rx.el.a(p['author'],href='/perfil/'+p['user_id'],class_name='font-semibold'),", "    return rx.el.article(rx.el.a(p['author'],href='/perfil/'+p['user_id'],class_name='font-semibold'),\n        rx.el.p(p['published_at'],class_name='text-xs text-gray-500'),");p.write_text(s,encoding='utf8')
p=Path('xano/api/codeboxd/media_GET.xs');s=p.read_text(encoding='utf8');s=s.replace(' input {',' input {\ntext identity_key?="" filters=trim',1).replace('db.query media {','db.query media {\n where = $input.identity_key == "" || $db.media.identity_key == $input.identity_key');p.write_text(s,encoding='utf8')
p=Path('xano/api/codeboxd/likes_GET.xs');p.write_text('''query "likes" verb=GET {
 api_group = "Codeboxd"
 auth = "user"
 input {
  int page?=1 filters=min:1
  int per_page?=100 filters=min:1|max:100
 }
 stack {
  db.get user {
   field_name = "id"
   field_value = $auth.id
   output = ["id", "account_status"]
  } as $actor
  precondition ($actor != null && $actor.account_status != "disabled") {
   error_type = "accessdenied"
   error = "Operacao nao permitida."
  }
  db.query post_like {
   where = $db.post_like.user_id == $auth.id
   sort = {post_like.id: "asc"}
   return = {type: "list", paging: {page: $input.page, per_page: $input.per_page, metadata: false}}
  } as $rows
 }
 response = $rows
}
''',encoding='utf8')
