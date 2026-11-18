"""Make only fixture 43's two default lists private, with one attempt each."""
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import httpx

from tools.shared_xano_acceptance import digest
from tools.session_revocation import ROOT, metadata_config

CHANGE = ROOT/'openspec/changes/validar-integracoes-xano-atual'
BASELINE = ROOT/'.local/shared-xano-preflight-20261118-after-orphan-delete/baseline-hashes.json'
OUTPUT = CHANGE/'fixture43-privacy-reconciliation.json'
TARGETS = {104: '43:planned', 105: '43:completed'}


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
        elif total != body['itemsTotal']:
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
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    tables = baseline['table_ids']
    report = {'layer': 'fixture_default_list_privacy_reconciliation', 'workspace': 147717,
              'user_id': 43, 'list_ids': list(TARGETS), 'remote_writes': 0,
              'passed': False, 'write_attempts': [], 'references': {}}
    base, headers = metadata_config()
    try:
        with httpx.Client(timeout=35, follow_redirects=False, trust_env=False) as client:
            users = rows(client, base, headers, tables['user'])
            actor = next((r for r in users if r.get('id') == 43), None)
            if not actor or actor.get('account_status') != 'disabled' or actor.get('role') != 'member':
                raise Stop('fixture_user_43_identity_or_status_mismatch')
            current_lists = rows(client, base, headers, tables['user_list'])
            current_items = rows(client, base, headers, tables['user_list_item'])
            before_list_hashes, before_item_hashes = hashes(current_lists), hashes(current_items)
            if before_list_hashes != baseline['tables']['user_list']:
                raise Stop('list_inventory_changed_since_review')
            if before_item_hashes != baseline['tables']['user_list_item']:
                raise Stop('item_inventory_changed_since_review')
            by_id = {r['id']: r for r in current_lists}
            before = {}
            for list_id, key in TARGETS.items():
                row = by_id.get(list_id)
                if (not row or row.get('user_id') != 43 or row.get('default_key') != key
                        or row.get('is_public') is not True):
                    raise Stop('fixture_list_identity_or_visibility_mismatch')
                refs = [x['id'] for x in current_items if x.get('list_id') == list_id]
                report['references'][str(list_id)] = refs
                if refs:
                    raise Stop('fixture_list_has_items')
                before[list_id] = row
            report['list_hashes_before'] = {str(k): before_list_hashes[str(k)] for k in TARGETS}
            report['item_count_before'] = len(current_items)
            save(report)

            last_write = None
            for list_id in TARGETS:
                if last_write is not None:
                    pause = max(0.0, 1.25-(time.monotonic()-last_write))
                    if pause:
                        time.sleep(pause)
                attempt = {'action': 'make_list_private_'+str(list_id), 'state': 'attempting',
                           'started_at': datetime.now(timezone.utc).isoformat()}
                report['write_attempts'].append(attempt)
                report['remote_writes'] += 1
                save(report)
                try:
                    response = client.put(f'{base}/table/{tables["user_list"]}/content/{list_id}',
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
                last_write = time.monotonic()
                save(report)
                verify = client.get(f'{base}/table/{tables["user_list"]}/content/{list_id}',
                    headers={**headers, 'x-data-source': 'live'})
                if verify.status_code != 200:
                    raise Stop('privacy_write_verification_read_failed')
                after = verify.json()
                if after.get('id') != list_id or after.get('user_id') != 43 or after.get('default_key') != TARGETS[list_id] or after.get('is_public') is not False:
                    raise Stop('privacy_write_verification_failed')
                allowed = {'is_public', 'updated_at'}
                if any(after.get(k) != v for k, v in before[list_id].items() if k not in allowed):
                    raise Stop('unrelated_list_field_changed')

            after_lists = rows(client, base, headers, tables['user_list'])
            after_items = rows(client, base, headers, tables['user_list_item'])
            after_by_id = {r['id']: r for r in after_lists}
            for list_id in TARGETS:
                if after_by_id[list_id].get('is_public') is not False:
                    raise Stop('privacy_not_persisted')
            if hashes(after_items) != before_item_hashes:
                raise Stop('list_items_changed')
            after_hashes = hashes(after_lists)
            changed_ids = {str(k) for k in TARGETS}
            if any(after_hashes[k] != before_list_hashes[k]
                   for k in before_list_hashes if k not in changed_ids):
                raise Stop('unrelated_list_changed')
            report.update(passed=True, phase='complete', list_count=len(after_lists),
                          item_count=len(after_items), unrelated_lists_unchanged=True,
                          all_items_unchanged=True, verified_private=list(TARGETS))
            save(report)
            return 0
    except (httpx.HTTPError, ValueError, KeyError, TypeError, Stop) as exc:
        report['failure_reason'] = str(exc) if isinstance(exc, Stop) else type(exc).__name__
        save(report)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
