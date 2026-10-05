"""Opt-in live integration checks; creates only uniquely named test data."""
import json
import secrets
import time
from pathlib import Path
import httpx
from dotenv import dotenv_values, set_key

config=dotenv_values('.env')
auth=config['XANO_AUTH_URL'].rstrip('/')
social=auth.split('/api:')[0]+'/api:codeboxd'
client=httpx.Client(timeout=30)
passed=[]
def call(method,path,data=None,token='',group='social',expected=(200,)):
    for retry in range(6):
        response=client.request(method,(auth if group=='auth' else social)+path,json=data,
            headers={'Authorization':'Bearer '+token} if token else {})
        if response.status_code!=429: break
        time.sleep(21)
    if response.status_code not in expected:
        # Keep diagnostics local; never print credentials or auth responses.
        Path('.local/remote-error.json').write_text(json.dumps({'method':method,'path':path,'status':response.status_code,
            'response':response.text if group!='auth' else 'Authentication response omitted'},ensure_ascii=False),encoding='utf8')
        raise AssertionError(f'{method} {path}: HTTP {response.status_code}, expected {expected}')
    try: return response.json()
    except ValueError: return None

def record(label):
    passed.append(label)
    print('PASS',label,flush=True)
    Path('.local/remote-results.json').write_text(json.dumps(passed,indent=2,ensure_ascii=False),encoding='utf8')

call('GET','/media')
record('Published social API responds')
set_key('.env','XANO_SOCIAL_URL',social)
account_file=Path('.local/test-accounts.json')
if account_file.exists():
    accounts=json.loads(account_file.read_text(encoding='utf8'))
else:
    suffix=secrets.token_hex(5)
    accounts=[{'name':'Codeboxd teste '+str(i),'username':f'cbtest_{suffix}_{i}',
               'email':f'cbtest_{suffix}_{i}@example.com','password':secrets.token_urlsafe(24)+'A1'} for i in (1,2)]
    account_file.write_text(json.dumps(accounts),encoding='utf8')
for account in accounts:
    if not account.get('id'):
        result=call('POST','/auth/signup',{k:account[k] for k in ('name','username','email','password')},group='auth')
        account['id']=result['user_id']; account['token']=result['authToken']
        account_file.write_text(json.dumps(accounts),encoding='utf8')
    result=call('POST','/auth/login',{'email':account['email'],'password':account['password']},group='auth')
    account['token']=result['authToken']
    account_file.write_text(json.dumps(accounts),encoding='utf8')
    user=call('GET','/auth/me',token=account['token'],group='auth')
    assert user['id']==account['id']
record('Two real accounts: signup, login and verified identity')
a,b=accounts; ta,tb=a['token'],b['token']
call('POST','/auth/signup',{k:a[k] for k in ('name','username','email','password')},group='auth',expected=(400,403,409))
record('Duplicate account rejected')
profile=call('GET',f"/profiles/{a['id']}")
assert profile['profile']['username']==a['username']
assert 'email' not in profile['profile'] and 'password' not in profile['profile']
call('PUT','/profile',{'username':a['username'],'display_name':'Perfil de teste','bio':'Validação de integração','avatar_url':''},token=ta)
call('PUT','/profile',{'username':'invalid space','display_name':'Inválido'},token=ta,expected=(400,))
record('Public profile, privacy and backend username validation')
media=call('POST','/media',{'external_source':'openlibrary','external_id':'OL45804W','media_type':'book',
    'title':'Pride and Prejudice','description':'','cover_url':'','year':1813,'details':{}},token=ta)
mid=media['id']
same=call('POST','/media',{'external_source':'openlibrary','external_id':'OL45804W','media_type':'book',
    'title':'Pride and Prejudice','description':'','cover_url':'','year':1813,'details':{}},token=tb)
assert mid==same['id']
record('Media persistence and deduplication')
for token,status,rating in ((ta,'planned',4.5),(tb,'completed',3)):
    call('PUT','/interactions',{'media_id':mid,'status':status,'rating':rating,'review':'Teste de integração','spoiler':True},token=token)
ia=call('GET','/interactions',token=ta); ib=call('GET','/interactions',token=tb)
assert all(i['user_id']==a['id'] for i in ia) and all(i['user_id']==b['id'] for i in ib)
call('PUT','/interactions',{'media_id':mid,'status':'completed','rating':7},token=ta,expected=(400,))
call('PUT','/interactions',{'media_id':mid,'status':'completed','rating':4},expected=(401,))
record('Independent interactions, invalid rating and anonymous write rejection')
call('PUT',f"/follows/{b['id']}",token=ta)
call('PUT',f"/follows/{b['id']}",token=ta)
call('PUT',f"/follows/{a['id']}",token=ta,expected=(400,))
post=call('POST','/posts',{'media_id':mid,'body':'Publicação de teste de integração','spoiler':True},token=tb)
pid=post['id']
feed=call('GET','/feed',token=ta)
assert any(p['id']==pid for p in feed)
call('PUT',f'/posts/{pid}',{'body':'Edição indevida','media_id':mid,'spoiler':False},token=ta,expected=(403,))
call('PUT',f'/posts/{pid}',{'body':'Publicação editada','media_id':mid,'spoiler':False},token=tb)
record('Follow, feed and post ownership')
call('PUT',f'/posts/{pid}/like',token=ta)
call('PUT',f'/posts/{pid}/like',token=ta)
comment=call('POST','/comments',{'post_id':pid,'body':'Comentário teste'},token=ta)
discussion=call('GET',f'/posts/{pid}/discussion')
assert len([like for like in discussion['likes'] if like['user_id']==a['id']])==1
call('DELETE',f"/comments/{comment['id']}",token=tb,expected=(403,))
call('PUT',f"/comments/{comment['id']}",{'body':'Comentário editado'},token=ta)
call('DELETE',f'/posts/{pid}/like',token=ta)
record('Like deduplication, unlike and comment ownership')
collection=call('POST','/lists',{'title':'Lista de teste de integração','description':'Teste','is_public':False},token=ta)
lid=collection['id']
call('POST',f'/lists/{lid}/items',{'media_id':mid},token=ta)
call('POST',f'/lists/{lid}/items',{'media_id':mid},token=ta)
items=call('GET',f'/lists/{lid}/items',token=ta)
assert len(items)==1
call('GET',f'/lists/{lid}/items',token=tb,expected=(403,))
call('GET',f'/lists/public/{lid}/items',expected=(403,))
call('DELETE',f'/lists/{lid}',token=tb,expected=(403,))
call('PUT',f'/lists/{lid}',{'title':'Lista pública de teste','description':'Teste','is_public':True},token=ta)
assert len(call('GET',f'/lists/public/{lid}/items'))==1
record('List privacy, ownership, visibility and deduplication')
call('DELETE',f'/lists/{lid}',token=ta)
call('GET',f'/lists/{lid}/items',token=ta,expected=(404,))
call('DELETE',f'/posts/{pid}',token=tb)
call('GET',f'/posts/{pid}/discussion',expected=(404,))
call('DELETE',f"/follows/{b['id']}",token=ta)
record('Post/list deletion and unfollow')
print('Completed',len(passed),'integration groups; credentials retained only under .local.',flush=True)
