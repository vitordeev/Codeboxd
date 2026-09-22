import unittest
from unittest.mock import AsyncMock, patch
import reflex as rx
from Codeboxd_main.state.social import SocialState
from Codeboxd_main.services import catalog


class DiscoveryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))

    async def drain(self, events):
        return [event async for event in events]

    async def test_text_search_ignores_every_selected_category(self):
        for kind in catalog.TYPES:
            with self.subTest(kind=kind):
                self.state.search_type = kind
                with patch.object(catalog, 'search', new=AsyncMock(return_value=([], []))) as search:
                    await self.drain(self.state.search({'query': 'Batman', 'kind': kind}))
                search.assert_awaited_once_with('Batman', 'all')
                self.assertTrue(self.state.search_active)
                self.assertFalse(self.state.has_more_results)

    async def test_category_browse_then_text_search_is_global(self):
        with patch.object(catalog, 'search', new=AsyncMock(return_value=([], []))) as search:
            await self.drain(self.state.browse_category('anime'))
            search.assert_awaited_with('', 'anime')
            await self.drain(self.state.search({'query': 'Dune'}))
            search.assert_awaited_with('Dune', 'all')

    async def test_pagination_uses_submitted_query_and_deduplicates(self):
        first = catalog.media('tmdb', 'movie', '1', 'Batman')
        second = catalog.media('tmdb', 'series', '2', 'Batman TV')
        with patch.object(catalog, 'search', new=AsyncMock(side_effect=[([first], []), ([first, second], []), ([], [])])) as search:
            await self.drain(self.state.search({'query': 'Batman'}))
            self.state.update_search_term('unsent draft')
            await self.drain(self.state.more_results())
            search.assert_awaited_with('Batman', 'all', 2)
            self.assertEqual(len(self.state.search_results), 2)
            await self.drain(self.state.more_results())
            self.assertFalse(self.state.has_more_results)

    async def test_home_keeps_full_popular_page_and_retries_missing_shelf(self):
        items = [catalog.media('tmdb', 'movie', str(i), 'Movie') for i in range(20)]
        with patch.object(SocialState, '_validate_session', new=AsyncMock()), patch.object(SocialState, '_load_media', new=AsyncMock()), patch.object(catalog, 'search', new=AsyncMock(side_effect=[(items, []), ([], ['Series unavailable'])])):
            await self.state.load_home()
        self.assertEqual(len(self.state.popular_movies), 20)
        with patch.object(SocialState, '_validate_session', new=AsyncMock()), patch.object(SocialState, '_load_media', new=AsyncMock()), patch.object(catalog, 'search', new=AsyncMock(return_value=([catalog.media('tmdb', 'series', '1', 'Series')], []))) as search:
            await self.state.load_home()
        search.assert_awaited_once_with('', 'series')
        self.assertEqual(len(self.state.popular_series), 1)

    async def test_failed_cover_is_recorded_once(self):
        self.state.cover_failed('https://example.com/missing.jpg')
        self.state.cover_failed('https://example.com/missing.jpg')
        self.assertEqual(len(self.state.failed_covers), 1)

    async def test_failed_provider_keeps_cached_results_across_categories(self):
        self.state._media = {'1': dict(catalog.media('openlibrary', 'book', 'OL1W', 'Batman'), id=1)}
        with patch.object(catalog, 'search', new=AsyncMock(return_value=([], ['Anime unavailable']))), patch.object(SocialState, '_call', new=AsyncMock(return_value={'items': []})):
            await self.drain(self.state.search({'query': 'Batman', 'kind': 'movie'}))
        self.assertEqual(self.state.search_results[0]['kind'], 'Livro')
        self.assertTrue(self.state.has_more_results)

    async def test_more_popular_appends_below_and_preserves_other_section(self):
        from Codeboxd_main.state.social import present_media
        first=catalog.media('tmdb','movie','1','First')
        second=catalog.media('tmdb','movie','2','Second')
        self.state.popular_movies=[present_media(first)]
        self.state.popular_series=[{'key':'series:1','title':'Series'}]
        with patch.object(catalog,'search',new=AsyncMock(side_effect=[([first,second],[]),([],[])])) as search:
            await self.drain(self.state.more_popular('movie'))
            search.assert_awaited_with('','movie',2)
            self.assertEqual(len(self.state.popular_movies),2)
            self.assertEqual(self.state.popular_series[0]['title'],'Series')
            await self.drain(self.state.more_popular('movie'))
            self.assertIn('movie',self.state.popular_exhausted)
        self.assertFalse(self.state.busy)

    async def test_popular_provider_failure_keeps_page_for_retry(self):
        with patch.object(catalog,'search',new=AsyncMock(return_value=([],['Unavailable']))) as search:
            await self.drain(self.state.more_popular('movie'))
            await self.drain(self.state.more_popular('movie'))
            self.assertEqual([c.args for c in search.await_args_list],[('', 'movie',2),('', 'movie',2)])
        self.assertNotIn('movie',self.state.popular_exhausted)


if __name__ == '__main__':
    unittest.main()
