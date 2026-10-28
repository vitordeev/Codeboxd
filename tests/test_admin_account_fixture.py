"""Offline safety/negative tests for generated Xano account acceptance fixtures."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.admin_account_fixture import CASES, ROOT, check_result, main, script


def accepted_result(scenario='suspend'):
    previous = 'disabled' if scenario == 'reactivate' else 'active'
    current = 'active' if scenario == 'reactivate' else 'disabled'
    reason = '' if scenario == 'suspend_without_reason' else 'Synthetic account fixture'
    return {'status': 'ok', 'result': {
        'actor_id': 1, 'target_id': 2,
        'operation': {'success': True, 'user_id': 2, 'previous_status': previous,
                      'account_status': current},
        'target': {'id': 2, 'account_status': current, 'session_version': 7},
        'events_total': 1,
        'events': [{'user_id': 1, 'created_at': 123456,
                    'action': 'admin_account_status_changed',
                    'metadata': {'target_user_id': 2, 'previous_status': previous,
                                 'new_status': current, 'reason': reason}}]}}


class AdminAccountFixtureTests(unittest.TestCase):
    def test_every_scenario_generates_only_isolated_tables_and_functions(self):
        for scenario in CASES:
            with self.subTest(scenario=scenario):
                generated = script(scenario)
                self.assertNotIn('auth =', generated)
                self.assertNotIn('$auth.', generated)
                self.assertNotIn('api_group', generated)
                self.assertNotIn('guid =', generated)
                self.assertNotRegex(generated, r'\bdb\.(get|edit|add|query)\s+(user|event_log)\b')
                self.assertIn('function "account_fixture_guard"', generated)
                self.assertIn('function "account_fixture_change"', generated)
                self.assertIn('function "account_fixture"', generated)

    def test_real_claim_policy_and_status_transaction_are_retained(self):
        guard = (ROOT / 'xano/function/security/require_current_session.xs').read_text(encoding='utf-8')
        status = (ROOT / 'xano/api/codeboxd/admin_users_id_status_PUT.xs').read_text(encoding='utf-8')
        generated = script('suspend')
        self.assertIn(next(line for line in guard.splitlines() if 'code =' in line), generated)
        transaction = status[status.index('    db.transaction'):status.index('\n  response =')]
        transaction = transaction.replace('db.edit user', 'db.edit account_fixture_user')
        transaction = transaction.replace('db.add event_log', 'db.add account_fixture_event')
        transaction = transaction.replace('$auth.id', '$input.actor_id')
        self.assertIn(transaction, generated)
        self.assertIn('enum account_status { values = ["active", "disabled"] }', generated)

    def test_unknown_scenario_is_rejected(self):
        with self.assertRaises(ValueError):
            script('not_a_case')
        with self.assertRaises(ValueError):
            check_result({}, 'not_a_case')

    def test_missing_or_changed_contract_fails_without_generating_partial_script(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            endpoint = root / 'xano/api/codeboxd/admin_users_id_status_PUT.xs'
            endpoint.parent.mkdir(parents=True)
            endpoint.write_text('query "changed" {}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'structure changed'):
                script('suspend', root)

    def test_suspension_reactivation_and_empty_reason_expectations(self):
        for scenario in ('suspend', 'reactivate', 'suspend_without_reason'):
            with self.subTest(scenario=scenario):
                self.assertTrue(all(check_result(accepted_result(scenario), scenario).values()))

    def test_each_denial_requires_exact_error_not_arbitrary_failure(self):
        for scenario, case in CASES.items():
            if 'error' not in case:
                continue
            with self.subTest(scenario=scenario):
                data = {'status': 'exception', 'exception': {'error_type': case['error']}}
                self.assertTrue(all(check_result(data, scenario).values()))
                data['exception']['error_type'] = 'INTERPRETER_SYNTAX_ERROR'
                self.assertFalse(all(check_result(data, scenario).values()))
                self.assertFalse(all(check_result(accepted_result(), scenario).values()))

    def test_partial_pending_and_malformed_outputs_cannot_pass(self):
        for data in (None, [], {}, {'status': 'pending'}, {'status': 'ok', 'result': {}},
                     accepted_result() | {'truncated': True}, accepted_result() | {'maxed': True}):
            with self.subTest(data=data):
                self.assertFalse(all(check_result(data, 'suspend').values()))

    def test_wrong_persistence_identity_and_missing_audit_are_rejected(self):
        mutations = (
            lambda r: r['target'].update(account_status='active'),
            lambda r: r['target'].update(id=99),
            lambda r: r['target'].update(session_version=8),
            lambda r: r.update(actor_id=True),
            lambda r: r.update(events=[]),
            lambda r: r.update(events_total=True),
            lambda r: r['operation'].update(success=1),
        )
        for mutate in mutations:
            data = accepted_result()
            mutate(data['result'])
            with self.subTest(mutation=mutate):
                self.assertFalse(all(check_result(data, 'suspend').values()))

    def test_wrong_audit_actor_previous_status_reason_or_timestamp_is_rejected(self):
        for mutate in (
            lambda e: e.update(user_id=2),
            lambda e: e.update(action='other_action'),
            lambda e: e['metadata'].update(previous_status='disabled'),
            lambda e: e['metadata'].update(target_user_id=99),
            lambda e: e['metadata'].update(reason='other'),
            lambda e: e.update(created_at=None),
            lambda e: e.update(created_at=True),
        ):
            data = accepted_result()
            mutate(data['result']['events'][0])
            self.assertFalse(all(check_result(data, 'suspend').values()))

    def test_duplicate_or_malformed_events_fail(self):
        for events in ([None], [{'user_id': 1}], [deepcopy(accepted_result()['result']['events'][0])] * 2):
            data = accepted_result()
            data['result']['events'] = events
            self.assertFalse(all(check_result(data, 'suspend').values()))

    def test_active_guard_requires_no_mutation_or_audit(self):
        data = accepted_result()
        data['result'].update(operation=None, events=[], events_total=0)
        data['result']['target']['account_status'] = 'active'
        self.assertTrue(all(check_result(data, 'active_session').values()))
        data['result']['events_total'] = 1
        self.assertFalse(all(check_result(data, 'active_session').values()))

    def test_output_contains_only_checks_not_private_failure_messages(self):
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / 'synthetic.json'
            result_path.write_text(json.dumps({'status': 'exception', 'exception': {
                'error_type': 'ERROR_CODE_ACCESS_DENIED', 'message': 'PRIVATE_UNTRUSTED_DETAIL'}}), encoding='utf-8')
            capture = io.StringIO()
            with redirect_stdout(capture):
                code = main(['--scenario', 'member_denied', '--check-result', str(result_path)])
            self.assertEqual(code, 0)
            self.assertNotIn('PRIVATE_UNTRUSTED_DETAIL', capture.getvalue())
            self.assertFalse(json.loads(capture.getvalue())['remote_validated'])

    def test_cli_generation_never_uses_network_or_credentials(self):
        with patch('socket.socket', side_effect=AssertionError('Network forbidden')):
            capture = io.StringIO()
            with redirect_stdout(capture):
                self.assertEqual(main(['--scenario', 'suspend']), 0)
            self.assertIn('function "account_fixture"', capture.getvalue())

    def test_cli_invalid_file_reports_sanitized_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / 'synthetic.json'
            result_path.write_text('PRIVATE_INVALID_JSON', encoding='utf-8')
            capture = io.StringIO()
            with redirect_stdout(capture):
                self.assertEqual(main(['--scenario', 'suspend', '--check-result', str(result_path)]), 1)
            self.assertEqual(json.loads(capture.getvalue()), {
                'passed': False, 'error': 'invalid_synthetic_result'})


if __name__ == '__main__':
    unittest.main()
