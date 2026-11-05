"""Pending 9.2 criteria against stateful, localhost-only fictional APIs.

Real application pages/events, production frontend; no remote administrative data.
Every scenario records expected/observed, screenshot and request evidence.
"""
import argparse
import asyncio
from copy import deepcopy
from http.server import BaseHTTPRequestHandler
import json
from pathlib import Path
import threading
import time
from urllib.parse import parse_qs, urlsplit

from playwright.async_api import expect
from tools import feed_lists_browser as runner
from tools.admin_browser_sync import section_ready, capture_ready

RESPONSES, WRITES, RESULTS, JOURNALS = [], [], [], []
FAULT = ''
USERS, MEDIA, REPORTS = [], [], []
LOCK = threading.RLock()
BASE = 'http://127.0.0.1:3031'
GROUPS = (1, 2, 3, 4)
REMAINING_ONLY = False


def seed():
    global FAULT
    FAULT = ''
    RESPONSES.clear()
    WRITES.clear()
    USERS[:] = [dict(id=101+i, name=f'Pessoa {i+1}', username=f'pessoa{i+1}', role='member',
                    account_status='active', created_at='2026-11-05') for i in range(2)]
    MEDIA[:] = [dict(id=201+2*j+i, title=f'Obra {kind} {i+1}', description='Descrição inicial',
                    media_type=kind, identity_key=f'fixture:{kind}:{i+1}', external_source='fixture',
                    external_id=str(i+1), cover_url='', year=2020)
                for j, kind in enumerate(('movie', 'series', 'book', 'anime')) for i in range(2)]
    REPORTS[:] = [dict(id=301+i, target_type=kind, target_id=901+i, reporter_user_id=101,
                      reason='spam', status='pending', description='Descrição fictícia', decision='',
                      target_snapshot={'body': '<script>window.fixture_xss=true</script> Contexto preservado'})
                 for i, kind in enumerate(('message', 'media'))]


class Fixture(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.respond()

    def do_POST(self):
        self.respond()

    def do_PUT(self):
        self.respond()

    def respond(self):
        with LOCK:
            path = urlsplit(self.path).path
            query = {k: v[0] for k, v in parse_qs(urlsplit(self.path).query).items()}
            payload = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
            token = self.headers.get('Authorization', '').removeprefix('Bearer ')
            status, data = 200, {}
            if path == '/auth/login':
                if payload.get('password') == 'invalid-password':
                    status, data = 401, {'message': 'Credenciais inválidas.'}
                else:
                    data = {'authToken': 'fixture-member' if payload.get('email', '').startswith('member') else 'fixture-admin'}
            elif path == '/auth/me':
                if token not in ('fixture-admin', 'fixture-member', 'fixture-disabled'):
                    status = 401
                else:
                    data = dict(id=7, role='admin' if token != 'fixture-member' else 'member',
                                account_status='disabled' if token == 'fixture-disabled' else 'active')
            elif path.startswith('/admin/'):
                if token != 'fixture-admin':
                    status = 403 if token else 401
                elif FAULT == self.command + ' ' + path:
                    status, data = 503, {'message': 'Falha controlada da seção.'}
                elif path == '/admin/dashboard':
                    data = dict(users_total=2, posts_total=0, media_total=8, reports_pending=2,
                                recent_posts=[], pending_reports=[])
                    if FAULT == 'dashboard_partial':
                        data['pending_reports'] = 'invalid-section'
                elif self.command == 'PUT':
                    target = int(path.split('/')[3])
                    rows = USERS if '/users/' in path else MEDIA if '/catalog/' in path else REPORTS
                    item = next(row for row in rows if row['id'] == target)
                    item.update(payload)
                    WRITES.append(dict(endpoint=path, payload=deepcopy(payload)))
                    data = deepcopy(item)
                else:
                    rows = USERS if path.endswith('/users') else MEDIA if path.endswith('/catalog') else REPORTS
                    rows = deepcopy(rows)
                    term = query.get('search', '').casefold()
                    if term:
                        rows = [row for row in rows if term in ' '.join(str(row.get(k, '')) for k in ('name', 'username', 'title', 'id')).casefold()]
                    for key in ('role', 'account_status', 'media_type', 'status', 'target_type', 'reason'):
                        if query.get(key):
                            rows = [row for row in rows if row.get(key) == query[key]]
                    page = int(query.get('page', 1))
                    # Deliberate server-side page size 1 makes UI pagination deterministic.
                    data = dict(items=rows[page-1:page], total=len(rows), page=page, per_page=1,
                                next_page=page+1 if page < len(rows) else None)
            content = json.dumps(data).encode()
            if path.startswith('/admin/'):
                time.sleep(.3)
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            self.wfile.flush()
            RESPONSES.append(dict(endpoint=path, method=self.command, status=status,
                                  query=query, data=deepcopy(data)))


async def text(page, value):
    await expect(page.get_by_text(value, exact=True)).to_be_visible()


async def settle(page, cursor, endpoint, expected, *, status=200, method='GET'):
    section = endpoint.split('/')[2]
    label = {'users': 'Carregando contas…', 'catalog': 'Carregando catálogo…',
             'reports': 'Carregando reports…', 'dashboard': 'Carregando os indicadores…'}[section]
    control = page.get_by_role('button', name={'users': 'Pesquisar', 'catalog': 'Pesquisar',
        'reports': 'Filtrar', 'dashboard': 'Atualizar'}[section], exact=True)
    async def rendered():
        await text(page, expected)
    return await section_ready(page, RESPONSES, cursor, endpoint, result=rendered,
        loading=label, control=control, method=method, status=status)


async def record(page, name, width, expected, observed):
    filename = f'{name}-{width}.png'
    if await page.get_by_role('dialog').count() and name in (
            'user-write-error', 'catalog-invalid', 'catalog-write-error',
            'report-required-decision', 'report-write-error'):
        alert = page.get_by_role('dialog').get_by_role('alert')
        await expect(alert).to_be_visible()
        await alert.scroll_into_view_if_needed()
        assert await alert.evaluate('''el => {
            const r = el.getBoundingClientRect();
            const hit = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2);
            return hit === el || el.contains(hit);
        }'''), 'Dialog feedback is obstructed'
    await capture_ready(page, runner.OUTPUT / filename)
    RESULTS.append(dict(scenario=name, width=width, status='approved', expected=expected,
                        observed=observed, evidence=filename))
    save()


def save():
    (runner.OUTPUT / 'scenarios.json').write_text(json.dumps(dict(layer='browser_stateful_fictional_api',
        scenarios=RESULTS, journals=JOURNALS, current_responses=RESPONSES,
        current_writes=WRITES), ensure_ascii=False, indent=2), encoding='utf-8')


async def login(page, email='admin@example.invalid', password='fictional-password'):
    await page.get_by_label('E-mail', exact=True).fill(email)
    await page.get_by_label('Senha', exact=True).fill(password)
    await page.get_by_role('button', name='Entrar na administração', exact=True).click()


async def dashboard(page):
    cursor = len(RESPONSES)
    await page.goto(BASE + '/admin/login')
    await login(page)
    await expect(page.get_by_role('heading', name='Dashboard', exact=True)).to_be_visible()
    await settle(page, cursor, '/admin/dashboard', 'Nenhum report pendente.')


async def users(page, query='101'):
    await page.locator('.admin-sidebar').get_by_role('link', name='Usuários', exact=True).click()
    await expect(page.get_by_label('Buscar por nome, usuário ou ID')).to_be_visible()
    cursor = len(RESPONSES)
    await page.get_by_label('Buscar por nome, usuário ou ID').fill(query)
    await page.get_by_role('button', name='Pesquisar', exact=True).click()
    await settle(page, cursor, '/admin/users', 'Pessoa 1')


async def auth_cases(context, page, width):
    await page.goto(BASE + '/admin/users')
    await expect(page).to_have_url(__import__('re').compile(r'/admin/login/?$'))
    assert not any(r['endpoint'].startswith('/admin/') for r in RESPONSES)
    await record(page, 'auth-guest', width, 'Visitante redirecionado sem consulta restrita', 'Login visível; zero GET admin')
    await login(page, password='invalid-password')
    await expect(page.get_by_role('alert')).to_be_visible()
    await expect(page.get_by_role('button', name='Entrar na administração', exact=True)).to_be_enabled()
    await record(page, 'auth-invalid', width, 'Erro sem perder formulário', 'Alerta e formulário disponíveis')
    await login(page, email='member@example.invalid')
    await text(page, 'Esta conta não tem permissão para acessar a área administrativa.')
    assert not any(r['endpoint'].startswith('/admin/') for r in RESPONSES)
    await record(page, 'auth-member-login', width, 'Membro não recebe acesso admin', 'Negado antes de GET admin')
    await context.add_cookies([dict(name='codeboxd_auth', value='fixture-member', url=BASE)])
    await page.goto(BASE + '/admin/')
    await expect(page).to_have_url(__import__('re').compile(r':3031/$'))
    assert not any(r['endpoint'].startswith('/admin/') for r in RESPONSES)
    await record(page, 'auth-member-direct', width, 'Membro redirecionado para início', 'Rota inicial; zero GET admin')
    await context.clear_cookies()
    await page.goto(BASE + '/admin/login')
    cursor = len(RESPONSES)
    await login(page)
    await settle(page, cursor, '/admin/dashboard', 'Nenhum report pendente.')
    await expect(page).to_have_url(__import__('re').compile(r'/admin/?$'))
    await record(page, 'auth-admin', width, 'Admin acessa dashboard renderizado', 'Dashboard carregado')
    cursor = len(RESPONSES)
    await page.goto(BASE + '/admin/login')
    await settle(page, cursor, '/admin/dashboard', 'Nenhum report pendente.')
    await expect(page).to_have_url(__import__('re').compile(r'/admin/?$'))
    await record(page, 'auth-existing', width, 'Sessão admin dispensa novo login', 'Redirecionado ao dashboard')


async def account_cases(page, width):
    global FAULT
    await dashboard(page)
    await users(page)
    await page.get_by_role('button', name='Detalhes', exact=True).click()
    await text(page, 'Identificador: 101')
    await record(page, 'user-details', width, 'Detalhes permitidos visíveis', 'ID/papel/status exibidos')
    await page.get_by_role('button', name='Suspender', exact=True).click()
    dialog = page.get_by_role('dialog')
    await expect(dialog).to_be_visible()
    await record(page, 'user-dialog', width, 'Confirmação legível', 'Diálogo aberto')
    await dialog.get_by_role('button', name='Cancelar', exact=True).click()
    await expect(dialog).to_have_count(0)
    assert not WRITES and USERS[0]['account_status'] == 'active'
    await record(page, 'user-cancel', width, 'Cancelar sem PUT', 'Zero gravações; conta ativa')
    await page.get_by_role('button', name='Suspender', exact=True).click()
    FAULT = 'PUT /admin/users/101/status'
    cursor = len(RESPONSES)
    await dialog.get_by_role('button', name='Confirmar', exact=True).click()
    await settle(page, cursor, '/admin/users/101/status', 'Serviço indisponível. Tente novamente.', status=503, method='PUT')
    await expect(dialog).to_be_visible()
    assert not WRITES
    await record(page, 'user-write-error', width, 'Erro preserva confirmação e conta', '503; nenhuma gravação')
    FAULT = ''
    cursor = len(RESPONSES)
    await dialog.get_by_role('button', name='Confirmar', exact=True).click()
    await settle(page, cursor, '/admin/users', 'Estado da conta atualizado e ação registrada.')
    await expect(dialog).to_have_count(0)
    await expect(page.get_by_role('button', name='Reativar', exact=True)).to_be_visible()
    assert USERS[0]['account_status'] == 'disabled' and len(WRITES) == 1
    await record(page, 'user-confirm', width, 'Confirmar grava uma vez e atualiza UI', 'Conta suspensa e feedback')
    await page.get_by_role('button', name='Reativar', exact=True).click()
    cursor = len(RESPONSES)
    await dialog.get_by_role('button', name='Confirmar', exact=True).click()
    await settle(page, cursor, '/admin/users', 'Estado da conta atualizado e ação registrada.')
    await expect(dialog).to_have_count(0)
    assert USERS[0]['account_status'] == 'active' and len(WRITES) == 2
    await record(page, 'user-reactivate', width, 'Reativação refletida', 'Conta ativa')


async def catalog_cases(page, width):
    global FAULT
    await dashboard(page)
    for label, kind in [('Filmes', 'movie'), ('Séries', 'series'), ('Livros', 'book'), ('Animes', 'anime')]:
        cursor = len(RESPONSES)
        await page.locator('.admin-sidebar').get_by_role('link', name=label, exact=True).click()
        await settle(page, cursor, '/admin/catalog', f'Obra {kind} 1')
        await expect(page.get_by_role('heading', name=label, exact=True)).to_be_visible()
    await page.get_by_role('button', name='Editar', exact=True).click()
    dialog = page.get_by_role('dialog')
    await expect(dialog).to_be_visible()
    await dialog.get_by_label('Título', exact=True).fill('Cancelado')
    await dialog.get_by_role('button', name='Cancelar', exact=True).click()
    await expect(dialog).to_have_count(0)
    assert not WRITES
    await record(page, 'catalog-cancel', width, 'Cancelar preserva obra', 'Nenhum PUT')
    await page.get_by_role('button', name='Editar', exact=True).click()
    await dialog.get_by_label('Ano', exact=True).fill('1700')
    await dialog.get_by_role('button', name='Salvar alterações', exact=True).click()
    await text(page, 'Informe um ano entre 1800 e 2200.')
    await expect(dialog.get_by_label('Ano', exact=True)).to_have_value('1700')
    assert not WRITES
    await record(page, 'catalog-invalid', width, 'Ano inválido sem PUT e rascunho preservado', 'Erro exibido; ano 1700 mantido')
    await dialog.get_by_label('Ano', exact=True).fill('2021')
    await dialog.get_by_label('Título', exact=True).fill('Obra corrigida')
    original = deepcopy(next(x for x in MEDIA if x['media_type'] == 'anime'))
    endpoint = f'/admin/catalog/{original["id"]}'
    FAULT = 'PUT ' + endpoint
    cursor = len(RESPONSES)
    await dialog.get_by_role('button', name='Salvar alterações', exact=True).click()
    await settle(page, cursor, endpoint, 'Serviço indisponível. Tente novamente.', status=503, method='PUT')
    await expect(dialog.get_by_label('Título', exact=True)).to_have_value('Obra corrigida')
    assert not WRITES
    await record(page, 'catalog-write-error', width, 'Falha mantém editor e rascunho', '503; título preservado')
    FAULT = ''
    cursor = len(RESPONSES)
    await dialog.get_by_role('button', name='Salvar alterações', exact=True).click()
    await settle(page, cursor, '/admin/catalog', 'Obra corrigida')
    await expect(dialog).to_have_count(0)
    current = next(x for x in MEDIA if x['id'] == original['id'])
    assert all(current[k] == original[k] for k in ('id', 'identity_key', 'external_id', 'external_source', 'media_type'))
    assert len(WRITES) == 1
    await record(page, 'catalog-save', width, 'Edição refletida com identidade preservada', 'Novo título/ano; um PUT')


async def moderation_cases(page, width):
    global FAULT
    await dashboard(page)
    cursor = len(RESPONSES)
    await page.locator('.admin-sidebar').get_by_role('link', name='Reports', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Report #301')
    await expect(page.locator('.admin-report-card')).to_have_count(1)
    await page.get_by_text('Contexto salvo no envio do report', exact=True).click()
    await expect(page.locator('.admin-report-snapshot')).to_contain_text('Contexto preservado')
    assert not await page.evaluate('Boolean(window.fixture_xss)') and not WRITES
    await record(page, 'reports-ready-snapshot', width, 'Fila carregada; snapshot escapado sem alvo ao vivo', 'Uma linha; loading encerrado; script não executado')
    cursor = len(RESPONSES)
    await page.get_by_role('button', name='Próxima', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Report #302')
    await expect(page.get_by_role('button', name='Próxima', exact=True)).to_be_disabled()
    await record(page, 'reports-pagination', width, 'Página seguinte sem duplicação', 'Report 302; próxima desabilitada')
    cursor = len(RESPONSES)
    await page.locator('select[name=target_type]').select_option('message')
    await page.locator('select[name=reason]').select_option('spam')
    await page.get_by_role('button', name='Filtrar', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Report #301')
    await record(page, 'reports-filter', width, 'Tipo/motivo selecionam somente mensagem spam', 'Report 301')
    await page.get_by_role('button', name='Resolver', exact=True).click()
    dialog = page.get_by_role('dialog')
    await expect(dialog).to_be_visible()
    await dialog.get_by_role('button', name='Cancelar', exact=True).click()
    await expect(dialog).to_have_count(0)
    assert not WRITES
    await record(page, 'report-cancel', width, 'Cancelar não altera report/alvo', 'Zero PUT')
    await page.get_by_role('button', name='Resolver', exact=True).click()
    await dialog.get_by_role('button', name='Confirmar decisão', exact=True).click()
    await text(page, 'Registre uma decisão antes de atualizar o report.')
    assert not WRITES
    await record(page, 'report-required-decision', width, 'Decisão obrigatória', 'Sem PUT; diálogo preservado')
    await dialog.get_by_label('Decisão ou nota de análise', exact=True).fill('Decisão fictícia')
    FAULT = 'PUT /admin/reports/301'
    cursor = len(RESPONSES)
    await dialog.get_by_role('button', name='Confirmar decisão', exact=True).click()
    await settle(page, cursor, '/admin/reports/301', 'Serviço indisponível. Tente novamente.', method='PUT', status=503)
    await expect(dialog.get_by_label('Decisão ou nota de análise', exact=True)).to_have_value('Decisão fictícia')
    assert not WRITES
    await record(page, 'report-write-error', width, 'Falha preserva decisão', '503; sem mutação')
    FAULT = ''
    cursor = len(RESPONSES)
    before = deepcopy(REPORTS[0]['target_snapshot'])
    await dialog.get_by_role('button', name='Confirmar decisão', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Nenhum report corresponde aos filtros.')
    await expect(dialog).to_have_count(0)
    assert len(WRITES) == 1 and REPORTS[0]['status'] == 'resolved' and REPORTS[0]['target_snapshot'] == before
    await record(page, 'report-decision', width, 'Confirmar atualiza estado e preserva snapshot', 'Um PUT; resolvido; fila pendente vazia')
    cursor = len(RESPONSES)
    await page.locator('select[name=status]').select_option('resolved')
    await page.get_by_role('button', name='Filtrar', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Decisão registrada: Decisão fictícia')
    await record(page, 'report-decision-filter', width, 'Filtro resolvido exibe decisão', 'Decisão persistida na fixture')
    FAULT = 'GET /admin/reports'
    cursor = len(RESPONSES)
    await page.get_by_role('button', name='Filtrar', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Serviço indisponível. Tente novamente.', status=503)
    await text(page, 'Decisão registrada: Decisão fictícia')
    await record(page, 'reports-read-error', width, 'Falha preserva dados carregados', 'Alerta e decisão anterior visíveis')
    FAULT = ''
    cursor = len(RESPONSES)
    await page.get_by_role('button', name='Filtrar', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Decisão registrada: Decisão fictícia')
    await expect(page.get_by_role('alert')).to_have_count(0)
    await record(page, 'reports-retry', width, 'Nova tentativa recupera sem novo login', 'Alerta limpo; dados renderizados')
    FAULT = 'dashboard_partial'
    cursor = len(RESPONSES)
    await page.locator('.admin-sidebar').get_by_role('link', name='Dashboard', exact=True).click()
    await settle(page, cursor, '/admin/dashboard', 'O serviço retornou reports pendentes em formato inesperado.')
    await expect(page.locator('.admin-metric-value').first).to_have_text('2')
    await record(page, 'dashboard-partial', width, 'Falha de seção não descarta indicadores válidos', 'Payload parcial sintético; métricas preservadas')
    FAULT = ''
    cursor = len(RESPONSES)
    await page.get_by_role('button', name='Atualizar', exact=True).click()
    await settle(page, cursor, '/admin/dashboard', 'Nenhum report pendente.')
    await expect(page.get_by_role('alert')).to_have_count(0)
    await record(page, 'dashboard-retry', width, 'Recuperação da seção', 'Alerta limpo; sessão preservada')


async def remaining_cases(page, width, case):
    """Only decision states and read recoveries not proved by the first battery."""
    global FAULT
    await dashboard(page)
    if case in (2, 3):
        if case == 2:
            await users(page)
            endpoint, expected, button = '/admin/users', 'Pessoa 1', 'Pesquisar'
        else:
            cursor = len(RESPONSES)
            await page.locator('.admin-sidebar').get_by_role('link', name='Filmes', exact=True).click()
            await settle(page, cursor, '/admin/catalog', 'Obra movie 1')
            endpoint, expected, button = '/admin/catalog', 'Obra movie 1', 'Pesquisar'
        name = 'users' if case == 2 else 'catalog'
        FAULT = 'GET ' + endpoint
        cursor = len(RESPONSES)
        await page.get_by_role('button', name=button, exact=True).click()
        await settle(page, cursor, endpoint, 'Serviço indisponível. Tente novamente.', status=503)
        await text(page, expected)
        await record(page, name+'-read-error', width, 'Dados anteriores preservados após falha da seção', '503 e dados confirmados visíveis')
        FAULT = ''
        cursor = len(RESPONSES)
        await page.get_by_role('button', name=button, exact=True).click()
        await settle(page, cursor, endpoint, expected)
        await expect(page.get_by_role('alert')).to_have_count(0)
        await record(page, name+'-retry', width, 'Retry recupera sem login', 'Alerta limpo; dados carregados')
        return
    cursor = len(RESPONSES)
    await page.locator('.admin-sidebar').get_by_role('link', name='Reports', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Report #301')
    cursor = len(RESPONSES)
    await page.locator('select[name=target_type]').select_option('message')
    await page.get_by_role('button', name='Filtrar', exact=True).click()
    await settle(page, cursor, '/admin/reports', 'Report #301')
    before = deepcopy(REPORTS[0]['target_snapshot'])
    for index, (button, status, decision) in enumerate([
            ('Em análise', 'reviewing', 'Análise fictícia'), ('Rejeitar', 'rejected', 'Rejeição fictícia')]):
        await page.get_by_role('button', name=button, exact=True).click()
        dialog = page.get_by_role('dialog')
        await dialog.get_by_label('Decisão ou nota de análise', exact=True).fill(decision)
        cursor = len(RESPONSES)
        await dialog.get_by_role('button', name='Confirmar decisão', exact=True).click()
        await settle(page, cursor, '/admin/reports', 'Nenhum report corresponde aos filtros.')
        await expect(dialog).to_have_count(0)
        cursor = len(RESPONSES)
        await page.locator('select[name=status]').select_option(status)
        await page.get_by_role('button', name='Filtrar', exact=True).click()
        await settle(page, cursor, '/admin/reports', 'Decisão registrada: '+decision)
        assert REPORTS[0]['status'] == status and REPORTS[0]['target_snapshot'] == before
        assert len(WRITES) == index+1
        await record(page, 'report-'+status, width, 'Estado/decisão atualizados sem alterar snapshot', status+'; uma gravação por confirmação')


async def check(browser, width, case):
    if case not in GROUPS:
        return dict(case=case, width=width, skipped=True, reason='Reusing previous evidence')
    seed()
    context, page, errors = await runner.context_for(browser, width)
    start = len(RESULTS)
    try:
        if REMAINING_ONLY:
            await remaining_cases(page, width, case)
        elif case == 1:
            await auth_cases(context, page, width)
        elif case == 2:
            await account_cases(page, width)
        elif case == 3:
            await catalog_cases(page, width)
        else:
            await moderation_cases(page, width)
        assert not errors, errors
        return dict(case=case, width=width, passed=True, scenarios=len(RESULTS)-start)
    except Exception as error:
        name = f'failure-group-{case}-{width}.png'
        await page.screenshot(path=str(runner.OUTPUT / name), full_page=True)
        RESULTS.append(dict(scenario=f'group-{case}', width=width, status='failed',
            expected='Todos os critérios do grupo', observed=str(error), evidence=name))
        return dict(case=case, width=width, passed=False, failure=type(error).__name__)
    finally:
        JOURNALS.append(dict(case=case, width=width, responses=deepcopy(RESPONSES), writes=deepcopy(WRITES)))
        save()
        await context.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--frontend-workdir', required=True, type=Path)
    parser.add_argument('--groups', nargs='+', type=int, choices=(1, 2, 3, 4), default=[1, 2, 3, 4])
    parser.add_argument('--remaining-only', action='store_true', help='Only unproved read recoveries and decision states')
    args = parser.parse_args()
    GROUPS = tuple(args.groups)
    REMAINING_ONLY = args.remaining_only
    if REMAINING_ONLY:
        GROUPS = tuple(group for group in GROUPS if group != 1)
    runner.Fixture, runner.check = Fixture, check
    code = asyncio.run(runner.main(args.output, args.frontend_workdir))
    raise SystemExit(code or int(any(row['status'] == 'failed' for row in RESULTS)))
