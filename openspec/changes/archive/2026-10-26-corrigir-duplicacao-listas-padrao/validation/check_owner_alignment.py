"""Read-only browser geometry checks; never logs profile names or images."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright, expect


async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=True)
        try:
            page = await browser.new_page(viewport={'width':1440, 'height':900})
            await page.goto('http://127.0.0.1:3030/listas')
            headers = page.locator('.public-list-owner')
            await expect(headers.first).to_be_visible(timeout=60000)
            for width in (1440, 390, 320):
                await page.set_viewport_size({'width':width, 'height':900})
                for long_name in (False, True):
                    count = await headers.count()
                    for index in range(count):
                        header = headers.nth(index)
                        name = header.locator('.public-list-owner-name')
                        original = await name.text_content()
                        if long_name:
                            await name.evaluate('(el) => el.textContent = "NomeMuitoLongo".repeat(10)')
                        avatar_box = await header.locator('.avatar').bounding_box()
                        name_box = await name.bounding_box()
                        assert avatar_box and name_box
                        assert name_box['x'] >= avatar_box['x'] + avatar_box['width'] + 8
                        assert name_box['x'] + name_box['width'] <= width
                        assert await header.evaluate('(el) => getComputedStyle(el).display') == 'grid'
                        if long_name: await name.evaluate('(el, value) => el.textContent = value', original)
                    assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
                    results.append(dict(width=width, long_name=long_name, headers=count, passed=True))
            await page.close()
        finally:
            await browser.close()
    report = dict(layer='browser_local_app_public_read_only', results=results,
                  authenticated=False, writes=False, profile_data_logged=False)
    Path(__file__).with_name('owner-alignment.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__': asyncio.run(main())
