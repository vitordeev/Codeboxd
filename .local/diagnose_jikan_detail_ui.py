from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page()
    page.set_default_timeout(60000)
    page.goto('http://localhost:3001/obra?external_source=jikan&external_id=1&media_type=anime')
    page.locator('.media-detail-title').wait_for()
    print('detail:', page.locator('.media-detail-title').inner_text())
    print('description:', bool(page.locator('.media-detail-description').inner_text().strip()))
    browser.close()
