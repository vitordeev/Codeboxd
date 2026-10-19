"""Controlled browser checks; private account credentials never enter output."""
import argparse
import json
import time
from pathlib import Path
from urllib.parse import unquote

import httpx
from dotenv import dotenv_values
from playwright.sync_api import sync_playwright


checks = []
errors = []
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', required=True)
parser.add_argument('--account-file', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
if args.output.exists():
    parser.error('Use a new output file to preserve historical evidence')
scratch = Path('.local') / ('browser-probe-' + str(time.time_ns()))
scratch.mkdir(parents=True)
account = json.loads(args.account_file.read_text(encoding='utf-8'))[0]
base = args.base_url.rstrip('/')
fixture = scratch / 'post-image-probe.png'
fixture.write_bytes(Path('assets/default-movie-cover.png').read_bytes())
invalid_fixture = scratch / 'post-image-invalid.png'
invalid_fixture.write_bytes(b'not an image')
output = args.output
marker = 'Codeboxd image probe ' + str(time.time_ns())
cleanup_token = ''
config = dotenv_values('.env')


def record(name, passed=True):
    checks.append({'scenario': name, 'passed': passed})
    print(name, passed, flush=True)
    output.write_text(json.dumps({'layer': 'browser', 'checks': checks,
                                 'javascript_error_count': len(errors)}, indent=2) + '\n', encoding='utf-8')


with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 1000})
    page = context.new_page()
    page.set_default_timeout(25000)
    page.on('pageerror', lambda error: errors.append(type(error).__name__))
    try:
        page.goto(base + '/admin')
        page.wait_for_url('**/admin/login')
        page.get_by_role('heading', name='Acesso administrativo').wait_for()
        record('guest_admin_redirect')
        for width in (1440, 390):
            page.set_viewport_size({'width': width, 'height': 1000})
            page.screenshot(path=str(scratch / f'admin-login-{width}.png'), full_page=True)
            record(f'admin_login_no_overflow_{width}', page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
        page.set_viewport_size({'width': 1440, 'height': 1000})
        page.goto(base + '/login')
        page.locator('input[name=email]').fill(account['email'])
        page.locator('input[name=password]').fill(account['password'])
        page.locator('button[type=submit]').click()
        page.wait_for_url('**/conta')
        page.get_by_role('button', name='Editar perfil', exact=True).wait_for()
        record('member_browser_login')
        cleanup_token = page.evaluate("sessionStorage.getItem('codeboxd_session')") or ''
        if not cleanup_token:
            cleanup_token = next((cookie['value'] for cookie in context.cookies(base)
                                  if cookie['name'] == 'codeboxd_auth'), '')
        cleanup_token = unquote(cleanup_token)
        if cleanup_token.startswith('"'):
            cleanup_token = json.loads(cleanup_token)
        page.goto(base + '/admin')
        page.wait_for_url(base + '/')
        record('member_admin_route_denied')
        page.goto(base + '/feed')
        page.get_by_role('heading', name='Entre histórias', exact=True).wait_for()
        page.get_by_role('button', name='+ Criar publicação', exact=True).click()
        page.locator('input[type=file]').set_input_files(str(invalid_fixture))
        page.get_by_role('button', name='Carregar imagem', exact=True).click()
        page.get_by_role('dialog').get_by_text('Envie uma imagem PNG, JPG, WEBP ou GIF válida.', exact=True).wait_for()
        record('invalid_image_rejected')
        page.locator('input[type=file]').set_input_files(str(fixture))
        page.get_by_role('button', name='Carregar imagem', exact=True).click()
        preview = page.get_by_alt_text('Previa da imagem enviada', exact=True)
        preview.wait_for()
        page.wait_for_function("document.querySelector('img[alt=\"Previa da imagem enviada\"]')?.naturalWidth > 0")
        record('post_image_staging_and_preview')
        page.get_by_role('button', name='Remover imagem', exact=True).click()
        preview.wait_for(state='hidden')
        record('post_image_removed_from_draft')
        page.locator('input[type=file]').set_input_files(str(fixture))
        page.get_by_role('button', name='Carregar imagem', exact=True).click()
        preview.wait_for()
        page.locator('textarea[name=body]').fill(marker)
        page.wait_for_timeout(20000)
        page.get_by_role('button', name='Publicar', exact=True).click()
        page.get_by_role('dialog').wait_for(state='hidden')
        card = page.locator('article.post-card').filter(has_text=marker)
        card.wait_for()
        image = card.get_by_alt_text('Imagem anexada a publicacao', exact=True)
        image.wait_for()
        image.scroll_into_view_if_needed()
        page.wait_for_function('(img) => img.naturalWidth > 0', arg=image.element_handle())
        record('post_with_image_created')
        page.reload()
        card.wait_for()
        image.wait_for()
        image.scroll_into_view_if_needed()
        page.wait_for_function('(img) => img.naturalWidth > 0', arg=image.element_handle())
        record('post_image_persists_after_reload')
        page.wait_for_timeout(20000)
        card.get_by_role('button', name='Editar', exact=True).click()
        page.locator('textarea[name=body]').fill(marker + ' edited')
        page.get_by_role('button', name='Salvar edição', exact=True).click()
        page.get_by_role('dialog').wait_for(state='hidden')
        card.get_by_text(marker + ' edited', exact=True).wait_for()
        record('post_edit_preserves_image', image.count() == 1)
        page.wait_for_timeout(20000)
        card.get_by_role('button', name='Excluir publicação', exact=True).click()
        page.get_by_role('button', name='Confirmar exclusão', exact=True).click()
        card.wait_for(state='hidden')
        record('controlled_post_deleted_in_browser')
        page.get_by_role('button', name='+ Criar publicação', exact=True).click()
        page.locator('input[type=file]').set_input_files(str(fixture))
        page.get_by_role('button', name='Carregar imagem', exact=True).click()
        preview.wait_for()
        page.get_by_role('dialog').get_by_role('button', name='Fechar', exact=True).click()
        page.get_by_role('dialog').wait_for(state='hidden')
        record('post_cancel_discards_staged_image', not any(Path('uploaded_files/posts').glob('staged-*.png')))
        page.screenshot(path=str(scratch / 'feed-image-draft.png'), full_page=True)
        record('no_javascript_errors', not errors)
    except Exception as exc:
        record('browser_exception_' + type(exc).__name__, False)
        page.screenshot(path=str(scratch / 'browser-failure.png'), full_page=True)
        print('url_path', page.url.replace(base, '').split('?')[0], flush=True)
        print('headings', page.locator('h1,h2').all_text_contents(), flush=True)
        print('buttons', page.locator('button').all_text_contents(), flush=True)
        raise
    finally:
        if page.get_by_role('dialog').is_visible():
            page.get_by_role('dialog').get_by_role('button', name='Fechar', exact=True).click()
            page.get_by_role('dialog').wait_for(state='hidden')
        browser.close()
        if cleanup_token:
            with httpx.Client(timeout=20) as client:
                headers = {'Authorization': 'Bearer ' + cleanup_token}
                def call(method, path, **kwargs):
                    for attempt in range(3):
                        response = client.request(method, config['XANO_SOCIAL_URL'].rstrip('/') + path,
                                                  headers=headers, **kwargs)
                        if response.status_code != 429 or attempt == 2:
                            return response
                        time.sleep(20)
                response = call('GET', '/posts', params={'user_id': account['id']})
                cleaned = response.status_code == 200
                if cleaned:
                    items = response.json()
                    if isinstance(items, dict):
                        items = items.get('items', [])
                    for item in items:
                        if item.get('user_id') == account['id'] and str(item.get('body', '')).startswith(marker):
                            deleted = call('DELETE', '/posts/' + str(item['id']))
                            cleaned = cleaned and deleted.status_code in (200, 204, 404)
                record('temporary_posts_cleanup_confirmed', cleaned)
