import asyncio,json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
import httpx
from dotenv import load_dotenv
from Codeboxd_main.services import catalog
load_dotenv()

async def main():
    accounts=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
    async with httpx.AsyncClient(timeout=25) as client:
        auth=await client.post(os.environ['XANO_AUTH_URL'].rstrip('/')+'/auth/login',
            json={'email':accounts[0]['email'],'password':accounts[0]['password']})
        print('Xano login HTTP',auth.status_code,flush=True)
        auth.raise_for_status()
        headers={'Authorization':'Bearer '+auth.json()['authToken']}
        root=os.environ['XANO_SOCIAL_URL'].rstrip('/')
        response=await client.get(root+'/media',params={'per_page':100},headers=headers)
        print('Xano catalog HTTP',response.status_code,flush=True)
        response.raise_for_status()
        payload=response.json()
        rows=payload.get('items',[]) if isinstance(payload,dict) else payload
        old=next((row for row in rows if row['external_source']=='jikan' and str(row['external_id'])=='1'),None)
        if old is None: raise AssertionError('Existing Cowboy Bebop record required for non-creating deduplication test')
        detail=await catalog.detail(catalog.media('kitsu','anime','1','Cowboy Bebop'))
        data={key:detail[key] for key in ('external_source','external_id','media_type','title','description','cover_url','year','details')}
        saved=await client.post(root+'/media',headers=headers,json=data)
        print('Xano Kitsu save HTTP',saved.status_code,flush=True)
        saved.raise_for_status()
        assert saved.json()['id']==old['id'],'Legacy identity was duplicated'
        print('PASS existing library identity preserved; no duplicate created',flush=True)
        denied=await client.post(root+'/media',headers=headers,json={**data,'media_type':'book'})
        print('Xano invalid category HTTP',denied.status_code,flush=True)
        assert denied.status_code in (400,422)
asyncio.run(main())
