import json
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True); page=b.new_page(); page.set_default_timeout(15000)
 errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
 a=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
 page.goto('http://localhost:3011/login'); page.locator('input[name=email]').fill(a['email']); page.locator('input[name=password]').fill(a['password']); page.get_by_role('button',name='Entrar',exact=True).click(); page.wait_for_url('**/conta')
 print('PROFILE',page.get_by_role('button',name='Sair',exact=True).count(),flush=True)
 page.goto('http://localhost:3011/comunidade',wait_until='domcontentloaded'); page.wait_for_timeout(4000)
 print('URL',page.url,flush=True); print('LOGOUT_BUTTONS',page.get_by_role('button',name='Sair',exact=True).count(),flush=True)
 print('BODY',page.locator('body').inner_text()[:2000],flush=True); print('ERRORS',errors,flush=True)
 b.close()