"""Generate isolated catalog diagnostics; never connects to Xano or reads secrets.

The generated functions preserve GET/PUT business logic, but substitute synthetic
tables and an explicit actor ID. Session/token validation is intentionally NOT
covered. Generation and Python checker tests do not execute XanoScript.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'admin_catalog_fixture_'
MEDIA = (
    dict(id=1, media_type='movie', title='Arrival'),
    dict(id=2, media_type='movie', title='Arrival'),
    dict(id=3, media_type='movie', title='100%_literal\\movie [Edition]'),
    dict(id=4, media_type='book', title='Duna'),
    dict(id=5, media_type='anime', title='Anime fixture'),
    dict(id=6, media_type='series', title='Series fixture'),
)
IDENTITY_FIELDS = ('id', 'identity_key', 'external_source', 'external_id', 'media_type')
EDIT_FIELDS = ('title', 'description', 'cover_url', 'year')


def source(operation):
    if operation not in ('get', 'put'):
        raise ValueError('operation must be get or put')
    name = 'admin_catalog_GET.xs' if operation == 'get' else 'admin_catalog_id_PUT.xs'
    return (ROOT/'xano/api/codeboxd'/name).read_text(encoding='utf-8')


def sections(text):
    """Fail closed if the known contract layout/security boundary changes."""
    pattern = (r'  input \{(?P<input>.*?)\n  \}\s*\n  stack \{\s*'
               r'function\.run "Security/require_current_session" \{\s*'
               r'input = \{[^\n]*\}\s*\n    \}'
               r'(?P<stack>.*?)\n  \}\s*\n  response = '
               r'(?P<response>.*?)\n  guid =')
    match = re.search(pattern, text, re.S)
    if not match:
        raise ValueError('Unsupported catalog contract layout; review extraction')
    values = match.groupdict()
    if 'db.get user {' not in values['stack']:
        raise ValueError('Missing production actor lookup')
    if '$auth.' in values['input'] or '$auth.' in values['response']:
        raise ValueError('Unexpected authentication reference outside stack')
    values['stack'] = values['stack'].replace('$auth.id', '$input.actor_id')
    if '$auth.' in values['stack'] or 'function.run' in values['stack']:
        raise ValueError('Unsubstituted external function or authentication reference')
    return values


def synthetic_tables(text):
    for table in ('user', 'media'):
        text = re.sub(r'\bdb\.(get|query|edit) '+table+r'\b',
                      lambda match: 'db.'+match[1]+' '+PREFIX+table, text)
        text = re.sub(r'\b'+table+r'\.', PREFIX+table+'.', text)
    return text


def script(operation):
    parts = sections(source(operation))
    definitions = {
        'user': 'int id\n text role\n text account_status',
        'media': ('int id\n text identity_key\n text external_source\n text external_id\n'
                  ' enum media_type { values = ["movie", "series", "anime", "book"] }\n'
                  ' text title filters=trim|min:1|max:500\n text description?\n'
                  ' text cover_url?\n int year?'),
    }
    tables = ['table '+PREFIX+name+' {\n schema {\n '+fields+
              '\n }\n index = [{type: "primary", field: [{name: "id"}]}]\n}'
              for name, fields in definitions.items()]
    setup = []
    # Fresh interpreter-only table definitions assign IDs in insertion order.
    for role, status in [('admin', 'active'), ('member', 'active'), ('admin', 'disabled')]:
        setup.append('    db.add '+PREFIX+'user { data = '+
                     json.dumps(dict(role=role, account_status=status))+' }')
    for row in MEDIA:
        data = {key: value for key, value in row.items() if key != 'id'}
        data.update(identity_key='fixture:'+row['media_type']+':'+str(row['id']),
                    external_source='fixture', external_id=str(row['id']),
                    description='Original fixture', cover_url='https://fixture.test/cover.jpg', year=2000)
        setup.append('    db.add '+PREFIX+'media { data = '+json.dumps(data)+' }')
    before = after = ''
    result = parts['response'].strip()
    if operation == 'put':
        before = ('\n    db.get '+PREFIX+'media { field_name = "id"'
                  ' field_value = $input.id } as $fixture_before\n')
        after = ('\n    db.get '+PREFIX+'media { field_name = "id"'
                 ' field_value = $input.id } as $fixture_after\n')
        result = '{result: '+result+', before: $fixture_before, after: $fixture_after}'
    function = ('function "admin_catalog_'+operation+'_fixture" {\n  input {'+
                parts['input']+'\n    int actor_id?=1\n  }\n  stack {\n'+
                '\n'.join(setup)+before+synthetic_tables(parts['stack'])+after+
                '\n  }\n  response = '+result+'\n}')
    return '\n---\n'.join([*tables, function])+'\n'


def cases():
    """Inputs/expectations for a separately authorized interpreter execution."""
    rows = [dict(name='type_'+kind, operation='get', inputs=dict(media_type=kind), expected='success')
            for kind in ('movie', 'series', 'anime', 'book')]
    rows += [dict(name=name, operation='get', inputs=dict(media_type='movie', **inputs), expected='success')
             for name, inputs in [('movie_page_1', dict(page=1, per_page=1)),
                                  ('movie_page_2', dict(page=2, per_page=1)),
                                  ('movie_page_3', dict(page=3, per_page=1)),
                                  ('uppercase', dict(search='ARRIVAL')),
                                  ('literal_symbols', dict(search='%_literal\\movie [Edition]')),
                                  ('empty_result', dict(search='fixture_no_match'))]]
    valid = dict(id=1, title='Arrival corrected', description='New fixture',
                 cover_url='https://fixture.test/new.jpg', year=2016)
    rows.append(dict(name='valid_edit', operation='put', inputs=valid, expected='success'))
    for name, changes in [('invalid_title', dict(title=' ')), ('invalid_year', dict(year=2201)),
                          ('invalid_cover', dict(cover_url='http://fixture.test/bad.jpg')),
                          ('missing_record', dict(id=9999))]:
        rows.append(dict(name=name, operation='put', inputs=valid | changes, expected='error'))
    for operation in ('get', 'put'):
        for actor in (2, 3, 999):
            inputs = dict(media_type='movie') if operation == 'get' else valid.copy()
            rows.append(dict(name=operation+'_actor_'+str(actor), operation=operation,
                             inputs=inputs | dict(actor_id=actor), expected='error'))
    return rows


def check_get(data, inputs):
    """Check the intended literal/case-insensitive search, not Python regex."""
    if not isinstance(data, dict) or not isinstance(data.get('items'), list):
        return dict(page_contract=False)
    page, size = inputs.get('page', 1), inputs.get('per_page', 25)
    term = inputs.get('search', '').strip().casefold()
    matches = [row for row in MEDIA if row['media_type'] == inputs['media_type']
               and term in row['title'].casefold()]
    items = data['items']
    valid_rows = all(isinstance(row, dict) and type(row.get('id')) is int for row in items)
    ids = [row.get('id') for row in items] if valid_rows else []
    expected_size = min(size, max(0, len(matches)-(page-1)*size))
    allowed = {row['id']: row for row in matches}
    return dict(
        totals=type(data.get('total')) is int and data['total'] == len(matches),
        pagination=(type(data.get('page')) is int and data['page'] == page
                    and type(data.get('per_page')) is int and data['per_page'] == size
                    and (data.get('next_page') is None or type(data['next_page']) is int)
                    and data.get('next_page') == (page+1 if page*size < len(matches) else None)),
        items=(valid_rows and len(items) == expected_size and len(set(ids)) == len(ids)
               and all(row.get('id') in allowed and row.get('media_type') == inputs['media_type']
                       and row.get('title') == allowed[row['id']]['title'] for row in items)),
    )


def check_pages(pages, inputs):
    """Require complete, non-overlapping pages; equal titles may use either ID order."""
    if not isinstance(pages, list) or not pages:
        return dict(complete=False)
    size = inputs.get('per_page', 25)
    term = inputs.get('search', '').strip().casefold()
    expected = [row for row in MEDIA if row['media_type'] == inputs['media_type']
                and term in row['title'].casefold()]
    if not all(all(check_get(data, inputs | dict(page=index)).values())
               for index, data in enumerate(pages, 1)):
        return dict(pages=False)
    rows = [row for data in pages for row in data['items']]
    ids = [row['id'] for row in rows]
    titles = [row['title'] for row in rows]
    return dict(complete=(len(pages) == max(1, (len(expected)+size-1)//size)
                          and len(ids) == len(set(ids))
                          and set(ids) == {row['id'] for row in expected}),
                ordered=titles == sorted(titles))


def check_put(data, inputs):
    if not isinstance(data, dict) or not all(isinstance(data.get(key), dict)
                                           for key in ('result', 'before', 'after')):
        return dict(snapshots=False)
    before, after = data['before'], data['after']
    return dict(
        target=(type(before.get('id')) is int and before['id'] == inputs['id']),
        identity=all(field in before and field in after
                     and type(before[field]) is type(after[field]) and before[field] == after[field]
                     for field in IDENTITY_FIELDS),
        edits=all(after.get(field) == inputs.get(field) for field in EDIT_FIELDS),
        response=all(field in data['result'] and field in after
                     and type(data['result'][field]) is type(after[field])
                     and data['result'][field] == after[field]
                     for field in ('id', *EDIT_FIELDS, 'media_type')),
    )


def manifest():
    return dict(layer='offline_catalog_fixture_preparation', xano_executed=False,
                session_validation_covered=False,
                limitations=['No remote execution or publication.',
                             'Invalid-edit failure alone cannot prove stored-row preservation.',
                             'check_pages requires complete actual execution results.',
                             'Literal/case-insensitive search remains a diagnostic expectation.'],
                source_sha256={operation: hashlib.sha256(source(operation).encode()).hexdigest()
                               for operation in ('get', 'put')}, cases=cases())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operation', choices=('get', 'put'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if bool(args.operation) != bool(args.output):
        parser.error('--operation and --output must be supplied together')
    if args.operation:
        # Never overwrite a historical fixture or an existing project file.
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(script(args.operation))
    else:
        print(json.dumps(manifest(), indent=2))


if __name__ == '__main__':
    main()
