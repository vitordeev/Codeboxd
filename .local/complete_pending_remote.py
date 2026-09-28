"""Focused Xano checks for remaining post, list and interaction cases."""
import json
import asyncio
import time
import sys
from pathlib import Path

import httpx
from dotenv import dotenv_values, load_dotenv

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from Codeboxd_main.services import catalog

config=dotenv_values('.env')
load_dotenv()
auth=config['XANO_AUTH_URL'].rstrip('/')
social=config.get('XANO_SOCIAL_URL','').rstrip('/') or auth.split('/api:')[0]+'/api:codeboxd'
accounts=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
client=httpx.Client(timeout=30)

def await_search(query,kind):
    return asyncio.run(catalog.search(query,kind))

def await_detail(item):
    return asyncio.run(catalog.detail(item))
created_lists=[]
created_posts=[]
restores=[]

def call(method,path,data=None,token='',group='social',expected=(200,)):
    base=auth if group=='auth' else social
    for attempt in range(5):
        response=client.request(method,base+path,json=data,
            headers={'Authorization':'Bearer '+token} if token else {})
        if response.status_code!=429: break
        time.sleep(3*(attempt+1))
    if response.status_code not in expected:
        raise AssertionError(f'{method} {path} returned HTTP {response.status_code}')
    try: return response.json()
    except ValueError: return None

def cleanup():
    for token,mid,old in restores:
        try: call('PUT','/interactions',old,token=token)
        except Exception: pass
    for token,pid in reversed(created_posts):
        try: call('DELETE',f'/posts/{pid}',token=token,expected=(200,204,404))
        except Exception: pass
    for token,lid in reversed(created_lists):
        try: call('DELETE',f'/lists/{lid}',token=token,expected=(200,204,404))
        except Exception: pass

try:
    tokens=[]
    for account in accounts[:2]:
        result=call('POST','/auth/login',{'email':account['email'],'password':account['password']},group='auth')
        tokens.append(result['authToken'])
    a,b=tokens

    wrong=call('POST','/auth/login',{'email':accounts[0]['email'],'password':'invalid-test-password'},
               group='auth',expected=(400,401,403))
    assert not isinstance(wrong,dict) or not wrong.get('authToken')
    print('PASS invalid credentials do not return an auth token',flush=True)

    media_by_kind={}
    for kind,query in [('movie','Interestelar'),('series','Breaking Bad'),('anime','Cowboy Bebop'),('book','Pride and Prejudice')]:
        items,errors=await_search(query,kind)
        if errors or not items: raise AssertionError(f'{kind} provider search did not return media')
        found=next((item for item in items if item['media_type']==kind),None)
        if not found: raise AssertionError(f'{kind} result type mismatch')
        checked=await_detail(found)
        if checked.get('media_type')!=kind or not checked.get('title'):
            raise AssertionError(f'{kind} provider detail was incomplete')
        data={key:checked[key] for key in ('external_source','external_id','media_type','title','description','cover_url','year','details')}
        media_by_kind[kind]=call('POST','/media',data,token=a)
    media_ids=[int(media_by_kind[k]['id']) for k in ('movie','series','anime','book')]
    print('PASS real provider search and detail for all four media categories',flush=True)

    list_one=call('POST','/lists',{'title':'Validação pendente A','description':'','is_public':False},token=a)
    list_two=call('POST','/lists',{'title':'Validação pendente B','description':'','is_public':False},token=a)
    created_lists.extend([(a,int(list_one['id'])),(a,int(list_two['id']))])
    for mid in media_ids:
        call('POST',f"/lists/{list_one['id']}/items",{'media_id':mid},token=a)
        call('POST',f"/lists/{list_two['id']}/items",{'media_id':mid},token=a)
    for collection in (list_one,list_two):
        items=call('GET',f"/lists/{collection['id']}/items",token=a)
        assert {int(item['media_id']) for item in items}==set(media_ids)
    print('PASS each supported media category and the same media can appear in separate lists',flush=True)

    post_without=call('POST','/posts',{'body':'Post sem mídia — validação'},token=a)
    post_with=call('POST','/posts',{'body':'Post com mídia — validação','media_id':media_ids[0]},token=a)
    created_posts.extend([(a,int(post_without['id'])),(a,int(post_with['id']))])
    assert int(post_without.get('media_id') or 0)==0
    assert int(post_with['media_id'])==media_ids[0]
    print('PASS posts persist with and without a media association',flush=True)

    existing_a=call('GET','/interactions',token=a)
    existing_b=call('GET','/interactions',token=b)
    shared=next((int(item['media_id']) for item in existing_a if any(int(row['media_id'])==int(item['media_id']) for row in existing_b)),None)
    if shared is None: raise AssertionError('Test accounts have no existing shared interaction to safely snapshot')
    snapshots=[]
    for token,rows in ((a,existing_a),(b,existing_b)):
        current=next((item for item in rows if int(item['media_id'])==shared),None)
        if current is not None:
            old={'media_id':shared,'status':current['status'],'rating':float(current.get('rating') or 0),
                 'review':str(current.get('review') or ''),'spoiler':bool(current.get('spoiler'))}
            restores.append((token,shared,old))
            snapshots.append(old)
        else:
            snapshots.append(None)
    for token,status,rating,review in ((a,'in_progress',3,'First review'),(a,'dropped',4.5,'Edited review'),(b,'completed',2,'Other user review')):
        call('PUT','/interactions',{'media_id':shared,'status':status,'rating':rating,'review':review,'spoiler':False},token=token)
    after_a=call('GET','/interactions',token=a)
    after_b=call('GET','/interactions',token=b)
    item_a=next(item for item in after_a if int(item['media_id'])==shared)
    item_b=next(item for item in after_b if int(item['media_id'])==shared)
    assert (item_a['status'],float(item_a['rating']),item_a['review'])==('dropped',4.5,'Edited review')
    assert (item_b['status'],float(item_b['rating']),item_b['review'])==('completed',2,'Other user review')
    renewed=call('POST','/auth/login',{'email':accounts[0]['email'],'password':accounts[0]['password']},group='auth')['authToken']
    after_login=call('GET','/interactions',token=renewed)
    persisted=next(item for item in after_login if int(item['media_id'])==shared)
    assert persisted['review']=='Edited review' and persisted['status']=='dropped'
    print('PASS status changes, rating/review edits, user isolation and persistence after login',flush=True)
finally:
    cleanup()
    client.close()
