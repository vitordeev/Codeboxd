"""Exercise the actual admin catalog query on synthetic interpreter-only rows."""
import argparse
import json
from pathlib import Path
import re
import time

import httpx
from tools.session_revocation import metadata_config

ROOT = Path(__file__).resolve().parents[1]


def script():
    source = (ROOT / 'xano/api/codeboxd/admin_catalog_GET.xs').read_text(encoding='utf-8')
    inputs = re.search(r'  input \{(.*?)\n  \}', source, re.S).group(1)
    start = '    var $catalog' if '    var $catalog' in source else '    db.query media'
    query = source[source.index(start):source.rindex('\n  }\n\n  response')]
    query = query.replace('db.query media', 'db.query catalog_fixture_media').replace('media.', 'catalog_fixture_media.')
    response = source[source.index('  response ='):source.index('\n  guid =')]
    table = '''table catalog_fixture_media {
  schema {
    int id
    text identity_key?
    text external_source?
    text external_id?
    text media_type
    text title
    text description?
    text cover_url?
    int year?
  }
  index = [{type: "primary", field: [{name: "id"}]}]
}'''
    setup = '\n'.join('    db.add catalog_fixture_media { data = ' + json.dumps({
        'media_type': kind, 'title': title, 'identity_key': kind + ':' + str(i)}) + ' }'
        for kind in ('movie', 'series', 'book', 'anime')
        for i, title in enumerate(('Alpha 100%_title', 'Beta title')))
    return table + '\n---\nfunction "catalog_fixture" {\n  input {' + inputs + '\n  }\n  stack {\n' + setup + '\n' + query + '\n  }\n' + response + '\n}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve previous evidence')
    report = {'layer': 'synthetic_xano_catalog_interpreter', 'published': False, 'cases': []}
    base, headers = metadata_config()
    with httpx.Client(timeout=30) as client:
        cases = [(kind, '', 1, 2, ['Alpha 100%_title']) for kind in ('movie', 'series', 'book', 'anime')]
        cases += [('movie', 'Alpha', 1, 1, ['Alpha 100%_title']),
                  ('movie', 'ALPHA', 1, 1, ['Alpha 100%_title']),
                  ('movie', '100%_', 1, 1, ['Alpha 100%_title']),
                  ('movie', '100X_', 1, 0, []),
                  ('movie', 'absent-7fa56e31', 1, 0, []), ('movie', '', 2, 2, ['Beta title'])]
        for kind, search, page, total, titles in cases:
            inputs = {'media_type': kind, 'search': search, 'page': page, 'per_page': 1}
            response = client.post(base + '/multidoc/debug', headers={**headers, 'Content-Type': 'text/x-xanoscript'},
                params={'entry_obj_type': 'function', 'entry_obj_name': 'catalog_fixture', 'input': json.dumps(inputs)}, content=script())
            response.raise_for_status()
            data = response.json()
            debug_id = data.get('id') or data.get('debug_id')
            for _ in range(15):
                if data.get('status') not in ('pending', 'running', 'queued'):
                    break
                time.sleep(1)
                response = client.get(base + '/multidoc/debug/' + str(debug_id), headers=headers)
                response.raise_for_status()
                data = response.json()
            result = data.get('result') or {}
            checks = {'total': result.get('total') == total,
                      'titles': [r.get('title') for r in result.get('items', [])] == titles,
                      'type': all(r.get('media_type') == kind for r in result.get('items', [])),
                      'page': result.get('page') == page,
                      'next_page': result.get('next_page') == (page + 1 if page < total else None)}
            report['cases'].append({'kind': kind, 'search': search, 'page': page,
                'status': data.get('status'), 'checks': checks, 'passed': data.get('status') == 'ok' and all(checks.values())})
            args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
            if data.get('status') != 'ok':
                report['interpreter_error'] = str(data.get('exception', 'unknown'))[:1000]
                break
    report['passed'] = len(report['cases']) == len(cases) and all(c['passed'] for c in report['cases'])
    args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
