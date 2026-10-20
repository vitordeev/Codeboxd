import unittest
from unittest.mock import AsyncMock, patch
import reflex as rx
from Codeboxd_main.state.social import SocialState
from Codeboxd_main.services import catalog


class DiscoveryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        collections = patch.object(catalog, 'home_collection', new=AsyncMock(return_value=[]))
        self.collection_fetch = collections.start()
        self.addCleanup(collections.stop)
        highlights = patch.object(catalog, 'series_highlights', new=AsyncMock(return_value=[]))
        self.highlights_fetch = highlights.start()
        self.addCleanup(highlights.stop)

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

    async def test_categories_keep_saved_works_when_provider_is_unavailable(self):
        saved = [dict(catalog.media('tmdb', 'movie', '11', 'Filme salvo'), id=1),
                 dict(catalog.media('tmdb', 'series', '22', 'Série salva'), id=2),
                 dict(catalog.media('openlibrary', 'book', 'OL1W', 'Livro salvo'), id=3)]
        for kind in ['movie', 'series', 'book']:
            with self.subTest(kind=kind), \
                    patch.object(catalog, 'search', new=AsyncMock(return_value=([], ['Indisponível']))), \
                    patch.object(SocialState, '_call', new=AsyncMock(return_value=saved)):
                await self.drain(self.state.browse_category(kind))
                self.assertEqual(len(self.state.search_results), 1)
                self.assertEqual(self.state._results[self.state.search_results[0]['key']]['media_type'], kind)

    async def test_home_restores_saved_movies_and_series_without_external_results(self):
        self.state._media = {
            '1': dict(catalog.media('tmdb', 'movie', '11', 'Filme salvo'), id=1),
            '2': dict(catalog.media('tmdb', 'series', '22', 'Série salva'), id=2),
        }
        with patch.object(SocialState, '_validate_session', new=AsyncMock()), \
                patch.object(SocialState, '_load_media', new=AsyncMock()), \
                patch.object(catalog, 'search', new=AsyncMock(return_value=([], ['Indisponível']))):
            await self.state.load_home()
        self.assertEqual(self.state.popular_movies[0]['title'], 'Filme salvo')
        self.assertEqual(self.state.popular_series[0]['title'], 'Série salva')
        self.assertEqual(self.state.featured_items, self.state.popular_movies[:2])

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

    async def test_home_collections_keep_other_providers_when_one_fails(self):
        from Codeboxd_main.services.api import APIError
        async def provider(key):
            if key == 'books_fantasy': raise APIError('Unavailable')
            kind=catalog.HOME_COLLECTIONS[key][0]
            return [catalog.media('test',kind,key,'A story')]
        self.collection_fetch.side_effect=provider
        await self.state._load_home_collections()
        self.assertEqual(self.state.home_collection_errors,['books_fantasy'])
        self.assertEqual(self.state.home_collections['books_fiction'][0]['kind'],'Livro')
        self.assertEqual(self.state.home_collections['anime_rated'][0]['kind'],'Anime')
        self.collection_fetch.reset_mock()
        self.collection_fetch.side_effect=None
        self.collection_fetch.return_value=[catalog.media('openlibrary','book','OL1W','Fantasy')]
        await self.state._load_home_collections()
        self.collection_fetch.assert_awaited_once_with('books_fantasy')
        self.assertEqual(self.state.home_collection_errors,[])

    def test_return_to_home_clears_search_without_losing_collections(self):
        self.state.search_active=True
        self.state.search_term='Batman'
        self.state.submitted_query='Batman'
        self.state.home_collections['books_fiction']=[{'title':'Dune'}]
        self.state.show_home_catalog()
        self.assertFalse(self.state.search_active)
        self.assertEqual(self.state.submitted_query,'')
        self.assertEqual(self.state.home_collections['books_fiction'],[{'title':'Dune'}])

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
        self.state._popular_loaded=['movie']
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
        self.state._popular_loaded=['movie']
        with patch.object(catalog,'search',new=AsyncMock(return_value=([],['Unavailable']))) as search:
            await self.drain(self.state.more_popular('movie'))
            await self.drain(self.state.more_popular('movie'))
            self.assertEqual([c.args for c in search.await_args_list],[('', 'movie',2),('', 'movie',2)])
        self.assertNotIn('movie',self.state.popular_exhausted)

    async def test_home_replaces_three_fallback_series_when_provider_recovers(self):
        from Codeboxd_main.state.social import present_media
        fallback = [catalog.media('tmdb', 'series', str(i), 'Salva') for i in range(3)]
        self.state.popular_series = [present_media(item) for item in fallback]
        self.state.popular_movies = [present_media(catalog.media('tmdb', 'movie', '99', 'Filme'))]
        self.state._popular_loaded = ['movie']
        recovered = [catalog.media('tmdb', 'series', str(i + 10), 'Popular') for i in range(20)]
        with patch.object(SocialState, '_validate_session', new=AsyncMock()), \
                patch.object(SocialState, '_load_media', new=AsyncMock()), \
                patch.object(catalog, 'search', new=AsyncMock(return_value=(recovered, []))) as search:
            await self.state.load_home()
        search.assert_awaited_once_with('', 'series')
        self.assertEqual(len(self.state.popular_series), 20)
        self.assertIn('series', self.state._popular_loaded)

    async def test_home_prioritizes_requested_series_without_duplicates(self):
        requested = [catalog.media('tmdb', 'series', str(i), title) for i, title in
                     [(66732, 'Stranger Things'), (76479, 'The Boys'),
                      (108978, 'Reacher'), (71446, 'La casa de papel')]]
        self.highlights_fetch.return_value = requested
        self.state._popular_loaded = ['series']
        self.state.popular_series = [{'title': 'Lista anterior'}]
        with patch.object(SocialState, '_validate_session', new=AsyncMock()), \
                patch.object(SocialState, '_load_media', new=AsyncMock()), \
                patch.object(catalog, 'search', new=AsyncMock(return_value=([requested[0]], []))):
            await self.state.load_home()
        self.assertEqual([item['title'] for item in self.state.popular_series],
                         [item['title'] for item in requested])

    async def test_more_series_recovers_first_page_before_pagination(self):
        from Codeboxd_main.state.social import present_media
        self.state.popular_series = [present_media(catalog.media('tmdb', 'series', '1', 'Salva'))]
        recovered = [catalog.media('tmdb', 'series', '2', 'Popular')]
        with patch.object(catalog, 'search', new=AsyncMock(return_value=(recovered, []))) as search:
            await self.drain(self.state.more_popular('series'))
            search.assert_awaited_once_with('', 'series', 1)
        self.assertEqual(self.state.popular_series[0]['title'], 'Popular')
        self.assertEqual(self.state._popular_pages['series'], 1)


if __name__ == '__main__':
    unittest.main()
