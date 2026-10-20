"""Validate paginated library in production Reflex with local synthetic services."""
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
from tools.real_login_measurement import VisitCycle, normal_app_roots, restore_normal_app, stop_process_tree

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'openspec/changes/otimizar-performance-app/validation'
MODE={}
CALLS=Counter()
CURSORS=[]
CASES=('empty','small','exact','large','slow-initial','slow-next','initial-error','next-error','next-429')


class Fixture(BaseHTTPRequestHandler):
    def log_message(self,*args): pass

    def do_GET(self):
        parsed=urlsplit(self.path)
        CALLS[parsed.path]+=1
        status=200
        if parsed.path=='/auth/me':
            data={'id':7,'role':'member','account_status':'active'}
        elif parsed.path=='/library':
            cursor=int(parse_qs(parsed.query).get('after_id',['0'])[0])
            CURSORS.append(cursor)
            case=MODE['case']
            if (case=='slow-initial' and cursor==0) or (case=='slow-next' and cursor==20):
                time.sleep(2)
            fail=((case=='initial-error' and cursor==0) or
                  (case in ('next-error','next-429') and cursor==20)) and not MODE.get('failed')
            if fail:
                MODE['failed']=True
                status=429 if case=='next-429' else 503
                data={}
            else:
                size=MODE['size']
                data={'items':[dict(id=i,user_id=7,media_id=i,status='completed',rating=3.5,
                    review='Crítica fictícia',spoiler=True,media_title=f'Livro fictício {i}',
                    media_type='book',media_cover_url='',media_year=2020)
                    for i in range(cursor+1,min(cursor+20,size)+1)],'has_more':cursor+20<size}
        else:
            status=404; data={}
        body=json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        if status==429: self.send_header('Retry-After','4')
        self.end_headers()
        try: self.wfile.write(body)
        except (BrokenPipeError,ConnectionResetError): pass


async def check(browser,width,case):
    MODE.clear(); MODE.update(case=case,size={'empty':0,'small':5,'exact':20,'large':250}.get(case,25))
    CALLS.clear(); CURSORS.clear()
    context=await browser.new_context(viewport={'width':width,'height':900})
    await context.add_cookies([dict(name='codeboxd_auth',value='local-fixture-token',url='http://127.0.0.1:3031')])
    await context.route('**/*',lambda route: route.continue_() if
        urlsplit(route.request.url).hostname in ('localhost','127.0.0.1') else route.abort())
    page=await context.new_page(); errors=[]
    page.on('pageerror',lambda error: errors.append(type(error).__name__))
    cycle=VisitCycle()
    page.on('websocket',lambda socket: socket.on('framereceived',cycle.received))
    await page.goto('http://127.0.0.1:3031/biblioteca')
    loading=page.get_by_text('Carregando…',exact=True)
    empty=page.get_by_text('Sua biblioteca está vazia. Descubra uma obra e salve sua experiência.',exact=True)
    if case=='slow-initial':
        await expect(loading).to_be_visible(timeout=20000)
        await expect(empty).not_to_be_visible()
    deadline=time.monotonic()+30
    while not cycle.finished_at and time.monotonic()<deadline: await asyncio.sleep(.1)
    assert cycle.started_at and cycle.finished_at,'Missing visit cycle'
    cards=page.locator('.activity-card')
    if case=='initial-error':
        await expect(page.get_by_role('alert')).to_be_visible()
        await expect(empty).not_to_be_visible()
        await expect(cards).to_have_count(0)
        await page.get_by_role('button',name='Tentar novamente',exact=True).click()
    initial=min(20,MODE['size'])
    await expect(cards).to_have_count(initial)
    if case=='empty': await expect(empty).to_be_visible()
    else:
        await expect(page.get_by_role('link',name='Livro fictício 1',exact=True)).to_have_attribute('href','/obra/1')
        await expect(cards.first).to_contain_text('3,5')
    initial_reads=CALLS['/library']
    more=page.get_by_role('button',name='Mostrar mais',exact=True)
    if MODE['size']<=20:
        await expect(more).not_to_be_visible()
        assert initial_reads==1
    elif case in ('next-error','next-429'):
        await more.click()
        await expect(page.get_by_role('alert')).to_be_visible()
        await expect(cards).to_have_count(20)
        assert CURSORS==[0,20]
        retry=page.get_by_role('button',name='Tentar novamente',exact=True)
        if case=='next-429':
            await retry.click()
            await expect(retry).to_be_enabled()
            assert CURSORS==[0,20],'Cooldown made an extra request'
            await asyncio.sleep(4.2)
        await retry.click()
        await expect(cards).to_have_count(25)
        await expect(page.get_by_role('alert')).not_to_be_visible()
        assert CURSORS==[0,20,20]
    elif case=='slow-next':
        await more.click()
        busy=page.get_by_role('button',name='Carregando…',exact=True)
        await expect(busy).to_be_disabled()
        await expect(cards).to_have_count(20)
        await expect(page.get_by_role('link',name='Livro fictício 1',exact=True)).to_be_visible()
        await expect(cards).to_have_count(25)
        assert CURSORS==[0,20]
    else:
        for count in range(20,MODE['size'],20):
            before=CALLS['/library']
            await more.click()
            await expect(cards).to_have_count(min(count+20,MODE['size']))
            assert CALLS['/library']==before+1,'Show more must read one page'
        ids=await cards.evaluate_all('(cards)=>cards.map(card=>card.querySelector("a").getAttribute("href"))')
        assert len(ids)==len(set(ids))==MODE['size'],'Duplicate/missing cards'
        if case=='large': assert CURSORS==list(range(0,250,20))
    await expect(more).not_to_be_visible()
    assert not any(path!='/library' and path!='/auth/me' for path in CALLS),'Unexpected data endpoint'
    assert not errors,'Browser reported page errors'
    overflow=await page.evaluate('document.documentElement.scrollWidth > innerWidth')
    assert not overflow,'Horizontal page overflow'
    await page.screenshot(path=str(OUTPUT/f'biblioteca-paginada-{width}-{case}.png'),full_page=True)
    result=dict(width=width,case=case,initial_data_reads=initial_reads,library_reads=CALLS['/library'],
        auth_reads=CALLS['/auth/me'],cursors=list(CURSORS),final_cards=await cards.count(),
        page_errors=errors,overflow=overflow,passed=True)
    await context.close()
    return result


async def main():
    roots=normal_app_roots()
    server=ThreadingHTTPServer(('127.0.0.1',3040),Fixture)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    env=dict(os.environ,XANO_AUTH_URL='http://127.0.0.1:3040',XANO_SOCIAL_URL='http://127.0.0.1:3040',
        COOKIE_SECURE='false',REFLEX_STATE_MANAGER_MODE='memory',LIBRARY_PAGINATION_ENABLED='true')
    results=[]; failure=''; restored=False
    with (ROOT/'library-pagination-browser-server.log').open('w',encoding='utf-8') as log:
        process=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod',
            '--single-port','--frontend-port','3031','--backend-port','3031'],cwd=ROOT,
            env=env,stdout=log,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            import urllib.request
            for _ in range(240):
                if process.poll() is not None: raise RuntimeError('Test server exited')
                try:
                    with urllib.request.urlopen('http://127.0.0.1:3031/login',timeout=1): break
                except OSError: await asyncio.sleep(1)
            else: raise TimeoutError('Test server startup')
            async with async_playwright() as playwright:
                browser=await playwright.chromium.launch(channel='msedge',headless=True)
                for width in (1440,390):
                    for case in CASES:
                        result=await check(browser,width,case)
                        results.append(result); print(json.dumps(result),flush=True)
                await browser.close()
        except Exception as exc:
            failure=type(exc).__name__+': '+str(exc)
            print('VALIDATION_FAILURE: '+failure,flush=True)
        finally:
            stop_process_tree(process); server.shutdown()
            print('RESTORING_NORMAL_APP',flush=True)
            restored=await restore_normal_app(roots,'normal-restored-after-library-pagination.log')
            (OUTPUT/'biblioteca-paginada-browser-2026-10-20.json').write_text(json.dumps(dict(
                layer='browser-with-local-fixtures',remote_validated=False,expected_cases=18,
                completed=results,failure=failure,normal_restored=restored),indent=2),encoding='utf-8')
            print(json.dumps(dict(completed=len(results),failure=failure,normal_restored=restored)),flush=True)
    if failure or not restored: raise SystemExit(1)


if __name__=='__main__': asyncio.run(main())
