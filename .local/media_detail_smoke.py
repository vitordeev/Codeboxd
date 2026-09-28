from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.set_default_timeout(45000)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    for media_type, external_id, expected in (
        ('movie', '157336', 'Interestelar'),
        ('series', '1396', 'Breaking Bad'),
    ):
        page.goto(f'http://localhost:3002/obra?external_source=tmdb&external_id={external_id}&media_type={media_type}')
        page.locator('.media-detail-hero').wait_for()
        page.get_by_role('heading', name=expected).wait_for()
        assert page.get_by_role('heading', name='Ficha da obra').count() == 1
        assert page.get_by_role('heading', name='Outros comentários').count() == 1
        assert page.get_by_role('heading', name='Outras recomendações').count() == 1
        for width in (1440, 390):
            page.set_viewport_size({'width': width, 'height': 1000})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{media_type} overflow at {width}px'
            page.screenshot(path=f'.local/detail-{media_type}-{width}.png', full_page=True)
    assert not errors, errors
    print('PASS movie and series details, responsive layout, no browser errors')
    browser.close()
