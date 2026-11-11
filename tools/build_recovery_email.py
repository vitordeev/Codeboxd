"""Build the inline Xano email from its editable HTML template; no network."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'xano/templates/recovery_email.html'
ENDPOINT = ROOT / 'xano/api/authentication/reset/request_reset_link_GET.xs'
TEXT = ('Codeboxd - Recuperacao de acesso\n\nSeu codigo: {{code}}\n\n'
        'Use este codigo na pagina de recuperacao para criar sua nova senha.\n'
        'Valido por 15 minutos. Uso unico.\n\n'
        'Se voce nao solicitou a troca, ignore esta mensagem. '
        'Sua senha continua a mesma. Nunca compartilhe este codigo.')


def expression(template):
    if template.count('{{code}}') != 1:
        raise ValueError('Expected exactly one code slot')
    before, after = template.split('{{code}}')
    return json.dumps(before, ensure_ascii=False) + ' ~ $token_and_email.token ~ ' + json.dumps(after, ensure_ascii=False)


def build():
    html = TEMPLATE.read_text(encoding='utf-8')
    source = ENDPOINT.read_text(encoding='utf-8')
    generated = ('        var $message {\n          value = ' + expression(html) + '\n        }\n'
                 '        var $plain_message {\n          value = ' + expression(TEXT) + '\n        }\n')
    source, count = re.subn(r'        var \$message \{.*?\n        \}\n(?:        var \$plain_message \{.*?\n        \}\n)?',
                            lambda _: generated, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Missing mail body')
    ENDPOINT.write_text(source, encoding='utf-8')
    preview = ROOT / '.local/recovery-email-preview.html'
    preview.parent.mkdir(exist_ok=True)
    preview.write_text(html.replace('{{code}}', '482619'), encoding='utf-8')
    print(json.dumps({'html_bytes': len(html.encode()), 'external_images': False}))


if __name__ == '__main__':
    build()
