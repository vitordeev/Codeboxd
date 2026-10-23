"""List metadata regression in production with a fictional local backend."""
import argparse
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import time
from urllib.parse import urlsplit

from playwright.async_api import expect

from tools import feed_lists_browser as runner

ORIGINAL_LISTS = deepcopy(runner.LISTS)
MODE = {'case': 1, 'written': False}


class Fixture(runner.Fixture):
    def do_DELETE(self): self.respond()

    def respond(self):
        path = urlsplit(self.path).path
        mutation = (self.command in ('POST', 'PUT', 'DELETE')
                    and (path == '/lists' or path in ('/lists/12', '/lists/42')))
        refresh_failure = self.command == 'GET' and path == '/lists' and MODE['case'] == 4 and MODE['written']
        if not mutation and not refresh_failure:
            return super().respond()
        runner.CALLS[(self.command, path)] += 1
        payload = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))) or b'{}')
        status, data = 200, {}
        if refresh_failure or MODE['case'] == 2:
            status = 503
        else:
            if MODE['case'] == 3: time.sleep(2)
            if self.command == 'POST':
                data = dict(payload, id=42, user_id=7)
                runner.LISTS.append(data)
            elif self.command == 'PUT':
                data = next(row for row in runner.LISTS if row['id'] == int(path.rsplit('/', 1)[1]))
                data.update(payload)
            else:
                runner.LISTS[:] = [row for row in runner.LISTS if row['id'] != int(path.rsplit('/', 1)[1])]
            MODE['written'] = True
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


async def check(browser, width, case):
    runner.CALLS.clear()
    runner.LISTS[:] = deepcopy(ORIGINAL_LISTS)
    MODE.update(case=case, written=False)
    context, page, errors = await runner.context_for(browser, width)
    try:
        await page.goto('http://127.0.0.1:3031/login')
        await page.locator('input[name=email]').fill('reader@example.invalid')
        await page.locator('input[name=password]').fill('fictional-password')
        await page.get_by_role('button', name='Entrar', exact=True).click()
        await expect(page.get_by_role('heading', name='Conta fictícia', exact=True)).to_be_visible(timeout=30000)
        await page.goto('http://127.0.0.1:3031/listas')
        await expect(page.get_by_role('button').filter(has_text='Coleção de teste')).to_be_visible(timeout=30000)
        media_before = runner.CALLS[('GET', '/media')]
        if case in (1, 3):
            await page.get_by_role('button', name='Criar lista', exact=True).click()
            expected_path, method = '/lists', 'POST'
        else:
            await page.get_by_role('button').filter(has_text='Coleção de teste').click()
            await page.get_by_role('button', name='Editar lista', exact=True).click()
            expected_path, method = '/lists/12', 'PUT'
        dialog = page.get_by_role('dialog')
        await dialog.locator('input[name=title]').fill('Lista de performance')
        await dialog.locator('textarea[name=description]').fill('Rascunho preservado')
        await dialog.get_by_role('button', name='Salvar lista', exact=True).click()
        if case == 3:
            saving = dialog.get_by_role('button', name='Salvando…', exact=True)
            await expect(saving).to_be_disabled()
            # A second native click on a disabled control must have no effect.
            await saving.evaluate('(button) => button.click()')
        if case in (2, 4):
            await expect(dialog.get_by_role('button', name='Salvar lista', exact=True)).to_be_enabled(timeout=30000)
            await expect(dialog.get_by_text('Serviço indisponível. Tente novamente.', exact=True)).to_be_visible()
            assert await dialog.locator('input[name=title]').input_value() == 'Lista de performance'
            assert await dialog.locator('textarea[name=description]').input_value() == 'Rascunho preservado'
            assert runner.CALLS[(method, expected_path)] == 1
        else:
            await expect(dialog).not_to_be_visible(timeout=30000)
            await expect(page.get_by_role('heading', name='Lista de performance', exact=True)).to_be_visible()
            assert runner.CALLS[(method, expected_path)] == 1
        if case == 1:
            await page.get_by_role('button', name='Editar lista', exact=True).click()
            await dialog.locator('input[name=title]').fill('Lista editada')
            await dialog.get_by_role('button', name='Salvar lista', exact=True).click()
            await expect(dialog).not_to_be_visible(timeout=30000)
            await expect(page.get_by_role('heading', name='Lista editada', exact=True)).to_be_visible()
            assert runner.CALLS[('PUT', '/lists/42')] == 1
            await page.get_by_role('button', name='Excluir lista', exact=True).click()
            await page.get_by_role('button', name='Confirmar exclusão', exact=True).click()
            await expect(page.get_by_text('Lista removida.', exact=True)).to_be_visible(timeout=30000)
            await expect(page.get_by_role('heading', name='Lista editada', exact=True)).not_to_be_visible(timeout=30000)
            assert runner.CALLS[('DELETE', '/lists/42')] == 1
            assert len(runner.LISTS) == len(ORIGINAL_LISTS)
        assert runner.CALLS[('GET', '/media')] == media_before, 'Unexpected catalog reload'
        assert not errors, errors
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth'), 'Horizontal overflow'
        await page.screenshot(path=str(runner.OUTPUT/f'case-{case}-{width}.png'), full_page=True)
        return dict(case=case, width=width, passed=True, catalog_refetched=False,
                    javascript_errors=errors)
    except Exception:
        (runner.OUTPUT/f'failure-{case}-{width}-calls.json').write_text(
            json.dumps([dict(method=method, path=path, count=count)
                        for (method, path), count in runner.CALLS.items()], indent=2), encoding='utf-8')
        await page.screenshot(path=str(runner.OUTPUT/f'failure-{case}-{width}.png'), full_page=True)
        raise
    finally:
        await context.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--frontend-workdir', type=Path, required=True)
    args = parser.parse_args()
    runner.Fixture, runner.check = Fixture, check
    raise SystemExit(asyncio.run(runner.main(args.output, args.frontend_workdir)))
