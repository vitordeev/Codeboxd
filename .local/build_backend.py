"""Generate explicit XanoScript endpoints for the initial social schema."""
from pathlib import Path
import json

ROOT = Path('xano')
def write(path, text):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text.strip()+'\n',encoding='utf-8')
def table(name, fields, unique=(), indexes=()):
    idx=['{type: "primary", field: [{name: "id"}]}']
    for field in unique: idx.append('{type: "btree|unique", field: [{name: "'+field+'", op: "asc"}]}')
    for field in indexes: idx.append('{type: "btree", field: [{name: "'+field+'", op: "asc"}]}')
    write(Path('table')/(name+'.xs'), 'table '+name+' {\n  auth = false\n  schema {\n    int id\n    timestamp created_at?=now\n'+fields+'\n  }\n  index = [\n    '+'\n    '.join(idx)+'\n  ]\n}')
def ref(name, table): return f'    int {name} {{ table = "{table}" }}'
table('profile',ref('user_id','user')+'\n    text username filters=trim|lower|min:3|max:30\n    text display_name filters=trim|min:1|max:80\n    text bio? filters=trim|max:1000\n    text avatar_url? filters=trim|max:500',('user_id','username'))
table('media','    text identity_key\n    text external_source\n    text external_id\n    enum media_type { values = ["movie", "series", "anime", "book"] }\n    text title filters=trim|min:1|max:500\n    text description?\n    text cover_url?\n    int year?\n    json details?',('identity_key',),('media_type',))
table('user_media_interaction',ref('user_id','user')+'\n'+ref('media_id','media')+'\n    text identity_key\n    enum status { values = ["planned", "in_progress", "completed", "dropped"] }\n    decimal rating?\n    text review? filters=trim|max:10000\n    bool spoiler?\n    timestamp updated_at?=now',('identity_key',),('user_id','media_id'))
table('user_follow',ref('follower_id','user')+'\n'+ref('followed_id','user')+'\n    text identity_key',('identity_key',),('follower_id','followed_id'))
table('post',ref('user_id','user')+'\n    int media_id? { table = "media" }\n    text body filters=trim|min:1|max:5000\n    bool spoiler?\n    timestamp updated_at?=now',(),('user_id','media_id'))
table('post_like',ref('user_id','user')+'\n'+ref('post_id','post')+'\n    text identity_key',('identity_key',),('user_id','post_id'))
table('comment',ref('user_id','user')+'\n'+ref('post_id','post')+'\n    text body filters=trim|min:1|max:2000\n    timestamp updated_at?=now',(),('user_id','post_id'))
table('user_list',ref('user_id','user')+'\n    text title filters=trim|min:1|max:120\n    text description? filters=trim|max:2000\n    bool is_public?=true\n    timestamp updated_at?=now',(),('user_id',))
table('user_list_item',ref('list_id','user_list')+'\n'+ref('media_id','media')+'\n    text identity_key',('identity_key',),('list_id','media_id'))
write(Path('api/codeboxd/codeboxd.xs'),'api_group Codeboxd {\n  canonical = "codeboxd"\n}')
def check(cond,msg='Operação não permitida.',kind='accessdenied'):
    return f'precondition ({cond}) {{\n  error_type = "{kind}"\n  error = {json.dumps(msg,ensure_ascii=False)}\n}}'
def get(tbl, value, alias='record', field='id', output=''):
    return f'db.get {tbl} {{\n field_name = "{field}"\n field_value = {value}\n'+(f' output = {output}\n' if output else '')+f'}} as ${alias}'
def query(tbl,where='',alias='rows',single=False):
    return f'db.query {tbl} {{\n'+(f' where = {where}\n' if where else '')+f' return = {{type: "'+('single' if single else 'list')+f'"}}\n}} as ${alias}'
def add(tbl,data,alias='result'): return f'db.add {tbl} {{\n data = {{{data}}}\n}} as ${alias}'
def edit(tbl,value,data,alias='result'): return f'db.edit {tbl} {{\n field_name = "id"\n field_value = {value}\n data = {{{data}}}\n}} as ${alias}'
def delete(tbl,value): return f'db.del {tbl} {{\n field_name = "id"\n field_value = {value}\n}}'
def upsert(tbl,key,data,alias='result'): return f'db.add_or_edit {tbl} {{\n field_name = "identity_key"\n field_value = {key}\n data = {{{data}, identity_key: {key}}}\n}} as ${alias}'
def transaction(code):return 'db.transaction {\n stack {\n'+code+'\n }\n}'
def exists(tbl,value,alias='record'):return get(tbl,value,alias)+'\n'+check(f'${alias} != null','Registro não encontrado.','notfound')
def owned(tbl,value='$input.id',alias='record'):return exists(tbl,value,alias)+'\n'+check(f'${alias}.user_id == $auth.id')
def endpoint(path,verb,inputs,stack,response='$result',auth=True):
    guard=''
    if auth:
        guard=get('user','$auth.id','actor',output='["id", "account_status"]')+'\n'+check('$actor != null && $actor.account_status != "disabled"')+'\n'
    write(Path('api/codeboxd')/(path.replace('/','_').replace('{','').replace('}','')+'_'+verb+'.xs'),f'query "{path}" verb={verb} {{\n api_group = "Codeboxd"\n'+(' auth = "user"\n' if auth else '')+' input {\n'+inputs+'\n }\n stack {\n'+guard+stack+'\n }\n response = '+response+'\n}')

# Public projection comes only from profile; private authentication data never joins responses.
endpoint('profiles','GET','',query('profile'), '$rows',False)
endpoint('profiles/{user_id}','GET','int user_id',query('profile','$db.profile.user_id == $input.user_id','profile',True)+'\n'+check('$profile != null','Perfil não encontrado.','notfound')+'\n'+query('user_media_interaction','$db.user_media_interaction.user_id == $input.user_id','interactions')+'\n'+query('user_follow','$db.user_follow.followed_id == $input.user_id','followers')+'\n'+query('user_follow','$db.user_follow.follower_id == $input.user_id','following'),'{profile: $profile, interactions: $interactions, followers: $followers, following: $following}',False)
endpoint('profile','PUT','text username filters=trim|lower|min:3|max:30\ntext display_name filters=trim|min:1|max:80\ntext bio? filters=trim|max:1000\ntext avatar_url? filters=trim|max:500',
    query('profile','$db.profile.username == $input.username','duplicate',True)+'\n'+check('$duplicate == null || $duplicate.user_id == $auth.id','Nome de usuário indisponível.','inputerror')+'\n'+query('user','$db.user.username == $input.username && $db.user.id != $auth.id','legacy',True)+'\n'+check('$legacy == null','Nome de usuário indisponível.','inputerror')+'\n'+transaction('db.add_or_edit profile {\n field_name = "user_id"\n field_value = $auth.id\n data = {user_id: $auth.id, username: $input.username, display_name: $input.display_name, bio: $input.bio, avatar_url: $input.avatar_url}\n} as $result\n'+edit('user','$auth.id','username: $input.username, name: $input.display_name','updated_user')))
endpoint('media','GET','',query('media'), '$rows',False)
endpoint('media/{id}','GET','int id',exists('media','$input.id','result'),'$result',False)
media_inputs='text external_source filters=trim|min:1|max:40\ntext external_id filters=trim|min:1|max:100\nenum media_type { values = ["movie", "series", "anime", "book"] }\ntext title filters=trim|min:1|max:500\ntext description?\ntext cover_url?\nint year?\njson details?'
endpoint('media','POST',media_inputs,'var $key { value = $input.external_source ~ ":" ~ $input.media_type ~ ":" ~ $input.external_id }\n'+get('media','$key','existing','identity_key')+'\nconditional {\n if ($existing == null) {\n'+add('media','identity_key: $key, external_source: $input.external_source, external_id: $input.external_id, media_type: $input.media_type, title: $input.title, description: $input.description, cover_url: $input.cover_url, year: $input.year, details: $input.details')+'\n }\n else {\n var $result { value = $existing }\n }\n}')
endpoint('interactions','GET','',query('user_media_interaction','$db.user_media_interaction.user_id == $auth.id'),'$rows')
endpoint('interactions','PUT','int media_id\nenum status { values = ["planned", "in_progress", "completed", "dropped"] }\ndecimal rating?=0\ntext review? filters=trim|max:10000\nbool spoiler?=false',exists('media','$input.media_id')+'\n'+check('$input.rating >= 0 && $input.rating <= 5 && ($input.rating * 2) % 1 == 0','Nota deve estar entre 0,5 e 5, em passos de 0,5.','inputerror')+'\nvar $key { value = $auth.id ~ ":" ~ $input.media_id }\n'+upsert('user_media_interaction','$key','user_id: $auth.id, media_id: $input.media_id, status: $input.status, rating: $input.rating, review: $input.review, spoiler: $input.spoiler, updated_at: now'))
endpoint('follows/{user_id}','PUT','int user_id',exists('user','$input.user_id','target')+'\n'+check('$input.user_id != $auth.id','Você não pode seguir a si mesmo.','inputerror')+'\nvar $key { value = $auth.id ~ ":" ~ $input.user_id }\n'+upsert('user_follow','$key','follower_id: $auth.id, followed_id: $input.user_id'))
endpoint('follows/{user_id}','DELETE','int user_id',query('user_follow','$db.user_follow.follower_id == $auth.id && $db.user_follow.followed_id == $input.user_id','record',True)+'\nconditional { if ($record != null) {\n'+delete('user_follow','$record.id')+'\n}}','{success: true}')
endpoint('posts','GET','int user_id?=0',query('post','$db.post.user_id == $input.user_id || $input.user_id == 0'),'$rows',False)
endpoint('feed','GET','',query('user_follow','$db.user_follow.follower_id == $auth.id','follows')+'\napi.lambda { code = "return $var.follows.map(f => f.followed_id);" } as $following_ids\n'+query('post','$db.post.user_id in $following_ids'),'$rows')
post_inputs='text body filters=trim|min:1|max:5000\nint media_id?=0\nbool spoiler?=false'
post_check='conditional { if ($input.media_id > 0) {\n'+exists('media','$input.media_id','media')+'\n}}'
endpoint('posts','POST',post_inputs,post_check+'\n'+add('post','user_id: $auth.id, media_id: $input.media_id, body: $input.body, spoiler: $input.spoiler, updated_at: now'))
endpoint('posts/{id}','PUT','int id\n'+post_inputs,owned('post')+'\n'+post_check+'\n'+edit('post','$input.id','body: $input.body, media_id: $input.media_id, spoiler: $input.spoiler, updated_at: now'))
def cascade(tbl,parentfield,parentid,alias):
    return query(tbl,f'$db.{tbl}.{parentfield} == {parentid}',alias)+'\nforeach ($'+alias+') { each as child {\n'+delete(tbl,'$child.id')+'\n}}'
endpoint('posts/{id}','DELETE','int id',owned('post')+'\n'+transaction(cascade('comment','post_id','$input.id','comments')+'\n'+cascade('post_like','post_id','$input.id','likes')+'\n'+delete('post','$input.id')),'{success: true}')
endpoint('posts/{id}/discussion','GET','int id',exists('post','$input.id')+'\n'+query('comment','$db.comment.post_id == $input.id','comments')+'\n'+query('post_like','$db.post_like.post_id == $input.id','likes'),'{comments: $comments, likes: $likes}',False)
endpoint('posts/{id}/like','PUT','int id',exists('post','$input.id')+'\nvar $key { value = $auth.id ~ ":" ~ $input.id }\n'+upsert('post_like','$key','user_id: $auth.id, post_id: $input.id'))
endpoint('posts/{id}/like','DELETE','int id',query('post_like','$db.post_like.user_id == $auth.id && $db.post_like.post_id == $input.id','record',True)+'\nconditional { if ($record != null) {\n'+delete('post_like','$record.id')+'\n}}','{success: true}')
endpoint('comments','POST','int post_id\ntext body filters=trim|min:1|max:2000',exists('post','$input.post_id')+'\n'+add('comment','user_id: $auth.id, post_id: $input.post_id, body: $input.body, updated_at: now'))
endpoint('comments/{id}','PUT','int id\ntext body filters=trim|min:1|max:2000',owned('comment')+'\n'+edit('comment','$input.id','body: $input.body, updated_at: now'))
endpoint('comments/{id}','DELETE','int id',owned('comment')+'\n'+delete('comment','$input.id'),'{success: true}')
endpoint('lists/public','GET','',query('user_list','$db.user_list.is_public == true'),'$rows',False)
endpoint('lists','GET','',query('user_list','$db.user_list.user_id == $auth.id'),'$rows')
list_inputs='text title filters=trim|min:1|max:120\ntext description? filters=trim|max:2000\nbool is_public?=true'
endpoint('lists','POST',list_inputs,add('user_list','user_id: $auth.id, title: $input.title, description: $input.description, is_public: $input.is_public, updated_at: now'))
endpoint('lists/{id}','PUT','int id\n'+list_inputs,owned('user_list')+'\n'+edit('user_list','$input.id','title: $input.title, description: $input.description, is_public: $input.is_public, updated_at: now'))
endpoint('lists/{id}','DELETE','int id',owned('user_list')+'\n'+transaction(cascade('user_list_item','list_id','$input.id','items')+'\n'+delete('user_list','$input.id')),'{success: true}')
endpoint('lists/{id}/items','GET','int id',exists('user_list','$input.id')+'\n'+check('$record.is_public == true || $record.user_id == $auth.id')+'\n'+query('user_list_item','$db.user_list_item.list_id == $input.id'),'$rows')
endpoint('lists/public/{id}/items','GET','int id',exists('user_list','$input.id')+'\n'+check('$record.is_public == true')+'\n'+query('user_list_item','$db.user_list_item.list_id == $input.id'),'$rows',False)
endpoint('lists/{id}/items','POST','int id\nint media_id',owned('user_list')+'\n'+exists('media','$input.media_id','media')+'\nvar $key { value = $input.id ~ ":" ~ $input.media_id }\n'+upsert('user_list_item','$key','list_id: $input.id, media_id: $input.media_id'))
endpoint('lists/{id}/items/{media_id}','DELETE','int id\nint media_id',owned('user_list')+'\n'+query('user_list_item','$db.user_list_item.list_id == $input.id && $db.user_list_item.media_id == $input.media_id','item',True)+'\nconditional { if ($item != null) {\n'+delete('user_list_item','$item.id')+'\n}}','{success: true}')

# Safe audit records across all pre-existing authentication flows.
for p in ROOT.glob('api/authentication/**/*.xs'):
    t=p.read_text(encoding='utf-8').replace('metadata: $user1','metadata: {}').replace('metadata: $user','metadata: {}')
    p.write_text(t,encoding='utf-8')
# Protect legacy writes, preserve their existing schemas and GUIDs.
for p in ROOT.glob('api/titulos/**/*.xs'):
    if p.stem.endswith(('_POST','_PUT','_PATCH','_DELETE')):
        t=p.read_text(encoding='utf-8').replace('api_group = "Titulos"','api_group = "Titulos"\n  auth = "user"')
        t=t.replace('  stack {','  stack {\n    function.run "Quick Start/enforce_role" {\n      input = {user_id: $auth.id, required_role: "admin"}\n    } as $role_check',1)
        p.write_text(t,encoding='utf-8')
# Signup: full validation and atomic profile creation; preserve endpoint GUID.
p=ROOT/'api/authentication/auth/signup_POST.xs'
old=p.read_text(encoding='utf-8'); guid=old.split('guid = ')[1].splitlines()[0]
stack=query('user','$db.user.email == $input.email || $db.user.username == $input.username','existing',True)+'\n'+check('$existing == null','E-mail ou nome de usuário indisponível.','inputerror')+'\n'+query('profile','$db.profile.username == $input.username','existing_profile',True)+'\n'+check('$existing_profile == null','Nome de usuário indisponível.','inputerror')+'\n'+transaction(add('user','name: $input.name, username: $input.username, email: $input.email, password: $input.password, role: "member", account_status: "active"','user')+'\n'+add('profile','user_id: $user.id, username: $input.username, display_name: $input.name, bio: "", avatar_url: ""','profile'))+'\nsecurity.create_auth_token { table = "user"\n extras = {}\n expiration = 86400\n id = $user.id\n} as $authToken'
write(Path('api/authentication/auth/signup_POST.xs'),'query "auth/signup" verb=POST {\n api_group = "Authentication"\n input {\n text name filters=trim|min:1|max:80\n text username filters=trim|lower|min:3|max:30\n email email filters=trim|lower\n text password filters=min:8|minAlpha:1|minDigit:1\n }\n stack {\n'+stack+'\n }\n response = {authToken: $authToken, user_id: $user.id}\n guid = '+guid+'\n}')
for file in ['login_POST.xs','me_GET.xs']:
    p=ROOT/'api/authentication/auth'/file;t=p.read_text(encoding='utf-8')
    t=t.replace('"password", "role"','"password", "role", "account_status"').replace('"email", "role"','"email", "role", "username", "account_status"')
    if file.startswith('login'):
        t=t.replace('// Create an authentication token',check('$user.account_status != "disabled"')+'\n    // Create an authentication token')
    else: t=t.replace('// Create an event log',check('$user.account_status != "disabled"')+'\n    // Create an event log')
    p.write_text(t,encoding='utf-8')
print('Generated social schema/endpoints and applied authentication fixes.')
