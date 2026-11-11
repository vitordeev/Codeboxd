import asyncio
from contextlib import asynccontextmanager
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx
from reflex.istate.proxy import StateProxy

from Codeboxd_main.services import catalog
from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


async def drain(events):
    return [event async for event in events]


class HomeBackgroundTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.original_load_media = SocialState._load_media
        self.root = rx.State(_reflex_internal_init=True)
        self.root.router.url.path = '/'
        self.state = self.root.get_substate(SocialState.get_full_name().split('.'))
        self.lock = asyncio.Lock()
        @asynccontextmanager
        async def modify(**kwargs):
            async with self.lock:
                yield self.root
        self.context = SimpleNamespace(token='p0-fictional', state_manager=SimpleNamespace(modify_state_with_links=modify),
                                       emit_delta=AsyncMock())
        self.context_patch = patch('reflex.istate.proxy.EventContext.get', return_value=self.context)
        self.context_patch.start(); self.addCleanup(self.context_patch.stop)
        self.proxy = StateProxy(self.state)
        self.movie = catalog.media('tmdb', 'movie', '1', 'Destaque')
        self.gate = asyncio.Event()
        async def collection(key):
            await self.gate.wait()
            return [self.movie]
        self.patches = [patch.object(SocialState, '_validate_navigation_session', new=AsyncMock()),
            patch.object(SocialState, '_load_media', new=AsyncMock()),
            patch.object(catalog, 'search', new=AsyncMock(return_value=([self.movie], []))),
            patch.object(catalog, 'series_highlights', new=AsyncMock(return_value=[])),
            patch.object(catalog, 'home_collection', side_effect=collection)]
        for item in self.patches:
            item.start(); self.addCleanup(item.stop)
        self.jobs = []

    async def asyncTearDown(self):
        self.gate.set()
        for task in self.jobs:
            if not task.done(): task.cancel()
        await asyncio.gather(*self.jobs, return_exceptions=True)

    async def start_home(self):
        events = await drain(self.state.visit('home'))
        self.assertTrue(any(event is not None for event in events))
        self.assertFalse(self.state.busy)
        job = asyncio.create_task(SocialState.load_home_background.fn(
            self.proxy, self.state._home_request_id, self.state._visit_generation))
        self.jobs.append(job)
        async def ready():
            while not self.state.featured_items and not job.done():
                await asyncio.sleep(.001)
        await asyncio.wait_for(ready(), 2)
        if job.done(): await job
        return job

    async def test_search_really_finishes_while_home_provider_is_pending(self):
        job = await self.start_home()
        self.assertTrue(self.state.home_loading)
        self.assertFalse(job.done())
        await drain(self.state.search({'query': 'Destaque'}))
        self.assertTrue(self.state.search_active)
        self.assertEqual(self.state.submitted_query, 'Destaque')
        self.assertEqual(self.state.search_results[0]['title'], 'Destaque')
        self.assertFalse(job.done())
        self.gate.set(); await job
        self.assertTrue(self.state.home_loaded)
        self.assertFalse(self.state.home_loading)
        self.assertTrue(self.state.search_active)
        self.assertGreater(self.context.emit_delta.await_count, 0)

    async def test_finishing_home_cannot_release_pending_search_or_overwrite_its_notice(self):
        job = await self.start_home()
        search_started, search_release = asyncio.Event(), asyncio.Event()
        async def search(*args):
            search_started.set(); await search_release.wait()
            return [self.movie], []
        with patch.object(catalog, 'search', side_effect=search):
            query = asyncio.create_task(drain(self.state.search({'query': 'Batman'})))
            self.jobs.append(query)
            await search_started.wait()
            self.state.notice = 'Aviso da busca atual'
            self.gate.set(); await job
            self.assertTrue(self.state.busy)
            self.assertEqual(self.state.notice, 'Aviso da busca atual')
            search_release.set(); await query
        self.assertFalse(self.state.busy)

    async def test_double_search_submission_does_not_duplicate_query(self):
        home = await self.start_home()
        started, release = asyncio.Event(), asyncio.Event()
        async def search(*args):
            started.set(); await release.wait(); return [self.movie], []
        with patch.object(catalog, 'search', side_effect=search) as request:
            first = asyncio.create_task(drain(self.state.search({'query': 'Batman'})))
            self.jobs.append(first); await started.wait()
            await drain(self.state.search({'query': 'Dune'}))
            self.assertEqual(request.await_count, 1)
            self.assertEqual(self.state.submitted_query, 'Batman')
            release.set(); await first
        self.gate.set(); await home

    async def test_late_home_cannot_publish_after_route_token_or_generation_changes(self):
        # Separate setup per subtest is essential: every run uses a fresh root.
        for changed in ('route', 'token', 'generation'):
            with self.subTest(changed=changed):
                self.gate.clear(); self.root.router.url.path = '/'
                self.state.home_collections = {key: [] for key in catalog.HOME_COLLECTIONS}
                self.state.featured_items = []; self.state.popular_movies = []
                self.state._popular_loaded = []
                job = await self.start_home()
                if changed == 'route': self.root.router.url.path = '/obra/9'
                elif changed == 'token': self.state.session_token = 'new-fictional-session'
                else: self.state._visit_generation += 1
                self.state._home_request_id += 1
                self.state._home_running_id = self.state._home_request_id
                self.state.home_loading = True
                self.state.featured_items = [{'title': 'Current'}]
                self.state.notice = 'Current notice'; self.state.busy = True
                self.gate.set(); await job
                self.assertEqual(self.state.featured_items, [{'title': 'Current'}])
                self.assertEqual(self.state.notice, 'Current notice')
                self.assertTrue(self.state.busy)
                self.assertTrue(self.state.home_loading)
                self.state.busy = False

    async def test_duplicate_background_event_does_not_start_second_provider_batch(self):
        job = await self.start_home()
        before = catalog.home_collection.call_count
        await SocialState.load_home_background.fn(self.proxy, self.state._home_request_id, self.state._visit_generation)
        self.assertEqual(catalog.home_collection.call_count, before)
        self.gate.set(); await job

    async def test_retry_and_more_popular_keep_their_pending_guards(self):
        job = await self.start_home()
        request_id = self.state._home_request_id
        with patch.object(catalog, 'search', new=AsyncMock()) as search:
            self.assertEqual(await drain(self.state.retry_home_collections()), [])
            self.assertEqual(await drain(self.state.more_popular('movie')), [])
            search.assert_not_awaited()
        self.assertEqual(self.state._home_request_id, request_id)
        self.gate.set(); await job

    async def test_partial_failure_retry_preserves_content_and_search_results(self):
        async def shelf(key):
            if key == 'anime_rated': raise APIError('Fictional provider failure', 503)
            return [self.movie]
        with patch.object(catalog, 'home_collection', side_effect=shelf):
            await drain(self.state.visit('home'))
            await SocialState.load_home_background.fn(self.proxy, self.state._home_request_id, self.state._visit_generation)
        self.assertFalse(self.state.home_loading)
        self.assertTrue(self.state.home_loaded)
        self.assertIn('anime_rated', self.state.home_collection_errors)
        self.assertTrue(self.state.home_collections['movies_now'])
        self.state.search_results = [{'title': 'Current search'}]
        before = self.state._home_request_id
        with patch.object(catalog, 'home_collection', new=AsyncMock(return_value=[self.movie])) as fetch:
            await drain(self.state.retry_home_collections())
            self.assertEqual(self.state._home_request_id, before + 1)
            self.assertTrue(self.state.home_loading)
            await SocialState.load_home_background.fn(self.proxy, self.state._home_request_id, self.state._visit_generation)
        fetch.assert_awaited_once_with('anime_rated')
        self.assertNotIn('anime_rated', self.state.home_collection_errors)
        self.assertEqual(self.state.search_results, [{'title': 'Current search'}])

    async def test_home_publication_does_not_overwrite_search_reference_data(self):
        job = await self.start_home()
        self.state._media = {'99': {'id': 99, 'title': 'New reference'}}
        self.state.catalog_items = [{'title': 'New catalog'}]
        self.state.search_results = [{'title': 'New result'}]
        self.gate.set(); await job
        self.assertEqual(self.state._media, {'99': {'id': 99, 'title': 'New reference'}})
        self.assertEqual(self.state.catalog_items, [{'title': 'New catalog'}])
        self.assertEqual(self.state.search_results, [{'title': 'New result'}])

    async def test_old_dispatch_is_ignored_before_any_provider_request(self):
        await drain(self.state.visit('home'))
        with patch.object(catalog, 'search', new=AsyncMock()) as search:
            await SocialState.load_home_background.fn(self.proxy, self.state._home_request_id - 1, self.state._visit_generation)
            search.assert_not_awaited()


    async def test_preparation_does_not_wait_for_community_io(self):
        await drain(self.state.visit('home'))
        SocialState._load_media.assert_not_awaited()
        self.assertFalse(self.state.busy)
        self.assertTrue(self.state.home_loading)
        self.assertTrue(self.state._home_media_pending)

    async def test_search_joins_pending_media_once_and_preserves_saved_results(self):
        started, release = asyncio.Event(), asyncio.Event()
        saved = dict(catalog.media('tmdb', 'movie', '7', 'Saved'), id=7)
        async def request(*args, **kwargs):
            started.set(); await release.wait(); return [saved]
        original = self.original_load_media
        with patch.object(SocialState, '_load_media', new=original), \
                patch('Codeboxd_main.state.social.request', side_effect=request) as transport:
            home = await self.start_home()
            await started.wait()
            with patch.object(catalog, 'search', new=AsyncMock(return_value=([], []))):
                query = asyncio.create_task(drain(self.state.search({'query': 'Saved'})))
                self.jobs.append(query)
                await asyncio.sleep(.02)
                self.assertEqual(transport.await_count, 1)
                self.assertTrue(self.state.busy)
                release.set(); await query
            self.assertEqual(self.state.search_results[0]['title'], 'Saved')
            self.gate.set(); await home
            self.assertEqual(transport.await_count, 1)
            self.assertTrue(self.state._navigation_reads)

    async def test_current_community_401_clears_session_and_pending_flags(self):
        self.state.session_token = 'expired-fictional'
        self.gate.set()
        with patch.object(SocialState, '_load_media', new=self.original_load_media), \
                patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=APIError('Expired', 401))):
            await drain(self.state.visit('home'))
            await SocialState.load_home_background.fn(self.proxy, self.state._home_request_id, self.state._visit_generation)
        self.assertFalse(self.state._token())
        self.assertFalse(self.state.home_loading)
        self.assertFalse(self.state._home_media_pending)


if __name__ == '__main__':
    unittest.main()
