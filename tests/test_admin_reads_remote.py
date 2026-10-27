import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

import httpx

from tools.admin_reads_remote import Probe, UserSearchProbe, login_server, no_secrets, page_contract


class AdminReadProbeTests(unittest.TestCase):
    def test_search_diagnostic_distinguishes_omitted_id_without_exporting_terms(self):
        calls = []
        def handler(request):
            calls.append(request)
            params = request.url.params
            items = [] if 'user_id' not in params else [dict(id=14, name='PRIVATE NAME',
                username='PRIVATE_USERNAME', role='admin', account_status='active')]
            return httpx.Response(200, json=dict(items=items, total=len(items), page=1,
                per_page=1, next_page=None))
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            output = Path(tmp)/'report.json'
            probe = UserSearchProbe(client, 'https://example.test', 'https://example.test', output, pause=0)
            probe.token = 'PRIVATE_TOKEN'
            probe.run()
            result = json.loads(output.read_text())
            self.assertTrue(result['passed'])
            self.assertFalse(result['search_acceptance_passed'])
            comparisons = {row['scenario']: row for row in result['comparisons']}
            self.assertEqual(comparisons['omitted']['total'], 0)
            self.assertEqual(comparisons['zero_id']['total'], 1)
            self.assertEqual(comparisons['username_all_defaults']['matching_count'], 1)
            self.assertEqual(len(calls), 9)
            self.assertTrue(all(request.method == 'GET' for request in calls))
            self.assertNotIn('PRIVATE', output.read_text())

    def test_search_diagnostic_aborts_when_known_account_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=dict(items=[], total=0, page=1,
                per_page=1, next_page=None)))) as client:
            probe = UserSearchProbe(client, 'https://example.test', 'https://example.test',
                Path(tmp)/'report.json', pause=0)
            probe.token = 'private-token'
            with self.assertRaisesRegex(RuntimeError, 'contract_check_failed'):
                probe.run()
            self.assertFalse(probe.report['passed'])
            self.assertEqual(probe.calls, 1)

    def test_disconnected_browser_does_not_turn_response_into_login_failure(self):
        server, _, _ = login_server(None)
        try:
            for stage in ('end_headers', 'write'):
                for error in (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    with self.subTest(stage=stage, error=error):
                        handler = object.__new__(server.RequestHandlerClass)
                        handler.send_response = Mock()
                        handler.send_header = Mock()
                        handler.end_headers = Mock(side_effect=error if stage == 'end_headers' else None)
                        handler.wfile = Mock()
                        if stage == 'write': handler.wfile.write.side_effect = error
                        handler.reply(200, 'Login confirmado')
        finally:
            server.server_close()

    def test_pagination_rejects_unpaged_or_invalid_metadata(self):
        valid = dict(items=[{'id': 1}], total=2, page=1, per_page=1, next_page=2)
        self.assertTrue(page_contract(valid))
        for invalid in ([], dict(valid, next_page=1), dict(valid, total=-1),
                        dict(valid, items=[{}, {}]), dict(valid, page=2)):
            self.assertFalse(page_contract(invalid))

    def test_secrets_checked_recursively(self):
        self.assertTrue(no_secrets({'items': [{'id': 14, 'name': 'Example'}]}))
        for key in ('password', 'authToken', 'token', 'email'):
            self.assertFalse(no_secrets({'items': [{key: 'private'}]}))

    def test_only_approved_active_admin_can_start(self):
        for user in (dict(id=14, role='member', account_status='active'),
                     dict(id=15, role='admin', account_status='active'),
                     dict(id=14, role='admin', account_status='disabled'),
                     dict(id=14, role='admin', account_status='active')):
            def handler(request):
                data = {'authToken': 'private-token'} if request.method == 'POST' else user
                return httpx.Response(200, json=data)
            with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
                probe = Probe(client, 'https://example.test/auth', 'https://example.test/social',
                              Path(tmp)/'report.json', pause=0)
                expected = user == dict(id=14, role='admin', account_status='active')
                self.assertEqual(probe.authenticate('private-email', 'private-password'), expected)
                self.assertEqual(bool(probe.token), expected)

    def test_rate_limit_stops_without_retry(self):
        calls = []
        def handler(request):
            calls.append(request)
            return httpx.Response(429, headers={'Retry-After': '30'})
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            probe = Probe(client, 'https://example.test', 'https://example.test', Path(tmp)/'r.json', pause=0)
            probe.token = 'private-token'
            with self.assertRaisesRegex(RuntimeError, 'remote_rate_limit'):
                probe.run()
            self.assertEqual(len(calls), 1)
            self.assertEqual(probe.report['retry_after_seconds'], 30)

    def test_result_does_not_export_returned_payload(self):
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(
                lambda request: httpx.Response(200, json={'password': 'never-export'}))) as client:
            output = Path(tmp)/'report.json'
            probe = Probe(client, 'https://example.test', 'https://example.test', output, pause=0)
            probe.token = 'private-token'
            with self.assertRaises(RuntimeError):
                probe.run()
            saved = output.read_text()
            self.assertNotIn('never-export', saved)
            self.assertNotIn('private-token', saved)
            self.assertFalse(json.loads(saved)['passed'])

    def test_login_server_binds_loopback_and_uses_random_path(self):
        first, path, ready = login_server(None)
        second, another, _ = login_server(None)
        try:
            self.assertEqual(first.server_address[0], '127.0.0.1')
            self.assertNotEqual(path, another)
            self.assertFalse(ready.is_set())
        finally:
            first.server_close()
            second.server_close()

    def test_read_journey_exports_only_checks(self):
        calls = []
        def handler(request):
            calls.append((request.method, request.url.path))
            params = request.url.params
            if params.get('role') == 'invalid' or params.get('account_status') == 'invalid':
                return httpx.Response(400, json={'message': 'Invalid filter'})
            if request.url.path.endswith('/dashboard'):
                return httpx.Response(200, json=dict(users_total=1, posts_total=0,
                                                     media_total=0, reports_pending=0))
            items = []
            if request.url.path.endswith('/users') and not params.get('search', '').startswith('cbnomatch_'):
                if params.get('role', 'admin') == 'admin' and params.get('account_status', 'active') == 'active':
                    items = [dict(id=14, name='PRIVATE DISPLAY NAME', username='private_username', role='admin',
                                  account_status='active')]
            return httpx.Response(200, json=dict(items=items, total=len(items), page=1,
                                                  per_page=1, next_page=None))
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            output = Path(tmp)/'report.json'
            probe = Probe(client, 'https://example.test', 'https://example.test', output, pause=0)
            probe.token = 'private-token'
            probe.run()
            result = json.loads(output.read_text())
            self.assertTrue(result['passed'])
            self.assertTrue(all(x['passed'] for x in result['checks']))
            self.assertTrue(all(method == 'GET' for method, _ in calls))
            self.assertNotIn('PRIVATE DISPLAY NAME', output.read_text())
            self.assertNotIn('private_username', output.read_text())
            self.assertEqual(len(result['requests']), len(calls))
            self.assertTrue(all(row['duration_ms'] >= 0 for row in result['requests']))
            self.assertTrue(all(set(row) == {'method', 'endpoint', 'status', 'duration_ms'}
                                for row in result['requests']))

    def test_user_search_rejects_unrelated_results_without_exporting_search(self):
        def handler(request):
            return httpx.Response(200, json=dict(items=[dict(id=99, name='Unrelated',
                username='someone_else')], total=1, page=1, per_page=1, next_page=None))
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            output = Path(tmp)/'report.json'
            probe = Probe(client, 'https://example.test', 'https://example.test', output, pause=0)
            probe.token = 'private-token'
            with self.assertRaisesRegex(RuntimeError, 'contract_check_failed'):
                probe.user_filters({'items': [dict(username='private_search', name='Private Name')]})
            self.assertNotIn('private_search', output.read_text())
            self.assertNotIn('someone_else', output.read_text())
            self.assertFalse(probe.report['checks'][-1]['passed'])

    def test_combined_user_filters_cannot_succeed_with_empty_result(self):
        def handler(request):
            params = request.url.params
            if params.get('user_id'):
                items = []
            elif params.get('account_status') == 'disabled':
                items = [dict(id=15, account_status='disabled')]
            else:
                items = [dict(id=14, username='example', name='Example', account_status='active')]
            return httpx.Response(200, json=dict(items=items, total=len(items), page=1,
                per_page=1, next_page=None))
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            probe = Probe(client, 'https://example.test', 'https://example.test', Path(tmp)/'r.json', pause=0)
            probe.token = 'private-token'
            with self.assertRaisesRegex(RuntimeError, 'contract_check_failed'):
                probe.user_filters({'items': [dict(username='example', name='Example')]})
            self.assertEqual(probe.report['checks'][-1]['scenario'], 'users_combined_matches')
