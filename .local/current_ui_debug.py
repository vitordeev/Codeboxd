from playwright.sync_api import sync_playwright
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1280,'height':900})
    page.on('pageerror',lambda err: errors.append(str(err)))
    page.goto('http://localhost:3011/obra/3',wait_until='domcontentloaded',timeout=20000)
    page.locator('.media-detail-hero').wait_for(timeout=20000)
    page.wait_for_timeout(2500)
    text=page.locator('.review-layout').inner_text()
    print('GUEST_RATING_PANEL=', 'Avalie esta obra' in text)
    print('LOGIN_PROMPT=', 'Entre para avaliar e organizar suas obras.' in text)
    print('DETAIL_TITLE=',page.locator('.media-detail-title').inner_text())
    print('TRAILERS=',page.locator('.media-trailer').count())
    page.get_by_role('button',name='Nota 5 de 5').click()
    page.wait_for_function("localStorage.getItem('codeboxd_guest_ratings')?.includes('tmdb:movie:157336')")
    print('GUEST_RATING_SAVED=',page.evaluate("localStorage.getItem('codeboxd_guest_ratings')"))
    print('PAGE_ERRORS=',errors)
    browser.close()