"""Read-only metadata audit. Raw data and credentials never leave process output."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

from audit_inventory import ROOT, HERE, git


def main():
    report = {'mode': 'GET-only', 'accounts': [], 'limitations': []}
    config = dotenv_values(ROOT / '.env')
    origin = urlsplit(config.get('XANO_AUTH_URL', ''))
    if origin.scheme != 'https' or not origin.hostname or not origin.hostname.endswith(('.xano.io', '.xano.com')) or origin.username or origin.password:
        raise RuntimeError('Unexpected metadata origin')
    raw = (Path.home() / '.xano/credentials.yaml').read_text(encoding='utf-8')
    profiles = re.findall(r'^  [^:\r\n]+:\s*\n((?:^    .*\n?)+)', raw, re.M)
    matching = []
    for block in profiles:
        endpoint = re.search(r'^    instance_origin:\s*([^\r\n]+)', block, re.M)
        if endpoint and urlsplit(endpoint.group(1).strip().strip('\'"')).hostname == origin.hostname:
            matching.append(block)
    if len(matching) != 1:
        raise RuntimeError('Ambiguous metadata credential')
    tokens = re.findall(r'^\s*access_token:\s*(.*?)\s*$', matching[0], re.M)
    if len(tokens) != 1:
        raise RuntimeError('Ambiguous metadata credential')
    headers = {'Authorization': 'Bearer ' + tokens[0].strip().strip('\'"')}
    base = f'{origin.scheme}://{origin.netloc}/api:meta/workspace/147717'
    targets = []
    seen = set()

    def collect(item):
        if isinstance(item, dict):
            if 'email' in item and 'password' in item:
                targets.append({'email': item['email'], 'id': item.get('id') or item.get('user_id')})
            for value in item.values():
                collect(value)
        elif isinstance(item, list):
            for child in item:
                collect(child)

    inv = json.loads((HERE / 'inventory.json').read_text(encoding='utf-8'))
    for item in inv['findings']:
        if item['scope'] == 'history' and item['path'].startswith('.local/') and item['path'].endswith('.json') and item['object'] not in seen:
            seen.add(item['object'])
            collect(json.loads(git('cat-file', 'blob', item['object'])))
    with httpx.Client(timeout=20, follow_redirects=False) as client:
        response = client.get(base + '/table', headers=headers)
        report['metadata_tables_status'] = response.status_code
        if response.status_code != 200:
            report['limitations'].append('Metadata table access unavailable; no raw response retained')
        else:
            tables = response.json()
            if isinstance(tables, dict):
                tables = tables.get('items', [])
            table = next((x for x in tables if x.get('name') == 'user'), None)
            report['user_table_found'] = table is not None
            if table:
                for index, target in enumerate(targets, 1):
                    row = {'account': f'A.{index:02}', 'historical_id_available': isinstance(target['id'], int)}
                    if isinstance(target['id'], int):
                        record = client.get(base + f'/table/{int(table["id"])}/content/{target["id"]}', headers=headers)
                        row['record_status'] = record.status_code
                        if record.status_code == 200:
                            current = record.json()
                            matched = str(current.get('email', '')).strip().lower() == str(target['email']).strip().lower()
                            row['identity_matches_history'] = matched
                            if matched:
                                row['role'] = current.get('role') if current.get('role') in ('admin', 'member', 'moderator') else 'unknown'
                                row['account_status'] = current.get('account_status') if current.get('account_status') in ('active', 'disabled') else 'unknown'
                    else:
                        row['limitation'] = 'No historical numeric ID; no broad user enumeration performed'
                    report['accounts'].append(row)
    (HERE / 'access-audit.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except httpx.RequestError:
        raise SystemExit('Network unavailable for read-only Xano metadata audit; no raw output retained') from None
    except RuntimeError as exc:
        message = str(exc)
        allowed = ('Unexpected metadata origin', 'Ambiguous metadata credential', 'Git inventory operation failed; raw output suppressed')
        raise SystemExit(message if message in allowed else 'Metadata audit failed; details suppressed') from None
    except Exception as exc:
        raise SystemExit('Metadata audit failed (' + type(exc).__name__ + '); raw output suppressed') from None
