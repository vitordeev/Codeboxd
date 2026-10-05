import json
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True); page=b.new_page(); page.set_default_timeout(15000)
 errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
 a=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
 page.goto('http://localhost:3012/login',wait_until='domcontentloaded'); page.locator('input[name=email]').fill(a['email']); page.locator('input[name=password]').fill(a['password']); page.get_by_role('button',name='Entrar',exact=True).click(); page.wait_for_url('**/conta'); page.locator('.profile-panel').wait_for(); page.get_by_role('button',name='Sair',exact=True).wait_for()
 for route in ['/biblioteca','/feed','/comunidade','/listas']:
  page.goto('http://localhost:3012'+route,wait_until='domcontentloaded'); page.get_by_role('button',name='Sair',exact=True).wait_for(timeout=15000)
  loading=page.get_by_text('Carregando…',exact=True)
  if loading.count(): loading.wait_for(state='hidden',timeout=30000)
  page.wait_for_timeout(300)
  print(route,'url=',page.url,'logout=',page.get_by_role('button',name='Sair',exact=True).count(),'text=',page.locator('main').inner_text()[:180].replace('\n',' | '),flush=True)
 print('errors=',errors,flush=True); b.close()
