from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.goto('http://localhost:3014/',wait_until='domcontentloaded')
    page.locator('.shelf-skeleton').first.wait_for(state='hidden',timeout=120000)
    page.wait_for_timeout(3000)
    page.screenshot(path='.local/home-catalog-desktop-top.png')
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path='.local/home-catalog-mobile-top.png')
    page.locator('#home-livros').scroll_into_view_if_needed()
    page.wait_for_timeout(3000)
    page.screenshot(path='.local/home-catalog-mobile-books.png')
    print('loaded_images',page.locator('img').evaluate_all('(images)=>images.filter(i=>i.complete && i.naturalWidth>0).length'),flush=True)
    card=page.locator('#books_fiction .shelf-card').first
    if card.count():
        card.click()
        page.wait_for_url('**/obra?**')
        print('book_route', 'media_type=book' in page.url,flush=True)
    browser.close()
