"""Probe regressions: no application import or remote operations."""
import json
import unittest
from datetime import datetime, timezone
from email.utils import format_datetime

import httpx

from tools.performance_probe import (HttpProbe, demo, retry_after_seconds,
                                    safe_endpoint, service_name)


class ProbeTests(unittest.IsolatedAsyncioTestCase):
    async def test_counts_responses_and_preserves_result(self):
        result = await demo()
        self.assertEqual(result['total_requests'], 2)
        self.assertEqual(result['rate_limited'], 1)
        self.assertEqual(result['statuses'], {'429': 1, '200': 1})
        self.assertEqual(result['validation_layer'], 'simulated')

    async def test_retry_after_is_numeric_and_only_attached_to_429(self):
        responses = iter((
            httpx.Response(429, headers={'Retry-After': '2.2'}),
            httpx.Response(200, headers={'Retry-After': '999'}),
            httpx.Response(429),
            httpx.Response(429, headers={'Retry-After': 'invalid-private-header'}),
        ))
        probe = HttpProbe()
        with probe.capture():
            async with httpx.AsyncClient(
                    transport=httpx.MockTransport(lambda request: next(responses))) as client:
                for _ in range(4):
                    await client.get('https://example.invalid/media')
        self.assertEqual([event['retry_after_seconds'] for event in probe.events],
                         [3, None, None, None])
        self.assertNotIn('invalid-private-header', json.dumps(probe.report()))

    def test_retry_after_http_date_uses_controlled_clock(self):
        now = datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc)
        future = format_datetime(datetime(2026, 10, 28, 12, 0, 8, tzinfo=timezone.utc),
                                 usegmt=True)
        past = format_datetime(datetime(2026, 10, 28, 11, 59, 58, tzinfo=timezone.utc),
                               usegmt=True)
        self.assertEqual(retry_after_seconds(future, now=now), 8)
        self.assertEqual(retry_after_seconds(past, now=now), 1)
        self.assertIsNone(retry_after_seconds(None, now=now))
        self.assertIsNone(retry_after_seconds('NaN', now=now))
        self.assertIsNone(retry_after_seconds('not a date', now=now))

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
                    lambda request: httpx.Response(429, headers={'Retry-After': '4'}))) as client:
                for _ in range(3):
                    await client.get('https://example.invalid/media')
        self.assertEqual(probe.report()['total_requests'], 3)
        self.assertEqual(probe.report()['rate_limited'], 3)
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
