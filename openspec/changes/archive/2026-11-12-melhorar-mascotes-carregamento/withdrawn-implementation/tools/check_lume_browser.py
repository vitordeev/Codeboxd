"""Verify Lume in real Reflex pages with isolated production and fictional APIs."""
import argparse
import asyncio
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import urllib.request
from playwright.async_api import async_playwright, expect
from tools.feed_lists_browser import Fixture
from tools.real_login_measurement import stop_process_tree

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'openspec/changes/melhorar-mascotes-carregamento'

async def run(frontend):
    frontend=frontend.resolve()
    if not frontend.is_relative_to((ROOT/'.local/frontends').resolve()) or not frontend.is_dir():
        raise ValueError('Use an existing isolated frontend directory')
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1',3031))==0:
            raise RuntimeError('Isolated preview port 3031 is already in use')
    output=BASE/'validation'/('integration-'+str(os.getpid()))
    output.mkdir(parents=True,exist_ok=False)
    api=ThreadingHTTPServer(('127.0.0.1',0),Fixture)
    threading.Thread(target=api.serve_forever,daemon=True).start()
    auth='http://127.0.0.1:'+str(api.server_port)
    env=dict(os.environ,XANO_AUTH_URL=auth,XANO_SOCIAL_URL=auth,COOKIE_SECURE='false',
        REFLEX_STATE_MANAGER_MODE='memory',DEEPL_API_KEY='',TMDB_READ_TOKEN='',
        DEFAULT_LIST_IDENTITY_ENABLED='false',REFLEX_WEB_WORKDIR=str(frontend),
        REFLEX_USE_NPM='true',REFLEX_APP_MODULE_IMPORT='tools.lume_browser_fixture')
    origin='http://127.0.0.1:3031'
    rows=[];errors=[];failure=''
    with (output/'server.log').open('w',encoding='utf-8') as log:
        proc=subprocess.Popen([sys.executable,'-m','reflex','run','--env','prod','--single-port',
            '--frontend-port','3031','--backend-port','3031'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            print('STARTING_ISOLATED_LUME_PREVIEW',flush=True)
            for _ in range(240):
                if proc.poll() is not None:raise RuntimeError('Preview stopped; inspect server.log')
                try:
                    with urllib.request.urlopen(origin+'/login',timeout=1):break
                except OSError:await asyncio.sleep(1)
            else:raise TimeoutError('Preview startup')
            async with async_playwright() as pw:
                browser=await pw.chromium.launch(channel='msedge',headless=True)
                try:
                    context=await browser.new_context(viewport={'width':1440,'height':1000})
                    await context.route('**/*',lambda route: route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
                    page=await context.new_page()
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    for route in ['/login','/cadastro']:
                        await page.goto(origin+route)
                        await expect(page.locator('[data-illustration=onboarding]')).to_have_count(1)
                        for width in [360,1440]:
                            await page.set_viewport_size({'width':width,'height':1000})
                            await page.screenshot(path=str(output/(route.strip('/')+'-'+str(width)+'.png')),full_page=True)
                            assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
                            assert await page.locator('img[src*="mascot.png"]').count()==0
                            rows.append(dict(route=route,width=width,scene='onboarding',passed=True))
                    await page.goto(origin+'/')
                    await page.get_by_role('textbox',name='Buscar título').fill('zzzz-inexistente-xyz')
                    await page.get_by_role('button',name='Buscar',exact=True).click()
                    await expect(page.locator('[data-illustration=no-results]')).to_be_visible(timeout=20000)
                    rows.append(dict(route='/',state='search-no-results',passed=True))
                    await page.screenshot(path=str(output/'no-results.png'),full_page=True)
                    await page.goto(origin+'/login')
                    await page.locator('input[name=email]').fill('lume@example.invalid')
                    await page.locator('input[name=password]').fill('fictional-password1')
                    await page.get_by_role('button',name='Entrar',exact=True).click()
                    await expect(page.get_by_role('button',name='Sair',exact=True)).to_be_visible(timeout=20000)
                    for route in ['/biblioteca','/feed']:
                        await page.goto(origin+route)
                        await expect(page.locator('[data-illustration=empty]')).to_be_visible(timeout=20000)
                        for width in [360,1440]:
                            await page.set_viewport_size({'width':width,'height':1000})
                            assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
                            await page.screenshot(path=str(output/(route.strip('/')+'-'+str(width)+'.png')),full_page=True)
                            rows.append(dict(route=route,width=width,scene='empty',passed=True))
                    await context.close()
                finally:await browser.close()
            assert not errors,errors
        except Exception as err:
            failure=type(err).__name__+': '+str(err)
            print(failure,flush=True)
        finally:
            stop_process_tree(proc)
            api.shutdown()
    report=dict(layer='real_reflex_production_local_fictional_backend',cases=rows,javascript_errors=errors,failure=failure,passed=not failure and not errors,normal_server_modified=False)
    (output/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(output=str(output),passed=report['passed'],cases=len(rows),failure=failure)),flush=True)
    return 0 if report['passed'] else 1

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frontend-workdir',type=Path,required=True)
    args=parser.parse_args()
    raise SystemExit(asyncio.run(run(args.frontend_workdir)))
