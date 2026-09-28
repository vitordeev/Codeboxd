from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True); page=b.new_page(); page.goto('http://localhost:3001/')
 page.locator('input[name=query]').fill('Interestelar')
 print(page.locator('input[name=query]').evaluate('(e)=>e.outerHTML'),flush=True)
 print(page.locator('form').first.evaluate('(e)=>e.outerHTML.slice(0,1000)'),flush=True)
 print('formdata',page.locator('form').first.evaluate('(e)=>new FormData(e).get("query")'),flush=True)
 b.close()
