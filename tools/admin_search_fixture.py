"""Exercise admin search SQL against synthetic rows in the Xano interpreter only."""
import argparse
import json
from pathlib import Path
import re
import time

import httpx

from tools.session_revocation import metadata_config

SCRIPT = '''table admin_search_fixture {
  schema {
    int id
    text name
    text username
  }
  index = [{type: "primary", field: [{name: "id"}]}]
}
---
function "compare_admin_search_fixture" {
  input {
    int user_id?=0 filters=min:0
    text search?="" filters=trim
  }
  stack {
    db.add admin_search_fixture {
      data = {name: "Fixture Alpha", username: "fixture_alpha"}
    } as $first
    db.add admin_search_fixture {
      data = {name: "Fixture Beta", username: "fixture_beta"}
    }
    db.add admin_search_fixture {
      data = {name: "Another", username: "other"}
    }
    db.query admin_search_fixture {
      return = {type: "count"}
    } as $all_count
    db.query admin_search_fixture {
      where = (($input.user_id > 0 && $db.admin_search_fixture.id == $input.user_id) || ($input.user_id == 0 && ($input.search == "" || $db.admin_search_fixture.username ~ $input.search || $db.admin_search_fixture.name ~ $input.search)))
      return = {type: "count"}
    } as $original_count
    db.query admin_search_fixture {
      where = $input.search == "" || $db.admin_search_fixture.username ~ $input.search || $db.admin_search_fixture.name ~ $input.search
      return = {type: "count"}
    } as $text_count
    db.query admin_search_fixture {
      where = $db.admin_search_fixture.id == $first.id
      return = {type: "count"}
    } as $exact_count
  }
  response = {all_count: $all_count, original_count: $original_count, text_count: $text_count, exact_count: $exact_count}
}'''

CASES = [
    ('empty', {}, [1, 2, 3], 3),
    ('username', {'search': 'fixture_alpha'}, [1], 1),
    ('name_case', {'search': 'FIXTURE ALPHA'}, [1], 1),
    ('partial', {'search': 'Fixture'}, [1, 2], 2),
    ('no_match', {'search': 'absent'}, [], 0),
    ('literal_regex', {'search': '.'}, [], 0),
    ('literal_underscore', {'search': '_'}, [1, 2], 2),
    ('literal_percent', {'search': '%'}, [], 0),
    ('literal_backslash', {'search': '\\'}, [], 0),
    ('exact_id', {'user_id': 2}, [2], 1),
    ('id_precedence', {'user_id': 2, 'search': 'absent'}, [2], 1),
    ('disabled', {'account_status': 'disabled'}, [2], 1),
    ('member', {'role': 'member'}, [2, 3], 2),
    ('combined', {'search': 'Fixture', 'role': 'member', 'account_status': 'disabled'}, [2], 1),
    ('id_mismatched_filter', {'user_id': 2, 'account_status': 'active'}, [], 0),
    ('page_one', {'per_page': 1}, [1], 3),
    ('page_two', {'page': 2, 'per_page': 1}, [2], 3),
    ('page_three', {'page': 3, 'per_page': 1}, [3], 3),
]


def candidate_script(batch=False):
    """Extract the production query branches; do not reimplement search in Python."""
    source = (Path(__file__).resolve().parents[1]/'xano/api/codeboxd/admin_users_GET.xs').read_text(encoding='utf-8')
    inputs = re.search(r'  input \{(.*?)\n  \}', source, re.S).group(1)
    query = source[source.index('    var $users'):source.rindex('\n  }\n\n  response')]
    query = query.replace('db.query user', 'db.query admin_search_fixture').replace(
        '$db.user.', '$db.admin_search_fixture.').replace('sort = {user.id:', 'sort = {admin_search_fixture.id:')
    response = source[source.index('  response ='):source.index('\n  guid =')]
    table = '''table admin_search_fixture {
  schema { int id\n text name\n text username\n text role\n text account_status\n timestamp created_at?=now }
  index = [{type: "primary", field: [{name: "id"}]}]
}'''
    candidate = 'function "candidate_admin_search" {\n  input {'+inputs+'\n  }\n  stack {\n'+query+'\n  }\n'+response+'\n}'
    setup = '''    db.add admin_search_fixture { data = {name: "Fixture Alpha", username: "fixture_alpha", role: "admin", account_status: "active"} }
    db.add admin_search_fixture { data = {name: "Fixture Beta", username: "fixture_beta", role: "member", account_status: "disabled"} }
    db.add admin_search_fixture { data = {name: "Another", username: "other", role: "member", account_status: "active"} }
'''
    if batch:
        calls = []
        for name, inputs, *_ in CASES:
            values = dict(user_id=0, search='', role='', account_status='', page=1, per_page=25) | inputs
            calls.append('    function.run "candidate_admin_search" { input = '+json.dumps(values)+' } as $'+name)
        wrapper = 'function "compare_admin_search_candidate" {\n  input {}\n  stack {\n'+setup+'\n'.join(calls)+'\n  }\n  response = {'+', '.join(name+': $'+name for name, *_ in CASES)+'}\n}'
        return '\n---\n'.join((table, candidate, wrapper))
    # Each scenario is a direct entry-point call, just like API inputs. Avoid
    # custom-function input handling obscuring which scenario failed.
    candidate = candidate.replace('  stack {\n', '  stack {\n'+setup, 1)
    return '\n---\n'.join((table, candidate))


def candidate_checks(result, scenario=None):
    checks = []
    allowed = {'id', 'name', 'username', 'role', 'account_status', 'created_at'}
    for name, inputs, ids, total in CASES:
        if scenario is not None and name != scenario:
            continue
        data = result.get(name, {})
        items = data.get('items', [])
        page, size = inputs.get('page', 1), inputs.get('per_page', 25)
        expected_next = page + 1 if page * size < total else None
        checks.append(dict(scenario=name, passed=(
            data.get('total') == total and [item.get('id') for item in items] == ids
            and data.get('page') == inputs.get('page', 1)
            and data.get('per_page') == inputs.get('per_page', 25)
            and data.get('next_page') == expected_next
            and all(set(item) <= allowed for item in items)), total=data.get('total'),
            items_count=len(items)))
    return checks


def main(output, candidate=False, batch=False):
    if output.exists():
        raise FileExistsError('Preserve previous evidence')
    base, headers = metadata_config()
    report = {'layer': 'isolated_xano_synthetic_search', 'published': False,
              'real_data_validated': False, 'cases': []}
    with httpx.Client(timeout=30, follow_redirects=False) as client:
        scenarios = [(name, inputs) for name, inputs, *_ in CASES] if candidate else [('empty', {}), ('username', {'search': 'fixture_alpha'}),
                             ('partial', {'search': 'Fixture'}), ('no_match', {'search': 'absent'})]
        if batch:
            scenarios = [('batch', {})]
        script = candidate_script(batch) if candidate else SCRIPT
        entry = 'candidate_admin_search' if candidate else 'compare_admin_search_fixture'
        if batch:
            entry = 'compare_admin_search_candidate'
        for name, inputs in scenarios:
            response = client.post(base+'/multidoc/debug',
                headers={**headers, 'Content-Type': 'text/x-xanoscript'},
                params={'entry_obj_type': 'function', 'entry_obj_name': entry,
                        'input': json.dumps(inputs)}, content=script)
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
            if data.get('exception'):
                error = data['exception']
                report['error'] = str(error.get('message', error) if isinstance(error, dict) else error)[:1000]
            if candidate and data.get('status') == 'ok':
                report.setdefault('checks', []).extend(candidate_checks(result) if batch else candidate_checks({name: result}, name))
            report['cases'].append({'scenario': name, 'status': data.get('status'),
                'counts': {key: result[key] for key in ('all_count', 'original_count', 'text_count', 'exact_count')
                           if isinstance(result, dict) and type(result.get(key)) is int}})
            output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
            if data.get('status') != 'ok':
                break
    if candidate:
        passed = len(report.get('checks', [])) == len(CASES) and all(row['passed'] for row in report['checks'])
    else:
        passed = len(report['cases']) == 4 and all(row['status'] == 'ok' for row in report['cases'])
    report['passed'] = passed
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))
    return 0 if passed else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--batch', action='store_true')
    args = parser.parse_args()
    if args.batch and not args.candidate:
        parser.error('--batch requires --candidate')
    raise SystemExit(main(args.output, args.candidate, args.batch))
