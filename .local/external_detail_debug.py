from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True); page=b.new_page(); page.set_default_timeout(15000)
 page.goto('http://localhost:3001/obra?external_source=tmdb&external_id=157336&media_type=movie')
 page.wait_for_timeout(4000)
 print('url',page.url,'title',page.locator('.media-hero h2').inner_text() if page.locator('.media-hero h2').count() else 'empty',flush=True)
 print('notice',page.locator('[role=status]').all_inner_texts(),flush=True)
 b.close()
