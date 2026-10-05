from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page()
    page.set_default_timeout(60000)
    page.goto('http://localhost:3001/')
    page.locator('input[aria-label="Buscar título"]').wait_for()
    page.locator('input[aria-label="Buscar título"]').fill('Pride and Prejudice')
    page.get_by_text('Livros', exact=True).click()
    page.get_by_role('button', name='Buscar', exact=True).click()
    page.wait_for_function("() => document.body.innerText.includes('Pride and Prejudice') || document.body.innerText.includes('Livro:')", timeout=90000)
    result = page.locator('.catalog-grid .media-card').first
    result.wait_for()
    result.click()
    page.wait_for_timeout(8000)
    print('url:', page.url)
    print(page.locator('body').inner_text()[:900])
    if page.locator('.media-detail-title').count():
        print('detail:', page.locator('.media-detail-title').inner_text())
        print('description:', bool(page.locator('.media-detail-description').inner_text().strip()))
    browser.close()
