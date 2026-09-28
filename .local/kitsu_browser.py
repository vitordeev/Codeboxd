import json,time,urllib.request
from playwright.sync_api import sync_playwright
for _ in range(60):
    try:
        with urllib.request.urlopen('http://localhost:3014/',timeout=2) as r:
            if r.status==200: break
    except OSError: time.sleep(1)
else: raise SystemExit('Preview unavailable')
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto('http://localhost:3014/',wait_until='domcontentloaded')
    page.locator('#anime_rated .shelf-card').first.wait_for(timeout=120000)
    print('anime_home_cards',page.locator('#anime_rated .shelf-card').count(),flush=True)
    page.locator('#home-animes').scroll_into_view_if_needed()
    page.wait_for_function("Array.from(document.querySelectorAll('#anime_rated img')).some(img => img.complete && img.naturalWidth > 0)",timeout=30000)
    print('anime_covers_loaded',page.locator('#anime_rated img').evaluate_all('(items)=>items.filter(i=>i.complete && i.naturalWidth>0).length'),flush=True)
    page.screenshot(path='.local/kitsu-home-desktop.png')
    page.locator('input[name=query]').fill('Cowboy Bebop')
    page.get_by_role('button',name='Buscar',exact=True).click()
    page.locator('.catalog-grid .media-card').first.wait_for(timeout=90000)
    page.get_by_role('button',name='Cowboy Bebop Anime',exact=False).first.click()
    page.wait_for_url('**/obra?**',timeout=20000)
    page.locator('.media-detail-title').filter(has_text='Cowboy Bebop').wait_for(timeout=30000)
    page.screenshot(path='.local/kitsu-detail-desktop.png')
    print('detail_title',page.locator('.media-detail-title').inner_text(),flush=True)
    print('facts',page.locator('.media-facts').inner_text(),flush=True)
    print('page_errors',json.dumps(errors),flush=True)
    assert not errors
    assert 'Kitsu ID' not in page.locator('.media-facts').inner_text()
    browser.close()
