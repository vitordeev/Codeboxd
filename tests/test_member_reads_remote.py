import json
from pathlib import Path
import tempfile
import unittest

import httpx

from tools.member_reads_remote import MemberProbe


class MemberReadsTests(unittest.TestCase):
    def test_five_samples_stay_within_budget_and_hide_private_values(self):
        methods = []
        def handler(request):
            methods.append(request.method)
            path = request.url.path
            data = []
            if path == '/auth/login': data = {'authToken': 'PRIVATE_TOKEN'}
            elif path == '/auth/me': data = dict(id=7, role='member', account_status='active')
            elif path == '/profiles/7': data = {'profile': {'user_id': 7, 'name': 'PRIVATE_NAME'}}
            elif path == '/library': data = {'items': [{'user_id': 7}]}
            return httpx.Response(200, json=data)
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            output = Path(tmp)/'result.json'
            probe = MemberProbe(client, 'https://example.test', 'https://example.test', output, pause=0)
            self.assertTrue(probe.authenticate('PRIVATE_EMAIL', 'PRIVATE_PASSWORD'))
            probe.run()
            saved = output.read_text()
            result = json.loads(saved)
            self.assertTrue(result['passed'])
            self.assertEqual(probe.calls, 37)
            self.assertEqual(methods.count('POST'), 1)
            self.assertTrue(all(len(row['samples']) == 5 for row in result['summary'].values()))
            for secret in ('PRIVATE_TOKEN', 'PRIVATE_EMAIL', 'PRIVATE_PASSWORD', 'PRIVATE_NAME'):
                self.assertNotIn(secret, saved)
            self.assertNotIn('/profiles/7', saved)

    def test_admin_is_rejected_as_member(self):
        def handler(request):
            return httpx.Response(200, json={'authToken': 'private'} if request.method == 'POST'
                                  else dict(id=14, role='admin', account_status='active'))
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            probe = MemberProbe(client, 'https://example.test', 'https://example.test', Path(tmp)/'r.json', pause=0)
            self.assertFalse(probe.authenticate('private', 'private'))
            self.assertIsNone(probe.token)

    def test_library_cross_account_result_fails_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(
                lambda request: httpx.Response(200, json={'profile': {'user_id': 7}}
                    if request.url.path == '/profiles/7' else {'items': [{'user_id': 8}]}))) as client:
            probe = MemberProbe(client, 'https://example.test', 'https://example.test', Path(tmp)/'r.json', pause=0)
            probe.token, probe.owner = 'private', 7
            with self.assertRaisesRegex(RuntimeError, 'contract_check_failed'):
                probe.run()
            self.assertFalse(probe.report['passed'])
