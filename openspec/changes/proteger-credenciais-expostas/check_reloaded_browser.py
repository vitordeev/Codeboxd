"""Public catalog validation against the reloaded app. No account or credentials."""
import json
from playwright.sync_api import sync_playwright
from audit_inventory import HERE


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='msedge', headless=True)
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 900})
            response = page.goto('http://127.0.0.1:3030/', wait_until='domcontentloaded')
            report = {'layer': 'real-browser-public', 'home_status': response.status, 'shelves': {}}
            for title in ('Agora nos cinemas', 'Filmes muito bem avaliados',
                          'No radar: próximos filmes', 'Séries muito bem avaliadas'):
                shelf = page.locator('.catalog-shelf').filter(has=page.get_by_role('heading', name=title, exact=True))
                shelf.locator('.shelf-card').first.wait_for(timeout=60000)
                report['shelves'][title] = shelf.locator('.shelf-card').count()
            report['passed'] = report['home_status'] == 200 and all(n > 0 for n in report['shelves'].values())
            (HERE / 'reloaded-browser.json').write_text(json.dumps(report, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(report, ensure_ascii=True))
            if not report['passed']:
                raise RuntimeError('Incomplete public catalog')
        finally:
            browser.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('Browser validation failed (' + type(exc).__name__ + '); raw details suppressed') from None
