"""Check real admin pages against fictional APIs, in isolated production."""
import argparse
import asyncio
from http.server import BaseHTTPRequestHandler
import json
from pathlib import Path
import time
from urllib.parse import parse_qs, urlsplit

from playwright.async_api import expect
from tools import feed_lists_browser as runner

MODE = 'ready'
CALLS = []


class Fixture(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        self.respond()

    def do_GET(self):
        self.respond()

    def respond(self):
        self.rfile.read(int(self.headers.get('Content-Length', '0')))
        path = urlsplit(self.path).path
        query = {k: v[0] for k, v in parse_qs(urlsplit(self.path).query).items()}
        CALLS.append((self.command, path, query))
        data = {}
        status = 200
        if path == '/auth/login':
            data = {'authToken': 'fictional-admin-session'}
        elif path == '/auth/me':
            data = {'id': 7, 'role': 'admin', 'account_status': 'active'}
        elif path == '/admin/dashboard':
            if MODE == 'partial':
                data = dict(users_total=26, posts_total=True, media_total=4, reports_pending=0,
                            recent_posts={'invalid': 'shape'}, pending_reports=[])
            else:
                data = dict(users_total=26, posts_total=2, media_total=4, reports_pending=0,
                            recent_posts=[], pending_reports=[])
        elif path in ('/admin/users', '/admin/catalog', '/admin/reports'):
            page = int(query.get('page', 1))
            if path.endswith('users'):
                item = dict(id=page, name='Pessoa fictícia '+str(page), username='fixture',
                            role='member', account_status='active', created_at='2026-10-22')
            elif path.endswith('catalog'):
                item = dict(id=page, title='Obra fictícia '+str(page), media_type=query.get('media_type'),
                            description='Descrição para leitura no celular', year=2020)
            else:
                item = dict(id=page, target_type='message', target_id=90, reporter_user_id=8,
                            status='pending', reason='spam', description='Descrição fictícia do report',
                            target_snapshot={'body': 'Mensagem preservada no snapshot'})
            empty = query.get('search') == 'vazio' or MODE == 'empty'
            data = dict(items=[] if empty else [item], total=0 if empty else 26,
                        page=page, next_page=2 if page == 1 and not empty else 0)
        if path.startswith('/admin/'):
            time.sleep(.8)
            if MODE == 'error':
                status, data = 503, {}
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


async def screenshot(page, name, width):
    assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth'), name
    await page.screenshot(path=str(runner.OUTPUT/f'{name}-{width}.png'), full_page=True)


async def check(browser, width, case):
    global MODE
    MODE = 'ready'
    CALLS.clear()
    context, page, errors = await runner.context_for(browser, width)
    try:
        await page.goto('http://127.0.0.1:3031/admin/login')
        await page.get_by_label('E-mail', exact=True).fill('admin@example.invalid')
        await page.get_by_label('Senha', exact=True).fill('fictional-password')
        await page.get_by_role('button', name='Entrar na administração', exact=True).click()
        await expect(page.get_by_role('heading', name='Dashboard', exact=True)).to_be_visible(timeout=30000)
        await expect(page.locator('.admin-metric-value').first).to_have_text('26', timeout=30000)
        if case == 1:
            await expect(page.get_by_text('Nenhum report pendente.', exact=True)).to_be_visible()
            await screenshot(page, 'dashboard-empty', width)
            MODE = 'error'
            await page.get_by_role('button', name='Atualizar', exact=True).click()
            await expect(page.get_by_text('Carregando os indicadores…', exact=True)).to_be_visible()
            await expect(page.get_by_role('alert')).to_contain_text('Serviço indisponível', timeout=30000)
            await expect(page.locator('.admin-metric-value')).to_have_text(['—', '—', '—', '—'])
            await expect(page.locator('.admin-dashboard-updated')).to_have_count(0)
            await screenshot(page, 'dashboard-error', width)
            MODE = 'partial'
            await page.get_by_role('button', name='Atualizar', exact=True).click()
            await expect(page.locator('.admin-metric-value').nth(0)).to_have_text('26', timeout=30000)
            await expect(page.locator('.admin-metric-value').nth(1)).to_have_text('—')
            await expect(page.locator('.admin-metric-detail').nth(1)).to_contain_text('indicador indisponível')
            await expect(page.locator('.admin-activity-card').nth(1).get_by_role('alert'))\
                .to_contain_text('Atividade recente indisponível')
            await expect(page.locator('.admin-activity-card').nth(0).get_by_text(
                'Nenhum report pendente.', exact=True)).to_be_visible()
            await screenshot(page, 'dashboard-partial', width)
            MODE = 'ready'
            await page.get_by_role('button', name='Atualizar', exact=True).click()
            await expect(page.locator('.admin-metric-value').nth(1)).to_have_text('2', timeout=30000)
            await expect(page.locator('.admin-metric-detail').nth(1)).to_have_text('Histórias compartilhadas')
            await expect(page.locator('.admin-activity-card').nth(1).get_by_role('alert')).to_have_count(0)
            await expect(page.locator('.admin-dashboard-updated')).to_be_visible()
        elif case == 2:
            await page.locator('.admin-sidebar').get_by_role('link', name='Usuários', exact=True).click()
            await expect(page.get_by_role('heading', name='Usuários', exact=True)).to_be_visible()
            search = page.get_by_label('Buscar por nome, usuário ou ID')
            await search.fill('vazio')
            await page.get_by_role('button', name='Pesquisar', exact=True).click()
            await expect(page.get_by_role('button', name='Buscando…', exact=True)).to_be_disabled()
            await expect(page.get_by_text('Nenhuma conta encontrada para esta pesquisa.', exact=True)).to_be_visible()
            await screenshot(page, 'users-empty', width)
            await search.fill('Pessoa')
            await page.locator('select[name=account_status]').select_option('active')
            await page.locator('select[name=role]').select_option('member')
            await page.get_by_role('button', name='Pesquisar', exact=True).click()
            await expect(page.get_by_text('Pessoa fictícia 1', exact=True)).to_be_visible()
            await page.get_by_role('button', name='Próxima', exact=True).click()
            await expect(page.get_by_text('Pessoa fictícia 2', exact=True)).to_be_visible()
            await expect(page.get_by_role('button', name='Próxima', exact=True)).to_be_disabled()
            assert any(q.get('page') == '2' and q.get('role') == 'member' and q.get('account_status') == 'active'
                       for _, p, q in CALLS if p == '/admin/users')
            await screenshot(page, 'users-page-two', width)
            MODE = 'error'
            await page.get_by_role('button', name='Pesquisar', exact=True).click()
            await expect(page.get_by_role('alert')).to_contain_text('Serviço indisponível', timeout=30000)
            await expect(page.get_by_text('Pessoa fictícia 2', exact=True)).to_be_visible()
            await screenshot(page, 'users-error', width)
        elif case == 3:
            for label, kind in [('Filmes', 'movie'), ('Séries', 'series'), ('Livros', 'book'), ('Animes', 'anime')]:
                await page.locator('.admin-sidebar').get_by_role('link', name=label, exact=True).click()
                await expect(page.get_by_role('heading', name=label, exact=True)).to_be_visible()
                for _ in range(600):
                    if any(p == '/admin/catalog' and q.get('media_type') == kind for _, p, q in CALLS):
                        break
                    await asyncio.sleep(.05)
                else:
                    raise AssertionError('Catalog request did not use '+kind)
                await expect(page.get_by_text('Carregando catálogo…', exact=True)).not_to_be_visible(timeout=30000)
                await expect(page.get_by_text('Obra fictícia 1', exact=True)).to_be_visible()
                assert CALLS[-1][2].get('media_type') == kind, CALLS[-1]
                await screenshot(page, 'catalog-'+kind, width)
            await page.get_by_role('button', name='Próxima', exact=True).click()
            await expect(page.get_by_role('button', name='Próxima', exact=True)).to_be_disabled()
            await expect(page.get_by_text('Obra fictícia 2', exact=True)).to_be_visible()
            await page.get_by_label('Pesquisar título').fill('vazio')
            await page.get_by_role('button', name='Pesquisar', exact=True).click()
            await expect(page.get_by_text('Nenhuma obra encontrada para esta pesquisa.', exact=True)).to_be_visible()
            await screenshot(page, 'catalog-empty', width)
            MODE = 'error'
            await page.get_by_role('button', name='Ver todas', exact=True).click()
            await expect(page.get_by_role('alert')).to_contain_text('Serviço indisponível', timeout=30000)
            await screenshot(page, 'catalog-error', width)
        else:
            await page.locator('.admin-sidebar').get_by_role('link', name='Reports', exact=True).click()
            await expect(page.get_by_text('Report #1', exact=True)).to_be_visible()
            await page.get_by_text('Contexto salvo no envio do report', exact=True).click()
            await expect(page.locator('.admin-report-snapshot')).to_contain_text('Mensagem preservada')
            await screenshot(page, 'reports-ready', width)
            await page.get_by_role('button', name='Próxima', exact=True).click()
            await expect(page.get_by_text('Report #2', exact=True)).to_be_visible()
            MODE = 'empty'
            await page.locator('select[name=target_type]').select_option('message')
            await page.locator('select[name=reason]').select_option('spam')
            await page.get_by_role('button', name='Filtrar', exact=True).click()
            await expect(page.get_by_text('Carregando reports…', exact=True)).to_be_visible()
            await expect(page.get_by_text('Nenhum report corresponde aos filtros.', exact=True)).to_be_visible()
            assert any(q.get('target_type') == 'message' and q.get('reason') == 'spam'
                       for _, p, q in CALLS if p == '/admin/reports')
            await screenshot(page, 'reports-empty', width)
            MODE = 'error'
            await page.get_by_role('button', name='Filtrar', exact=True).click()
            await expect(page.get_by_role('alert')).to_contain_text('Serviço indisponível', timeout=30000)
            await screenshot(page, 'reports-error', width)
        assert not errors, errors
        assert not any(method != 'GET' for method, path, _ in CALLS if path.startswith('/admin/'))
        return dict(case=case, width=width, passed=True, javascript_errors=errors)
    except Exception:
        (runner.OUTPUT/f'failure-{case}-{width}-calls.json').write_text(
            json.dumps(CALLS, ensure_ascii=False, indent=2), encoding='utf-8')
        await page.screenshot(path=str(runner.OUTPUT/f'failure-{case}-{width}.png'), full_page=True)
        raise
    finally:
        await context.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--frontend-workdir', type=Path, required=True)
    args = parser.parse_args()
    runner.Fixture = Fixture
    runner.check = check
    raise SystemExit(asyncio.run(runner.main(args.output, args.frontend_workdir)))
