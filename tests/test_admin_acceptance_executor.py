"""Local rehearsal only: every request uses MockTransport and .invalid hosts."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import httpx

from tools.admin_acceptance_executor import RehearsalExecutor
from tools.admin_acceptance_guard import Approval, Destination, Fixture, GuardRejected, digest, identity_digest


RUN = 'cbh9_aabbcc112233'


class RehearsalExecutorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.network = patch('socket.socket', side_effect=AssertionError('real network forbidden'))
        self.network.start()
        self.addCleanup(self.network.stop)
        self.destination = Destination('https://admin.invalid', 1, 'v1', 'live', 'api:social', True)
        self.actor = dict(id=900, role='admin', account_status='active')
        self.records = {
            'user': dict(id=901, username=RUN + '_b', role='member', account_status='active'),
            'media': dict(id=902, identity_key=RUN + '_movie', external_source='test',
                          external_id='synthetic', media_type='movie', title=RUN + ' movie'),
            'report': dict(id=903, reporter_user_id=901, target_type='message', target_id='synthetic',
                           description=RUN + ' report', status='pending',
                           target_snapshot={'body': 'synthetic content'}),
        }
        self.payloads = {
            'user': dict(account_status='disabled', reason=RUN + ' test'),
            'media': dict(title=RUN + ' edited', year=2026),
            'report': dict(status='resolved', decision=RUN + ' decision'),
        }
        self.paths = {'user': '/admin/users/901/status', 'media': '/admin/catalog/902',
                      'report': '/admin/reports/903'}
        self.manifest = tuple(Fixture(table, row['id'], RUN, identity_digest(table, row),
                                     digest(row)) for table, row in self.records.items())
        self.approval = Approval('SYNTHETIC CONSENT FOR TEST ONLY', self.destination, RUN, 900,
            frozenset({'A3'}), True, frozenset((table, row['id'], digest(self.payloads[table]))
                                              for table, row in self.records.items()))
        self.state = copy.deepcopy(self.records)
        self.calls = []
        self.now, self.waits = 0.0, []

    def sleep(self, duration):
        self.waits.append(duration)
        self.now += duration

    def handler(self, request):
        self.calls.append(request)
        if request.url.path == '/api:auth/auth/me':
            return httpx.Response(200, json=self.actor)
        table = next(table for table, row in self.records.items()
                     if request.url.path.endswith('/' + str(row['id'])) or
                     request.url.path.endswith('/' + str(row['id']) + '/status'))
        if request.method == 'GET':
            return httpx.Response(200, json=self.state[table])
        payload = json.loads(request.content)
        if table == 'user':
            payload.pop('reason')
        if table == 'report':
            payload.update(reviewer_user_id=900, reviewed_at=1)
        self.state[table].update(payload)
        return httpx.Response(200, json={'success': True})

    def executor(self, handler=None, **changes):
        args = dict(destination=self.destination, approval=self.approval,
            manifest=self.manifest, table_ids={'user': 11, 'media': 12, 'report': 13},
            transport=httpx.MockTransport(handler or self.handler),
            journal_path=Path(self.tmp.name)/'journal.jsonl',
            clock=lambda: self.now, sleep=self.sleep)
        executor = RehearsalExecutor(**dict(args, **changes))
        self.addCleanup(executor.close)
        return executor

    def update(self, executor, table='user', **changes):
        return executor.update(**dict(dict(path=self.paths[table], payload=self.payloads[table],
            cached_record=self.state[table], confirmed=True), **changes))

    def journal(self):
        return [json.loads(line) for line in (Path(self.tmp.name)/'journal.jsonl').read_text().splitlines()]

    def test_three_successes_require_independent_reads(self):
        executor = self.executor()
        for table in self.records:
            result = self.update(executor, table)
            self.assertEqual(result['mode'], 'simulated_verified')
            self.assertFalse(result['remote_execution'])
        self.assertEqual([r.method for r in self.calls], ['GET', 'GET', 'PUT', 'GET'] * 3)
        self.assertEqual(executor.calls, 12)
        self.assertEqual(sum(row['event'] == 'verified' for row in self.journal()), 3)

    def test_non_mock_and_non_synthetic_destinations_are_rejected(self):
        with self.assertRaisesRegex(GuardRejected, 'mock_transport_required'):
            self.executor(transport=object())
        with self.assertRaisesRegex(GuardRejected, 'synthetic_destination_required'):
            self.executor(destination=replace(self.destination, origin='https://example.com'))
        self.assertEqual(self.calls, [])

    def test_cancellation_sends_no_request(self):
        executor = self.executor()
        with self.assertRaisesRegex(GuardRejected, 'confirmation_required'):
            self.update(executor, confirmed=False)
        self.assertEqual(executor.calls, 0)
        self.assertEqual([row['event'] for row in self.journal()], ['simulation_started'])

    def test_read_only_approval_cannot_send_requests(self):
        executor = self.executor(approval=replace(self.approval, phases=frozenset({'A0', 'A1'})))
        with self.assertRaisesRegex(GuardRejected, 'phase_not_approved'):
            self.update(executor)
        self.assertEqual(self.calls, [])

    def test_unapproved_payload_is_blocked_before_transport(self):
        executor = self.executor()
        with self.assertRaisesRegex(GuardRejected, 'update_not_approved'):
            self.update(executor, payload=dict(self.payloads['user'], reason=RUN + ' altered'))
        self.assertEqual(self.calls, [])

    def test_current_actor_must_still_be_active_admin(self):
        executor = self.executor()
        self.actor['account_status'] = 'disabled'
        with self.assertRaisesRegex(GuardRejected, 'actor_not_authorized'):
            self.update(executor)
        self.assertTrue(executor.halted)
        self.assertEqual([r.method for r in self.calls], ['GET'])

    def test_missing_approval_cannot_create_journal(self):
        with self.assertRaisesRegex(GuardRejected, 'approval_required'):
            self.executor(approval=None)
        self.assertFalse((Path(self.tmp.name)/'journal.jsonl').exists())

    def test_wrong_actor_and_member_stop_before_target_read(self):
        for actor in (dict(id=999, role='admin', account_status='active'),
                      dict(id=900, role='member', account_status='active')):
            with self.subTest(actor=actor):
                self.actor = actor
                executor = self.executor(journal_path=Path(self.tmp.name)/f"actor-{actor['id']}.jsonl")
                with self.assertRaisesRegex(GuardRejected, 'actor_not_authorized'):
                    self.update(executor)
                self.assertEqual(executor.calls, 1)
                self.assertTrue(executor.halted)

    def test_foreign_id_is_rejected_before_reads(self):
        executor = self.executor()
        with self.assertRaisesRegex(GuardRejected, 'foreign_target'):
            self.update(executor, path='/admin/users/999/status')
        self.assertEqual(self.calls, [])

    def test_fresh_snapshot_drift_stops_before_put(self):
        executor = self.executor()
        cached = copy.deepcopy(self.state['user'])
        self.state['user']['account_status'] = 'disabled'
        with self.assertRaisesRegex(GuardRejected, 'snapshot_changed'):
            self.update(executor, cached_record=cached)
        self.assertTrue(executor.halted)
        self.assertEqual([r.method for r in self.calls], ['GET', 'GET'])

    def test_remaining_budget_must_cover_whole_sequence(self):
        executor = self.executor(request_limit=7)
        self.update(executor)
        with self.assertRaisesRegex(GuardRejected, 'insufficient_request_budget'):
            self.update(executor, 'media')
        self.assertEqual(executor.calls, 4)

    def test_spacing_is_enforced_with_virtual_clock(self):
        executor = self.executor()
        self.update(executor)
        self.assertEqual(len(self.waits), 3)
        self.assertTrue(all(wait >= 3.1 for wait in self.waits))

    def test_redirect_rate_limit_and_bad_json_stop_without_retry(self):
        for status, body in [(302, {}), (429, {}), (200, [])]:
            with self.subTest(status=status, body=body):
                path = Path(self.tmp.name)/f'{status}-{type(body).__name__}.jsonl'
                executor = self.executor(lambda request: httpx.Response(status, json=body), journal_path=path)
                with self.assertRaisesRegex(GuardRejected, 'response_rejected_no_retry'):
                    self.update(executor)
                self.assertTrue(executor.halted)
                self.assertEqual(executor.calls, 1)
                with self.assertRaisesRegex(GuardRejected, 'executor_stopped'):
                    self.update(executor)

    def test_http_200_without_persistence_is_not_success(self):
        def handler(request):
            if request.method == 'PUT':
                self.calls.append(request)
                return httpx.Response(200, json={'success': True})
            return self.handler(request)
        executor = self.executor(handler)
        with self.assertRaisesRegex(GuardRejected, 'write_requires_reconciliation'):
            self.update(executor)
        self.assertTrue(executor.halted)
        self.assertEqual(self.journal()[-1]['event'], 'requires_reconciliation')
        self.assertNotIn('verified', [row['event'] for row in self.journal()])

    def test_timeout_after_effect_is_never_replayed(self):
        def handler(request):
            response = self.handler(request)
            if request.method == 'PUT':
                raise httpx.ReadTimeout('SYNTHETIC PRIVATE DETAILS', request=request)
            return response
        executor = self.executor(handler)
        with self.assertRaisesRegex(GuardRejected, '^write_requires_reconciliation$'):
            self.update(executor)
        self.assertEqual(self.state['user']['account_status'], 'disabled')
        with self.assertRaisesRegex(GuardRejected, 'executor_stopped'):
            self.update(executor)
        self.assertEqual(sum(r.method == 'PUT' for r in self.calls), 1)
        self.assertEqual(self.journal()[-1]['event'], 'requires_reconciliation')

    def test_intent_is_durable_before_put_and_journal_has_no_payload(self):
        def handler(request):
            if request.method == 'PUT':
                self.assertEqual(self.journal()[-1]['event'], 'intent')
            return self.handler(request)
        executor = self.executor(handler)
        self.update(executor)
        contents = (Path(self.tmp.name)/'journal.jsonl').read_text()
        for private in (RUN, 'username', 'reason', 'disabled', 'SYNTHETIC CONSENT'):
            self.assertNotIn(private, contents)

    def test_journal_failure_before_intent_prevents_put(self):
        executor = self.executor()
        original = executor._append
        def append(event, **fields):
            if event == 'intent':
                with patch('os.fsync', side_effect=OSError('private location')):
                    original(event, **fields)
            else:
                original(event, **fields)
        with patch.object(executor, '_append', side_effect=append):
            with self.assertRaisesRegex(GuardRejected, 'journal_write_failed'):
                self.update(executor)
        self.assertTrue(executor.halted)
        self.assertEqual([r.method for r in self.calls], ['GET', 'GET'])

    def test_existing_journal_blocks_restart(self):
        executor = self.executor()
        self.update(executor)
        with self.assertRaisesRegex(GuardRejected, 'journal_exists_requires_reconciliation'):
            self.executor()

    def test_success_cannot_be_repeated_silently(self):
        executor = self.executor()
        self.update(executor)
        with self.assertRaisesRegex(GuardRejected, 'operation_already_attempted'):
            self.update(executor)
        self.assertEqual(executor.calls, 4)

    def test_target_identity_and_snapshot_are_preserved(self):
        def handler(request):
            response = self.handler(request)
            if request.method == 'PUT':
                self.state['report']['target_snapshot']['body'] = 'unexpected modification'
            return response
        executor = self.executor(handler)
        with self.assertRaisesRegex(GuardRejected, 'write_requires_reconciliation'):
            self.update(executor, 'report')
        self.assertTrue(executor.halted)

    def test_failed_verification_read_does_not_repeat_write(self):
        def handler(request):
            if request.method == 'GET' and self.state['user']['account_status'] == 'disabled':
                self.calls.append(request)
                raise httpx.ReadTimeout('synthetic timeout', request=request)
            return self.handler(request)
        executor = self.executor(handler)
        with self.assertRaisesRegex(GuardRejected, 'write_requires_reconciliation'):
            self.update(executor)
        self.assertTrue(executor.halted)
        self.assertEqual(executor.calls, 4)
        self.assertEqual(sum(r.method == 'PUT' for r in self.calls), 1)
        self.assertEqual(self.journal()[-1]['event'], 'requires_reconciliation')

    def test_invalid_limits_and_mapping(self):
        for changes in ({'request_limit': 3}, {'request_limit': 501}, {'interval': 0},
                        {'interval': float('nan')}, {'table_ids': {'user': 11}},
                        {'table_ids': {'user': 1, 'media': 1, 'report': 1}}):
            with self.subTest(changes=changes), self.assertRaises(GuardRejected):
                self.executor(**changes)


if __name__ == '__main__':
    unittest.main()
