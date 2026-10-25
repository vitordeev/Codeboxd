import asyncio
import json
import unittest
from unittest.mock import AsyncMock, patch

import httpx

from Codeboxd_main.services import api


class APIConnectionPoolTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.original = httpx.AsyncClient
        self.clients, self.requests = [], []

    def factory(self, *args, **kwargs):
        def respond(request):
            self.requests.append(request)
            if request.headers.get('Authorization') == 'Bearer expired':
                return httpx.Response(401, json={})
            return httpx.Response(200, json={'actor': request.headers.get('Authorization', ''),
                                            'call': len(self.requests)},
                                  headers={'Set-Cookie': 'identity=private; Path=/'})
        kwargs['transport'] = httpx.MockTransport(respond)
        client = self.original(*args, **kwargs)
        self.clients.append(client)
        return client

    async def test_concurrent_accounts_and_guest_keep_authorization_on_each_request(self):
        with patch.object(api.httpx, 'AsyncClient', side_effect=self.factory), \
             patch.object(api, 'base_url', return_value='https://fixture.test'):
            async with api.api_connection_pool():
                results = await asyncio.gather(api.request('GET', '/profile', token='account-a'),
                                               api.request('GET', '/profile', token='account-b'))
                guest = await api.request('GET', '/profile')
                self.assertEqual([row['actor'] for row in results], ['Bearer account-a', 'Bearer account-b'])
                self.assertEqual(guest['actor'], '')
                self.assertFalse(self.clients[0].cookies)
                self.assertEqual(self.clients[0].timeout.connect, 3)
                self.assertEqual(self.clients[0].timeout.read, 10)
        self.assertEqual(len(self.clients), 1)
        self.assertTrue(self.clients[0].is_closed)
        self.assertTrue(all('Cookie' not in request.headers for request in self.requests))
        self.assertNotIn(asyncio.get_running_loop(), api._connection_clients)

    async def test_rejected_token_does_not_affect_next_account_or_cache_response(self):
        with patch.object(api.httpx, 'AsyncClient', side_effect=self.factory), \
             patch.object(api, 'base_url', return_value='https://fixture.test'):
            async with api.api_connection_pool():
                with self.assertRaises(api.APIError) as error:
                    await api.request('GET', '/profile', token='expired')
                self.assertEqual(error.exception.status, 401)
                first = await api.request('GET', '/profile', token='valid')
                second = await api.request('GET', '/profile', token='valid')
                self.assertNotEqual(first['call'], second['call'])
                self.assertEqual(second['actor'], 'Bearer valid')
        self.assertEqual(len(self.requests), 3)

    async def test_groups_payloads_and_methods_are_preserved(self):
        with patch.object(api.httpx, 'AsyncClient', side_effect=self.factory), \
             patch.object(api, 'base_url', side_effect=lambda group: f'https://{group}.test'):
            async with api.api_connection_pool():
                await api.request('GET', '/auth/me', group='auth', token='account-a')
                await api.request('PUT', '/posts/1', token='account-b', data={'body': 'Draft'}, params={'version': 2})
        self.assertEqual(self.requests[0].url.host, 'auth.test')
        self.assertEqual(self.requests[1].url.host, 'social.test')
        self.assertEqual(self.requests[1].method, 'PUT')
        self.assertEqual(json.loads(self.requests[1].content), {'body': 'Draft'})
        self.assertEqual(self.requests[1].url.params['version'], '2')

    async def test_pool_does_not_retry_mutations_or_email_and_keeps_read_retry_bound(self):
        for method, path, group in (('POST', '/posts', 'social'),
                                    ('GET', '/reset/request-reset-link', 'auth'),
                                    ('GET', '/media', 'social')):
            calls = []
            def factory(*args, **kwargs):
                def limited(request):
                    calls.append(request)
                    return httpx.Response(429, headers={'Retry-After': '1'})
                kwargs['transport'] = httpx.MockTransport(limited)
                return self.original(*args, **kwargs)
            with self.subTest(method=method, path=path), \
                 patch.object(api.httpx, 'AsyncClient', side_effect=factory), \
                 patch.object(api, 'base_url', return_value='https://fixture.test'), \
                 patch.object(api.asyncio, 'sleep', new=AsyncMock()):
                async with api.api_connection_pool():
                    with self.assertRaises(api.APIError) as error:
                        await api.request(method, path, group=group)
                self.assertEqual(error.exception.status, 429)
                self.assertEqual(len(calls), 3 if path == '/media' else 1)

    async def test_fallback_keeps_per_request_lifetime(self):
        with patch.object(api.httpx, 'AsyncClient', side_effect=self.factory), \
             patch.object(api, 'base_url', return_value='https://fixture.test'):
            await api.request('GET', '/profile', token='a')
            await api.request('GET', '/profile', token='b')
        self.assertEqual(len(self.clients), 2)
        self.assertTrue(all(client.is_closed for client in self.clients))

    async def test_nested_context_rejected_and_owner_closed_after_exception(self):
        with patch.object(api.httpx, 'AsyncClient', side_effect=self.factory):
            with self.assertRaisesRegex(RuntimeError, 'fixture_exception'):
                async with api.api_connection_pool():
                    with self.assertRaises(RuntimeError):
                        async with api.api_connection_pool():
                            pass
                    self.assertFalse(self.clients[0].is_closed)
                    raise RuntimeError('fixture_exception')
        self.assertTrue(self.clients[0].is_closed)
        self.assertNotIn(asyncio.get_running_loop(), api._connection_clients)

    async def test_different_loops_never_share_client(self):
        async def read():
            await api.request('GET', '/profile')
        with patch.object(api.httpx, 'AsyncClient', side_effect=self.factory), \
             patch.object(api, 'base_url', return_value='https://fixture.test'):
            async with api.api_connection_pool():
                await asyncio.to_thread(lambda: asyncio.run(read()))
                await read()
                self.assertTrue(self.clients[1].is_closed)
                self.assertFalse(self.clients[0].is_closed)
        self.assertEqual(len(self.clients), 2)
