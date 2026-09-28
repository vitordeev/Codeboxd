import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto('http://localhost:3014/',wait_until='domcontentloaded',timeout=60000)
    page.locator('.shelf-skeleton').first.wait_for(state='hidden',timeout=120000)
    page.screenshot(path='.local/home-catalog-desktop.png',full_page=True)
    print(json.dumps({'groups':page.locator('.catalog-group').count(),'cards':page.locator('.shelf-card').count(),'empty':page.locator('.shelf-empty').count(),'overflow':page.evaluate('document.documentElement.scrollWidth > innerWidth'),'errors':errors},ensure_ascii=False),flush=True)
    rail=page.locator('.catalog-rail').filter(has=page.locator('.shelf-card')).first
    if rail.count():
        shelf=rail.locator('..')
        shelf.locator('.shelf-arrow').last.click()
        page.wait_for_timeout(600)
        print('arrow_scroll',rail.evaluate('(el)=>el.scrollLeft'),flush=True)
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path='.local/home-catalog-mobile.png',full_page=True)
    print('mobile_overflow',page.evaluate('document.documentElement.scrollWidth > innerWidth'),flush=True)
    page.get_by_role('link',name='Livros',exact=True).click()
    print('books_anchor',page.url.endswith('#home-livros'),flush=True)
    browser.close()
