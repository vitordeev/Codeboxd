"""Production browser regression using only local fictional records.

Writes a new report; preserves previous browser evidence and uses independent
generated frontend files so the normal application can keep running.
"""
import asyncio
import argparse
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import urllib.request
import uuid

from playwright.async_api import async_playwright, expect

from tools.real_login_measurement import normal_app_roots, normal_network_available, restore_normal_app, stop_process_tree
from tools.isolated_frontend import prepare_frontend

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'openspec/changes/otimizar-performance-app/validation/continuacao-browser-2026-10-20'
MODE={'case':'ready'}
CALLS=Counter()


class Fixture(BaseHTTPRequestHandler):
    def log_message(self,*args): pass

    def do_POST(self):
        self.rfile.read(int(self.headers.get('Content-Length','0')))
        self.do_GET()

    def do_GET(self):
        path=self.path.split('?')[0]
        CALLS[path]+=1
        data={
            '/auth/login':{'authToken':'fictional-browser-token'},
            '/auth/signup':{'authToken':'fictional-browser-token'},
            '/auth/me':{'id':7,'role':'member','username':'fixture','account_status':'active'},
            '/profiles/7':{'profile':{'user_id':7,'username':'fixture','display_name':'Conta fictícia'},
                           'interactions':[],'followers':[],'following':[]},
            '/profiles':[], '/media':[], '/interactions':[],
            '/lists':[{'id':1,'title':'Quero ver / ler'},{'id':2,'title':'Já assisti / li'}],
            '/reset/request-reset-link':{},
        }
        if path.startswith('/media/'):
            identifier=int(path.rsplit('/',1)[-1])
            kind=('movie','series','anime','book')[identifier-1]
            data[path]={'id':identifier,'title':'Obra fictícia '+kind,'media_type':kind,
                        'identity_key':'fixture:'+kind+':'+str(identifier),'external_source':'',
                        'cover_url':'','description':'Descrição fictícia','year':2020}
        if path=='/interactions' and MODE['case']=='slow-review': time.sleep(3)
        code=429 if ((path=='/auth/signup' and MODE['case']=='signup-429') or
                     (path=='/reset/request-reset-link' and MODE['case']=='reset-429')) else 200
        body=json.dumps(data.get(path,{})).encode()
        self.send_response(code if path in data else 404)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        if code==429: self.send_header('Retry-After','2')
        self.end_headers()
        self.wfile.write(body)


async def context_for(browser,width):
    context=await browser.new_context(viewport={'width':width,'height':900})
    await context.route('**/*',lambda route: route.continue_() if
        route.request.url.startswith(('http://127.0.0.1:3031/','http://localhost:3031/')) else route.abort())
    page=await context.new_page()
    errors=[]
    page.on('pageerror',lambda error:errors.append(type(error).__name__))
    return context,page,errors


async def media_case(browser,width,identifier):
    MODE['case']='ready'
    context,page,errors=await context_for(browser,width)
    try:
        await page.goto('http://127.0.0.1:3031/login')
        await page.locator('input[name=email]').fill('reader@example.invalid')
        await page.locator('input[name=password]').fill('fictional-password1')
        await page.get_by_role('button',name='Entrar',exact=True).click()
        await expect(page.get_by_role('heading',name='Conta fictícia',exact=True)).to_be_visible(timeout=30000)
        MODE['case']='slow-review'
        start=time.perf_counter()
        await page.goto(f'http://127.0.0.1:3031/obra/{identifier}')
        await expect(page.locator('.media-detail-title')).to_be_visible(timeout=30000)
        primary_ms=round((time.perf_counter()-start)*1000)
        await expect(page.get_by_text('Carregando sua avaliação…',exact=True)).to_be_visible()
        await expect(page.get_by_role('button',name='Salvar avaliação',exact=True)).not_to_be_visible()
        await expect(page.get_by_role('button',name='Salvar avaliação',exact=True)).to_be_visible(timeout=15000)
        await expect(page.get_by_text('Carregando informações complementares…',exact=True)).not_to_be_visible()
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        assert not errors
        await page.screenshot(path=str(OUTPUT/f'media-{identifier}-{width}.png'),full_page=True)
        return dict(case='media-progressive',width=width,identifier=identifier,
                    primary_visible_ms=primary_ms,review_loading_observed=True,errors=errors,passed=True)
    finally: await context.close()


async def auth_case(browser,width,case):
    MODE['case']=case
    context,page,errors=await context_for(browser,width)
    try:
        if case=='signup-429':
            await page.goto('http://127.0.0.1:3031/cadastro')
            for key,value in {'name':'Pessoa fictícia','username':'fixture_reader',
                'email':'reader@example.invalid','password':'fictional-password1',
                'confirm_password':'fictional-password1'}.items():
                await page.locator(f'input[name={key}]').fill(value)
            button=page.locator('button[type=submit]')
            await button.click()
            await expect(page.get_by_text('Muitas solicitações.',exact=False)).to_be_visible(timeout=15000)
            assert await page.locator('input[name=email]').input_value()=='reader@example.invalid'
        else:
            await page.goto('http://127.0.0.1:3031/redefinir-senha')
            form=page.locator('form').first
            await form.locator('input[name=email]').fill('reader@example.invalid')
            before=CALLS['/reset/request-reset-link']
            await form.locator('button[type=submit]').click()
            await expect(page.get_by_role('status')).to_contain_text('segundos')
            await form.locator('button[type=submit]').click()
            await expect(page.get_by_role('status')).to_contain_text('segundos')
            assert CALLS['/reset/request-reset-link']==before+1
            assert await form.locator('input[name=email]').input_value()=='reader@example.invalid'
        assert not errors
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        return dict(case=case,width=width,preserved_email=True,errors=errors,passed=True)
    finally: await context.close()


async def main():
    if not await normal_network_available():
        raise RuntimeError('Network is blocked: run from an approved network-enabled process before changing the frontend.')
    OUTPUT.mkdir(parents=True,exist_ok=True)
    if (OUTPUT/'result.json').exists(): raise RuntimeError('Preserve existing report; choose a new output directory')
    roots=normal_app_roots()
    web_dir=prepare_frontend('browser-'+uuid.uuid4().hex)
    server=ThreadingHTTPServer(('127.0.0.1',3040),Fixture)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    env=dict(os.environ,XANO_AUTH_URL='http://127.0.0.1:3040',XANO_SOCIAL_URL='http://127.0.0.1:3040',
             COOKIE_SECURE='false',REFLEX_STATE_MANAGER_MODE='memory',DEEPL_API_KEY='',TMDB_READ_TOKEN='',
             REFLEX_WEB_WORKDIR=str(web_dir))
    results=[]; failure=''; restored=False
    with (OUTPUT/'server.log').open('w',encoding='utf-8') as log:
        process=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod','--single-port',
            '--frontend-port','3031','--backend-port','3031'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            print('STARTING_ISOLATED_BROWSER_SERVER',flush=True)
            for _ in range(240):
                if process.poll() is not None: raise RuntimeError('Test server exited')
                try:
                    with urllib.request.urlopen('http://127.0.0.1:3031/login',timeout=1): break
                except OSError: await asyncio.sleep(1)
            else: raise TimeoutError('Test server startup')
            async with async_playwright() as playwright:
                browser=await playwright.chromium.launch(channel='msedge',headless=True)
                try:
                    for width in (1440,390):
                        for identifier in (1,2,3,4):
                            result=await media_case(browser,width,identifier)
                            results.append(result); print(json.dumps(result),flush=True)
                        for case in ('signup-429','reset-429'):
                            result=await auth_case(browser,width,case)
                            results.append(result); print(json.dumps(result),flush=True)
                finally: await browser.close()
        except Exception as exc:
            failure=type(exc).__name__+': '+str(exc)
            print('VALIDATION_FAILURE: '+failure,flush=True)
        finally:
            stop_process_tree(process); server.shutdown()
            try:
                with urllib.request.urlopen('http://127.0.0.1:3030/login',timeout=3):
                    restored=True
                print('NORMAL_APP_PRESERVED',flush=True)
            except OSError:
                print('RESTORING_NORMAL_APP',flush=True)
                restored=await restore_normal_app(roots,'normal-restored-after-continuation.log')
            (OUTPUT/'result.json').write_text(json.dumps(dict(layer='browser-local-fixtures',
                expected=12,completed=results,failure=failure,normal_restored=restored),indent=2),encoding='utf-8')
    if failure or not restored: raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    OUTPUT=args.output.resolve()
    asyncio.run(main())
