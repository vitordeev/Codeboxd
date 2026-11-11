"""Offline pilot planning and cleanup previews. No network, credentials or apply mode."""
from collections import Counter
from dataclasses import dataclass
import re

from tools.admin_acceptance_guard import GuardRejected, digest


@dataclass(frozen=True)
class Receipt:
    symbol: str
    table: str
    row_id: int
    snapshot_digest: str


def pilot_plan(run_id):
    if not isinstance(run_id, str) or not re.fullmatch(r'cbh9_[0-9a-f]{12}', run_id):
        raise GuardRejected('invalid_run_id')
    rows = []

    def add(symbol, table, identity, retain=True):
        rows.append(dict(symbol=symbol, table=table, identity=identity, retain=retain))

    for actor in ('R', 'B'):
        username = run_id + '_' + actor.lower()
        add(actor, 'user', dict(username=username))
        add(actor + '_profile', 'profile', dict(user_id='$' + actor, username=username))
        for kind in ('planned', 'completed'):
            add(actor + '_' + kind, 'user_list', dict(user_id='$' + actor, default_key='$' + actor + ':' + kind))
    for kind in ('movie', 'series', 'book', 'anime'):
        for number in (1, 2):
            identity = run_id + ':' + kind + ':' + str(number)
            add('M_' + kind + '_' + str(number), 'media', dict(identity_key=identity,
                external_source='test', external_id=identity, media_type=kind), False)
    add('P', 'post', dict(user_id='$R', body=run_id + ' disposable post'), False)
    for number in range(1, 9):
        kind = 'message' if number <= 4 else 'post' if number <= 6 else 'media'
        target = run_id + ':message:' + str(number) if kind == 'message' else '$P' if kind == 'post' else '$M_movie_' + str(number - 6)
        add('Q' + str(number), 'report', dict(reporter_user_id='$R', target_type=kind,
                                            target_id=target, description=run_id + ' report ' + str(number)))
    return dict(mode='offline_plan', remote_execution=False, run_id=run_id,
                records=rows, domain_records=len(rows), expected_retained_records=16,
                expected_deleted_records=9, audit_policy='retain_all',
                counts=dict(Counter(row['table'] for row in rows)),
                final_acceptance_complete=False)


def _resolve(value, ids):
    if isinstance(value, str) and value.startswith('$'):
        symbol, separator, suffix = value[1:].partition(':')
        number = ids[symbol]
        return str(number) + ':' + suffix if separator else number
    return value


def _positive_id(value):
    return type(value) is int and value > 0


def cleanup_preview(*, run_id, receipts, baseline, current, admin_id,
                    inventory_complete=False, references_reviewed=False):
    """Validate independent snapshots and exact provisioning receipts, never delete.

    baseline contains hashes keyed by table/id; current contains full records in
    memory only. Receipts must come from an independently verified provisioning
    journal, refreshed after approved edits. Boolean attestations do not verify
    remote pagination/cascades; the caller must establish those facts first.
    """
    plan = pilot_plan(run_id)
    if inventory_complete is not True or references_reviewed is not True:
        raise GuardRejected('complete_inventory_and_reference_review_required')
    if not isinstance(baseline, dict) or not isinstance(current, dict) or baseline.keys() != current.keys():
        raise GuardRejected('inventory_tables_changed')
    if any(not isinstance(rows, dict) for rows in [*baseline.values(), *current.values()]):
        raise GuardRejected('invalid_inventory')
    required = {row['table'] for row in plan['records']} | {'event_log'}
    if not required <= current.keys():
        raise GuardRejected('required_tables_missing')
    if not _positive_id(admin_id):
        raise GuardRejected('invalid_actor')
    actor = current['user'].get(admin_id, {})
    if (admin_id not in baseline['user'] or actor.get('role') != 'admin'
            or actor.get('account_status') != 'active'):
        raise GuardRejected('actor_not_original_active_admin')
    expected = {row['symbol']: row for row in plan['records']}
    if (not receipts or any(not isinstance(row, Receipt) for row in receipts)
            or len(receipts) != len(expected) or {row.symbol for row in receipts} != expected.keys()):
        raise GuardRejected('exact_pilot_receipts_required')
    owned = {(row.table, row.row_id) for row in receipts}
    if len(owned) != len(receipts):
        raise GuardRejected('duplicate_receipt_id')
    ids = {row.symbol: row.row_id for row in receipts}
    for receipt in receipts:
        resource = expected[receipt.symbol]
        if receipt.table != resource['table'] or not _positive_id(receipt.row_id):
            raise GuardRejected('receipt_identity_invalid')
        if receipt.row_id in baseline[receipt.table]:
            raise GuardRejected('original_record_is_not_fixture')
        record = current[receipt.table].get(receipt.row_id)
        if not isinstance(record, dict) or record.get('id') != receipt.row_id:
            raise GuardRejected('fixture_record_missing')
        if digest(record) != receipt.snapshot_digest:
            raise GuardRejected('fixture_snapshot_changed')
        for field, value in resource['identity'].items():
            resolved = _resolve(value, ids)
            if field == 'target_id':
                resolved = str(resolved)
            if record.get(field) != resolved:
                raise GuardRejected('fixture_ownership_changed')
        if receipt.table == 'user' and (record.get('role') != 'member' or record.get('account_status') != 'disabled'):
            raise GuardRejected('retained_fixture_account_must_be_disabled_member')
        if receipt.table == 'report' and (record.get('status') not in ('resolved', 'rejected')
                or record.get('reviewer_user_id') != admin_id or run_id not in str(record.get('decision', ''))):
            raise GuardRejected('reviewed_report_required')
    for table, rows in baseline.items():
        for row_id, original_digest in rows.items():
            if not _positive_id(row_id) or not isinstance(current[table].get(row_id), dict):
                raise GuardRejected('original_record_missing')
            if digest(current[table][row_id]) != original_digest:
                raise GuardRejected('original_record_changed')
    deletes = {(row['table'], ids[row['symbol']]) for row in plan['records'] if not row['retain']}
    # New or original records outside the manifest must not reference deletions.
    foreign_keys = {'user_id': 'user', 'reporter_user_id': 'user', 'reviewer_user_id': 'user',
                    'media_id': 'media', 'post_id': 'post', 'list_id': 'user_list'}
    for table, rows in current.items():
        for row_id, record in rows.items():
            if not _positive_id(row_id) or not isinstance(record, dict) or record.get('id') != row_id:
                raise GuardRejected('invalid_record_in_inventory')
            if (table, row_id) in owned:
                continue
            for field, target_table in foreign_keys.items():
                value = record.get(field)
                if value is not None and not _positive_id(value):
                    raise GuardRejected('invalid_reference_in_inventory')
                if (target_table, value) in deletes:
                    raise GuardRejected('external_reference_to_fixture')
            if table == 'report':
                target = record.get('target_id')
                if str(target).isdigit() and (record.get('target_type'), int(target)) in deletes:
                    raise GuardRejected('external_report_targets_fixture')
    new_events = [row for row_id, row in current['event_log'].items() if row_id not in baseline['event_log']]
    for symbol in ('R', 'B', *('Q' + str(number) for number in range(1, 9))):
        is_user = symbol in ('R', 'B')
        action = 'admin_account_status_changed' if is_user else 'admin_report_status_changed'
        field = 'target_user_id' if is_user else 'report_id'
        target = current['user' if is_user else 'report'][ids[symbol]]
        def matches(event):
            metadata = event.get('metadata')
            if not isinstance(metadata, dict):
                return False
            marker = metadata.get('reason' if is_user else 'decision', '')
            return (event.get('user_id') == admin_id and event.get('action') == action
                    and type(metadata.get(field)) is int and metadata[field] == ids[symbol]
                    and metadata.get('new_status') == ('disabled' if is_user else target['status'])
                    and (is_user or metadata.get('decision') == target.get('decision'))
                    and run_id in str(marker))
        if not any(matches(event) for event in new_events):
            raise GuardRejected('final_fixture_audit_missing')
    return dict(mode='offline_cleanup_preview', remote_execution=False,
                delete_ids={table: sorted(row_id for kind, row_id in deletes if kind == table)
                            for table in ('post', 'media')},
                retained_records=16, preserved_audit_events=len(current['event_log']),
                original_records_preserved=sum(len(rows) for rows in baseline.values()),
                current_snapshot_digest=digest(current))
