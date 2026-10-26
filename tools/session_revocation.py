"""Prepare/deploy a narrowly scoped session policy; raw exports remain private."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
CHANGE = ROOT / 'openspec/changes/revogar-sessoes-apos-troca-senha'
PRIVATE = ROOT / '.local/session-revocation'
GUARD_NAME = 'Security/require_current_session'


def guard_call(allow_reset=False, indent='    '):
    return (f'{indent}function.run "{GUARD_NAME}" {{\n'
            f'{indent}  input = {{user_id: $auth.id, extras: $auth.extras, allow_reset: {str(allow_reset).lower()}}}\n'
            f'{indent}}}\n')


def transform(block):
    if GUARD_NAME in block:
        return block
    if re.search(r'^table user\s*{', block, re.M):
        if 'session_version' in block:
            raise RuntimeError('Existing session schema requires review')
        return re.sub(r'(\bschema\s*{\s*\n)', r'\1    int session_version?=0 filters=min:0\n', block, count=1)
    name = re.search(r'^query\s+(?:"([^"]+)"|([A-Za-z_]\w*))\s+verb=(\w+)', block, re.M)
    if not name:
        return block
    route = name[1] or name[2]
    if re.search(r'\bauth\s*=\s*"user"', block):
        block = re.sub(r'(\bstack\s*{\s*\n)', lambda m: m[1] + guard_call(route == 'reset/update_password') + '\n', block, count=1)
    if route in ('auth/login', 'auth/signup'):
        if route == 'auth/login':
            block = re.sub(r'(\boutput\s*=\s*\[)', r'\1"session_version", ', block, count=1)
        claim = '    api.lambda {\n      code = "return $var.user.session_version ?? 0;"\n    } as $session_version\n\n'
        block, count = re.subn(r'    security\.create_auth_token\s*{', lambda m: claim + m[0], block, count=1)
        if count != 1:
            raise RuntimeError('Missing token issuer')
        block, count = re.subn(r'extras\s*=\s*{}', 'extras = {session_version: $session_version, purpose: "session"}', block, count=1)
        if count != 1:
            raise RuntimeError('Unexpected existing claims')
    if route == 'reset/magic-link-login':
        block = re.sub(r'(\bstack\s*{\s*\n)', r'\1    var $reset_session_version { value = 0 }\n', block, count=1)
        capture = ('\n                    api.lambda {\n'
                   '                      code = "return $var.locked_user.session_version ?? 0;"\n'
                   '                    } as $consumed_session_version\n'
                   '                    var.update $reset_session_version { value = $consumed_session_version }\n')
        block, count = re.subn(r'(var\.update \$reset_user_id\s*{\s*value\s*=\s*\$user.id\s*})', lambda m: m[1] + capture, block, count=1)
        if count != 1:
            raise RuntimeError('Missing transactional reset capture')
        block, count = re.subn(r'extras\s*=\s*{\s*purpose:\s*"password_reset"\s*}',
                              'extras = {purpose: "password_reset", session_version: $reset_session_version}', block, count=1)
        if count != 1:
            raise RuntimeError('Unexpected reset claims')
    if route == 'reset/update_password':
        transaction = '''    db.transaction {
      stack {
        // Lock the account, then revalidate against the current version.
        db.edit user {
          field_name = "id"
          field_value = $auth.id
          data = {updated_at: now}
        }
        db.get user {
          field_name = "id"
          field_value = $auth.id
          output = ["id", "session_version"]
        } as $locked_user
'''
        transaction += guard_call(True, '        ')
        transaction += '''        api.lambda {
          code = "return ($var.locked_user.session_version ?? 0) + 1;"
        } as $next_session_version
        db.edit user {
          field_name = "id"
          field_value = $auth.id
          data = {password: $input.password, session_version: $next_session_version}
        } as $user
      }
    }'''
        block, count = re.subn(r'    db\.edit user\s*{\s*field_name\s*=\s*"id"\s*field_value\s*=\s*\$auth.id\s*data\s*=\s*{password:\s*\$input.password}\s*}\s*as \$user',
                              lambda m: transaction, block, count=1)
        if count != 1:
            raise RuntimeError('Unexpected password update')
    return block


def prepare(source):
    changed = [(block, transform(block)) for block in blocks(source)]
    changed = [(before, after) for before, after in changed if before != after]
    guard = (ROOT / 'xano/function/security/require_current_session.xs').read_text(encoding='utf-8').strip()
    tables = [after for before, after in changed if re.search(r'^table user\s*{', after, re.M)]
    queries = [after for before, after in changed if re.search(r'^query ', after, re.M)]
    if len(tables) != 1 or len(queries) != 42:
        # 39 authenticated queries + login/signup/reset issuer, all inventoried.
        raise RuntimeError('Unexpected deployment coverage')
    return '\n---\n'.join([*tables, guard, *queries]) + '\n', changed


def blocks(text):
    return [part.strip() for part in re.split(r'(?m)^---\s*$', text) if part.strip()]


def identity(block):
    match = re.search(r'\bguid\s*=\s*"([^"]+)"', block)
    return match.group(1) if match else block.splitlines()[0]


def metadata_config():
    config = dotenv_values(ROOT / '.env')
    origin = urlsplit(config.get('XANO_AUTH_URL', ''))
    if origin.scheme != 'https' or not origin.hostname or not origin.hostname.endswith('.xano.io') or origin.username or origin.password:
        raise RuntimeError('Unexpected metadata origin')
    raw = (Path.home() / '.xano/credentials.yaml').read_text(encoding='utf-8')
    matches = []
    for block in re.findall(r'^  [^:\r\n]+:\s*\n((?:^    .*\n?)+)', raw, re.M):
        endpoint = re.search(r'^    instance_origin:\s*([^\r\n]+)', block, re.M)
        if endpoint and urlsplit(endpoint.group(1).strip().strip('\'"')).hostname == origin.hostname:
            matches.append(block)
    if len(matches) != 1:
        raise RuntimeError('Ambiguous instance profile')
    tokens = re.findall(r'^\s*access_token:\s*(.*?)\s*$', matches[0], re.M)
    if len(tokens) != 1:
        raise RuntimeError('Ambiguous credential')
    return (f'{origin.scheme}://{origin.netloc}/api:meta/workspace/147717',
            {'Authorization': 'Bearer ' + tokens[0].strip().strip('\'"')})


def export_workspace(client, base, headers):
    response = client.get(base + '/multidoc', headers=headers, params={'env': 'false', 'records': 'false'})
    if response.status_code != 200:
        raise RuntimeError('Workspace export unavailable')
    return response.text


def inventory(source):
    result = {'documents': len(blocks(source)), 'authenticated': [], 'issuers': []}
    for block in blocks(source):
        name = re.search(r'^query\s+(?:"([^"]+)"|([A-Za-z_]\w*))\s+verb=(\w+)', block, re.M)
        if name:
            row = {'route': name[1] or name[2], 'method': name[3], 'guid': identity(block)}
            if re.search(r'\bauth\s*=\s*"user"', block):
                result['authenticated'].append(row)
            if 'security.create_auth_token' in block:
                result['issuers'].append(row)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--inspect', action='store_true')
    args = parser.parse_args()
    base, headers = metadata_config()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=45, follow_redirects=False) as client:
        source = export_workspace(client, base, headers)
        if args.inspect:
            (PRIVATE / 'published.xs').write_text(source, encoding='utf-8')
            baseline = (PRIVATE / 'baseline.xs').read_text(encoding='utf-8')
            _, changed = prepare(baseline)
            touched = {identity(before) for before, revised in changed}
            after_by_id = {identity(b): b for b in blocks(source)}
            before_ids = {identity(b) for b in blocks(baseline)}
            added = [b for key, b in after_by_id.items() if key not in before_ids]
            unrelated = [identity(b) for b in blocks(baseline)
                         if identity(b) not in touched and after_by_id.get(identity(b)) != b]
            report = {'protected_count': len(inventory(source)['authenticated']),
                      'guard_calls': source.count('function.run "' + GUARD_NAME + '"'),
                      'unrelated_documents_changed': len(unrelated),
                      'added_documents': len(added),
                      'only_expected_function_added': len(added) == 1 and bool(re.search(r'^function "Security/require_current_session"', added[0], re.M)),
                      'has_version_schema': bool(re.search(r'int session_version', source))}
            report['passed'] = (report['protected_count'] == 39 and report['guard_calls'] == 40
                                and not unrelated and report['has_version_schema'] and report['only_expected_function_added'])
            (CHANGE / 'published-inspection.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
            deployment = CHANGE / 'deployment.json'
            if deployment.exists():
                previous = json.loads(deployment.read_text(encoding='utf-8'))
                if previous.get('applied') and previous.get('http_status') == 200:
                    previous['response_shape_differed_from_preview'] = not bool(previous.get('operations'))
                    previous['export_verification'] = report
                    previous['passed'] = report['passed']
                    deployment.write_text(json.dumps(previous, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(report, indent=2))
            return
        if args.preview or args.apply:
            baseline = (PRIVATE / 'baseline.xs').read_text(encoding='utf-8')
            if source != baseline:
                raise RuntimeError('Remote changed since baseline; review required')
            patch, changes = prepare(source)
            (PRIVATE / 'patch.xs').write_text(patch, encoding='utf-8')
            params = {'partial': 'true', 'env': 'false', 'records': 'false', 'delete': 'false'}
            digest = hashlib.sha256(patch.encode()).hexdigest()
            approved = PRIVATE / 'approved.json'
            if args.apply:
                approval = json.loads(approved.read_text(encoding='utf-8'))
                if approval.get('patch_hash') != digest or not approval.get('passed'):
                    raise RuntimeError('Missing matching successful preview')
            response = client.post(base + ('/multidoc' if args.apply else '/multidoc/dry-run'),
                                   headers={**headers, 'Content-Type': 'text/x-xanoscript'},
                                   params=params, content=patch.encode())
            report = {'applied': args.apply, 'http_status': response.status_code, 'passed': False}
            if response.status_code != 200:
                (CHANGE / 'deployment.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
                raise RuntimeError('Metadata operation unavailable')
            result = response.json()
            (PRIVATE / ('apply-response.json' if args.apply else 'preview-response.json')).write_text(json.dumps(result), encoding='utf-8')
            operations = result.get('operations', [])
            report['operations'] = [{key: op.get(key) for key in ('type', 'name', 'action')} for op in operations]
            report['summary'] = result.get('summary')
            errors = [str(op.get('details', '')) for op in operations if 'parse error' in str(op.get('details', '')).lower()]
            if errors:
                report['parse_errors'] = errors
            report['passed'] = (args.apply or bool(operations)) and not errors and all(op.get('type') in ('table', 'function', 'query')
                                                                      and op.get('action') != 'delete' for op in operations)
            (CHANGE / ('deployment.json' if args.apply else 'preview.json')).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(report, indent=2))
            if not report['passed']:
                raise RuntimeError('Unexpected metadata preview scope')
            if not args.apply:
                approved.write_text(json.dumps({'passed': True, 'patch_hash': digest}), encoding='utf-8')
            else:
                after = export_workspace(client, base, headers)
                (PRIVATE / 'published.xs').write_text(after, encoding='utf-8')
                report['protected_count'] = len(inventory(after)['authenticated'])
                report['guard_calls'] = after.count('function.run "' + GUARD_NAME + '"')
                before_by_id = {identity(b): b for b in blocks(source)}
                after_by_id = {identity(b): b for b in blocks(after)}
                touched = {identity(before) for before, revised in changes}
                unrelated = [key for key, value in before_by_id.items()
                             if key not in touched and after_by_id.get(key) != value]
                report['unrelated_documents_changed'] = len(unrelated)
                report['passed'] = report['protected_count'] == 39 and report['guard_calls'] == 40 and not unrelated
                (CHANGE / 'deployment.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
                if not report['passed']:
                    raise RuntimeError('Published coverage mismatch')
            return
    destination = PRIVATE / 'baseline.xs'
    if destination.exists() and destination.read_text(encoding='utf-8') != source:
        raise RuntimeError('Baseline changed; preserve and review before continuing')
    destination.write_text(source, encoding='utf-8')
    report = inventory(source)
    (CHANGE / 'remote-inventory.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except httpx.RequestError:
        raise SystemExit('Session deployment network unavailable; raw output suppressed') from None
    except Exception as exc:
        raise SystemExit('Session deployment stopped (' + type(exc).__name__ + '); raw output suppressed') from None
