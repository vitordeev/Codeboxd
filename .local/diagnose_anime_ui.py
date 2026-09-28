from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page()
    page.set_default_timeout(60000)
    page.goto('http://localhost:3001/')
    page.locator('input[aria-label="Buscar título"]').wait_for()
    page.locator('input[aria-label="Buscar título"]').fill('Cowboy Bebop')
    page.locator('input[name="kind"][value="anime"]').evaluate('(element) => element.click()')
    page.get_by_role('button', name='Buscar', exact=True).click()
    page.wait_for_function("() => document.body.innerText.includes('Cowboy Bebop')", timeout=60000)
    print('cached anime results:', page.locator('.catalog-grid .media-card').count())
    print('provider warning:', 'Anime: A fonte de catálogo está indisponível no momento.' in page.locator('body').inner_text())
    browser.close()
