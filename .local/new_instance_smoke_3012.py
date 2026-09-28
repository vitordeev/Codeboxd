import json
from pathlib import Path
from playwright.sync_api import sync_playwright
base='http://localhost:3012'
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page(); page.set_default_timeout(30000)
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(base+'/',wait_until='domcontentloaded')
    page.get_by_role('button',name='Buscar',exact=True).wait_for()
    page.wait_for_timeout(2500)
    assert page.get_by_role('link',name='Entrar').count()==1
    for width in (1440,390):
        page.set_viewport_size({'width':width,'height':900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'home overflow at '+str(width)
    print('PASS public home and responsive layout',flush=True)
    page.set_viewport_size({'width':1440,'height':1000})
    page.locator('input[name=query]').fill('Interestelar')
    page.locator('input[name=kind][value=movie]').check()
    page.get_by_role('button',name='Buscar',exact=True).click()
    page.get_by_role('heading',name='Resultados da busca').wait_for()
    page.locator('button.media-card').first.click()
    page.locator('.media-detail-hero').wait_for()
    assert 'Interestelar' in page.locator('.media-detail-title').inner_text()
    print('PASS public search and detail',flush=True)
    accounts=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))
    account=accounts[0]
    page.goto(base+'/login')
    page.locator('input[name=email]').fill(account['email'])
    page.locator('input[name=password]').fill(account['password'])
    page.get_by_role('button',name='Entrar',exact=True).click()
    page.wait_for_url('**/conta',timeout=30000)
    page.locator('.profile-panel').wait_for()
    print('PASS test-account login and profile',flush=True)
    for route,selector in [('/biblioteca','.site-main'),('/feed','.feed-layout'),('/comunidade','.site-main'),('/listas','.site-main')]:
        page.goto(base+route,wait_until='domcontentloaded')
        page.get_by_role('button',name='Sair',exact=True).wait_for()
        page.locator(selector).wait_for()
        page.wait_for_timeout(500)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),route+' overflow'
        print('PASS route',route,flush=True)
    page.goto(base+'/conta')
    page.get_by_role('button',name='Sair',exact=True).click()
    page.wait_for_url('**/login',timeout=20000)
    page.goto(base+'/biblioteca')
    page.wait_for_url('**/login',timeout=20000)
    assert not errors,errors
    print('PASS logout, protected library, and no JavaScript errors',flush=True)
    browser.close()
