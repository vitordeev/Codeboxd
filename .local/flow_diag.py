import json
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True); page=b.new_page(); page.set_default_timeout(20000); a=json.loads(Path('.local/test-accounts.json').read_text(encoding='utf8'))[0]
 def state(label):
  print(label,'url',page.url,'storage',page.evaluate("() => ({s:Object.entries(sessionStorage).map(([k,v])=>[k,v.length]),cookie:document.cookie.split(';').map(x=>x.trim().split('=')[0])})"),'main',page.locator('main').inner_text()[:250].replace('\n','|'),flush=True)
 page.goto('http://localhost:3012/login',wait_until='commit'); page.locator('input[name=email]').fill(a['email']); page.locator('input[name=password]').fill(a['password']); page.get_by_role('button',name='Entrar',exact=True).click(); page.wait_for_url('**/conta',timeout=30000); page.wait_for_timeout(1500); state('login')
 for route in ['/biblioteca','/feed','/comunidade']:
  page.goto('http://localhost:3012'+route,wait_until='commit'); page.locator('main.site-main').wait_for(); page.wait_for_timeout(1000)
  loading=page.locator('main.site-main > p.text-amber-300')
  if loading.is_visible(): loading.wait_for(state='hidden',timeout=60000)
  state(route)
 b.close()
