"""Real browser checks with two controlled accounts; writes only to test list."""
from collections import Counter
import argparse
import json
import time
import traceback

from playwright.sync_api import sync_playwright, expect

from tools.default_list_deployment import PRIVATE
from tools.default_list_integrity import CHANGE
from tools.session_revocation import ROOT

REPORT = CHANGE / 'validation/default-lists-browser-real.json'
PAUSE = 4
MUTATION_WIDTHS = (1440,390)


def main():
    test = json.loads((PRIVATE / 'test-account.json').read_text(encoding='utf-8'))
    other = json.loads((ROOT / '.local/credential-rotation/account-03.json').read_text(encoding='utf-8'))
    backup = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
    report = dict(layer='real_browser_two_authenticated_accounts', checks=[], passed=False)
    if REPORT.exists():
        REPORT.rename(REPORT.with_name('default-lists-browser-real-' + str(time.time_ns()) + '.json'))
    def step(name):
        report['active_step'] = name
        REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    def check(name, condition=True):
        report['checks'].append(dict(scenario=name, passed=bool(condition)))
        REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
        if not condition: raise RuntimeError('Browser assertion failed')
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        try:
            for index, account in enumerate((test, other)):
                context = browser.new_context(viewport={'width':1440, 'height':900})
                try:
                    page = context.new_page()
                    step(f'account_{index+1}_login')
                    page.goto('http://127.0.0.1:3030/login', wait_until='domcontentloaded')
                    page.locator('input[name=email]').fill(account['email'])
                    page.locator('input[name=password]').fill(account['password'])
                    page.get_by_role('button', name='Entrar', exact=True).click()
                    expect(page).to_have_url('http://127.0.0.1:3030/conta', timeout=60000)
                    time.sleep(PAUSE)
                    step(f'account_{index+1}_personal_directory')
                    page.goto('http://127.0.0.1:3030/listas', wait_until='domcontentloaded')
                    expect(page.get_by_role('heading', name='Suas listas', exact=True)).to_be_visible(timeout=60000)
                    expected_titles = (['Quero ver / ler']*3 + ['Já assisti / li',test['browser_list_title']]
                                       if index == 0 else [r['title'] for r in backup['lists'] if r['user_id']==account['user_id']])
                    expect(page.locator('.list-row')).to_have_count(len(expected_titles), timeout=60000)
                    for width in (1440,390):
                        page.set_viewport_size({'width':width,'height':900})
                        titles = page.locator('.list-row > span:first-of-type').all_text_contents()
                        check(f'account_{index+1}_personal_lists_{width}', Counter(titles)==Counter(expected_titles))
                        check(f'account_{index+1}_layout_{width}', not page.evaluate('document.documentElement.scrollWidth > innerWidth'))
                    time.sleep(PAUSE)
                    step(f'account_{index+1}_public_directory')
                    page.get_by_role('button', name='Explorar listas públicas', exact=True).click()
                    foreign_owner = next(r['user_id'] for r in backup['lists'] if r['user_id']!=account['user_id'] and r['is_public'])
                    group = page.locator('.public-list-group').filter(has=page.locator(f'.public-list-owner[href="/perfil/{foreign_owner}"]'))
                    expect(group).to_be_visible(timeout=60000)
                    group.locator('.list-row').first.click()
                    time.sleep(PAUSE)
                    expect(page.get_by_role('button', name='Editar lista', exact=True)).to_have_count(0)
                    expect(page.get_by_role('searchbox', name='Buscar obras para a lista')).to_have_count(0)
                    check(f'account_{index+1}_foreign_list_read_only')
                    if index == 0:
                        for width in MUTATION_WIDTHS:
                            step(f'open_existing_media_{width}')
                            page.set_viewport_size({'width':width,'height':900})
                            time.sleep(PAUSE)
                            page.goto(f"http://127.0.0.1:3030/obra/{test['browser_media_id']}", wait_until='domcontentloaded')
                            time.sleep(PAUSE)
                            page.get_by_role('button', name='Adicionar a outra lista', exact=True).click(timeout=60000)
                            step(f'wait_destination_{width}')
                            select = page.get_by_label('Lista de destino')
                            expect(select.locator(f"option[value='{test['browser_list_id']}']")).to_have_count(1, timeout=60000)
                            time.sleep(PAUSE)
                            step(f'add_existing_media_{width}')
                            select.select_option(str(test['browser_list_id']))
                            page.get_by_role('button', name='Confirmar inclusão', exact=True).click()
                            expect(page.get_by_text('Obra adicionada à lista.', exact=True).first).to_be_visible(timeout=60000)
                            time.sleep(PAUSE)
                            step(f'confirm_added_list_items_{width}')
                            page.goto('http://127.0.0.1:3030/listas', wait_until='domcontentloaded')
                            page.locator('.list-row').filter(has_text=test['browser_list_title']).click(timeout=60000)
                            expect(page.locator('.list-media-item')).to_have_count(1, timeout=60000)
                            check(f'add_existing_media_persisted_{width}')
                            time.sleep(PAUSE)
                            step(f'remove_list_item_{width}')
                            page.get_by_role('button', name='Remover obra', exact=True).click()
                            dialog = page.get_by_role('alertdialog')
                            dialog.get_by_role('button', name='Confirmar exclusão', exact=True).click()
                            expect(page.locator('.list-media-item')).to_have_count(0, timeout=60000)
                            check(f'remove_test_media_persisted_{width}')
                except Exception as exc:
                    frames = [frame for frame in traceback.extract_tb(exc.__traceback__) if frame.filename.endswith('default_lists_browser_real.py')]
                    report['error'] = dict(type=type(exc).__name__, source_line=frames[-1].lineno if frames else None)
                    try:
                        (PRIVATE / 'browser-failure.html').write_text(page.content(), encoding='utf-8')
                        page.screenshot(path=str(PRIVATE / 'browser-failure.png'), full_page=True)
                    except Exception:
                        pass
                    raise
                finally:
                    context.close()
                time.sleep(8)
            report['passed'] = True
        finally:
            browser.close()
            REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(dict(passed=True, checks=len(report['checks']), accounts=2, widths=[1440,390])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pause', type=float, default=4)
    parser.add_argument('--mutation-widths', type=int, nargs='+', default=[1440,390])
    args = parser.parse_args()
    PAUSE = args.pause
    MUTATION_WIDTHS = tuple(args.mutation_widths)
    try: main()
    except Exception as exc:
        raise SystemExit('Real browser stopped (' + type(exc).__name__ + '); details suppressed; inspect sanitized report') from None
