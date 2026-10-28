"""Generate isolated Xano account scenarios and check synthetic debug results offline.

This module never contacts Xano or reads credentials. The generated functions
are interpreter fixtures, not API endpoints: actor_id/extras replace $auth only
inside synthetic functions. They must never be published as application APIs.
"""
import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    'suspend': {},
    'reactivate': {'initial': 'disabled', 'destination': 'active'},
    'suspend_without_reason': {'reason': ''},
    'member_denied': {'role': 'member', 'error': 'ERROR_CODE_ACCESS_DENIED'},
    'moderator_denied': {'role': 'moderator', 'error': 'ERROR_CODE_ACCESS_DENIED'},
    'disabled_admin_denied': {'actor_status': 'disabled', 'error': 'ERROR_CODE_UNAUTHORIZED'},
    'missing_actor_denied': {'missing_actor': True, 'error': 'ERROR_CODE_UNAUTHORIZED'},
    'stale_session_denied': {'version': 6, 'error': 'ERROR_CODE_UNAUTHORIZED'},
    'reset_token_denied': {'purpose': 'password_reset', 'error': 'ERROR_CODE_UNAUTHORIZED'},
    'legacy_session_denied': {'legacy': True, 'error': 'ERROR_CODE_UNAUTHORIZED'},
    'active_session': {'guard_only': True},
    'suspended_session_denied': {
        'guard_only': True, 'initial': 'disabled', 'error': 'ERROR_CODE_UNAUTHORIZED'},
}


def _fixture_names(source):
    """Rename only declared production DB operations and the guard dependency."""
    source = source.replace('"Security/require_current_session"', '"account_fixture_guard"')
    for original, replacement in (('user', 'account_fixture_user'),
                                  ('event_log', 'account_fixture_event')):
        source = re.sub(r'(\bdb\.(?:get|edit|add|query)\s+)' + original + r'\b',
                        lambda match: match[1] + replacement, source)
        source = source.replace('$db.' + original + '.', '$db.' + replacement + '.')
    return source


def _contracts(root):
    source = (root / 'xano/api/codeboxd/admin_users_id_status_PUT.xs').read_text(encoding='utf-8')
    match = re.search(r'  input \{(.*?)\n  \}\n\n  stack \{', source, re.S)
    if match is None:
        raise ValueError('Account endpoint structure changed; review fixture extraction')
    body = source[source.index('  stack {'):source.index('\n  guid =')]
    inputs = match[1] + '\n    int actor_id\n    json extras'
    operation = 'function "account_fixture_change" {\n  input {' + inputs + '\n  }\n' + body + '\n}'
    operation = operation.replace('$auth.id', '$input.actor_id').replace('$auth.extras', '$input.extras')
    guard = (root / 'xano/function/security/require_current_session.xs').read_text(encoding='utf-8')
    guard = guard[:guard.index('\n  guid =')] + '\n}'
    return _fixture_names(guard), _fixture_names(operation)


def script(scenario, root=ROOT):
    """Return a standalone multidoc fixture; do not execute or publish it."""
    if scenario not in CASES:
        raise ValueError('Unknown account fixture scenario')
    case = CASES[scenario]
    guard, operation = _contracts(Path(root))
    tables = '''table account_fixture_user {
  schema {
    int id
    text role
    text account_status
    int session_version
    timestamp updated_at?=now
  }
  index = [{type: "primary", field: [{name: "id"}]}]
}
---
table account_fixture_event {
  schema {
    int id
    timestamp created_at?=now
    int user_id
    text action
    json metadata
  }
  index = [{type: "primary", field: [{name: "id"}]}]
}'''
    actor = dict(role=case.get('role', 'admin'),
                 account_status=case.get('actor_status', 'active'), session_version=7)
    target = dict(role='member', account_status=case.get('initial', 'active'), session_version=7)
    extras = {} if case.get('legacy') else dict(
        session_version=case.get('version', 7), purpose=case.get('purpose', 'session'))
    setup = ('    db.add account_fixture_user { data = ' + json.dumps(actor) + ' } as $actor_seed\n'
             '    db.add account_fixture_user { data = ' + json.dumps(target) + ' } as $target_seed\n')
    if case.get('guard_only'):
        call = ('    function.run "account_fixture_guard" {\n'
                '      input = {user_id: $target_seed.id, extras: ' + json.dumps(extras) + ', allow_reset: false}\n'
                '    } as $operation\n')
    else:
        actor_id = '2147483647' if case.get('missing_actor') else '$actor_seed.id'
        call = ('    function.run "account_fixture_change" {\n'
                '      input = {id: $target_seed.id, actor_id: ' + actor_id + ', extras: ' + json.dumps(extras)
                + ', account_status: ' + json.dumps(case.get('destination', 'disabled'))
                + ', reason: ' + json.dumps(case.get('reason', 'Synthetic account fixture')) + '}\n'
                '    } as $operation\n')
    inspect = '''    db.get account_fixture_user {
      field_name = "id"
      field_value = $target_seed.id
    } as $target_after
    db.query account_fixture_event {
      return = {type: "list", paging: {page: 1, per_page: 10, totals: true}}
    } as $events
'''
    entry = ('function "account_fixture" {\n  input {}\n  stack {\n' + setup + call + inspect
             + '  }\n  response = {actor_id: $actor_seed.id, target_id: $target_seed.id, '
             'operation: $operation, target: $target_after, events: $events.items, events_total: $events.itemsTotal}\n}')
    return '\n---\n'.join((tables, guard, operation, entry))


def check_result(data, scenario):
    """Fail closed on incomplete/malformed interpreter output; return booleans only."""
    if scenario not in CASES:
        raise ValueError('Unknown account fixture scenario')
    case = CASES[scenario]
    if not isinstance(data, dict) or data.get('truncated') or data.get('maxed'):
        return {'complete_result': False}
    if 'error' in case:
        exception = data.get('exception')
        return {'expected_denial': data.get('status') == 'exception'
                and isinstance(exception, dict) and exception.get('error_type') == case['error']}
    result = data.get('result')
    if data.get('status') != 'ok' or not isinstance(result, dict):
        return {'successful_execution': False}
    target, events = result.get('target'), result.get('events')
    if not isinstance(target, dict) or not isinstance(events, list):
        return {'result_shape': False}
    actor, target_id = result.get('actor_id'), result.get('target_id')
    checks = dict(identities=type(actor) is int and type(target_id) is int
                  and actor > 0 and target_id > 0 and actor != target_id and target.get('id') == target_id,
                  session_version_preserved=type(target.get('session_version')) is int
                  and target['session_version'] == 7)
    if case.get('guard_only'):
        checks['active_session_accepted'] = (target.get('account_status') == 'active'
            and result.get('operation') is None and events == []
            and type(result.get('events_total')) is int and result['events_total'] == 0)
        return checks
    previous, destination = case.get('initial', 'active'), case.get('destination', 'disabled')
    expected_operation = dict(success=True, user_id=target_id,
                              previous_status=previous, account_status=destination)
    operation_result = result.get('operation')
    checks['operation_response'] = (isinstance(operation_result, dict)
        and operation_result == expected_operation and operation_result.get('success') is True
        and type(operation_result.get('user_id')) is int)
    checks['persisted_status'] = target.get('account_status') == destination
    checks['single_audit'] = (len(events) == 1 and type(result.get('events_total')) is int
                              and result['events_total'] == 1)
    if not checks['single_audit'] or not isinstance(events[0], dict):
        checks['audit_contents'] = False
        return checks
    event = events[0]
    checks['audit_contents'] = (type(event.get('user_id')) is int and event['user_id'] == actor
        and event.get('action') == 'admin_account_status_changed'
        and event.get('metadata') == dict(target_user_id=target_id, previous_status=previous,
            new_status=destination, reason=case.get('reason', 'Synthetic account fixture')))
    checks['audit_timestamp'] = (isinstance(event.get('created_at'), (str, int, float))
                                and not isinstance(event.get('created_at'), bool)
                                and bool(event['created_at']))
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=CASES, required=True)
    parser.add_argument('--check-result', type=Path, help='Read a synthetic debug response; never execute it')
    args = parser.parse_args(argv)
    if args.check_result is None:
        print(script(args.scenario))
        return 0
    try:
        checks = check_result(json.loads(args.check_result.read_text(encoding='utf-8')), args.scenario)
    except (OSError, ValueError, TypeError):
        print(json.dumps({'passed': False, 'error': 'invalid_synthetic_result'}))
        return 1
    passed = bool(checks) and all(checks.values())
    print(json.dumps(dict(layer='offline_synthetic_result_check', scenario=args.scenario,
                          passed=passed, checks=checks, remote_validated=False)))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
