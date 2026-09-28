import json
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True); page=b.new_page(); page.set_default_timeout(20000)
 a=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
 def report(label):
  snap=page.evaluate('''() => ({session:Object.entries(sessionStorage).map(([k,v])=>[k,Boolean(v),v.length]), local:Object.entries(localStorage).map(([k,v])=>[k,Boolean(v),v.length]), cookie:document.cookie.includes('codeboxd_auth=')})''')
  print(label,'logout=',page.get_by_role('button',name='Sair',exact=True).count(),'snapshot=',snap,'main=',page.locator('main').inner_text()[:180].replace('\n','|'),flush=True)
 page.goto('http://localhost:3011/login'); page.locator('input[name=email]').fill(a['email']); page.locator('input[name=password]').fill(a['password']); page.get_by_role('button',name='Entrar',exact=True).click(); page.wait_for_url('**/conta'); page.locator('.profile-panel').wait_for(); page.get_by_role('button',name='Sair',exact=True).wait_for(); report('LOGIN')
 for route in ['/biblioteca','/feed','/comunidade','/listas']:
  page.goto('http://localhost:3011'+route,wait_until='domcontentloaded'); page.wait_for_timeout(1600); report(route)
 b.close()