"""Validate the published library endpoint through a bounded local proxy.

The user enters credentials only in a visible temporary Edge window. Request
bodies and cookies are forwarded in memory and never logged or saved. The
report contains status codes, timings, counts and boolean contract checks only.
"""
import asyncio
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

import httpx
from dotenv import load_dotenv
from playwright.async_api import async_playwright, expect

from tools.performance_probe import safe_endpoint
from tools.real_login_measurement import normal_app_roots, restore_normal_app, stop_process_tree

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'openspec/changes/otimizar-performance-app/validation/biblioteca-paginada-xano-real-2026-10-20.json'
ALLOWED={('POST','/auth/auth/login'),('GET','/auth/auth/me'),('GET','/social/library')}


class Probe:
    def __init__(self):
        self.lock=threading.Lock(); self.calls=0; self.login_attempts=0
        self.events=[]; self.pages=[]; self.failures=0; self.rate_limited=False
        self.started=time.perf_counter()

    def record(self,method,path,status,started,*,contract=None):
        with self.lock:
            self.calls+=1
            if method=='POST': self.login_attempts+=1
            self.events.append(dict(method=method,endpoint=safe_endpoint(path),status=status,
                duration_ms=round((time.perf_counter()-started)*1000,2)))
            if status==429: self.rate_limited=True
            if contract is not None:
                self.pages.append(contract)


def handler_class(probe,bases):
    class Proxy(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def do_GET(self): self.forward()
        def do_POST(self): self.forward()

        def reply(self,status,body=b'{}',headers=None):
            self.send_response(status); self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(body)))
            for key,value in (headers or {}).items(): self.send_header(key,value)
            self.end_headers()
            try: self.wfile.write(body)
            except (BrokenPipeError,ConnectionResetError): pass

        def forward(self):
            parsed=urlsplit(self.path); path=parsed.path
            allowed=((self.command,path) in ALLOWED or
                     (self.command=='GET' and re.fullmatch(r'/social/profiles/[0-9]+',path)))
            if not allowed or parsed.fragment:
                probe.record(self.command,path,403,time.perf_counter())
                probe.failures+=1; self.reply(403); return
            if path=='/social/library':
                params=parse_qs(parsed.query,keep_blank_values=True)
                if set(params)-{'after_id'} or len(params.get('after_id',[]))!=1 or not params['after_id'][0].isdigit():
                    probe.record(self.command,path,400,time.perf_counter())
                    probe.failures+=1; self.reply(400); return
            elif parsed.query:
                probe.record(self.command,path,400,time.perf_counter())
                probe.failures+=1; self.reply(400); return
            if probe.rate_limited:
                probe.record(self.command,path,429,time.perf_counter())
                self.reply(429,headers={'Retry-After':'1'}); return
            if probe.calls>=24 or (self.command=='POST' and probe.login_attempts>=3):
                probe.record(self.command,path,429,time.perf_counter())
                probe.failures+=1; self.reply(429,headers={'Retry-After':'20'}); return
            group,relative=path.lstrip('/').split('/',1)
            headers={k:self.headers[k] for k in ('Authorization','Content-Type','Accept') if self.headers.get(k)}
            length=int(self.headers.get('Content-Length','0'))
            if not 0<=length<=65536:
                probe.failures+=1; self.reply(413); return
            body=self.rfile.read(length) if length else None
            start=time.perf_counter()
            try:
                with httpx.Client(timeout=15,follow_redirects=False) as client:
                    upstream=client.request(self.command,bases[group].rstrip('/')+'/'+relative,
                        params=parse_qs(parsed.query,keep_blank_values=True) if parsed.query else None,
                        headers=headers,content=body)
                contract=None
                if path=='/social/library' and upstream.status_code==200:
                    try:
                        payload=upstream.json(); items=payload['items']; ids=[x['id'] for x in items]
                        owners=[x['user_id'] for x in items]
                        after=int(parse_qs(parsed.query).get('after_id',['0'])[0])
                        valid=(isinstance(items,list) and len(items)<=20
                            and type(payload.get('has_more')) is bool
                            and (not payload['has_more'] or len(items)==20)
                            and all(type(value) is int for value in ids)
                            and ids==sorted(set(ids)) and all(value>after for value in ids)
                            and len(set(owners))<=1
                            and all(x.get('status') in ('planned','in_progress','completed','dropped')
                                    and type(x.get('media_id')) is int and isinstance(x.get('media_title'),str)
                                    for x in items))
                        contract=dict(item_count=len(items),has_more=payload['has_more'],
                                      ids_ordered_after_cursor=ids==sorted(set(ids)) and all(x>after for x in ids),
                                      one_owner=len(set(owners))<=1,shape_valid=valid)
                        if not valid: probe.failures+=1
                    except (ValueError,TypeError,KeyError):
                        contract=dict(shape_valid=False); probe.failures+=1
                probe.record(self.command,self.path,upstream.status_code,start,contract=contract)
                response_headers={k:v for k,v in upstream.headers.items()
                    if k.lower() in ('set-cookie','retry-after','cache-control')}
                self.reply(upstream.status_code,upstream.content,response_headers)
            except httpx.RequestError:
                probe.record(self.command,self.path,0,start); self.reply(502)
    return Proxy


async def main():
    load_dotenv(ROOT/'.env')
    bases={key:os.getenv(env,'').strip() for key,env in
           (('auth','XANO_AUTH_URL'),('social','XANO_SOCIAL_URL'))}
    if any(not value.startswith('https://') for value in bases.values()):
        raise RuntimeError('Configured remote HTTPS services are required')
    roots=normal_app_roots(); probe=Probe()
    proxy=ThreadingHTTPServer(('127.0.0.1',3041),handler_class(probe,bases))
    threading.Thread(target=proxy.serve_forever,daemon=True).start()
    env=dict(os.environ,XANO_AUTH_URL='http://127.0.0.1:3041/auth',
        XANO_SOCIAL_URL='http://127.0.0.1:3041/social',COOKIE_SECURE='false',
        REFLEX_STATE_MANAGER_MODE='memory',LIBRARY_PAGINATION_ENABLED='true')
    failure=''; restored=False; user_logged_in=False; browser=None; context=None
    with (ROOT/'real-library-validation-server.log').open('w',encoding='utf-8') as log:
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
                browser=await playwright.chromium.launch(channel='msedge',headless=False)
                context=await browser.new_context(viewport={'width':1440,'height':900})
                page=await context.new_page()
                await context.route('**/*',lambda route: route.continue_() if
                    urlsplit(route.request.url).hostname in ('localhost','127.0.0.1') else route.abort())
                await page.goto('http://127.0.0.1:3031/login')
                print('READY_FOR_USER_LOGIN: Entre na janela temporaria do Edge. Nao envie credenciais pelo chat.',flush=True)
                try:
                    await expect(page.get_by_role('button',name='Sair',exact=True)).to_be_visible(timeout=600000)
                    user_logged_in=True
                    # Ignore harmless, locally blocked reference reads from /conta.
                    # Only calls triggered by the library screen count toward this test.
                    probe.failures=0
                    await page.locator('footer a[href="/biblioteca"]').click()
                    await expect(page.get_by_role('heading',name='Minha biblioteca')).to_be_visible(timeout=30000)
                    deadline=time.monotonic()+30
                    while not probe.pages and time.monotonic()<deadline:
                        await asyncio.sleep(.1)
                    if not probe.pages:
                        failure='library-request-not-triggered'
                        raise RuntimeError(failure)
                    await expect(page.locator('.activity-card')).to_have_count(
                        min(20,probe.pages[0]['item_count']),timeout=30000)
                    if not probe.pages or not probe.pages[0].get('shape_valid'):
                        failure='invalid-first-page-contract'
                    elif probe.pages[0]['has_more']:
                        before=len(probe.pages)
                        await page.get_by_role('button',name='Mostrar mais',exact=True).click()
                        deadline=time.monotonic()+30
                        while len(probe.pages)<before+1 and time.monotonic()<deadline:
                            await asyncio.sleep(.1)
                        if len(probe.pages)<before+1 or not probe.pages[-1].get('shape_valid'):
                            failure='invalid-continuation-contract'
                        else:
                            await expect(page.locator('.activity-card')).to_have_count(
                                probe.pages[0]['item_count']+probe.pages[-1]['item_count'],timeout=30000)
                    if probe.rate_limited: failure='remote-429'
                    if probe.failures: failure=failure or 'local-proxy-denied-or-shape-invalid'
                except Exception as exc:
                    failure=failure or type(exc).__name__
                await context.clear_cookies(); await browser.close(); browser=None
        except Exception as exc:
            failure=type(exc).__name__
        finally:
            stop_process_tree(process); proxy.shutdown()
            restored=await restore_normal_app(roots,'normal-restored-after-library-real-xano.log')
            OUTPUT.write_text(json.dumps(dict(layer='published-xano-through-bounded-local-proxy',
                workspace=147717,endpoint_published=True,user_logged_in=user_logged_in,
                requests=probe.events,pages=probe.pages,proxy_rejections=probe.failures,
                rate_limited=probe.rate_limited,failure=failure,normal_restored=restored),indent=2),
                encoding='utf-8')
            print(json.dumps(dict(request_count=len(probe.events),pages=probe.pages,
                proxy_rejections=probe.failures,rate_limited=probe.rate_limited,
                failure=failure,normal_restored=restored)),flush=True)
    if failure or not user_logged_in or not probe.pages or probe.failures or not restored:
        raise SystemExit(1)


if __name__=='__main__': asyncio.run(main())
