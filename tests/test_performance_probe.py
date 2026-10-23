"""Probe regressions: no application import or remote operations."""
import json
import unittest

import httpx

from tools.performance_probe import HttpProbe, demo, safe_endpoint, service_name


class ProbeTests(unittest.IsolatedAsyncioTestCase):
    async def test_counts_responses_and_preserves_result(self):
        result = await demo()
        self.assertEqual(result['total_requests'], 2)
        self.assertEqual(result['rate_limited'], 1)
        self.assertEqual(result['statuses'], {'429': 1, '200': 1})
        self.assertEqual(result['validation_layer'], 'simulated')

    async def test_secrets_and_identifiers_are_not_exported(self):
        async def handler(request):
            return httpx.Response(200, json={'password': 'body-secret'})
        probe = HttpProbe()
        with probe.capture():
            async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
                response = await client.post(
                    'https://private-host.invalid/profiles/alice-private?email=private-email',
                    headers={'Authorization': 'Bearer private-token'},
                    json={'password': 'private-password'})
                self.assertEqual(response.json(), {'password': 'body-secret'})
        output = json.dumps(probe.report())
        for secret in ('private-host', 'alice-private', 'private-email',
                       'private-token', 'private-password', 'body-secret'):
            self.assertNotIn(secret, output)
        self.assertEqual(probe.events[0]['endpoint'], '/profiles/{value}')

    async def test_network_errors_propagate_without_message_export(self):
        async def fail(request):
            raise httpx.ConnectError('sensitive-detail', request=request)
        probe = HttpProbe()
        with probe.capture():
            async with httpx.AsyncClient(transport=httpx.MockTransport(fail)) as client:
                with self.assertRaises(httpx.ConnectError):
                    await client.get('https://example.invalid/auth/me')
        self.assertEqual(probe.events[0]['outcome'], 'network-error')
        self.assertNotIn('sensitive-detail', json.dumps(probe.report()))

    async def test_event_limit_keeps_aggregate_counts(self):
        probe = HttpProbe(max_events=1)
        with probe.capture():
            async with httpx.AsyncClient(transport=httpx.MockTransport(
                    lambda request: httpx.Response(200))) as client:
                for _ in range(3):
                    await client.get('https://example.invalid/media')
        self.assertEqual(probe.report()['total_requests'], 3)
        self.assertEqual(probe.report()['dropped_events'], 2)

    async def test_patch_restored_even_after_failure(self):
        original = httpx.AsyncClient.send
        with self.assertRaises(ValueError):
            with HttpProbe().capture():
                raise ValueError('test')
        self.assertIs(httpx.AsyncClient.send, original)

    def test_service_names_do_not_expose_host_and_routes_hide_ids(self):
        self.assertEqual(service_name('https://instance.xano.io/api:private/media'), 'xano')
        self.assertEqual(service_name('https://api.themoviedb.org/3/movie/42'), 'tmdb')
        self.assertEqual(service_name('https://xano.io.attacker.invalid'), 'other')
        self.assertEqual(service_name('https://kitsu.app/api/edge/anime'), 'kitsu')
        self.assertEqual(service_name('https://kitsu.io/api/edge/anime'), 'kitsu')
        self.assertEqual(service_name('https://kitsu.app.attacker.invalid'), 'other')
        self.assertEqual(safe_endpoint('https://host/api:private/media/42?token=secret'),
                         '/{value}/media/{value}')
