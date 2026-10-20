"""Browser checks for library/lists against local synthetic data only.

Uses production Reflex, Edge headless and temporary memory state. Restores the
normal app automatically. Run: python -B -m tools.library_lists_browser_validation
"""
import asyncio
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from playwright.async_api import async_playwright, expect

from tools.real_login_measurement import (VisitCycle, normal_app_roots,
    restore_normal_app, stop_process_tree)


ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'openspec/changes/otimizar-performance-app/validation'
MODE={}
CALLS=Counter()
OWN=[]


def reset_fixture(case):
    MODE['case']=case
    MODE['size']=250 if case=='large' else 5
    CALLS.clear()
    OWN[:]=[] if case=='missing-defaults' else [
        dict(id=1,title='Quero ver / ler',user_id=7,is_public=True),
        dict(id=2,title='Já assisti / li',user_id=7,is_public=True)]
    OWN.extend(dict(id=10+i,title=f'Lista privada {i}',user_id=7,is_public=False)
               for i in range(1,MODE['size']+1))


class Fixture(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self): self.respond()
    def do_POST(self): self.respond()

    def respond(self):
        parsed=urlsplit(self.path)
        path=parsed.path
        CALLS[(self.command,path)]+=1
        status=200
        if path=='/media' and MODE['case']=='slow-media': time.sleep(2)
        if path=='/profiles' or (path=='/media' and MODE['case']=='media-429'):
            status=429
            data={}
        elif path=='/auth/me':
            data={'id':7,'role':'member','account_status':'active'}
        elif path=='/media':
            data=[dict(id=i,title=f'Livro fictício {i}',media_type='book',cover_url='')
                  for i in range(1,MODE['size']+1)]
        elif path=='/interactions':
            data=[dict(media_id=i,status='completed',rating=1.5) for i in range(1,MODE['size']+1)]
        elif path=='/lists' and self.command=='POST':
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            data.update(id=30000+len(OWN),user_id=7)
            OWN.append(data)
        elif path=='/lists': data=OWN
        elif path=='/lists/public':
            data=[dict(id=20000+i,title=f'Lista pública {i}',user_id=8,is_public=True)
                  for i in range(1,MODE['size']+1)]
        elif path.startswith('/lists/') and path.endswith('/items'):
            data=[dict(media_id=1)]
        else:
            status=404
            data={}
        if isinstance(data,list):
            query=parse_qs(parsed.query)
            page=int(query.get('page',['1'])[0])
            per_page=int(query.get('per_page',['100'])[0])
            data=data[(page-1)*per_page:page*per_page]
        body=json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        if status==429: self.send_header('Retry-After','20')
        self.end_headers()
        try: self.wfile.write(body)
        except (BrokenPipeError,ConnectionResetError): pass


async def check(browser,width,section,case):
    reset_fixture(case)
    context=await browser.new_context(viewport={'width':width,'height':900})
    await context.add_cookies([dict(name='codeboxd_auth',value='local-fixture-token',
                                   url='http://127.0.0.1:3031')])
    await context.route('**/*',lambda route: route.continue_() if
        urlsplit(route.request.url).hostname in ('localhost','127.0.0.1') else route.abort())
    page=await context.new_page()
    errors=[]
    page.on('pageerror',lambda error: errors.append(type(error).__name__))
    cycle=VisitCycle()
    page.on('websocket',lambda socket: socket.on('framereceived',cycle.received))
    route='/biblioteca' if section=='library' else '/listas'
    started=time.perf_counter()
    await page.goto('http://127.0.0.1:3031'+route)
    if case=='slow-media':
        await expect(page.get_by_text('Carregando…',exact=True)).to_be_visible(timeout=20000)
    deadline=time.monotonic()+30
    while not cycle.finished_at and time.monotonic()<deadline:
        await asyncio.sleep(.1)
    assert cycle.started_at and cycle.finished_at,'Missing on_load cycle'
    await expect(page.get_by_text('Carregando…',exact=True)).not_to_be_visible()
    total_ms=round((time.perf_counter()-started)*1000)
    if case=='media-429':
        await expect(page.get_by_text('Muitas solicitações. Tente novamente em 20 segundos.',exact=True)).to_be_visible()
    else:
        cards=page.locator('.activity-card' if section=='library' else '.list-row')
        initial=20 if case=='large' else (5 if section=='library' else 12)
        await expect(cards).to_have_count(initial)
        if case=='large':
            before=sum(CALLS.values())
            await page.get_by_role('button',name='Mostrar mais',exact=True).click()
            await expect(cards).to_have_count(40)
            assert sum(CALLS.values())==before,'Unexpected network call from Show more'
        if section=='lists':
            # Large directories start with public lists; defaults are beyond
            # the first 40 rows and must not be assumed visible by this test.
            title='Lista pública 1' if case=='large' else 'Quero ver / ler'
            rows=page.locator('.list-row').filter(has=page.get_by_text(title,exact=True))
            await rows.first.click()
            await expect(page.locator('.list-media-item .media-card')).to_have_count(1)
            if case=='large':
                await expect(page.locator('select[name=media_id]')).to_have_count(0)
            else:
                await expect(page.locator('select[name=media_id] option')).to_have_count(MODE['size']+1)
    assert CALLS[('GET','/profiles')]==0,'Unneeded people request'
    overflow=await page.evaluate('document.documentElement.scrollWidth > innerWidth')
    await page.screenshot(path=str(OUTPUT/f'biblioteca-listas-{section}-{width}-{case}.png'),full_page=True)
    result=dict(width=width,section=section,case=case,load_cycle_ms=total_ms,
        people_requests=CALLS[('GET','/profiles')],total_fixture_requests=sum(CALLS.values()),
        fixture_writes=sum(count for (method,_),count in CALLS.items() if method!='GET'),
        overflow=overflow,page_errors=errors,cycle_confirmed=True)
    await context.close()
    assert not errors,'Browser reported page errors'
    assert not overflow,'Page overflows horizontally'
    return result


async def main():
    roots=normal_app_roots()
    server=ThreadingHTTPServer(('127.0.0.1',3040),Fixture)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    env=dict(os.environ,XANO_AUTH_URL='http://127.0.0.1:3040',
        XANO_SOCIAL_URL='http://127.0.0.1:3040',COOKIE_SECURE='false',REFLEX_STATE_MANAGER_MODE='memory')
    results=[]
    failure=''
    with (ROOT/'library-lists-browser-server.log').open('w',encoding='utf-8') as log:
        process=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod',
            '--single-port','--frontend-port','3031','--backend-port','3031'],cwd=ROOT,
            env=env,stdout=log,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            import urllib.request
            ready=False
            for _ in range(240):
                if process.poll() is not None: raise RuntimeError('Test server exited')
                try:
                    with urllib.request.urlopen('http://127.0.0.1:3031/login',timeout=1):
                        ready=True
                        break
                except OSError: await asyncio.sleep(1)
            if not ready: raise TimeoutError('Test server startup')
            async with async_playwright() as playwright:
                browser=await playwright.chromium.launch(channel='msedge',headless=True)
                for width in (1440,390):
                    for section in ('library','lists'):
                        cases=['ready','people-429','slow-media','media-429','large']
                        if section=='lists': cases.append('missing-defaults')
                        for case in cases:
                            result=await check(browser,width,section,case)
                            results.append(result)
                            print(json.dumps(result),flush=True)
                await browser.close()
        except Exception as exc:
            failure=type(exc).__name__
            print('VALIDATION_FAILURE: '+failure,flush=True)
        finally:
            stop_process_tree(process)
            server.shutdown()
            print('RESTORING_NORMAL_APP',flush=True)
            restored=await restore_normal_app(roots,'normal-restored-after-library-lists.log')
            (OUTPUT/'biblioteca-listas-browser-2026-10-20.json').write_text(json.dumps(
                dict(layer='browser-with-local-fixtures',remote_validated=False,
                     expected_cases=22,completed=results,failure=failure,normal_restored=restored),
                indent=2),encoding='utf-8')
            print(json.dumps(dict(finished=True,completed=len(results),failure=failure,
                                  normal_restored=restored)),flush=True)


if __name__=='__main__': asyncio.run(main())
