from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.set_default_timeout(60000)
    browser_errors = []
    page.on('pageerror', lambda error: browser_errors.append(str(error)))
    page.on('console', lambda message: browser_errors.append(message.text) if message.type == 'error' else None)
    page.goto('http://localhost:3001/')
    page.locator('input[aria-label="Buscar título"]').wait_for()
    page.wait_for_timeout(3000)
    for kind, query in [('movie', 'Interestelar'), ('series', 'Breaking Bad'),
                        ('anime', 'Cowboy Bebop'), ('book', 'Pride and Prejudice')]:
        page.locator('input[aria-label="Buscar título"]').fill(query)
        page.locator(f'input[name="kind"][value="{kind}"]').check(force=True)
        page.get_by_role('button', name='Buscar', exact=True).click()
        if kind == 'anime':
            page.get_by_text('Anime:', exact=False).wait_for()
        else:
            page.wait_for_function("(query) => document.body.innerText.includes(query)", arg=query, timeout=60000)
        cards = page.locator('.catalog-grid .media-card').count()
        body = page.locator('body').inner_text()
        print(f'{kind}: cards={cards}; text={body[:260]!r}; errors={browser_errors[-3:]}', flush=True)
    browser.close()
