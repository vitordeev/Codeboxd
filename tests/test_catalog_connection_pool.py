import asyncio
import unittest
from unittest.mock import patch

import httpx

from Codeboxd_main.services import catalog
from Codeboxd_main.services.api import APIError


class CatalogConnectionPoolTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.original = httpx.AsyncClient
        self.clients, self.requests = [], []

    def factory(self, *args, **kwargs):
        def respond(request):
            self.requests.append(request)
            return httpx.Response(200, json={'ok': True}, headers={'Set-Cookie': 'private=fixture; Path=/'})
        kwargs['transport'] = httpx.MockTransport(respond)
        client = self.original(*args, **kwargs)
        self.clients.append(client)
        return client

    async def test_lifespan_reuses_client_closes_once_and_does_not_store_cookies_or_auth(self):
        with patch.object(catalog.httpx, 'AsyncClient', side_effect=self.factory):
            async with catalog.catalog_connection_pool():
                await catalog.fetch('https://provider.test/one', headers={'Authorization': 'Bearer fixture-secret'})
                await catalog.fetch('https://provider.test/two')
                await catalog.fetch('https://other.test/three')
                self.assertEqual(len(self.clients), 1)
                self.assertFalse(self.clients[0].is_closed)
                self.assertFalse(self.clients[0].cookies)
            self.assertTrue(self.clients[0].is_closed)
            self.assertNotIn(asyncio.get_running_loop(), catalog._connection_clients)
        self.assertEqual(self.requests[0].headers['Authorization'], 'Bearer fixture-secret')
        self.assertNotIn('Authorization', self.requests[1].headers)
        self.assertNotIn('Authorization', self.requests[2].headers)
        self.assertTrue(all('Cookie' not in request.headers for request in self.requests))

    async def test_standalone_fallback_closes_a_client_for_each_call(self):
        with patch.object(catalog.httpx, 'AsyncClient', side_effect=self.factory):
            await catalog.fetch('https://provider.test/one')
            await catalog.fetch('https://provider.test/two')
        self.assertEqual(len(self.clients), 2)
        self.assertTrue(all(client.is_closed for client in self.clients))

    async def test_concurrent_requests_share_transport_without_deduplicating_distinct_reads(self):
        with patch.object(catalog.httpx, 'AsyncClient', side_effect=self.factory):
            async with catalog.catalog_connection_pool():
                await asyncio.gather(*(catalog.fetch(f'https://provider.test/{i}') for i in range(10)))
        self.assertEqual(len(self.clients), 1)
        self.assertEqual(len(self.requests), 10)

    async def test_failed_request_does_not_close_pool_or_cache_error(self):
        calls = 0
        def factory(*args, **kwargs):
            def respond(request):
                nonlocal calls
                calls += 1
                return httpx.Response(403 if calls == 1 else 200, json={'ok': True})
            kwargs['transport'] = httpx.MockTransport(respond)
            return self.original(*args, **kwargs)
        with patch.object(catalog.httpx, 'AsyncClient', side_effect=factory):
            async with catalog.catalog_connection_pool():
                with self.assertRaises(APIError):
                    await catalog.fetch('https://provider.test/retry', cache=True)
                self.assertEqual(await catalog.fetch('https://provider.test/retry', cache=True), {'ok': True})
        self.assertEqual(calls, 2)

    async def test_cancelled_lifespan_closes_transport(self):
        started, release = asyncio.Event(), asyncio.Event()
        async def worker():
            async with catalog.catalog_connection_pool():
                started.set()
                await release.wait()
        with patch.object(catalog.httpx, 'AsyncClient', side_effect=self.factory):
            task = asyncio.create_task(worker())
            await started.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(self.clients[0].is_closed)
        self.assertNotIn(asyncio.get_running_loop(), catalog._connection_clients)

    async def test_nested_lifespan_rejected_without_closing_owner(self):
        with patch.object(catalog.httpx, 'AsyncClient', side_effect=self.factory):
            async with catalog.catalog_connection_pool():
                with self.assertRaises(RuntimeError):
                    async with catalog.catalog_connection_pool():
                        pass
                self.assertFalse(self.clients[0].is_closed)
        self.assertEqual(len(self.clients), 1)

    async def test_other_event_loop_cannot_obtain_current_client(self):
        async def another_loop():
            await catalog.fetch('https://provider.test/other-loop')
        with patch.object(catalog.httpx, 'AsyncClient', side_effect=self.factory):
            async with catalog.catalog_connection_pool():
                await asyncio.to_thread(lambda: asyncio.run(another_loop()))
                await catalog.fetch('https://provider.test/owner-loop')
                self.assertFalse(self.clients[0].is_closed)
                self.assertTrue(self.clients[1].is_closed)
        self.assertEqual(len(self.clients), 2)
