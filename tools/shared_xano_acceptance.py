"""Offline batch previews for the existing Xano workspace. Never performs I/O to Xano.

Snapshots and provisioning receipts must be independently collected. Consistency
checks here cannot authenticate their origin or authorize a future live executor.
"""
import argparse
import json
import math
from pathlib import Path
import re
import time
from urllib.parse import urlsplit

from tools.admin_acceptance_guard import GuardRejected, digest, identity_digest

ROOT = Path(__file__).resolve().parents[1]
MAX_ACTIONS = 10
MAX_LIFETIME = 1800
IDENTITY = {'post': ('user_id',), 'user_list': ('user_id',)}
MARKER = {'user': 'username', 'media': 'identity_key', 'report': 'description',
          'post': 'body', 'user_list': 'title'}
ROUTES = (
    ('PUT', re.compile(r'/admin/users/([1-9][0-9]*)/status'), 'user'),
    ('PUT', re.compile(r'/admin/catalog/([1-9][0-9]*)'), 'media'),
    ('PUT', re.compile(r'/admin/reports/([1-9][0-9]*)'), 'report'),
    ('DELETE', re.compile(r'/posts/([1-9][0-9]*)'), 'post'),
    ('DELETE', re.compile(r'/lists/([1-9][0-9]*)'), 'user_list'),
)
FIELDS = {'user': {'account_status', 'reason'},
          'media': {'title', 'description', 'cover_url', 'year'},
          'report': {'status', 'decision'}}


def require(condition, reason):
    if not condition:
        raise GuardRejected(reason)


def positive(value):
    return type(value) is int and value > 0


def timestamp(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def destination(value):
    require(isinstance(value, dict), 'destination_required')
    require(set(value) == {'origin', 'workspace', 'branch', 'data_source', 'api_group', 'shared'},
            'destination_fields_invalid')
    origin = value['origin']
    require(isinstance(origin, str), 'invalid_origin')
    try:
        parts = urlsplit(origin)
        canonical = (parts.scheme == 'https' and bool(parts.hostname) and not parts.username
                     and not parts.password and not parts.path and not parts.query and not parts.fragment
                     and parts.netloc == parts.hostname and origin == 'https://' + parts.hostname)
    except ValueError:
        canonical = False
    require(canonical, 'invalid_origin')
    require(positive(value['workspace']) and value['shared'] is True, 'shared_destination_required')
    for key in ('branch', 'data_source'):
        require(isinstance(value[key], str) and re.fullmatch(r'[A-Za-z0-9_-]+', value[key]),
                'invalid_destination_scope')
    require(isinstance(value['api_group'], str) and re.fullmatch(r'api:[A-Za-z0-9_-]+', value['api_group']),
            'invalid_api_group')
    return value


def row_identity(table, record):
    require(isinstance(record, dict), 'invalid_record')
    if table in ('user', 'media', 'report'):
        return identity_digest(table, record)
    require(table in IDENTITY and positive(record.get('user_id')), 'invalid_record_owner')
    return digest({key: record[key] for key in IDENTITY[table]})


def preview(plan, *, now=None):
    now = time.time() if now is None else now
    require(timestamp(now) and isinstance(plan, dict), 'invalid_plan')
    target = destination(plan.get('destination'))
    run = plan.get('run_id')
    require(isinstance(run, str) and re.fullmatch(r'cbshared_[a-f0-9]{12}', run), 'invalid_run_id')
    created, expires = plan.get('created_at'), plan.get('expires_at')
    require(timestamp(created) and timestamp(expires) and created <= now < expires
            and 0 < expires - created <= MAX_LIFETIME, 'plan_expired_or_invalid_time')
    baseline = plan.get('baseline')
    require(isinstance(baseline, dict) and baseline.get('complete') is True, 'complete_baseline_required')
    require(baseline.get('destination_digest') == digest(target), 'baseline_destination_mismatch')
    require(timestamp(baseline.get('captured_at')) and baseline['captured_at'] <= created,
            'baseline_must_precede_plan')
    before = baseline.get('tables')
    current = plan.get('current')
    require(isinstance(before, dict) and isinstance(current, dict), 'inventory_required')
    require(all(isinstance(rows, dict) for rows in [*before.values(), *current.values()]), 'invalid_inventory')
    operator = plan.get('operator_id')
    require(positive(operator), 'invalid_operator')
    actor = current.get('user', {}).get(str(operator))
    require(isinstance(actor, dict) and type(actor.get('id')) is int and actor['id'] == operator
            and actor.get('role') == 'admin' and actor.get('account_status') == 'active'
            and before.get('user', {}).get(str(operator)) == digest(actor), 'original_admin_required')
    receipts = plan.get('receipts')
    require(isinstance(receipts, list) and 0 < len(receipts) <= 50, 'receipts_required')
    fixtures = {}
    for receipt in receipts:
        require(isinstance(receipt, dict), 'invalid_receipt')
        table, row_id = receipt.get('table'), receipt.get('id')
        require(isinstance(table, str) and table in MARKER and positive(row_id), 'invalid_fixture_id')
        key = (table, row_id)
        require(key not in fixtures, 'duplicate_fixture')
        require(table in before and table in current, 'fixture_inventory_missing')
        # Canonical IDs also prevent leading-zero or integer-key disguises.
        require(all(isinstance(k, str) and re.fullmatch(r'[1-9][0-9]*', k)
                    and isinstance(v, str) and re.fullmatch(r'[a-f0-9]{64}', v)
                    for k, v in before[table].items()), 'invalid_baseline')
        require(str(row_id) not in before[table], 'preexisting_record_is_not_fixture')
        record = current[table].get(str(row_id))
        original = receipt.get('created_snapshot')
        require(isinstance(record, dict) and type(record.get('id')) is int and record['id'] == row_id
                and isinstance(original, dict) and type(original.get('id')) is int and original['id'] == row_id,
                'fixture_record_missing')
        require(receipt.get('run_id') == run, 'foreign_run')
        require(receipt.get('created_digest') == digest(original), 'creation_receipt_changed')
        require(receipt.get('identity_digest') == row_identity(table, original)
                == row_identity(table, record), 'fixture_identity_changed')
        require(receipt.get('snapshot_digest') == digest(record), 'fixture_snapshot_changed')
        require(all(isinstance(row.get(MARKER[table]), str) and row[MARKER[table]].startswith(run)
                    for row in (record, original)), 'fixture_marker_missing')
        if table == 'user':
            require(row_id != operator and record.get('role') == original.get('role') == 'member',
                    'protected_account')
        fixtures[key] = record
    for (table, row_id), record in fixtures.items():
        if table in ('post', 'user_list'):
            require(('user', record.get('user_id')) in fixtures, 'fixture_owner_not_proven')
        if table == 'user_list':
            require(record.get('default_key') is None, 'default_list_not_supported')
        if table == 'report':
            require(positive(record.get('reporter_user_id')) and ('user', record['reporter_user_id']) in fixtures,
                    'fixture_reporter_not_proven')
            kind, target_id = record.get('target_type'), record.get('target_id')
            require(kind in ('post', 'media') and str(target_id).isdigit()
                    and (kind, int(target_id)) in fixtures, 'report_target_not_fixture')
    actions = plan.get('actions')
    require(isinstance(actions, list) and 0 < len(actions) <= MAX_ACTIONS, 'invalid_action_budget')
    touched = set()
    for action in actions:
        require(isinstance(action, dict) and set(action) == {'method', 'path', 'payload'}, 'invalid_action_fields')
        method, path, payload = action['method'], action['path'], action['payload']
        require(isinstance(method, str) and isinstance(path, str), 'invalid_action_route')
        match = next(((pattern.fullmatch(path), table) for verb, pattern, table in ROUTES
                      if verb == method and pattern.fullmatch(path)), None)
        require(match is not None, 'route_not_supported')
        found, table = match
        key = (table, int(found[1]))
        require(key in fixtures, 'target_not_fixture')
        require(key not in touched, 'duplicate_action_target')
        touched.add(key)
        require(isinstance(payload, dict), 'invalid_payload')
        if method == 'DELETE':
            require(payload == {}, 'delete_payload_not_supported')
            require(plan.get('references_complete') is True and isinstance(plan.get('references'), dict)
                    and plan['references'].get(f'{table}:{key[1]}') == [], 'empty_reference_inventory_required')
        else:
            require(bool(payload) and not set(payload) - FIELDS[table], 'payload_fields_not_allowed')
            if table == 'user':
                require(payload.get('account_status') in ('active', 'disabled'), 'invalid_account_status')
                marker = payload.get('reason')
            elif table == 'report':
                require(payload.get('status') in ('reviewing', 'resolved', 'rejected'), 'invalid_report_status')
                marker = payload.get('decision')
            else:
                marker = payload.get('title')
                require('year' not in payload or type(payload['year']) is int and 1000 <= payload['year'] <= 3000,
                        'invalid_media_year')
                require(not payload.get('cover_url'), 'external_cover_not_supported')
            require(isinstance(marker, str) and marker.startswith(run), 'payload_marker_missing')
        require(all(isinstance(value, (str, int)) and not isinstance(value, bool)
                    for value in payload.values()), 'invalid_payload_value')
    return {'mode': 'offline_shared_preview', 'remote_execution': False, 'approval_checked': False,
            'plan_digest': digest(plan), 'destination_digest': digest(target),
            'actions': len(actions), 'fixtures': len(fixtures), 'expires_at': expires,
            'baseline_verified_remotely': False}


def review_approval(plan, approval, *, now=None):
    now = time.time() if now is None else now
    report = preview(plan, now=now)
    require(isinstance(approval, dict), 'approval_required')
    require(isinstance(approval.get('reference'), str) and approval['reference'].strip(), 'approval_reference_required')
    require(approval.get('plan_digest') == report['plan_digest'], 'approval_digest_mismatch')
    reviewed, expires = approval.get('reviewed_at'), approval.get('expires_at')
    require(timestamp(reviewed) and timestamp(expires)
            and plan['created_at'] <= reviewed <= now < expires <= plan['expires_at']
            and expires - reviewed <= MAX_LIFETIME, 'approval_expired_or_invalid_time')
    return {**report, 'approval_checked': True}


def example(now=None):
    now = time.time() if now is None else now
    run = 'cbshared_012345abcdef'
    target = {'origin': 'https://example.invalid', 'workspace': 147717, 'branch': 'v1',
              'data_source': 'live', 'api_group': 'api:fixture', 'shared': True}
    actor = {'id': 7, 'role': 'admin', 'account_status': 'active'}
    member = {'id': 42, 'username': run+'_member', 'role': 'member', 'account_status': 'active'}
    post = {'id': 43, 'user_id': 42, 'body': run+' disposable post'}
    receipts = []
    for table, record in (('user', member), ('post', post)):
        receipts.append({'table': table, 'id': record['id'], 'run_id': run,
                         'created_snapshot': record.copy(), 'created_digest': digest(record),
                         'identity_digest': row_identity(table, record), 'snapshot_digest': digest(record)})
    return {'destination': target, 'run_id': run, 'operator_id': 7,
            'created_at': now, 'expires_at': now+900,
            'baseline': {'complete': True, 'captured_at': now-1, 'destination_digest': digest(target),
                         'tables': {'user': {'7': digest(actor)}, 'post': {}}},
            'current': {'user': {'7': actor, '42': member}, 'post': {'43': post}},
            'references_complete': True, 'references': {'post:43': []},
            'receipts': receipts, 'actions': [{'method': 'DELETE', 'path': '/posts/43', 'payload': {}}]}


def private_json(path):
    resolved = Path(path).resolve()
    require(resolved.is_relative_to(ROOT/'.local') and resolved.is_file(), 'private_input_required')
    require(resolved.stat().st_size <= 2*1024*1024, 'input_too_large')
    try:
        return json.loads(resolved.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError):
        raise GuardRejected('invalid_plan_json') from None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--plan', type=Path)
    mode.add_argument('--example', action='store_true')
    parser.add_argument('--approval', type=Path)
    args = parser.parse_args(argv)
    try:
        require(not args.example or args.approval is None, 'example_approval_not_supported')
        plan = example() if args.example else private_json(args.plan)
        report = review_approval(plan, private_json(args.approval)) if args.approval else preview(plan)
        print(json.dumps(report, sort_keys=True))
        return 0
    except (GuardRejected, OSError) as exc:
        code = str(exc) if isinstance(exc, GuardRejected) else 'private_input_unavailable'
        print(json.dumps({'mode': 'offline_shared_preview', 'remote_execution': False, 'error': code}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
