"""Describe historical account artifacts without printing identities or secrets."""
import json
from collections import Counter

from audit_inventory import HERE, ROOT, git


def summarize(value):
    counts = Counter()
    roles = Counter()

    def walk(item):
        if isinstance(item, dict):
            keys = {str(k).lower(): v for k, v in item.items()}
            if 'email' in keys and any(k in keys for k in ('password', 'senha')):
                counts['account_records_with_password'] += 1
            for key, content in keys.items():
                if key in ('password', 'senha') and isinstance(content, str) and content:
                    counts['nonempty_password_fields'] += 1
                if key in ('authtoken', 'auth_token', 'token', 'access_token') and isinstance(content, str) and content:
                    counts['nonempty_token_fields'] += 1
                if key == 'role' and content in ('member', 'admin', 'moderator'):
                    roles[content] += 1
                walk(content)
        elif isinstance(item, list):
            for child in item:
                walk(child)
    walk(value)
    return {'field_counts': dict(counts), 'explicit_roles': dict(roles)}


def main():
    inv = json.loads((HERE / 'inventory.json').read_text(encoding='utf-8'))
    output = []
    seen = set()
    secrets = set()
    identities = set()

    def collect(item):
        if isinstance(item, dict):
            for key, value in item.items():
                if str(key).lower() in ('email', 'password', 'senha', 'authtoken', 'auth_token', 'token', 'access_token') and isinstance(value, str):
                    if len(value) >= 8:
                        secrets.add(value)
                    if str(key).lower() == 'email':
                        identities.add(value.strip().lower())
                collect(value)
        elif isinstance(item, list):
            for child in item:
                collect(child)
    for item in inv['findings']:
        if item['scope'] != 'history' or not item['path'].startswith('.local/') or not item['path'].endswith('.json'):
            continue
        if item['object'] in seen:
            continue
        seen.add(item['object'])
        content = json.loads(git('cat-file', 'blob', item['object']))
        collect(content)
        output.append({'path': item['path'], 'object': item['object'], **summarize(content),
                       'same_path_present_locally': (ROOT / item['path']).exists()})
    (HERE / 'account-triage.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    from dotenv import dotenv_values
    secrets.update(v for k, v in dotenv_values(ROOT / '.env').items()
                   if v and len(v) >= 12 and any(word in k for word in ('TOKEN', 'KEY', 'PASSWORD', 'SECRET')))
    for private_file in (ROOT / '.local' / 'credential-rotation').glob('account-*.json'):
        collect(json.loads(private_file.read_text(encoding='utf-8')))
    private_policy = ROOT / '.local/session-revocation'
    legacy = private_policy / 'legacy-sessions.json'
    if legacy.exists():
        collect(json.loads(legacy.read_text(encoding='utf-8')))
    race = private_policy / 'password-race.json'
    if race.exists():
        race_data = json.loads(race.read_text(encoding='utf-8'))
        collect(race_data)
        secrets.update(value for value in race_data.get('candidates', []) if isinstance(value, str))
    artifacts = list(HERE.rglob('*')) + list((HERE.parent / 'revogar-sessoes-apos-troca-senha').rglob('*'))
    for artifact in artifacts:
        if artifact.suffix in ('.md', '.json', '.py'):
            text = artifact.read_text(encoding='utf-8')
            if any(secret in text for secret in secrets):
                raise RuntimeError('Private content found in audit artifact; output suppressed')
    print(json.dumps({'historical_account_artifacts': output, 'distinct_email_identities': len(identities),
                      'artifact_privacy_check': 'passed'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        raise SystemExit('Triage failed; raw exception suppressed') from None
