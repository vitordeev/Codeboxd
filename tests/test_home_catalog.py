import unittest
from unittest.mock import AsyncMock, patch

from Codeboxd_main.services import catalog
from Codeboxd_main.services.api import APIError


class HomeCatalogTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        catalog._kitsu_cache.clear()

    async def test_movie_collections_use_distinct_lists_and_exclude_adult_items(self):
        payload={'results':[{'id':1,'title':'A film'}, {'id':1,'title':'A film'},
                            {'id':2,'title':'Adult film','adult':True}]}
        with patch.dict(catalog.os.environ,{'TMDB_READ_TOKEN':'test-token'}), \
                patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)) as fetch:
            for key,path in [('movies_now','movie/now_playing'),('movies_rated','movie/top_rated'),
                             ('movies_upcoming','movie/upcoming'),('series_rated','tv/top_rated')]:
                items=await catalog.home_collection(key)
                self.assertEqual(fetch.call_args.args[0],'https://api.themoviedb.org/3/'+path)
                self.assertEqual(fetch.call_args.kwargs['params']['language'],'pt-BR')
                self.assertEqual(len(items),1)
                self.assertEqual(items[0]['media_type'],catalog.HOME_COLLECTIONS[key][0])

    async def test_books_are_selected_by_subject_without_title_relevance_filter(self):
        payload={'docs':[{'key':'/works/OL1W','title':'Dune','editions':{'docs':[{'title':'Duna'}]}}]}
        with patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)) as fetch:
            for key,subject in [('books_fiction','fiction'),('books_fantasy','fantasy'),('books_mystery','mystery')]:
                items=await catalog.home_collection(key)
                self.assertEqual(fetch.call_args.kwargs['params']['q'],'subject:'+subject)
                self.assertEqual(items[0]['external_id'],'OL1W')
                self.assertEqual(items[0]['search_titles'],['Duna'])

    async def test_home_books_include_popular_titles_and_specific_game_theory_search(self):
        payload={'docs':[{'key':'/works/OL1W','title':'Teoria dos Jogos','editions':{'docs':[]}}]}
        with patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)) as fetch:
            await catalog.home_collection('books_popular')
            self.assertEqual([call.kwargs['params']['title'] for call in fetch.call_args_list],
                             ['1984','Duna','Harry Potter','Sapiens','O Hobbit'])
            await catalog.home_collection('books_game_theory')
            self.assertEqual(fetch.call_args.kwargs['params']['title'],'Teoria dos Jogos')

    async def test_home_has_multiple_anime_shelves(self):
        self.assertEqual([key for key, value in catalog.HOME_COLLECTIONS.items()
                          if value[0] == 'anime'], ['anime_rated','anime_popular','anime_current'])

    async def test_anime_uses_ranked_catalog_and_preserves_source(self):
        with patch.object(catalog,'fetch',new=AsyncMock(return_value={'data':[{'id':'1','type':'anime','attributes':{'canonicalTitle':'Anime'}}]})) as fetch:
            items=await catalog.home_collection('anime_rated')
        self.assertEqual(fetch.call_args.args[0],catalog.KITSU_URL+'/anime')
        self.assertEqual(fetch.call_args.kwargs['params']['sort'],'-averageRating')
        self.assertEqual(items[0]['external_source'],'kitsu')

    async def test_missing_movie_credentials_do_not_make_anonymous_requests(self):
        with patch.dict(catalog.os.environ,{'TMDB_READ_TOKEN':''}), patch.object(catalog,'fetch') as fetch:
            with self.assertRaises(APIError): await catalog.home_collection('movies_rated')
        fetch.assert_not_called()
