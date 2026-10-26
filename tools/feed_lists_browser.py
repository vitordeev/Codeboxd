"""Production browser checks with isolated frontend and fictional local APIs."""
import argparse
import asyncio
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import urllib.request
from urllib.parse import urlsplit

from playwright.async_api import async_playwright, expect
from tools.isolated_frontend import prepare_frontend
from tools.real_login_measurement import stop_process_tree
from tools.performance_continuation_browser import context_for

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'openspec/changes/archive/2026-10-22-corrigir-edicao-feed-e-inclusao-listas/validation/browser-2026-10-22'
CALLS=Counter(); POSTS=[]; ENTRIES=[]
MEDIA=[dict(id=i+1,title='Fixture '+kind,media_type=kind,identity_key='fixture:'+kind,
            external_source='',cover_url='',description='Descrição fictícia',year=2020)
       for i,kind in enumerate(('movie','series','anime','book'))]
LISTS=[dict(id=1,user_id=7,title='Quero ver / ler',is_public=True),
       dict(id=2,user_id=7,title='Já assisti / li',is_public=True),
       dict(id=12,user_id=7,title='Coleção de teste',is_public=False)]


class Fixture(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_CONNECT(self): self.send_error(403)
    def do_GET(self): self.respond()
    def do_POST(self): self.respond()
    def do_PUT(self): self.respond()

    def respond(self):
        path=urlsplit(self.path).path
        CALLS[(self.command,path)]+=1
        payload=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))) or b'{}')
        status=200
        data={
            '/auth/login':{'authToken':'fictional-session'},
            '/auth/me':{'id':7,'role':'member','account_status':'active'},
            '/profiles/7':{'profile':{'user_id':7,'username':'fixture','display_name':'Conta fictícia'},'interactions':[],'followers':[],'following':[]},
            '/profiles':[{'user_id':7,'display_name':'Conta fictícia','username':'fixture'}],
            '/media':MEDIA,'/interactions':[],'/feed':POSTS,'/posts':POSTS,'/likes':[],
            '/lists':LISTS,'/lists/public':[dict(id=13,user_id=8,title='Lista de outra pessoa',is_public=True)],
        }.get(path,{})
        if path.startswith('/media/'):
            data=next(x for x in MEDIA if x['id']==int(path.rsplit('/',1)[1]))
        if path.startswith('/lists/') and path.endswith('/items'):
            if self.command=='POST':
                if payload['media_id'] not in ENTRIES: ENTRIES.append(payload['media_id'])
                data={'id':100,'media_id':payload['media_id']}
            else: data=[{'media_id':mid} for mid in ENTRIES]
        if path=='/posts/55' and self.command=='PUT':
            POSTS[0].update(payload); data=POSTS[0]
        if path=='/posts' and self.command=='POST':
            POSTS.append(dict(payload,id=56,user_id=7,created_at=1)); data=POSTS[-1]
        if path=='/lists/12/items' and self.command=='POST' and payload.get('media_id') not in range(1,5):
            status=400; data={}
        body=json.dumps(data).encode()
        self.send_response(status); self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)


async def check(browser,width,case):
    CALLS.clear(); ENTRIES.clear(); POSTS[:]=[dict(id=55,user_id=7,body='Texto original',media_id=1 if case==2 else 0,spoiler=False,created_at=1)]
    context,page,errors=await context_for(browser,width)
    try:
        await page.goto('http://127.0.0.1:3031/login')
        await page.locator('input[name=email]').fill('reader@example.invalid')
        await page.locator('input[name=password]').fill('fictional-password')
        await page.get_by_role('button',name='Entrar',exact=True).click()
        await expect(page.get_by_role('heading',name='Conta fictícia',exact=True)).to_be_visible(timeout=30000)
        await expect(page.get_by_text('Carregando…',exact=True)).not_to_be_visible(timeout=30000)
        if case in (1,2):
            await page.goto('http://127.0.0.1:3031/feed')
            await page.get_by_role('button',name='Editar',exact=True).click()
            dialog=page.get_by_role('dialog')
            await expect(dialog).to_be_visible()
            await dialog.locator('textarea[name=body]').fill('Publicação editada')
            if case==2: await dialog.get_by_role('button',name='Remover obra',exact=True).click()
            await dialog.get_by_role('button',name='Salvar edição',exact=True).click()
            await expect(dialog).not_to_be_visible(timeout=30000)
            await expect(page.get_by_text('Publicação editada',exact=True)).to_be_visible()
            assert len(POSTS)==1 and POSTS[0]['id']==55 and POSTS[0]['media_id']==0
            assert CALLS[('PUT','/posts/55')]==1 and CALLS[('POST','/posts')]==0
        elif case==3:
            await page.goto('http://127.0.0.1:3031/listas')
            await page.get_by_role('button').filter(has_text='Coleção de teste').click()
            await page.get_by_role('searchbox',name='Buscar obras para a lista').fill('Fixture')
            await page.get_by_role('button',name='Buscar obras',exact=True).click()
            buttons=page.get_by_role('button',name='Adicionar',exact=True)
            await expect(buttons).to_have_count(4,timeout=30000)
            await buttons.first.click()
            await expect(page.get_by_text('Obra adicionada à lista.',exact=True).first).to_be_visible()
            await buttons.first.click()
            await expect(page.get_by_text('Esta obra já está na lista.',exact=True).first).to_be_visible()
            assert len(ENTRIES)==1 and CALLS[('POST','/lists/12/items')]==1
        else:
            await page.goto('http://127.0.0.1:3031/obra/1')
            await page.get_by_role('button',name='Adicionar a outra lista',exact=True).click()
            select=page.get_by_label('Lista de destino')
            await expect(select.locator('option')).to_have_count(4,timeout=30000)
            assert await select.locator('option[value="13"]').count()==0
            await select.select_option('12')
            await page.get_by_role('button',name='Confirmar inclusão',exact=True).click()
            await expect(page.get_by_text('Obra adicionada à lista.',exact=True).first).to_be_visible()
            assert ENTRIES==[1] and CALLS[('POST','/lists/12/items')]==1
            assert CALLS[('PUT','/interactions')]==0
        assert not errors,errors
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        await page.screenshot(path=str(OUTPUT/f'case-{case}-{width}.png'),full_page=True)
        return {'case':case,'width':width,'passed':True,'javascript_errors':errors}
    finally:
        await context.close()


async def main(output, frontend_workdir=None):
    global OUTPUT
    OUTPUT=output.resolve()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    if (OUTPUT/'result.json').exists(): raise RuntimeError('Use another output directory to preserve evidence')
    if frontend_workdir:
        frontend=frontend_workdir.resolve()
        if not frontend.is_relative_to((ROOT/'.local/frontends').resolve()) or not frontend.is_dir():
            raise ValueError('Use only an existing isolated frontend directory')
    else:
        frontend=prepare_frontend('feed-lists-'+str(os.getpid()))
    server=ThreadingHTTPServer(('127.0.0.1',3040),Fixture)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    env=dict(os.environ,XANO_AUTH_URL='http://127.0.0.1:3040',XANO_SOCIAL_URL='http://127.0.0.1:3040',
             COOKIE_SECURE='false',REFLEX_STATE_MANAGER_MODE='memory',DEEPL_API_KEY='',TMDB_READ_TOKEN='',
             DEFAULT_LIST_IDENTITY_ENABLED='false',
             REFLEX_WEB_WORKDIR=str(frontend),REFLEX_USE_NPM='true',
             REFLEX_APP_MODULE_IMPORT='tools.feed_lists_fixture_app')
    results=[]; failure=''
    with (OUTPUT/'server.log').open('w',encoding='utf-8') as log:
        process=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod','--single-port',
                                 '--frontend-port','3031','--backend-port','3031'],cwd=ROOT,env=env,
                                 stdout=log,stderr=subprocess.STDOUT,
                                 creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            print('STARTING_ISOLATED_PRODUCTION',flush=True)
            for _ in range(240):
                if process.poll() is not None: raise RuntimeError('Production process exited; inspect server.log')
                try:
                    with urllib.request.urlopen('http://127.0.0.1:3031/login',timeout=1): break
                except OSError: await asyncio.sleep(1)
            else: raise TimeoutError('Production startup')
            async with async_playwright() as playwright:
                browser=await playwright.chromium.launch(channel='msedge',headless=True)
                try:
                    for width in (1440,390):
                        for case in (1,2,3,4):
                            result=await check(browser,width,case); results.append(result)
                            print(json.dumps(result),flush=True)
                finally: await browser.close()
        except Exception as error:
            failure=type(error).__name__+': '+str(error)
            print(json.dumps({'failure':failure}),flush=True)
        finally:
            stop_process_tree(process); server.shutdown()
            (OUTPUT/'result.json').write_text(json.dumps({'layer':'browser_local_fictional_backend',
                'expected':8,'completed':results,'failure':failure,'normal_server_modified':False},indent=2),encoding='utf-8')
    return 1 if failure else 0


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    parser.add_argument('--frontend-workdir',type=Path)
    args=parser.parse_args()
    raise SystemExit(asyncio.run(main(args.output,args.frontend_workdir)))
