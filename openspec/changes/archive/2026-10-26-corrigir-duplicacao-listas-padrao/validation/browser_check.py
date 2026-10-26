"""Current real UI against fictional local services; no Xano writes."""
import asyncio
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from playwright.async_api import expect
from tools import feed_lists_browser as harness
from tools.performance_continuation_browser import context_for


original_check = harness.check


async def check(browser, width, case):
    if case in (3, 4):
        return await original_check(browser, width, case)
    context, page, errors = await context_for(browser, width)
    try:
        harness.CALLS.clear()
        harness.ENTRIES.clear()
        if case == 1:
            await page.goto('http://127.0.0.1:3031/login')
            await page.locator('input[name=email]').fill('reader@example.invalid')
            await page.locator('input[name=password]').fill('fictional-password')
            await page.get_by_role('button', name='Entrar', exact=True).click()
            await expect(page.get_by_role('heading', name='Conta fictícia', exact=True)).to_be_visible(timeout=30000)
        await page.goto('http://127.0.0.1:3031/listas')
        rows = page.locator('.list-row')
        if case == 1:
            await expect(page.get_by_role('heading', name='Suas listas', exact=True)).to_be_visible(timeout=30000)
            await expect(rows).to_have_count(3, timeout=30000)
            assert harness.CALLS[('GET', '/lists/public')] == 0
            await expect(rows.filter(has_text='Quero ver / ler')).to_have_count(1)
            await expect(rows.filter(has_text='Já assisti / li')).to_have_count(1)
            await expect(rows.filter(has_text='Coleção de teste')).to_have_count(1)
            await page.get_by_role('button', name='Explorar listas públicas', exact=True).click()
        await expect(page.get_by_role('heading', name='Listas públicas', exact=True)).to_be_visible(timeout=30000)
        await expect(rows).to_have_count(1, timeout=30000)
        await expect(page.get_by_role('link', name='Ver perfil do autor')).to_have_attribute('href', '/perfil/8')
        await rows.first.click()
        await expect(page.get_by_text('Esta lista ainda não tem obras.', exact=True)).to_be_visible(timeout=30000)
        assert harness.CALLS[('GET', '/lists/public/13/items')] == 1
        await expect(page.get_by_role('button', name='Editar lista', exact=True)).to_have_count(0)
        await expect(page.get_by_role('searchbox', name='Buscar obras para a lista')).to_have_count(0)
        if case == 1:
            await page.get_by_role('button', name='Minhas listas', exact=True).click()
            await expect(rows).to_have_count(3, timeout=30000)
            await expect(page.get_by_role('heading', name='Suas listas', exact=True)).to_be_visible()
        assert not errors, errors
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        await page.screenshot(path=str(harness.OUTPUT / f'lists-{case}-{width}.png'), full_page=True)
        return dict(case=case, width=width, passed=True, javascript_errors=errors)
    finally:
        await context.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).parent / 'browser')
    parser.add_argument('--frontend-workdir', type=Path)
    args = parser.parse_args()
    harness.check = check
    raise SystemExit(asyncio.run(harness.main(args.output, args.frontend_workdir)))
