"""Real browser journey with disposable records and exact metadata cleanup.

No screenshots, traces, credentials, cookies or existing content are exported.
The running normal server is used unchanged; browser wire metrics do not count
its outbound Python requests. Writes happen through the actual interface.
"""
import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.parse import unquote, urlsplit
import uuid

from dotenv import dotenv_values
import httpx
from playwright.async_api import async_playwright, expect

from Codeboxd_main.services.api import retry_after_seconds
from tools.performance_probe import safe_endpoint

ROOT = Path(__file__).resolve().parents[1]
TABLES = ('user_list', 'user_list_item', 'post', 'user_media_interaction')


class Audit:
    def __init__(self, client, auth, social, meta, meta_token, report, *, pause=3):
        self.client, self.auth, self.social, self.meta = client, auth, social, meta
        self.meta_headers = {'Authorization': 'Bearer '+meta_token}
        self.report, self.pause = report, pause
        self.marker = 'cbj_'+uuid.uuid4().hex[:20]
        self.token, self.uid, self.mid = '', 0, 0
        self.tables, self.before, self.list_ids = {}, {}, set()
        self.last, self.calls, self.retry_until = 0, 0, 0
        self.ready = False
        self.journal = ROOT/'.local'/('journey-'+self.marker+'.json')

    def request(self, method, url, **kwargs):
        if self.calls >= 220: raise RuntimeError('verification_budget')
        time.sleep(max(0, self.last+self.pause-time.monotonic()))
        started = time.perf_counter()
        self.calls += 1
        try:
            response = self.client.request(method, url, **kwargs)
        finally:
            self.last = time.monotonic()
        self.report['verification_requests'].append(dict(method=method,
            endpoint=safe_endpoint(url), status=response.status_code,
            duration_ms=round((time.perf_counter()-started)*1000, 3)))
        if response.status_code == 429:
            self.retry_until = time.monotonic()+retry_after_seconds(response.headers.get('Retry-After', ''))
            raise RuntimeError('verification_rate_limit')
        if response.status_code not in (200, 204): raise RuntimeError('verification_http_failure')
        return response.json() if response.content else {}

    def api(self, path, params=None, *, auth=False):
        return self.request('GET', (self.auth if auth else self.social)+path,
                            params=params, headers={'Authorization': 'Bearer '+self.token})

    def rows(self, table):
        result, seen, page = [], set(), 1
        while page is not None:
            if page in seen or len(seen) >= 20: raise RuntimeError('metadata_page_limit')
            seen.add(page)
            data = self.request('GET', f'{self.meta}/table/{self.tables[table]}/content',
                                params={'page': page, 'per_page': 100}, headers=self.meta_headers)
            if not isinstance(data, dict) or not isinstance(data.get('items'), list):
                raise RuntimeError('metadata_shape')
            result.extend(data['items'])
            page = data.get('nextPage')
        return result

    def owned(self, table, row, list_ids=None):
        return (row.get('list_id') in (list_ids if list_ids is not None else self.list_ids)
                if table == 'user_list_item' else row.get('user_id') == self.uid)

    def hashes(self, table, rows, list_ids=None):
        return {str(row['id']): hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
                for row in rows if self.owned(table, row, list_ids)}

    def fixture(self, table, row):
        if str(row['id']) in self.before.get(table, {}): return False
        if table == 'user_list_item': return row.get('list_id') in self.list_ids
        if row.get('user_id') != self.uid: return False
        field = {'user_list': 'title', 'post': 'body', 'user_media_interaction': 'review'}[table]
        return (str(row.get(field) or '').startswith(self.marker)
                and (table != 'user_media_interaction' or row.get('media_id') == self.mid))

    def save_journal(self):
        self.journal.parent.mkdir(parents=True, exist_ok=True)
        self.journal.write_text(json.dumps(dict(marker=self.marker, owner=self.uid,
            media_id=self.mid, tables=self.tables, fixture_lists=sorted(self.list_ids),
            original_ids={table: sorted(rows) for table, rows in self.before.items()})), encoding='utf-8')

    def prepare(self):
        me = self.api('/auth/me', auth=True)
        if not (type(me.get('id')) is int and me['id'] > 0 and me.get('role') == 'member'
                and me.get('account_status') == 'active'):
            raise RuntimeError('active_member_required')
        self.uid = me['id']
        tables = self.request('GET', self.meta+'/table', headers=self.meta_headers)
        self.tables = {row['name']: row['id'] for row in (tables.get('items', []) if isinstance(tables, dict) else tables)}
        if not all(name in self.tables for name in (*TABLES, 'media')):
            raise RuntimeError('required_tables_missing')
        data = {table: self.rows(table) for table in TABLES}
        original_lists = {row['id'] for row in data['user_list'] if row.get('user_id') == self.uid}
        self.before = {table: self.hashes(table, rows, original_lists) for table, rows in data.items()}
        self.original_lists = original_lists
        used = {row['media_id'] for row in data['user_media_interaction'] if row.get('user_id') == self.uid}
        candidates = [row for row in self.rows('media') if row.get('external_source') == 'tmdb'
                      and row.get('media_type') == 'movie' and row['id'] not in used
                      and row.get('title') and row.get('identity_key')]
        if not candidates: raise RuntimeError('no_unrated_existing_movie')
        candidates.sort(key=lambda row: (str(row.get('external_id')) != '603', row['id']))
        self.media = candidates[0]
        self.mid = self.media['id']
        self.ready = True
        self.save_journal()

    def fixtures(self, table):
        rows = [row for row in self.rows(table) if self.fixture(table, row)]
        if table == 'user_list':
            self.list_ids.update(row['id'] for row in rows)
            self.save_journal()
        return rows

    def cleanup(self):
        if not self.ready: return
        self.fixtures('user_list')
        for table in ('user_list_item', 'post', 'user_media_interaction', 'user_list'):
            for row in self.fixtures(table):
                # Recheck the exact ID immediately before deletion.
                current = self.request('GET', f'{self.meta}/table/{self.tables[table]}/content/{row["id"]}',
                                       headers=self.meta_headers)
                if not self.fixture(table, current): raise RuntimeError('cleanup_identity_changed')
                self.request('DELETE', f'{self.meta}/table/{self.tables[table]}/content/{row["id"]}',
                             headers=self.meta_headers)
                self.report['cleanup'].append(dict(table=table, passed=True))
        after = {table: self.rows(table) for table in TABLES}
        current_lists = {row['id'] for row in after['user_list'] if row.get('user_id') == self.uid}
        self.report['existing_records_unchanged'] = {
            table: before == self.hashes(table, after[table], current_lists)
            for table, before in self.before.items()}
        if not all(self.report['existing_records_unchanged'].values()):
            raise RuntimeError('storage_comparison_failed')
        self.report['cleanup_complete'] = True


def unpack_rows(data):
    return data if isinstance(data, list) else data.get('items', [])


async def journey(page, audit, width, report, wire, base, pause):
    phase = ''
    async def step(name, action):
        nonlocal phase
        phase = name
        report['current_step'] = name
        print('STEP '+str(width)+' '+name, flush=True)
        await asyncio.sleep(pause)
        started, before = time.perf_counter(), dict(wire)
        await action()
        report['steps'].append(dict(name=name, width=width, passed=True,
            ui_ms=round((time.perf_counter()-started)*1000, 3),
            wire={key: value-before[key] for key, value in wire.items()}))
    async def api(path, params=None):
        return await asyncio.to_thread(audit.api, path, params)
    async def fixtures(table): return await asyncio.to_thread(audit.fixtures, table)
    title, identity = audit.media['title'], audit.media['identity_key']
    label, body = audit.marker+'-'+str(width), audit.marker+'-post-'+str(width)
    await page.set_viewport_size({'width': width, 'height': 900})

    async def search():
        await page.goto(base+'/')
        await page.get_by_label('Buscar título', exact=True).fill(title)
        await page.get_by_role('button', name='Buscar', exact=True).click()
        result = page.locator('button.media-card').filter(has=page.get_by_role('heading', name=title, exact=True)).first
        await expect(result).to_be_visible(timeout=60000)
        await result.click()
        await expect(page.locator('.media-detail-title')).to_have_text(title, timeout=60000)
    await step('search-and-detail', search)

    async def review(rating):
        buttons = page.get_by_role('button', name=re.compile(r'^(Salvar avaliação|Editar avaliação)$'))
        await expect(buttons.first).to_be_visible(timeout=60000)
        edit = page.get_by_role('button', name='Editar avaliação', exact=True)
        if await edit.is_visible(): await edit.click()
        await expect(page.locator('input[name=media_key]')).to_have_value(identity)
        await page.get_by_role('button', name='Concluído', exact=True).click()
        await expect(page.locator('input[name=status]')).to_have_value('completed')
        await page.locator('select[name=rating]').select_option(rating)
        await page.locator('textarea[name=review]').fill(label+' review '+rating)
        await page.get_by_role('button', name='Salvar avaliação', exact=True).click()
        await expect(page.get_by_role('button', name='Editar avaliação', exact=True)).to_be_visible(timeout=60000)
        saved = [row for row in unpack_rows(await api('/interactions')) if row.get('media_id') == audit.mid]
        if not (len(saved) == 1 and float(saved[0]['rating']) == float(rating)
                and saved[0].get('review') == label+' review '+rating):
            raise RuntimeError('review_persistence_failed')
    await step('save-review-4.5', lambda: review('4.5'))
    await step('edit-review-3.5', lambda: review('3.5'))

    async def library():
        await page.goto(base+'/biblioteca')
        link = page.locator('a[href="/obra/'+str(audit.mid)+'"]').filter(has_text=title)
        for _ in range(10):
            if await link.count(): break
            more = page.get_by_role('button', name='Mostrar mais', exact=True)
            if not await more.is_visible(): break
            await more.click()
            await asyncio.sleep(3)
        await expect(link.first).to_be_visible(timeout=60000)
        await expect(link.first.locator('xpath=ancestor::article[1]')).to_contain_text('3,5', timeout=60000)
    await step('library', library)

    async def lists():
        await page.goto(base+'/listas')
        await expect(page.locator('.list-row').first).to_be_visible(timeout=60000)
    await step('lists-directory', lists)
    dialog = page.get_by_role('dialog')
    async def create_list():
        await page.get_by_role('button', name='Criar lista', exact=True).click()
        await dialog.locator('input[name=title]').fill(label)
        await dialog.locator('textarea[name=description]').fill(label)
        await dialog.get_by_role('button', name='Salvar lista', exact=True).click()
        await expect(dialog).not_to_be_visible(timeout=60000)
        await expect(page.get_by_role('heading', name=label, exact=True)).to_be_visible()
        created = await fixtures('user_list')
        found = [row for row in created if row['title'] == label]
        if len(found) != 1: raise RuntimeError('list_create_persistence')
        audit.current_list = found[0]['id']
    await step('create-list', create_list)
    async def edit_list():
        await page.get_by_role('button', name='Editar lista', exact=True).click()
        await dialog.locator('input[name=title]').fill(label+' edit')
        await dialog.get_by_role('button', name='Salvar lista', exact=True).click()
        await expect(dialog).not_to_be_visible(timeout=60000)
        found = await fixtures('user_list')
        if not any(row['id'] == audit.current_list and row['title'] == label+' edit' for row in found):
            raise RuntimeError('list_edit_identity')
    await step('edit-list', edit_list)
    async def open_work():
        await page.goto(base+'/obra/'+str(audit.mid))
        await expect(page.locator('.media-detail-title')).to_have_text(title, timeout=60000)
        await expect(page.get_by_text('Carregando informações complementares…', exact=True)).not_to_be_visible(timeout=60000)
    await step('reopen-work', open_work)
    async def add_work():
        await page.get_by_role('button', name='Adicionar a outra lista', exact=True).click()
        select = page.get_by_label('Lista de destino', exact=True)
        await expect(select.locator('option[value="'+str(audit.current_list)+'"]')).to_have_count(1, timeout=60000)
        await select.select_option(str(audit.current_list))
        await page.get_by_role('button', name='Confirmar inclusão', exact=True).click()
        await expect(page.get_by_text('Obra adicionada à lista.', exact=True).first).to_be_visible(timeout=60000)
        rows = unpack_rows(await api(f'/lists/{audit.current_list}/items'))
        if sum(row.get('media_id') == audit.mid for row in rows) != 1:
            raise RuntimeError('list_item_persistence')
    await step('add-work-to-list', add_work)
    async def select_list():
        await lists()
        await page.get_by_role('button').filter(has_text=label+' edit').click()
        await expect(page.locator('a[href="/obra/'+str(audit.mid)+'"]').first).to_be_visible(timeout=60000)
    await step('open-created-list', select_list)
    async def remove_work():
        await page.get_by_role('button', name='Remover obra', exact=True).click()
        await page.get_by_role('button', name='Confirmar exclusão', exact=True).click()
        await expect(page.get_by_text('Esta lista ainda não tem obras.', exact=True)).to_be_visible(timeout=60000)
        rows = unpack_rows(await api(f'/lists/{audit.current_list}/items'))
        if any(row.get('media_id') == audit.mid for row in rows): raise RuntimeError('list_item_removal')
    await step('remove-work-from-list', remove_work)
    async def delete_list():
        await page.get_by_role('button', name='Excluir lista', exact=True).click()
        await page.get_by_role('button', name='Confirmar exclusão', exact=True).click()
        await expect(page.get_by_text('Lista removida.', exact=True)).to_be_visible(timeout=60000)
        if any(row['id'] == audit.current_list for row in await fixtures('user_list')):
            raise RuntimeError('list_removal')
    await step('delete-list', delete_list)

    async def feed():
        await page.goto(base+'/feed')
        await expect(page.get_by_role('button', name='+ Criar publicação', exact=True)).to_be_visible(timeout=60000)
        await asyncio.sleep(3)
    await step('feed', feed)
    async def create_post():
        await page.get_by_role('button', name='+ Criar publicação', exact=True).click()
        await dialog.locator('textarea[name=body]').fill(body)
        await dialog.get_by_role('button', name='Publicar', exact=True).click()
        await expect(dialog).not_to_be_visible(timeout=60000)
        await expect(page.get_by_text(body, exact=True)).to_be_visible(timeout=60000)
        rows = await fixtures('post')
        found = [row for row in rows if row.get('body') == body]
        if len(found) != 1: raise RuntimeError('post_create_persistence')
        audit.current_post = found[0]['id']
    await step('create-post', create_post)
    async def edit_post():
        article = page.get_by_text(body, exact=True).locator('xpath=ancestor::article[1]')
        await article.get_by_role('button', name='Editar', exact=True).click()
        await dialog.locator('textarea[name=body]').fill(body+' edit')
        await dialog.get_by_role('button', name='Salvar edição', exact=True).click()
        await expect(dialog).not_to_be_visible(timeout=60000)
        await expect(page.get_by_text(body+' edit', exact=True)).to_be_visible(timeout=60000)
        rows = await fixtures('post')
        if not any(row['id'] == audit.current_post and row['body'] == body+' edit' for row in rows):
            raise RuntimeError('post_edit_identity')
    await step('edit-post', edit_post)
    async def delete_post():
        article = page.get_by_text(body+' edit', exact=True).locator('xpath=ancestor::article[1]')
        await article.get_by_role('button', name='Excluir publicação', exact=True).click()
        await page.get_by_role('button', name='Confirmar exclusão', exact=True).click()
        await expect(page.get_by_text('Publicação removida.', exact=True)).to_be_visible(timeout=60000)
        if any(row['id'] == audit.current_post for row in await fixtures('post')):
            raise RuntimeError('post_removal')
        await expect(page.get_by_text(body+' edit', exact=True)).not_to_be_visible(timeout=60000)
    await step('delete-post', delete_post)
    async def profile():
        await page.goto(base+'/conta')
        await expect(page.locator('.profile-identity h2')).to_be_visible(timeout=60000)
    await step('profile', profile)


async def main(output, base):
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8'): pass
    report = dict(layer='real-browser-normal-server', started_at=datetime.now(timezone.utc).isoformat(),
                  passed=False, steps=[], verification_requests=[], cleanup=[],
                  backend_python_requests_measured=False, screenshots_saved=False)
    audit, browser, context = None, None, None
    wire = dict(sent_frames=0, received_frames=0, received_bytes=0, javascript_errors=0)
    def received(frame):
        wire['received_frames'] += 1
        wire['received_bytes'] += len(frame.encode() if isinstance(frame, str) else frame)
    try:
        config = dotenv_values(ROOT/'.env')
        auth, social = config['XANO_AUTH_URL'].rstrip('/'), config['XANO_SOCIAL_URL'].rstrip('/')
        origin = urlsplit(auth)
        raw = (Path.home()/'.xano/credentials.yaml').read_text(encoding='utf-8')
        tokens = re.findall(r'^\s*access_token:\s*(.*?)\s*$', raw, re.M)
        if len(tokens) != 1: raise RuntimeError('metadata_profile_ambiguous')
        meta = f'{origin.scheme}://{origin.netloc}/api:meta/workspace/147717'
        with httpx.Client(timeout=25, follow_redirects=False) as client:
            audit = Audit(client, auth, social, meta, tokens[0].strip().strip("'\""), report)
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(channel='msedge', headless=False)
                context = await browser.new_context(viewport={'width': 1440, 'height': 900})
                page = await context.new_page()
                page.on('pageerror', lambda _: wire.update(javascript_errors=wire['javascript_errors']+1))
                def socket(ws):
                    ws.on('framereceived', received)
                    ws.on('framesent', lambda _: wire.update(sent_frames=wire['sent_frames']+1))
                page.on('websocket', socket)
                await page.goto(base+'/login')
                print('READY_FOR_MEMBER_LOGIN: entre na janela Edge. Nao envie a senha pelo chat.', flush=True)
                report['current_step'] = 'manual-login'
                await page.wait_for_url('**/conta', timeout=600000)
                await expect(page.locator('.profile-identity h2')).to_be_visible(timeout=60000)
                # Read only this browser's real session; never persist its token.
                token = await page.evaluate("sessionStorage.getItem('codeboxd_session')")
                if not token:
                    token = next((row['value'] for row in await context.cookies() if row['name'] == 'codeboxd_auth'), '')
                token = unquote(token or '')
                if token.startswith('"'): token = json.loads(token)
                if not token: raise RuntimeError('browser_session_missing')
                audit.token = token
                report['current_step'] = 'member-preflight'
                await asyncio.sleep(22)
                await asyncio.to_thread(audit.prepare)
                for width in (1440, 390):
                    await journey(page, audit, width, report, wire, base, 22)
                    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
                report['current_step'] = 'logout'
                await page.get_by_role('button', name='Sair', exact=True).click()
                await page.wait_for_url('**/login', timeout=30000)
                await page.goto(base+'/biblioteca')
                await page.wait_for_url('**/login', timeout=30000)
                report['logout_protected_route_denied'] = True
                report['passed'] = not wire['javascript_errors']
    except Exception as error:
        report['failure_type'] = type(error).__name__
    finally:
        if audit is not None:
            try:
                delay = max(0, audit.retry_until-time.monotonic())
                while delay > 0:
                    await asyncio.sleep(min(30, delay))
                    delay = max(0, audit.retry_until-time.monotonic())
                print('CLEANUP_AND_STORAGE_COMPARISON', flush=True)
                with httpx.Client(timeout=25, follow_redirects=False) as cleanup_client:
                    audit.client = cleanup_client
                    await asyncio.to_thread(audit.cleanup)
            except Exception as error:
                report['cleanup_failure_type'] = type(error).__name__
                report['passed'] = False
            audit.token = ''
        report['passed'] = bool(report['passed'] and report.get('cleanup_complete'))
        report['wire_totals'] = wire
        output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        # Playwright's context manager closes its browser even after exceptions.
        print(json.dumps(dict(passed=report['passed'], steps=len(report['steps']),
            failed_step=report.get('current_step') if not report['passed'] else None,
            failure_type=report.get('failure_type'), cleanup_complete=report.get('cleanup_complete'))), flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--base', default='http://127.0.0.1:3030')
    args = parser.parse_args()
    if args.base not in ('http://127.0.0.1:3030', 'http://localhost:3030'):
        parser.error('Only the normal loopback server on port 3030 is supported')
    raise SystemExit(asyncio.run(main(args.output, args.base.rstrip('/'))))
