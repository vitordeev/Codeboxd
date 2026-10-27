"""Validate production dashboard queries against isolated synthetic tables."""
import argparse
import json
from pathlib import Path
import re
import time

import httpx

from tools.session_revocation import metadata_config


def script():
    source = (Path(__file__).resolve().parents[1]/'xano/api/codeboxd/admin_dashboard_GET.xs').read_text(encoding='utf-8')
    inputs = re.search(r'  input \{(.*?)\n  \}', source, re.S).group(1)
    queries = source[source.index('    db.query user'):source.rindex('\n  }\n\n  response')]
    tables = []
    definitions = {
        'user': 'int id', 'media': 'int id',
        'post': 'int id\n int user_id\n timestamp created_at?=now',
        'report': 'int id\n timestamp created_at?=now\n text status\n text target_type\n text reason',
    }
    for name, fields in definitions.items():
        fake = 'dashboard_fixture_'+name
        queries = re.sub(r'\bdb\.query '+name+r'\b', 'db.query '+fake, queries)
        queries = re.sub(r'\b'+name+r'\.', fake+'.', queries)
        tables.append('table '+fake+' {\n schema {\n'+fields+'\n }\n index = [{type: "primary", field: [{name: "id"}]}]\n}')
    setup = []
    for name, count in [('user', 3), ('media', 4), ('post', 2), ('report', 4)]:
        for i in range(count):
            values = {} if name in ('user', 'media') else {'created_at': 1000}
            if name == 'post':
                values['user_id'] = 1
            if name == 'report':
                values.update(status='pending' if i < 3 else 'resolved', target_type='post', reason='spam')
            setup.append('        db.add dashboard_fixture_'+name+' { data = '+json.dumps(values)+' }')
    seed = '    conditional {\n      if ($input.empty == false) {\n'+'\n'.join(setup)+'\n      }\n    }\n'
    response = source[source.index('  response ='):source.index('\n  guid =')]
    function = 'function "dashboard_fixture" {\n  input {'+inputs+'\n    bool empty?=false\n  }\n  stack {\n'+seed+queries+'\n  }\n'+response+'\n}'
    return '\n---\n'.join([*tables, function])


def check_result(data, inputs):
    empty = inputs.get('empty', False)
    posts_page, reports_page = inputs.get('page', 1), inputs.get('reports_page', 1)
    posts_size, reports_size = inputs.get('per_page', 1), inputs.get('reports_per_page', 1)
    posts, pending = ([] if empty else [2, 1]), ([] if empty else [3, 2, 1])
    checks = dict(known_totals=all(data.get(key) == value for key, value in {
        'users_total': 0 if empty else 3, 'posts_total': len(posts),
        'media_total': 0 if empty else 4, 'reports_pending': len(pending)}.items()))
    for field, ids, page, size, allowed in (
        ('recent_posts', posts, posts_page, posts_size, {'id', 'user_id', 'created_at'}),
        ('pending_reports', pending, reports_page, reports_size, {'id', 'created_at', 'target_type', 'reason'}),
    ):
        items = data.get(field, [])
        meta = data.get(field+'_pagination', {})
        checks[field] = ([row.get('id') for row in items] == ids[(page-1)*size:page*size]
            and all(set(row) <= allowed for row in items) and meta.get('total') == len(ids)
            and meta.get('page') == page and meta.get('per_page') == size
            and meta.get('next_page') == (page+1 if page*size < len(ids) else None))
    return checks


def main(output):
    if output.exists():
        raise FileExistsError('Preserve previous evidence')
    base, headers = metadata_config()
    report = dict(layer='isolated_xano_dashboard_fixture', published=False, real_data_validated=False, cases=[])
    with httpx.Client(timeout=30, follow_redirects=False) as client:
        for name, inputs in [('first', {}), ('second', {'page': 2, 'reports_page': 2}),
                             ('third_pending', {'reports_page': 3}), ('empty', {'empty': True})]:
            inputs = dict(per_page=1, reports_per_page=1) | inputs
            response = client.post(base+'/multidoc/debug',
                headers={**headers, 'Content-Type': 'text/x-xanoscript'}, params={
                    'entry_obj_type': 'function', 'entry_obj_name': 'dashboard_fixture', 'input': json.dumps(inputs)},
                content=script())
            response.raise_for_status()
            data = response.json()
            debug_id = data.get('id') or data.get('debug_id')
            for _ in range(12):
                if not debug_id or data.get('status') not in ('pending', 'running', 'queued'):
                    break
                time.sleep(1)
                response = client.get(base+'/multidoc/debug/'+str(debug_id), headers=headers)
                response.raise_for_status()
                data = response.json()
            result = data.get('result') or {}
            checks = check_result(result, inputs) if data.get('status') == 'ok' else {}
            report['cases'].append(dict(scenario=name, status=data.get('status'), checks=checks,
                passed=bool(checks) and all(checks.values())))
            output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
            if data.get('status') != 'ok':
                # Only synthetic tables/inputs are used by this diagnostic.
                report['error'] = str(data.get('exception', 'interpreter_failure'))[:1000]
                break
    report['passed'] = len(report['cases']) == 4 and all(row['passed'] for row in report['cases'])
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    raise SystemExit(main(parser.parse_args().output))
