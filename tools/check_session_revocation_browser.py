"""Validate expired-session redirect and controlled fresh login in the real app."""
import json
import re

from playwright.sync_api import sync_playwright, expect

from tools.session_revocation import ROOT, CHANGE, PRIVATE


def main():
    account = json.loads((ROOT / '.local/credential-rotation/account-03.json').read_text(encoding='utf-8'))
    legacy = json.loads((PRIVATE / 'legacy-sessions.json').read_text(encoding='utf-8'))[0]['token']
    report = {'layer': 'real-browser-authenticated', 'passed': False}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='msedge', headless=True)
        try:
            context = browser.new_context(viewport={'width': 1440, 'height': 900})
            context.add_cookies([{'name': 'codeboxd_auth', 'value': legacy, 'url': 'http://127.0.0.1:3030/'}])
            page = context.new_page()
            page.goto('http://127.0.0.1:3030/biblioteca', wait_until='domcontentloaded')
            expect(page).to_have_url(re.compile(r'/login(?:\?|$)'), timeout=60000)
            report['legacy_session_redirected_to_login'] = True
            page.locator('input[name=email]').fill(account['email'])
            page.locator('input[name=password]').fill(account['password'])
            page.get_by_role('button', name='Entrar', exact=True).click()
            expect(page).to_have_url('http://127.0.0.1:3030/conta', timeout=60000)
            report['fresh_login_redirected_account'] = True
            page.goto('http://127.0.0.1:3030/biblioteca', wait_until='domcontentloaded')
            expect(page.get_by_role('heading', name='Minha biblioteca', exact=True)).to_be_visible(timeout=60000)
            expect(page.get_by_role('button', name='Sair', exact=True)).to_be_visible(timeout=60000)
            report['fresh_session_library_visible'] = True
            report['passed'] = True
            context.close()
        finally:
            browser.close()
            (CHANGE / 'browser-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('Browser session check stopped (' + type(exc).__name__ + '); private details suppressed') from None
