import unittest
from unittest.mock import patch
import httpx

from tools.list_status_contracts import candidate
from tools.list_status_live import Run, PacedClient, PREFIX, route, staged_candidate
from tools.session_revocation import blocks, identity


class ListStatusLiveSafetyTests(unittest.TestCase):
    def test_rehearsal_never_replaces_existing_query_identities(self):
        original_queries = [doc for doc in blocks(candidate()) if route(doc)]
        staged = blocks(staged_candidate())
        queries = [doc for doc in staged if route(doc)]
        self.assertEqual(len(queries), len(original_queries))
        self.assertTrue(all(route(doc)[0].startswith(PREFIX) for doc in queries))
        self.assertFalse({identity(doc) for doc in queries} & {identity(doc) for doc in original_queries})
        self.assertEqual(len({identity(doc) for doc in staged}), len(staged))
        self.assertFalse(any(doc.startswith(('table user_follow', 'table post ')) for doc in staged))

    def test_rollback_after_release_is_refused_before_any_network_call(self):
        run = object.__new__(Run)
        run.journal = {'phase': 'released'}
        with self.assertRaisesRegex(ValueError, 'after writers released'):
            run.rollback_before_release()

    def test_rollback_without_a_known_gated_phase_is_refused(self):
        run = object.__new__(Run)
        run.journal = {}
        with self.assertRaisesRegex(ValueError, 'No cutover phase'):
            run.rollback_before_release()

    def test_metadata_write_is_never_retried_after_rate_limit(self):
        calls = []
        def respond(request):
            calls.append(request.method)
            return httpx.Response(429, json={'code': 'rate_limit'})
        with patch('tools.list_status_live.time.sleep'), PacedClient(transport=httpx.MockTransport(respond)) as client:
            result = client.post('https://example.invalid/api:meta/workspace/1/table', json={})
        self.assertEqual(result.status_code, 429)
        self.assertEqual(calls, ['POST'])

    def test_metadata_read_can_recover_after_rate_limit(self):
        calls = []
        def respond(request):
            calls.append(request.method)
            return httpx.Response(429 if len(calls) == 1 else 200, headers={'Retry-After': '2'}, json=[])
        with patch('tools.list_status_live.time.sleep'), PacedClient(transport=httpx.MockTransport(respond)) as client:
            result = client.get('https://example.invalid/api:meta/workspace/1/table')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(calls, ['GET', 'GET'])
