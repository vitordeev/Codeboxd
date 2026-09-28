import json
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True); page=b.new_page(); page.set_default_timeout(15000)
 errs=[]; page.on('pageerror',lambda e:errs.append(str(e)))
 a=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
 page.goto('http://localhost:3012/login',wait_until='commit')
 page.locator('input[name=email]').wait_for(); page.locator('input[name=email]').fill(a['email']); page.locator('input[name=password]').fill(a['password']); page.get_by_role('button',name='Entrar',exact=True).click()
 page.wait_for_timeout(10000)
 print('url',page.url,'text',page.locator('body').inner_text()[:1200],'errors',errs,flush=True)
 b.close()
