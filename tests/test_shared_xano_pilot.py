import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx

import tools.shared_xano_pilot as pilot_module
from tools.shared_xano_pilot import (Pilot, Stop, validate_minimum_write_interval,
                                     validate_review_window, baseline_drift,
                                     run_has_prior_write)


class PilotRateLimitTests(unittest.TestCase):
    def test_minimum_write_interval_is_bounded_and_rejects_boolean(self):
        self.assertEqual(validate_minimum_write_interval(10), 10.0)
        self.assertEqual(validate_minimum_write_interval(60), 60.0)
        for value in (True, 1.25, 9.99, 60.01, '10'):
            with self.subTest(value=value), self.assertRaises(Stop):
                validate_minimum_write_interval(value)

    def test_review_window_accepts_exact_30_minutes_and_rejects_expiry(self):
        self.assertTrue(validate_review_window(100, 1900, now=101))
        for created, expires, now in ((100, 1901, 101), (100, 1900, 1900),
                                      (True, 110, 105), (100, 101, 101)):
            with self.subTest(created=created, expires=expires, now=now), self.assertRaises(Stop):
                validate_review_window(created, expires, now=now)

    def test_baseline_drift_ignores_audit_growth_but_detects_domain_changes(self):
        approved = {'user': {'1': 'old'}, 'event_log': {'2': 'old'}}
        current = {'user': {'1': 'old'}, 'event_log': {'2': 'new'}}
        self.assertEqual(baseline_drift(approved, current), [])
        current['user'] = {'1': 'changed'}
        self.assertEqual(baseline_drift(approved, current), ['user'])

    def test_existing_write_receipt_blocks_reusing_a_run_id(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'pilot-execution-partial.json'
            receipt.write_text(json.dumps({'run_id': 'cbshared_012345abcdef',
                                           'remote_writes': 0, 'write_attempts': []}),
                               encoding='utf-8')
            self.assertFalse(run_has_prior_write(directory, 'cbshared_012345abcdef'))
            receipt.write_text(json.dumps({'run_id': 'cbshared_012345abcdef',
                                           'remote_writes': 1, 'write_attempts': [{'state': 'accepted'}]}),
                               encoding='utf-8')
            self.assertTrue(run_has_prior_write(directory, 'cbshared_012345abcdef'))

    def test_429_receipt_records_only_safe_rate_headers_without_retry(self):
        requests = []

        def respond(request):
            requests.append(request)
            return httpx.Response(
                429,
                headers={
                    'Retry-After': '12',
                    'X-RateLimit-Limit': '5',
                    'X-RateLimit-Remaining': '0',
                    'Set-Cookie': 'session=private-token',
                },
                json={'error': 'private response detail'},
            )

        client = httpx.Client(transport=httpx.MockTransport(respond))
        self.addCleanup(client.close)
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'receipt.json'
            pilot = Pilot(client, 'https://auth.invalid', 'https://social.invalid', receipt,
                          '', 0, 'admin@example.invalid', 10, Path(directory) / 'baseline.json')
            response = pilot.call('PUT', 'https://social.invalid/lists/1', 'test-token',
                                  json_body={'is_public': False}, write=True,
                                  label='privatize_default')
            saved = json.loads(receipt.read_text(encoding='utf-8'))

        self.assertEqual(response.status_code, 429)
        self.assertEqual(len(requests), 1)
        attempt = saved['write_attempts'][0]
        self.assertEqual(attempt['http_status'], 429)
        self.assertEqual(attempt['rate_limit_headers'], {
            'retry-after': '12',
            'x-ratelimit-limit': '5',
            'x-ratelimit-remaining': '0',
        })
        self.assertNotIn('response body', json.dumps(saved).casefold())
        self.assertNotIn('private-token', json.dumps(saved))
        self.assertNotIn('test-token', json.dumps(saved))

    def test_validation_checks_ownership_privacy_persistence_and_rejection(self):
        run = 'cbshared_012345abcdef'
        public = {'id': 119, 'user_id': 48, 'title': run+' public',
                  'description': run, 'is_public': True}
        private = {'id': 120, 'user_id': 48, 'title': run+' private',
                   'description': run, 'is_public': False}
        state = {'public': public.copy(), 'private': private.copy()}
        requests = []

        def respond(request):
            requests.append(request)
            token = request.headers.get('Authorization')
            if request.method == 'GET' and request.url.path.endswith('/lists/public'):
                rows = [state['public'].copy()] if state['public']['is_public'] else []
                return httpx.Response(200, json={'items': rows})
            if request.method == 'GET' and request.url.path.endswith('/lists'):
                rows = list(state.values()) if token == 'Bearer owner-a' else []
                return httpx.Response(200, json={'items': rows})
            if request.method == 'PUT' and request.url.path.endswith('/lists/119'):
                if token == 'Bearer owner-b':
                    return httpx.Response(403, json={'error': 'forbidden'})
                state['public'].update(request.read() and json.loads(request.content))
                return httpx.Response(200, json=state['public'])
            return httpx.Response(404, json={})

        client = httpx.Client(transport=httpx.MockTransport(respond))
        self.addCleanup(client.close)
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(pilot_module, 'RUN', run), \
             patch.object(pilot_module.time, 'monotonic', side_effect=[100, 101, 110]), \
             patch.object(pilot_module.time, 'sleep') as sleep:
            receipt = Path(directory) / 'receipt.json'
            pilot = Pilot(client, 'https://auth.invalid', 'https://social.invalid', receipt,
                          '', 0, 'admin@example.invalid', 10, Path(directory) / 'baseline.json')
            pilot.state['fixtures'] = {
                'custom': {'public': {'id': 119, 'user_id': 48, 'is_public': True},
                           'private': {'id': 120, 'user_id': 48, 'is_public': False}}
            }
            pilot.validate({'a': {'id': 48, 'token': 'owner-a'},
                            'b': {'id': 49, 'token': 'owner-b'}},
                           {'public': {'id': 119}, 'private': {'id': 120}})
            saved = json.loads(receipt.read_text(encoding='utf-8'))

        self.assertFalse(state['public']['is_public'])
        self.assertEqual(saved['remote_writes'], 2)
        self.assertEqual([item['state'] for item in saved['write_attempts']],
                         ['expected_rejection', 'accepted'])
        self.assertEqual(len(saved['checks']), 4)
        sleep.assert_called_once_with(9.0)
        self.assertTrue(all(request.headers['x-data-source'] == 'live' for request in requests))


if __name__ == '__main__':
    unittest.main()
