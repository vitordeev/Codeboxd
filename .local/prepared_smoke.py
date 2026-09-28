import json
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width':1440,'height':1000})
    page.set_default_timeout(60000)
    errors=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://localhost:3001/')
    page.locator('.featured-card').first.wait_for()
    for width in (1440,390):
        page.set_viewport_size({'width':width,'height':1000})
        page.screenshot(path=f'.local/prepared-home-{width}.png',full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'home overflow'
    page.locator('.featured-card button').first.click()
    page.locator('.media-hero').wait_for()
    print('PASS live TMDB home to details',flush=True)
    account=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
    page.goto('http://localhost:3001/login')
    page.locator('input[name=email]').fill(account['email'])
    page.locator('input[name=password]').fill(account['password'])
    page.locator('button[type=submit]').click()
    page.wait_for_url('**/conta')
    page.get_by_role('button',name='Editar perfil',exact=True).click()
    page.get_by_role('dialog').wait_for()
    page.get_by_role('button',name='Fechar',exact=True).click()
    for route,selector in [('/conta','.profile-panel'),('/feed','.feed-layout'),('/listas','.site-main')]:
        page.goto('http://localhost:3001'+route)
        page.wait_for_timeout(1800)
        page.locator(selector).wait_for()
        if route=='/conta': page.get_by_role('button',name='Editar perfil',exact=True).wait_for()
        if route=='/feed': page.get_by_role('button',name='+ Criar publica\u00e7\u00e3o',exact=True).wait_for()
        if route=='/listas': page.get_by_role('button',name='Criar lista',exact=True).wait_for()
        page.get_by_text('Preparando seu conte\u00fado\u2026',exact=True).wait_for(state='hidden')
        for width in (1440,390):
            page.set_viewport_size({'width':width,'height':1000})
            page.screenshot(path=f'.local/prepared-{route[1:]}-{width}.png',full_page=True)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), route+' overflow'
        if route=='/feed':
            page.get_by_role('button',name='+ Criar publica\u00e7\u00e3o',exact=True).click()
        elif route=='/listas':
            page.get_by_role('button',name='Criar lista',exact=True).click()
        if route!='/conta':
            page.get_by_role('dialog').wait_for()
            assert page.get_by_text('Conte\u00fado n\u00e3o encontrado.',exact=True).count()==0
            page.screenshot(path=f'.local/prepared-{route[1:]}-dialog.png',full_page=True)
            page.get_by_role('button',name='Fechar',exact=True).click()
        print('PASS responsive page and editor',route,flush=True)
    page.get_by_role('button',name='Sair',exact=True).click()
    page.wait_for_url('**/login')
    assert not errors, errors
    print('PASS logout and no JS errors',flush=True)
    browser.close()
