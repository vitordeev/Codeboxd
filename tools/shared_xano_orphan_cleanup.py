"""Delete only the reviewed orphaned public Xano list, once, after preflight."""
from datetime import datetime, timezone
import json
from pathlib import Path

import httpx

from tools.shared_xano_acceptance import digest
from tools.session_revocation import ROOT, metadata_config

CHANGE = ROOT/'openspec/changes/remover-lista-orfa-110'
BASELINE = ROOT/'.local/shared-xano-preflight-20261118-after-reconcile/baseline-hashes.json'
OUTPUT = CHANGE/'deletion-execution.json'
LIST_TABLE = 895415
ITEM_TABLE = 895416
ROW_ID = 110


class Stop(RuntimeError):
    pass


def paginated_rows(client, base, headers, table_id):
    rows, page, total, seen = [], 1, None, set()
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
        rows.extend(body['items'])
        next_page = body.get('nextPage')
        if next_page in (None, False, 0):
            break
        if type(next_page) is not int or next_page <= page:
            raise Stop('invalid_next_page')
        page = next_page
    if len(rows) != total:
        raise Stop('incomplete_inventory')
    return rows


def hashes(rows):
    result = {}
    for row in rows:
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
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    if baseline.get('destination', {}).get('workspace') != 147717 or baseline.get('complete') is not True:
        raise Stop('reviewed_baseline_mismatch')
    expected_hash = baseline.get('tables', {}).get('user_list', {}).get(str(ROW_ID))
    if not isinstance(expected_hash, str):
        raise Stop('candidate_missing_from_baseline')

    report = {'layer': 'single_orphan_row_cleanup', 'workspace': 147717,
              'table': 'user_list', 'row_id': ROW_ID, 'remote_writes': 0,
              'passed': False, 'write_attempts': [], 'references': None}
    base, headers = metadata_config()
    try:
        with httpx.Client(timeout=35, follow_redirects=False, trust_env=False) as client:
            list_response = client.get(f'{base}/table/{LIST_TABLE}/content/{ROW_ID}',
                headers={**headers, 'x-data-source': 'live'})
            if list_response.status_code != 200:
                raise Stop('candidate_read_http_'+str(list_response.status_code))
            row = list_response.json()
            exact = {'id': ROW_ID, 'user_id': 0, 'default_key': None,
                     'title': '', 'description': '', 'is_public': True}
            if any(row.get(key) != value for key, value in exact.items()):
                raise Stop('candidate_identity_changed')
            if digest(row) != expected_hash:
                raise Stop('candidate_hash_changed_since_review')

            current_lists = paginated_rows(client, base, headers, LIST_TABLE)
            current_items = paginated_rows(client, base, headers, ITEM_TABLE)
            before_lists, before_items = hashes(current_lists), hashes(current_items)
            if before_lists != baseline['tables']['user_list']:
                raise Stop('list_inventory_changed_since_review')
            if before_items != baseline['tables']['user_list_item']:
                raise Stop('item_inventory_changed_since_review')
            references = [item['id'] for item in current_items if item.get('list_id') == ROW_ID]
            report.update(candidate_sha256=expected_hash, list_count_before=len(current_lists),
                          item_count_before=len(current_items), references=references)
            if references:
                raise Stop('candidate_has_references')

            attempt = {'action': 'delete_user_list_110', 'state': 'attempting',
                       'started_at': datetime.now(timezone.utc).isoformat()}
            report['write_attempts'].append(attempt)
            report['remote_writes'] = 1
            save(report)
            try:
                response = client.delete(f'{base}/table/{LIST_TABLE}/content/{ROW_ID}',
                    headers={**headers, 'x-data-source': 'live'})
            except httpx.RequestError:
                attempt['state'] = 'uncertain_no_retry'
                report['failure_reason'] = 'delete_uncertain_no_retry'
                save(report)
                return 2
            attempt.update(http_status=response.status_code,
                           finished_at=datetime.now(timezone.utc).isoformat())
            if response.status_code not in (200, 204):
                attempt['state'] = 'rejected_no_retry'
                report['failure_reason'] = 'delete_rejected_'+str(response.status_code)
                save(report)
                return 2
            attempt['state'] = 'accepted'
            save(report)

            after_lists = paginated_rows(client, base, headers, LIST_TABLE)
            after_items = paginated_rows(client, base, headers, ITEM_TABLE)
            after_list_hashes, after_item_hashes = hashes(after_lists), hashes(after_items)
            expected_lists = dict(before_lists)
            expected_lists.pop(str(ROW_ID))
            if (str(ROW_ID) in after_list_hashes or after_list_hashes != expected_lists
                    or after_item_hashes != before_items):
                raise Stop('post_delete_preservation_check_failed')
            report.update(passed=True, verified_absent=True, list_count_after=len(after_lists),
                          item_count_after=len(after_items), other_lists_unchanged=True,
                          all_items_unchanged=True, phase='complete')
            save(report)
            return 0
    except (httpx.HTTPError, ValueError, KeyError, TypeError, Stop) as exc:
        report['failure_reason'] = str(exc) if isinstance(exc, Stop) else type(exc).__name__
        if not OUTPUT.exists():
            save(report)
        else:
            save(report)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
