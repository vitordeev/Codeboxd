import json
from pathlib import Path
from playwright.sync_api import sync_playwright

errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page()
    page.set_default_timeout(90000)
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('http://localhost:3001/')
    page.get_by_role('heading',name='Sua próxima história começa aqui.').wait_for()
    page.wait_for_timeout(2500)
    page.screenshot(path='.local/discovery-desktop.png',full_page=True)
    print('PASS discovery page',flush=True)
    account=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
    page.goto('http://localhost:3001/login')
    page.locator('input[name=email]').fill(account['email'])
    page.locator('input[name=password]').fill(account['password'])
    page.locator('button[type=submit]').click()
    page.wait_for_url('**/conta',timeout=90000)
    page.get_by_role('button',name='Salvar perfil').wait_for(timeout=90000)
    print('PASS browser login and own profile',flush=True)
    for route,title in [('/biblioteca','Minha biblioteca'),('/feed','Entre histórias'),('/comunidade','Encontre sua comunidade'),('/listas','Listas para cada universo')]:
        page.goto('http://localhost:3001'+route)
        page.get_by_role('heading',name=title,exact=True).wait_for()
        page.get_by_role('button',name='Sair',exact=True).wait_for()
        page.get_by_text('Preparando seu conteúdo…',exact=True).wait_for(state='hidden')
        print('PASS route',route,flush=True)
    page.goto('http://localhost:3001/conta')
    page.get_by_role('button',name='Sair',exact=True).click()
    page.wait_for_url('**/login',timeout=90000)
    page.goto('http://localhost:3001/biblioteca')
    page.wait_for_url('**/login',timeout=90000)
    print('PASS logout and protected route',flush=True)
    page.set_viewport_size({'width':390,'height':844})
    page.goto('http://localhost:3001/')
    page.get_by_role('heading',name='Sua próxima história começa aqui.').wait_for()
    page.screenshot(path='.local/discovery-mobile.png',full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Mobile horizontal overflow'
    assert not errors, errors
    print('PASS mobile layout and no browser JavaScript exceptions',flush=True)
    browser.close()
