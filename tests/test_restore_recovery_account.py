import json
from pathlib import Path
import tempfile
import unittest

import httpx

from tools.restore_recovery_account import Restoration, CheckStopped


class RestorationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.calls = []
        self.current = 'Temporary8!'
        self.reject = False
        self.timeout_write = False
        self.foreign = False
        def handle(request):
            path = request.url.path
            self.calls.append(path)
            body = json.loads(request.content) if request.content else {}
            if path.endswith('/auth/login'):
                return httpx.Response(200, json={'authToken':'private-session','user_id':7}) if body['password'] == self.current else httpx.Response(401)
            if path.endswith('/auth/me'):
                return httpx.Response(200, json={'id':7, 'email':'foreign@example.invalid' if self.foreign else 'controlled@example.invalid'})
            if path.endswith('/request-reset-link'):
                return httpx.Response(200)
            if path.endswith('/magic-link-login'):
                return httpx.Response(403) if self.reject else httpx.Response(200, json={'authToken':'private-reset','user_id':7})
            if path.endswith('/update_password'):
                if self.timeout_write:
                    raise httpx.ReadTimeout('private-transport-message',request=request)
                self.current = body['password']
                return httpx.Response(200)
            raise AssertionError('unexpected route')
        self.client = httpx.Client(transport=httpx.MockTransport(handle))
        self.addCleanup(self.client.close)
        self.output = Path(self.tmp.name)/'result.json'
        self.probe = Restoration(self.client,'https://fixture.invalid',self.output,
                                 approval_reference='specific restoration approval',sleep=lambda _:None)

    def begin(self):
        self.probe.begin_restore('controlled@example.invalid','Original9!','Original9!',True)

    def test_restore_uses_one_request_and_confirms_identity_without_temporary_write(self):
        self.begin()
        self.probe.restore('123456')
        self.assertTrue(self.probe.report['passed'])
        self.assertFalse(self.probe.restoration_needed)
        self.assertEqual(self.probe.mail_requests,1)
        self.assertEqual(self.current,'Original9!')
        self.assertEqual(sum(p.endswith('/update_password') for p in self.calls),1)
        raw = self.output.read_text()
        for private in ['controlled@example.invalid','Original9!','123456','private-session','private-reset']:
            self.assertNotIn(private,raw)

    def test_existing_password_avoids_email_and_write(self):
        self.current = 'Original9!'
        self.begin()
        self.assertTrue(self.probe.report['passed'])
        self.assertEqual(len(self.calls),2)
        self.assertEqual(self.probe.mail_requests,0)

    def test_rejected_code_never_writes_or_retries(self):
        self.begin()
        self.reject = True
        with self.assertRaises(CheckStopped):
            self.probe.restore('123456')
        count = len(self.calls)
        with self.assertRaises(CheckStopped):
            self.probe.restore('123456')
        self.assertEqual(len(self.calls),count)
        self.assertEqual(self.current,'Temporary8!')
        self.assertTrue(self.probe.restoration_needed)

    def test_uncertain_write_remains_pending_without_retry(self):
        self.begin()
        self.timeout_write = True
        with self.assertRaisesRegex(CheckStopped,'network_result_uncertain_no_retry'):
            self.probe.restore('123456')
        with self.assertRaises(CheckStopped):
            self.probe.restore('123456')
        self.assertEqual(sum(p.endswith('/update_password') for p in self.calls),1)
        self.assertTrue(self.probe.restoration_needed)

    def test_foreign_identity_cannot_be_declared_restored(self):
        self.current = 'Original9!'
        self.foreign = True
        with self.assertRaises(CheckStopped):
            self.begin()
        self.assertFalse(self.probe.report['passed'])
        self.assertTrue(self.probe.restoration_needed)

    def test_invalid_password_or_missing_confirmation_makes_no_network_call(self):
        for password, confirmation, same in [('short','short',True),('Original9!','Other9!',True),('Original9!','Original9!',False)]:
            with self.assertRaises(CheckStopped):
                self.probe.begin_restore('controlled@example.invalid',password,confirmation,same)
        self.assertEqual(self.calls,[])
