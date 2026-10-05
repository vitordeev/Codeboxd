"""Live browser signup check. Credentials stay in ignored local storage."""
import json
import secrets
from pathlib import Path
from playwright.sync_api import sync_playwright

account_path = Path('.local/signup-test-account.json')
if account_path.exists():
    account = json.loads(account_path.read_text(encoding='utf8'))
else:
    suffix = secrets.token_hex(5)
    account = dict(name='Teste visual Codeboxd', username='visual_' + suffix,
                   email='visual_' + suffix + '@example.com', password=secrets.token_urlsafe(24)+'A1')
    account_path.write_text(json.dumps(account), encoding='utf8')

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width':1440,'height':1000})
    page.set_default_timeout(60000)
    page.goto('http://localhost:3001/cadastro')
    for key in ('name','username','email','password'):
        page.locator(f'input[name={key}]').fill(account[key])
    page.locator('input[name=confirm_password]').fill('DifferentPassword1')
    page.get_by_role('button',name='Criar conta',exact=True).click()
    page.get_by_role('alert').filter(has_text='As senhas não coincidem.').wait_for()
    print('PASS signup password confirmation',flush=True)
    page.locator('input[name=confirm_password]').fill(account['password'])
    page.get_by_role('button',name='Criar conta',exact=True).click()
    # The account was created in the first run; also verify duplicate rejection.
    page.get_by_role('alert').filter(has_text='E-mail ou nome de usuário indisponível.').wait_for()
    print('PASS duplicate registration rejected',flush=True)
    page.goto('http://localhost:3001/login')
    page.locator('input[name=email]').fill(account['email'])
    page.locator('input[name=password]').fill(account['password'])
    page.get_by_role('button',name='Entrar',exact=True).click()
    page.wait_for_url('**/conta',timeout=90000)
    page.get_by_role('button',name='Salvar perfil').wait_for()
    print('PASS login of account created through signup',flush=True)
    page.reload()
    page.get_by_role('button',name='Salvar perfil').wait_for()
    print('PASS session survives reload',flush=True)
    page.get_by_role('button',name='Sair',exact=True).click()
    page.wait_for_url('**/login')
    page.locator('input[name=email]').fill(account['email'])
    page.locator('input[name=password]').fill(account['password'])
    page.get_by_role('button',name='Entrar',exact=True).click()
    page.wait_for_url('**/conta',timeout=90000)
    page.get_by_role('button',name='Salvar perfil').wait_for()
    print('PASS new account login after logout',flush=True)
    page.get_by_role('button',name='Sair',exact=True).click()
    page.wait_for_url('**/login')
    page.goto('http://localhost:3001/cadastro')
    page.screenshot(path='.local/signup-desktop.png',full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path='.local/signup-mobile.png',full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    print('PASS signup mobile layout',flush=True)
    browser.close()
