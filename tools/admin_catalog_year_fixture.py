"""Compare optional year input validation without reading/writing any tables."""
import argparse
import json
from pathlib import Path
import re
import time

from tools.list_status_live import PacedClient
from tools.session_revocation import metadata_config

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve previous evidence')
    source = (ROOT / 'xano/api/codeboxd/admin_catalog_id_PUT.xs').read_text(encoding='utf-8')
    inputs = re.search(r'  input \{(.*?)\n  \}', source, re.S).group(1)
    if 'int year?' not in inputs:
        raise ValueError('Original input no longer matches comparison')
    base, headers = metadata_config()
    report = {'layer': 'synthetic_input_validation_no_tables', 'published': False, 'cases': []}
    cases = [('omitted', {}, True), ('null', {'year': None}, True),
             ('minimum', {'year': 1800}, True), ('maximum', {'year': 2200}, True),
             ('below', {'year': 1799}, False), ('above', {'year': 2201}, False)]
    with PacedClient(timeout=30) as client:
        for variant in ('original', 'nullable'):
            definition = inputs if variant == 'original' else inputs.replace('int year?', 'int? year?')
            script = 'function "catalog_year_fixture" {\n input {' + definition + '\n }\n stack {}\n response = $input\n}'
            for label, extra, accepted in cases:
                response = client.post(base + '/multidoc/debug', headers={**headers, 'Content-Type': 'text/x-xanoscript'},
                    params={'entry_obj_type': 'function', 'entry_obj_name': 'catalog_year_fixture',
                            'input': json.dumps({'id': 1, 'title': 'Synthetic title', **extra})}, content=script)
                response.raise_for_status()
                data = response.json()
                debug_id = data.get('id') or data.get('debug_id')
                for _ in range(15):
                    if data.get('status') not in ('pending', 'running', 'queued'):
                        break
                    time.sleep(1)
                    result = client.get(base + '/multidoc/debug/' + str(debug_id), headers=headers)
                    result.raise_for_status()
                    data = result.json()
                actual = data.get('status') == 'ok'
                report['cases'].append({'variant': variant, 'scenario': label, 'accepted': actual,
                                        'expected_accepted': accepted, 'passed': actual == accepted})
                args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    report['passed'] = all(c['passed'] for c in report['cases'] if c['variant'] == 'nullable')
    args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
