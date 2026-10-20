"""Cache isolation and progressive home updates without real network calls."""
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import httpx
import reflex as rx

from Codeboxd_main.services import catalog
from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class HomePerformanceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        catalog._public_cache.clear()
        self.addCleanup(catalog._public_cache.clear)

    async def test_cache_expires_and_returns_independent_copies(self):
        client = AsyncMock()
        client.get.return_value = httpx.Response(200, json={'results': [{'id': 1}]},
            request=httpx.Request('GET', 'https://provider.example/list'))
        context = AsyncMock()
        context.__aenter__.return_value = client
        with patch.object(catalog.httpx, 'AsyncClient', return_value=context):
            first = await catalog.fetch('https://provider.example/list', cache=True)
            first['results'].clear()
            second = await catalog.fetch('https://provider.example/list', cache=True)
            self.assertEqual(second['results'], [{'id': 1}])
            self.assertEqual(client.get.await_count, 1)
            key = next(iter(catalog._public_cache))
            catalog._public_cache[key] = (catalog.time.monotonic() - 301, second)
            await catalog.fetch('https://provider.example/list', cache=True)
            self.assertEqual(client.get.await_count, 2)

    async def test_cache_does_not_cross_credentials_or_cache_errors(self):
        client = AsyncMock()
        request = httpx.Request('GET', 'https://provider.example/list')
        client.get.side_effect = [httpx.Response(403, request=request),
                                 httpx.Response(200, json={'ok': True}, request=request),
                                 httpx.Response(200, json={'ok': True}, request=request)]
        context = AsyncMock()
        context.__aenter__.return_value = client
        with patch.object(catalog.httpx, 'AsyncClient', return_value=context):
            with self.assertRaises(APIError):
                await catalog.fetch('https://provider.example/list', cache=True, headers={'Authorization': 'test-a'})
            self.assertFalse(catalog._public_cache)
            await catalog.fetch('https://provider.example/list', cache=True, headers={'Authorization': 'test-a'})
            await catalog.fetch('https://provider.example/list', cache=True, headers={'Authorization': 'test-b'})
            self.assertEqual(client.get.await_count, 3)

    async def test_home_yields_content_before_slow_collections_finish(self):
        state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        gate = asyncio.Event()
        async def slow_collection(key):
            await gate.wait()
            return []
        movie = catalog.media('tmdb', 'movie', '1', 'Já disponível')
        with patch.object(SocialState, '_validate_session', new=AsyncMock()), \
                patch.object(SocialState, '_load_media', new=AsyncMock()), \
                patch.object(catalog, 'series_highlights', new=AsyncMock(return_value=[])), \
                patch.object(catalog, 'home_collection', side_effect=slow_collection), \
                patch.object(catalog, 'search', new=AsyncMock(return_value=([movie], []))):
            updates = state._home_updates()
            try:
                await asyncio.wait_for(anext(updates), timeout=1)
                self.assertEqual(state.featured_items[0]['title'], 'Já disponível')
                self.assertFalse(state.home_loaded)
                gate.set()
                async for _ in updates:
                    pass
                self.assertTrue(state.home_loaded)
            finally:
                gate.set()
                await updates.aclose()
