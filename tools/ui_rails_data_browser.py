"""Read-only browser acceptance against the isolated fictional UI backend."""
import asyncio
import json
from pathlib import Path
from urllib.parse import urlsplit

from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


async def run():
    output = ROOT/'.local/rails-data-result.json'
    report = {'layer': 'browser_with_fictional_backend', 'cases': [], 'passed': False}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='msedge', headless=True)
        try:
            for width in (320, 390, 768, 1440):
                context = await browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
                async def route_request(route):
                    host = urlsplit(route.request.url).hostname
                    if host == 'ui-fixture.invalid':
                        if 'broken' in route.request.url:
                            await route.abort()
                        else:
                            await route.fulfill(content_type='image/png', body=(ROOT/'assets/default-movie-cover.png').read_bytes())
                    elif host in ('127.0.0.1', 'localhost'):
                        await route.continue_()
                    else:
                        await route.abort()
                await context.route('**/*', route_request)
                page = await context.new_page()
                errors = []
                page.on('pageerror', lambda exc: errors.append(str(exc)))
                await page.goto('http://127.0.0.1:3036/')
                rail = page.locator('#popular-movie')
                cards = rail.locator('[data-rail-item]')
                await expect(cards).to_have_count(12)
                more = page.get_by_role('button', name='Carregar mais filmes', exact=True)
                await expect(more).to_be_enabled()
                original = await cards.all_text_contents()
                other = await page.locator('#popular-series [data-rail-item]').all_text_contents()
                await rail.focus()
                await page.keyboard.press('End')
                await expect(cards).to_have_count(12)
                await more.click()
                await expect(cards).to_have_count(24)
                titles = await cards.all_text_contents()
                assert titles[:12] == original and len(set(titles)) == 24
                assert await page.locator('#popular-series [data-rail-item]').all_text_contents() == other
                await expect(more).to_be_enabled()
                await more.click()
                await expect(more).to_have_count(0)
                await expect(cards).to_have_count(24)
                await cards.first.focus()
                await expect(cards.first).to_be_in_viewport(ratio=1)
                before = await cards.first.bounding_box()
                first_title = await cards.first.locator('h3').inner_text()
                await cards.first.locator('img').evaluate('img=>img.src="https://ui-fixture.invalid/cover.png?broken=1"')
                await expect(cards.first.locator('img')).to_have_count(0)
                assert await cards.first.locator('h3').inner_text() == first_title
                after = await cards.first.bounding_box()
                assert abs(after['height']-before['height']) <= 1, 'fallback_layout_shift'
                assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                await cards.first.press('Enter')
                await expect(page).to_have_url(__import__('re').compile('/obra\\?'))
                assert not errors
                report['cases'].append({'width': width, 'initial_cards': 12, 'loaded_cards': 24,
                    'unique_titles': 24, 'first_page_preserved': True, 'other_collection_preserved': True,
                    'scroll_does_not_load': True, 'exhaustion_hides_more': True,
                    'broken_cover_preserves_title_and_geometry': True, 'keyboard_navigation': True,
                    'javascript_errors': errors, 'passed': True})
                await context.close()
            report['passed'] = True
        finally:
            await browser.close()
            output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    asyncio.run(run())
