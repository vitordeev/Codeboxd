"""Local-only browser check with synthetic Xano responses.

Starts a production test instance on 3031 and a fixture service on 3040.
Uses installed Edge. No real credentials or private API records are involved.
"""
import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from playwright.async_api import async_playwright, expect
import psutil


ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'openspec/changes/otimizar-performance-app/validation'
MODE={'case':'slow-media'}


class Fixture(BaseHTTPRequestHandler):
    def log_message(self,*args): pass

    def do_POST(self): self.respond()
    def do_GET(self): self.respond()

    def respond(self):
        path=self.path.split('?')[0]
        if path=='/media' and MODE['case']=='slow-media': time.sleep(3)
        if path=='/profiles' and MODE['case']=='slow-people': time.sleep(3)
        code=429 if path=='/media' and MODE['case']=='media-429' else 200
        data={
            '/auth/login':{'authToken':'browser-synthetic-token'},
            '/auth/me':{'id':7,'role':'member','username':'browser-test'},
            '/profiles/7':{'profile':{'user_id':7,'username':'browser-test',
                'display_name':'Perfil de teste','bio':'Dados fictícios para validação',
                'avatar_url':'','banner_url':''},
                'interactions':[{'media_id':9,'status':'completed','rating':1.5}],
                'followers':[{'follower_id':8}],'following':[{'followed_id':8}]},
            '/profiles':[{'user_id':8,'username':'amigo-teste','display_name':'Pessoa fictícia'}],
            '/media':[{'id':9,'title':'Livro de teste','media_type':'book','cover_url':''}],
        }
        if path not in data: code=404
        body=json.dumps(data.get(path,{})).encode()
        self.send_response(code)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        if code==429: self.send_header('Retry-After','20')
        self.end_headers()
        self.wfile.write(body)


async def check_case(browser,width,case):
    MODE['case']=case
    context=await browser.new_context(viewport={'width':width,'height':900})
    # Only local application requests are allowed in this browser scenario.
    await context.route('**/*',lambda route: route.continue_() if
        route.request.url.startswith(('http://127.0.0.1:3031/','http://localhost:3031/'))
        else route.abort())
    page=await context.new_page()
    errors=[]
    page.on('pageerror',lambda error: errors.append(type(error).__name__))
    await page.goto('http://127.0.0.1:3031/login')
    await page.locator('input[name=email]').fill('browser@example.invalid')
    await page.locator('input[name=password]').fill('synthetic-password1')
    started=time.perf_counter()
    await page.get_by_role('button',name='Entrar',exact=True).click()
    await expect(page.get_by_role('heading',name='Perfil de teste',exact=True)).to_be_visible(timeout=30000)
    primary_ms=round((time.perf_counter()-started)*1000)
    loading=page.get_by_text('Carregando atividades…' if case=='slow-media' else 'Carregando seguidores…',exact=True)
    if case!='media-429':
        await expect(loading).to_be_visible()
        await page.screenshot(path=str(OUTPUT/f'perfil-{width}-{case}-loading.png'),full_page=True)
    # The editor must respond while optional references are still pending.
    await page.get_by_role('button',name='Editar perfil',exact=True).click()
    await expect(page.get_by_role('dialog')).to_be_visible()
    await page.get_by_role('button',name='Fechar',exact=True).click()
    await expect(page.get_by_role('dialog')).not_to_be_visible()
    editor_during_loading=await loading.is_visible() if case!='media-429' else None
    if case!='media-429':
        assert editor_during_loading, 'Editor was not checked during loading'
    if case=='media-429':
        await expect(page.locator('#atividades').get_by_role('alert')).to_contain_text('20 segundos')
    else:
        await expect(page.locator('#atividades').get_by_text('Livro de teste',exact=True)).to_be_visible(timeout=15000)
    await expect(page.locator('#seguidores').get_by_text('Pessoa fictícia',exact=True)).to_be_visible(timeout=15000)
    overflow=await page.evaluate('document.documentElement.scrollWidth > innerWidth')
    await page.screenshot(path=str(OUTPUT/f'perfil-{width}-{case}-final.png'),full_page=True)
    result=dict(width=width,case=case,primary_visible_ms=primary_ms,
                overflow=overflow,page_errors=errors,editor_open_close=True,
                editor_during_loading=editor_during_loading)
    await context.close()
    assert not errors, 'Browser reported page errors'
    assert not overflow, 'Page overflows horizontally'
    return result


async def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',3040),Fixture)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    env=dict(os.environ,XANO_AUTH_URL='http://127.0.0.1:3040',
             XANO_SOCIAL_URL='http://127.0.0.1:3040',COOKIE_SECURE='false')
    log_path=ROOT/'profile-browser-server.log'
    results=[]
    with log_path.open('w',encoding='utf-8') as log:
        process=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod',
            '--single-port','--frontend-port','3031','--backend-port','3031'],cwd=ROOT,
            env=env,stdout=log,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            import urllib.request
            ready=False
            for _ in range(240):
                if process.poll() is not None: raise RuntimeError('Test server exited; inspect local log')
                try:
                    with urllib.request.urlopen('http://127.0.0.1:3031/login',timeout=1):
                        ready=True
                        break
                except OSError: await asyncio.sleep(1)
            if not ready: raise RuntimeError('Test server startup timed out')
            async with async_playwright() as playwright:
                browser=await playwright.chromium.launch(channel='msedge',headless=True)
                for width in (1440,390):
                    for case in ('slow-media','slow-people','media-429'):
                        result=await check_case(browser,width,case)
                        results.append(result)
                        print(json.dumps(result),flush=True)
                await browser.close()
        finally:
            # Only terminate processes descended from this specific test launcher.
            if process.poll() is None:
                parent=psutil.Process(process.pid)
                children=parent.children(recursive=True)
                for child in reversed(children):
                    try: child.terminate()
                    except psutil.NoSuchProcess: pass
                process.terminate()
                try: process.wait(timeout=10)
                except subprocess.TimeoutExpired: process.kill()
            server.shutdown()
            (OUTPUT/'perfil-browser-2026-10-20.json').write_text(json.dumps(
                dict(layer='browser-with-local-fixtures',remote_validated=False,
                     expected_cases=6,completed=results),indent=2),encoding='utf-8')


if __name__=='__main__': asyncio.run(main())
