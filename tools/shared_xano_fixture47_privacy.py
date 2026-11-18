"""Make only the interrupted fixture's remaining default list private once."""
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import httpx

from tools.shared_xano_acceptance import digest
from tools.session_revocation import ROOT, metadata_config

CHANGE = ROOT/'openspec/changes/validar-integracoes-xano-atual'
OUTPUT = CHANGE/'fixture47-list114-privacy-read-retry.json'
LIST_TABLE = 895415
ITEM_TABLE = 895416
ROW_ID = 114


class Stop(RuntimeError):
    pass


def rows(client, base, headers, table_id):
    result, page, total, seen = [], 1, None, set()
    while True:
        if page in seen or len(seen) >= 20:
            raise Stop('pagination_loop_or_budget')
        seen.add(page)
        response = client.get(f'{base}/table/{table_id}/content',
            headers={**headers, 'x-data-source': 'live'}, params={'page': page, 'per_page': 100})
        if response.status_code != 200:
            raise Stop('inventory_read_http_'+str(response.status_code))
        body = response.json()
        if not isinstance(body, dict) or not isinstance(body.get('items'), list) or type(body.get('itemsTotal')) is not int:
            raise Stop('inventory_shape_unknown')
        if total is None:
            total = body['itemsTotal']
        elif body['itemsTotal'] != total:
            raise Stop('inventory_changed_during_read')
        result.extend(body['items'])
        next_page = body.get('nextPage')
        if next_page in (None, False, 0):
            break
        if type(next_page) is not int or next_page <= page:
            raise Stop('invalid_next_page')
        page = next_page
    if len(result) != total:
        raise Stop('incomplete_inventory')
    return result


def hashes(records):
    result = {}
    for row in records:
        if not isinstance(row, dict) or type(row.get('id')) is not int or row['id'] <= 0:
            raise Stop('invalid_row_identity')
        key = str(row['id'])
        if key in result:
            raise Stop('duplicate_row_identity')
        result[key] = digest(row)
    return result


def save(report):
    temp = OUTPUT.with_suffix('.json.tmp')
    temp.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    temp.replace(OUTPUT)


def main():
    if OUTPUT.exists():
        raise Stop('receipt_already_exists_no_retry')
    report = {'layer': 'fixture_default_list_privacy_reconciliation', 'workspace': 147717,
              'run_id': 'cbshared_35b8a42f44c4', 'user_id': 47, 'list_id': ROW_ID,
              'remote_writes': 0, 'passed': False, 'write_attempts': [], 'references': []}
    base, headers = metadata_config()
    try:
        with httpx.Client(timeout=90, follow_redirects=False, trust_env=False) as client:
            list_response = client.get(f'{base}/table/{LIST_TABLE}/content/{ROW_ID}',
                headers={**headers, 'x-data-source': 'live'})
            if list_response.status_code != 200:
                raise Stop('candidate_read_http_'+str(list_response.status_code))
            candidate = list_response.json()
            expected = {'id': ROW_ID, 'user_id': 47, 'default_key': '47:completed',
                        'title': 'Já assisti / li', 'is_public': True}
            if any(candidate.get(k) != v for k, v in expected.items()):
                raise Stop('candidate_identity_or_visibility_mismatch')
            all_lists = rows(client, base, headers, LIST_TABLE)
            all_items = rows(client, base, headers, ITEM_TABLE)
            before_lists, before_items = hashes(all_lists), hashes(all_items)
            if before_lists.get(str(ROW_ID)) != digest(candidate):
                raise Stop('candidate_changed_during_read')
            refs = [item['id'] for item in all_items if item.get('list_id') == ROW_ID]
            report.update(candidate_sha256=digest(candidate), list_count_before=len(all_lists),
                          item_count_before=len(all_items), references=refs)
            if refs:
                raise Stop('candidate_has_items')
            save(report)

            attempt = {'action': 'make_list_private_114', 'state': 'attempting',
                       'started_at': datetime.now(timezone.utc).isoformat()}
            report['write_attempts'].append(attempt)
            report['remote_writes'] = 1
            save(report)
            try:
                response = client.put(f'{base}/table/{LIST_TABLE}/content/{ROW_ID}',
                    headers={**headers, 'x-data-source': 'live'}, json={'is_public': False})
            except httpx.RequestError:
                attempt['state'] = 'uncertain_no_retry'
                report['failure_reason'] = 'privacy_write_uncertain_no_retry'
                save(report)
                return 2
            attempt.update(http_status=response.status_code,
                           finished_at=datetime.now(timezone.utc).isoformat())
            if response.status_code != 200:
                attempt['state'] = 'rejected_no_retry'
                report['failure_reason'] = 'privacy_write_rejected_'+str(response.status_code)
                save(report)
                return 2
            attempt['state'] = 'accepted'
            save(report)

            verify = client.get(f'{base}/table/{LIST_TABLE}/content/{ROW_ID}',
                headers={**headers, 'x-data-source': 'live'})
            if verify.status_code != 200:
                raise Stop('privacy_verification_read_failed')
            after = verify.json()
            if (after.get('id') != ROW_ID or after.get('user_id') != 47
                    or after.get('default_key') != '47:completed' or after.get('is_public') is not False
                    or any(after.get(k) != v for k, v in candidate.items() if k not in ('is_public', 'updated_at'))):
                raise Stop('privacy_write_verification_failed')
            after_lists = rows(client, base, headers, LIST_TABLE)
            after_items = rows(client, base, headers, ITEM_TABLE)
            after_list_hashes = hashes(after_lists)
            if hashes(after_items) != before_items:
                raise Stop('list_items_changed')
            if any(after_list_hashes[k] != before_lists[k]
                   for k in before_lists if k != str(ROW_ID)):
                raise Stop('unrelated_list_changed')
            report.update(passed=True, phase='complete', list_count_after=len(after_lists),
                          item_count_after=len(after_items), unrelated_lists_unchanged=True,
                          all_items_unchanged=True, verified_private=True)
            save(report)
            return 0
    except (httpx.HTTPError, ValueError, KeyError, TypeError, Stop) as exc:
        report['failure_reason'] = str(exc) if isinstance(exc, Stop) else type(exc).__name__
        save(report)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
