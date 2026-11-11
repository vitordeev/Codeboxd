"""Two-code acceptance runner; every HTTP call uses an in-memory transport."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import httpx

from tools.password_recovery_remote import CheckStopped, Probe, main, available_actions

EMAIL, ORIGINAL = 'controlled@example.invalid', 'Original9!private'


class Fixture:
    def __init__(self):
        self.now = 0.0
        self.password = ORIGINAL
        self.calls = []
        self.updates = []
        self.version = 0
        self.sent = 0
        self.used = set()
        self.timeout_write = None
        self.commit_timeout = True
        self.reject_code = False
        self.foreign_identity = False
        self.timeout_send = False
        self.malformed_login = False

    def sleep(self, duration):
        self.now += duration

    def handle(self, request):
        path = request.url.path
        body = json.loads(request.content) if request.content else {}
        self.calls.append((request.method, path))
        if path.endswith('/auth/login'):
            if body['password'] != self.password:
                return httpx.Response(401)
            if self.malformed_login:
                return httpx.Response(200, json={'authToken': 'private-session', 'user_id': True})
            return httpx.Response(200, json={'authToken': 'private-session', 'user_id': 7})
        if path.endswith('/request-reset-link'):
            self.sent += 1
            if self.timeout_send:
                raise httpx.ReadTimeout('provider-private-value', request=request)
            return httpx.Response(200, json={'message': {'success': True}})
        if path.endswith('/magic-link-login'):
            code = body['magic_token']
            if self.reject_code or code in self.used or code not in ('123456', '654321'):
                return httpx.Response(401)
            self.used.add(code)
            return httpx.Response(200, json={'authToken': 'private-reset-' + code,
                                           'user_id': 8 if self.foreign_identity else 7})
        if path.endswith('/update_password'):
            authorization = request.headers.get('Authorization')
            self.updates.append(authorization)
            assert authorization.startswith('Bearer private-reset-')
            self.version += 1
            uncertain = self.timeout_write == self.version
            if not uncertain or self.commit_timeout:
                self.password = body['password']
            if uncertain:
                raise httpx.ReadTimeout('private-write-body', request=request)
            return httpx.Response(200, json={'message': {'success': True}})
        if path.endswith('/auth/me'):
            return httpx.Response(401)
        raise AssertionError(path)


class RecoveryAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.output = Path(self.folder.name) / 'result.json'
        self.fixture = Fixture()
        self.client = httpx.Client(transport=httpx.MockTransport(self.fixture.handle))
        self.addCleanup(self.client.close)
        self.probe = Probe(self.client, 'https://fixture.invalid/api:auth', self.output,
                           approval_reference='specific approval fixture',
                           clock=lambda: self.fixture.now, sleep=self.fixture.sleep)

    def begin(self):
        self.probe.begin(EMAIL, ORIGINAL)

    def first(self):
        self.begin()
        self.probe.first_code('123456')

    def restore(self):
        self.fixture.now += 61
        self.probe.request_restoration()
        self.probe.restore_code('654321')

    def test_complete_flow_uses_two_reset_credentials_and_restores_original(self):
        self.first()
        self.assertTrue(self.probe.restoration_needed)
        self.assertFalse(self.probe.report['passed'])
        self.restore()
        self.assertEqual(self.fixture.password, ORIGINAL)
        self.assertFalse(self.probe.restoration_needed)
        self.assertTrue(self.probe.report['passed'])
        self.assertEqual(self.fixture.sent, 2)
        self.assertEqual(self.fixture.updates, ['Bearer private-reset-123456', 'Bearer private-reset-654321'])
        evidence = self.output.read_text()
        self.assertEqual(json.loads(evidence)['layer'], 'simulated_transport')
        for value in (EMAIL, ORIGINAL, '123456', '654321', 'private-session', 'private-reset', 'specific approval fixture'):
            self.assertNotIn(value, evidence)
        self.assertEqual(self.probe.original, '')

    def test_timeout_after_committed_first_write_never_retries_and_allows_fresh_restore(self):
        self.fixture.timeout_write = 1
        self.begin()
        with self.assertRaisesRegex(CheckStopped, 'uncertain'):
            self.probe.first_code('123456')
        self.assertTrue(self.probe.restoration_needed)
        before = len(self.fixture.calls)
        with self.assertRaises(CheckStopped):
            self.probe.first_code('123456')
        self.assertEqual(len(self.fixture.calls), before)
        self.restore()
        self.assertEqual(self.fixture.password, ORIGINAL)
        self.assertFalse(self.probe.report['passed'])
        self.assertEqual(len(self.fixture.updates), 2)

    def test_uncommitted_timeout_reconciles_with_login_without_second_write(self):
        self.fixture.timeout_write, self.fixture.commit_timeout = 1, False
        self.begin()
        with self.assertRaises(CheckStopped):
            self.probe.first_code('123456')
        self.assertTrue(self.probe.confirm_original())
        self.assertFalse(self.probe.restoration_needed)
        self.assertFalse(self.probe.report['passed'])
        self.assertEqual(len(self.fixture.updates), 1)
        self.assertEqual(self.fixture.sent, 1)

    def test_timeout_during_restore_keeps_pending_until_original_login_confirmed(self):
        self.first()
        self.fixture.timeout_write = 2
        with self.assertRaises(CheckStopped):
            self.restore()
        self.assertTrue(self.probe.restoration_needed)
        before = len(self.fixture.updates)
        with self.assertRaises(CheckStopped):
            self.probe.restore_code('654321')
        self.assertEqual(len(self.fixture.updates), before)
        self.assertTrue(self.probe.confirm_original())
        self.assertFalse(self.probe.report['passed'])

    def test_rejected_or_expired_first_code_never_changes_password(self):
        self.fixture.reject_code = True
        self.begin()
        with self.assertRaises(CheckStopped):
            self.probe.first_code('123456')
        self.assertFalse(self.probe.restoration_needed)
        self.assertEqual(self.fixture.updates, [])

    def test_foreign_reset_identity_never_changes_password(self):
        self.begin()
        self.fixture.foreign_identity = True
        with self.assertRaisesRegex(CheckStopped, 'reset_identity_matches'):
            self.probe.first_code('123456')
        self.assertEqual(self.fixture.updates, [])

    def test_invalid_code_is_rejected_locally_without_consumption(self):
        self.begin()
        before = len(self.fixture.calls)
        for value in ('12345', '1234567', '１２３４５６', 'abcdef'):
            with self.assertRaises(CheckStopped):
                self.probe.first_code(value)
        self.assertEqual(len(self.fixture.calls), before)
        self.assertEqual(self.probe.phase, 'awaiting_first_code')

    def test_cooldown_and_request_replay_do_not_send_more_mail(self):
        self.first()
        before = len(self.fixture.calls)
        with self.assertRaisesRegex(CheckStopped, 'cooldown'):
            self.probe.request_restoration()
        self.assertEqual(len(self.fixture.calls), before)
        self.fixture.now += 61
        self.probe.request_restoration()
        with self.assertRaises(CheckStopped):
            self.probe.request_restoration()
        self.assertEqual(self.fixture.sent, 2)

    def test_uncertain_send_is_not_retried(self):
        self.fixture.timeout_send = True
        with self.assertRaisesRegex(CheckStopped, 'uncertain') as failure:
            self.begin()
        self.assertNotIn('provider-private-value', str(failure.exception))
        with self.assertRaises(CheckStopped):
            self.begin()
        self.assertEqual(self.fixture.sent, 1)
        self.assertFalse(self.probe.restoration_needed)

    def test_evidence_cannot_be_overwritten(self):
        with self.assertRaises(FileExistsError):
            Probe(self.client, 'https://fixture.invalid', self.output, approval_reference='approved')
        self.assertEqual(self.fixture.calls, [])

    def test_request_budget_stops_without_an_extra_network_call(self):
        self.probe.requests = 24
        with self.assertRaisesRegex(CheckStopped, 'request_budget'):
            self.begin()
        self.assertEqual(self.fixture.calls, [])

    def test_rejected_login_can_be_corrected_manually_without_sending_mail_first(self):
        with self.assertRaisesRegex(CheckStopped, 'login_rejected_check_current'):
            self.probe.begin(EMAIL, 'Wrong9!private')
        self.assertEqual(self.probe.phase, 'new')
        self.assertEqual(self.fixture.sent, 0)
        self.assertEqual(self.probe.original, '')
        self.assertEqual(self.probe.report['last_http_status'], 401)
        self.assertNotIn('Wrong9!private', self.output.read_text())
        self.begin()
        self.assertEqual(self.probe.phase, 'awaiting_first_code')
        self.assertEqual(self.fixture.sent, 1)

    def test_three_rejected_logins_stop_before_fourth_request(self):
        for _ in range(3):
            with self.assertRaisesRegex(CheckStopped, 'login_rejected'):
                self.probe.begin(EMAIL, 'Wrong9!private')
        before = len(self.fixture.calls)
        with self.assertRaisesRegex(CheckStopped, 'attempt_limit'):
            self.begin()
        self.assertEqual(len(self.fixture.calls), before)
        self.assertEqual(self.fixture.sent, 0)

    def test_ui_only_enables_actions_for_current_step(self):
        self.assertEqual(available_actions(self.probe), {'begin'})
        self.begin()
        self.assertEqual(available_actions(self.probe), {'first'})
        self.probe.first_code('123456')
        self.assertEqual(available_actions(self.probe), {'confirm'})
        self.fixture.now += 61
        self.assertEqual(available_actions(self.probe), {'confirm', 'request_restore'})
        self.probe.request_restoration()
        self.assertEqual(available_actions(self.probe), {'confirm', 'restore'})
        self.probe.restore_code('654321')
        self.assertEqual(available_actions(self.probe), set())

    def test_closed_window_can_reuse_pending_code_without_another_first_email(self):
        self.begin()
        resumed = Probe(self.client, 'https://fixture.invalid/api:auth',
                        Path(self.folder.name) / 'resumed.json',
                        approval_reference='specific approval fixture',
                        clock=lambda: self.fixture.now, sleep=self.fixture.sleep)
        resumed.resume_pending(self.output)
        resumed.begin(EMAIL, ORIGINAL)
        self.assertEqual(self.fixture.sent, 1)
        self.assertEqual(resumed.mail_requests, 1)
        resumed.first_code('123456')
        self.fixture.now += 61
        resumed.request_restoration()
        resumed.restore_code('654321')
        self.assertEqual(self.fixture.sent, 2)
        self.assertTrue(resumed.report['passed'])
        self.assertNotIn('operator_observation_seconds', resumed.report)

    def test_resume_rejects_pending_password_change(self):
        self.first()
        resumed = Probe(self.client, 'https://fixture.invalid/api:auth',
                        Path(self.folder.name) / 'resumed.json',
                        approval_reference='specific approval fixture',
                        clock=lambda: self.fixture.now, sleep=self.fixture.sleep)
        before = len(self.fixture.calls)
        with self.assertRaises(CheckStopped):
            resumed.resume_pending(self.output)
        self.assertEqual(len(self.fixture.calls), before)

    def test_failed_journal_prevents_password_write(self):
        self.begin()
        original_save = self.probe.save

        def save():
            if self.probe.phase == 'password_write_attempted':
                raise OSError('disk full')
            original_save()

        with patch.object(self.probe, 'save', side_effect=save), self.assertRaises(OSError):
            self.probe.first_code('123456')
        self.assertEqual(self.fixture.updates, [])

    def test_malformed_identity_stops_before_mail(self):
        self.fixture.malformed_login = True
        with self.assertRaises(CheckStopped):
            self.begin()
        self.assertEqual(self.fixture.sent, 0)

    def test_cli_without_specific_gate_never_reads_config_or_calls_network(self):
        for arguments in ([], ['--execute'], ['--approval-reference', 'approved']):
            with patch('tools.password_recovery_remote.dotenv_values') as config, \
                    patch('tools.password_recovery_remote.httpx.Client') as client, \
                    contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(['--output', str(self.output), *arguments])
            config.assert_not_called()
            client.assert_not_called()


if __name__ == '__main__':
    unittest.main()
