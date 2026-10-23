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

    async def test_cold_concurrent_reads_share_one_request_in_five_samples(self):
        for sample in range(5):
            catalog._public_cache.clear()
            calls = []
            async def respond(url, **kwargs):
                calls.append(url)
                await asyncio.sleep(0.01)
                return httpx.Response(200, json={'results': [{'id': sample}]},
                                      request=httpx.Request('GET', url))
            client = AsyncMock()
            client.get.side_effect = respond
            context = AsyncMock()
            context.__aenter__.return_value = client
            with patch.object(catalog.httpx, 'AsyncClient', return_value=context):
                await asyncio.gather(*(
                    catalog._fetch_response('https://provider.example/list', cache=True)
                    for _ in range(10)))
                self.assertEqual(len(calls), 10)
                calls.clear()
                catalog._public_cache.clear()
                results = await asyncio.gather(*(
                    catalog.fetch('https://provider.example/list', cache=True)
                    for _ in range(10)))
            self.assertEqual(len(calls), 1)
            results[0]['results'].clear()
            self.assertEqual(results[1]['results'], [{'id': sample}])
            self.assertFalse(catalog._public_pending)

    async def test_partial_failure_preserves_primary_covers_and_series_order(self):
        state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        movie = catalog.media('tmdb', 'movie', '1', 'Popular')
        cinema = catalog.media('tmdb', 'movie', '2', 'Cinema',
                               cover_url='https://images.example/cinema.jpg')
        series = [catalog.media('tmdb', 'series', str(identifier), str(identifier))
                  for identifier in catalog.SERIES_HIGHLIGHTS]
        async def search(query, kind):
            return ([movie] if kind == 'movie' else [series[-1]]), []
        async def shelf(key):
            if key == 'books_fantasy':
                raise APIError('Provider unavailable', 503)
            return [cinema] if key == 'movies_now' else [movie]
        with patch.object(SocialState, '_validate_navigation_session', new=AsyncMock()), \
                patch.object(SocialState, '_load_media', new=AsyncMock()), \
                patch.object(catalog, 'search', side_effect=search), \
                patch.object(catalog, 'series_highlights', new=AsyncMock(return_value=series)), \
                patch.object(catalog, 'home_collection', side_effect=shelf):
            async for _ in state._home_updates():
                pass
        self.assertTrue(state.home_loaded)
        self.assertEqual(state.featured_items[0]['title'], 'Cinema')
        self.assertEqual(state.featured_items[0]['cover'], 'https://images.example/cinema.jpg')
        self.assertEqual([item['external_id'] for item in state.popular_series],
                         [str(identifier) for identifier in catalog.SERIES_HIGHLIGHTS])
        self.assertEqual(state.home_collection_errors, ['books_fantasy'])
        self.assertTrue(state.home_collections['books_fiction'])

    async def test_pending_reads_separate_pages_credentials_and_uncached_calls(self):
        async def respond(*args, **kwargs):
            await asyncio.sleep(0.01)
            return {'ok': True}
        with patch.object(catalog, '_fetch_response', side_effect=respond) as remote:
            await asyncio.gather(*(
                catalog.fetch('https://provider.example/list', cache=True,
                              params={'page': page}, headers={'Authorization': token})
                for page, token in [(1, 'a'), (2, 'a'), (1, 'b')]),
                catalog.fetch('https://provider.example/list'),
                catalog.fetch('https://provider.example/list'))
            self.assertEqual(remote.await_count, 5)
        self.assertFalse(catalog._public_pending)

    async def test_cancelled_consumer_does_not_cancel_shared_read(self):
        started, release = asyncio.Event(), asyncio.Event()
        async def respond(*args, **kwargs):
            started.set()
            await release.wait()
            return {'ok': True}
        with patch.object(catalog, '_fetch_response', side_effect=respond) as remote:
            first = asyncio.create_task(catalog.fetch('https://provider.example/list', cache=True))
            await started.wait()
            second = asyncio.create_task(catalog.fetch('https://provider.example/list', cache=True))
            await asyncio.sleep(0)
            first.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await first
            release.set()
            self.assertEqual(await second, {'ok': True})
            self.assertEqual(remote.await_count, 1)
        self.assertFalse(catalog._public_pending)

    async def test_shared_failure_is_removed_and_next_attempt_reaches_provider(self):
        async def fail(*args, **kwargs):
            await asyncio.sleep(0.01)
            raise APIError('Unavailable', 503)
        with patch.object(catalog, '_fetch_response', side_effect=fail) as remote:
            results = await asyncio.gather(*(
                catalog.fetch('https://provider.example/list', cache=True)
                for _ in range(3)), return_exceptions=True)
            self.assertTrue(all(isinstance(result, APIError) for result in results))
            self.assertEqual(remote.await_count, 1)
            self.assertFalse(catalog._public_pending)
            self.assertFalse(catalog._public_cache)
            with self.assertRaises(APIError):
                await catalog.fetch('https://provider.example/list', cache=True)
            self.assertEqual(remote.await_count, 2)

    async def test_pending_registry_is_bounded_without_dropping_reads(self):
        release = asyncio.Event()
        async def respond(*args, **kwargs):
            await release.wait()
            return {'ok': True}
        with patch.object(catalog, '_fetch_response', side_effect=respond) as remote:
            tasks = [asyncio.create_task(catalog.fetch(
                f'https://provider.example/{index}', cache=True)) for index in range(130)]
            try:
                while remote.await_count < 130:
                    await asyncio.sleep(0)
                self.assertEqual(len(catalog._public_pending), 128)
            finally:
                release.set()
                results = await asyncio.gather(*tasks)
            self.assertEqual(len(results), 130)
            self.assertFalse(catalog._public_pending)
