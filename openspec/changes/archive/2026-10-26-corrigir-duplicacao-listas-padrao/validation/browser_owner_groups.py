"""Verify owner headers and nested public lists with fictional local APIs."""
import asyncio
import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from playwright.async_api import expect
from tools import feed_lists_browser as harness
from tools.performance_continuation_browser import context_for

OriginalFixture = harness.Fixture
original_check = harness.check
PROFILES = [dict(user_id=7, username='fixture', display_name='Conta fictícia'),
            dict(user_id=8, username='ana', display_name='Ana Leitora', avatar_url='https://avatars.example.invalid/ana.png'),
            dict(user_id=9, username='bruno', display_name='Bruno Cinéfilo', avatar_url='')]
PUBLIC = [dict(id=20+i*2+j, user_id=uid, title=title, is_public=True)
          for i, uid in enumerate((8, 9))
          for j, title in enumerate(('Quero ver / ler', 'Já assisti / li'))]


class Fixture(OriginalFixture):
    def respond(self):
        path = urlsplit(self.path).path
        if path == '/profiles': data = PROFILES
        elif path == '/lists/public': data = PUBLIC
        elif path in ('/profiles/8', '/profiles/9'):
            data = dict(profile=next(p for p in PROFILES if p['user_id'] == int(path.rsplit('/', 1)[1])),
                        interactions=[], followers=[], following=[])
        else:
            return super().respond()
        harness.CALLS[(self.command, path)] += 1
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


async def check(browser, width, case):
    if case in (3, 4): return await original_check(browser, width, case)
    context, page, errors = await context_for(browser, width)
    await context.route('https://avatars.example.invalid/**',
                        lambda route: route.fulfill(path=str(ROOT / 'assets/mascot.png'), content_type='image/png'))
    try:
        if case == 1:
            await page.goto('http://127.0.0.1:3031/login')
            await page.locator('input[name=email]').fill('reader@example.invalid')
            await page.locator('input[name=password]').fill('fictional-password')
            await page.get_by_role('button', name='Entrar', exact=True).click()
            await expect(page.get_by_role('heading', name='Conta fictícia', exact=True)).to_be_visible(timeout=30000)
        await page.goto('http://127.0.0.1:3031/listas')
        if case == 1:
            await expect(page.locator('.list-row')).to_have_count(3, timeout=30000)
            await expect(page.locator('.public-list-group')).to_have_count(0)
            await page.get_by_role('button', name='Explorar listas públicas', exact=True).click()
        groups = page.locator('.public-list-group')
        await expect(groups).to_have_count(2, timeout=30000)
        for index, name in enumerate(('Ana Leitora', 'Bruno Cinéfilo')):
            header = groups.nth(index).locator('.public-list-owner')
            await expect(header).to_have_attribute('href', '/perfil/' + str(8+index))
            await expect(header).to_contain_text(name)
            await expect(groups.nth(index).locator('.list-row')).to_have_count(2)
            for title in ('Quero ver / ler', 'Já assisti / li'):
                await expect(groups.nth(index).get_by_role('button').filter(has_text=title)).to_have_count(1)
        await expect(groups.first.locator('img')).to_have_attribute('alt', 'Ana Leitora')
        await expect(groups.first.locator('img')).to_have_js_property('complete', True)
        assert await groups.first.locator('img').evaluate('(image) => image.naturalWidth > 0')
        await expect(groups.nth(1).locator('.avatar-fallback')).to_be_visible()
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        await page.screenshot(path=str(harness.OUTPUT / f'groups-{case}-{width}.png'), full_page=True)
        await groups.first.get_by_role('link', name='Ana Leitora').click()
        await expect(page).to_have_url('http://127.0.0.1:3031/perfil/8', timeout=30000)
        await expect(page.get_by_role('heading', name='Ana Leitora', exact=True)).to_be_visible(timeout=30000)
        assert not errors, errors
        return dict(case=case, width=width, passed=True, javascript_errors=errors)
    finally:
        await context.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).parent / 'owner-groups-browser')
    args = parser.parse_args()
    harness.Fixture = Fixture
    harness.check = check
    raise SystemExit(asyncio.run(harness.main(args.output,
                                            ROOT / '.local/frontends/feed-lists-2004')))
