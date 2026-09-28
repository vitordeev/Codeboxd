from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.goto('http://localhost:3013/',wait_until='domcontentloaded')
    page.get_by_role('button',name='Buscar',exact=True).wait_for(state='visible')
    page.wait_for_function("document.querySelector('.media-shelf') || [...document.querySelectorAll('[role=status]')].some(e => !e.textContent.startsWith('Carregando'))",timeout=60000)
    print('cards',page.locator('.media-shelf .media-card').count())
    print('status',page.locator('[role=status]').all_text_contents())
    page.screenshot(path='.local/discovery-current.png',full_page=True)
    browser.close()
