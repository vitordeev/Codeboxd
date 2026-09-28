from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page()
    page.goto('http://localhost:3002/obra?external_source=tmdb&external_id=157336&media_type=movie')
    page.wait_for_timeout(12000)
    print('url',page.url)
    print('title',page.title())
    print('notices',page.locator('[role=status]').all_inner_texts())
    print('body',page.locator('body').inner_text()[:3000])
    browser.close()
