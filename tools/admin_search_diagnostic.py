"""Compare predicates in an isolated interpreter; no real-data acceptance or writes."""
import argparse
import json
from pathlib import Path
import re
import time

import httpx

from tools.session_revocation import metadata_config, export_workspace, blocks

SCRIPT = '''function "diagnose_admin_search_defaults" {
  input {
    int user_id?=0 filters=min:0
  }
  stack {
    api.lambda {
      code = "return Number($input.user_id || 0);"
    } as $normalized_id
    db.query user {
      where = ($input.user_id > 0 && $db.user.id == $input.user_id) || $input.user_id == 0
      return = {type: "count"}
    } as $original_count
    db.query user {
      where = ($normalized_id > 0 && $db.user.id == $normalized_id) || $normalized_id == 0
      return = {type: "count"}
    } as $normalized_count
    db.query user {
      return = {type: "count"}
    } as $all_count
    db.query user {
      where = $db.user.id == 14
      return = {type: "count"}
    } as $exact_count
  }
  response = {original_count: $original_count, normalized_count: $normalized_count, normalized_id: $normalized_id, all_count: $all_count, exact_count: $exact_count}
}'''


def main(output):
    if output.exists():
        raise FileExistsError('Preserve prior evidence')
    base, headers = metadata_config()
    report = {'layer': 'isolated_interpreter_query_diagnostic', 'published': False,
              'real_data_validated': False}
    with httpx.Client(timeout=30, follow_redirects=False) as client:
        source = export_workspace(client, base, headers)
        tables = [block for block in blocks(source) if re.search(r'(?m)^table user\s*\{', block)]
        if len(tables) != 1:
            raise RuntimeError('Expected existing user schema')
        response = client.post(base+'/multidoc/debug', headers={**headers, 'Content-Type': 'text/x-xanoscript'},
            params={'entry_obj_type': 'function', 'entry_obj_name': 'diagnose_admin_search_defaults', 'input': '{}'},
            content=tables[0]+'\n---\n'+SCRIPT)
        report['start_status'] = response.status_code
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
        # Export only counters from the final result, never the execution stack.
        report['status'] = data.get('status')
        error = data.get('exception')
        if error:
            # This diagnostic reads counters only; still suppress contact/auth text.
            message = str(error.get('message', error.get('error', 'diagnostic_exception'))) if isinstance(error, dict) else str(error)
            message = re.sub(r'[\w.+-]+@[\w.-]+|Bearer\s+\S+|https?://\S+', '[redacted]', message)
            report['error'] = message[:1000]
        result = data.get('output', data.get('result', data.get('response', {})))
        report['result_keys'] = list(result) if isinstance(result, dict) else []
        report['counts'] = {key: result[key] for key in ('original_count', 'normalized_count', 'normalized_id', 'all_count', 'exact_count')
                            if isinstance(result, dict) and type(result.get(key)) is int}
        report['passed'] = report['status'] == 'ok' and len(report['counts']) == 5
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    raise SystemExit(main(parser.parse_args().output))
