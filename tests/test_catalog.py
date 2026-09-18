import os
import unittest
from unittest.mock import AsyncMock, patch

from Codeboxd_main.services import catalog
from Codeboxd_main.services.api import APIError


class CatalogTests(unittest.IsolatedAsyncioTestCase):
    def test_url_validation(self):
        for value in ('javascript:alert(1)', 'http://example.com', 'https://', 'https://user:pass@example.com', 'https://[bad'):
            self.assertEqual(catalog.safe_url(value), '')
        self.assertEqual(catalog.safe_url('https://example.com/a.jpg'),'https://example.com/a.jpg')

    def test_tmdb_identity_separates_movie_and_series(self):
        movie=catalog.tmdb_item({'id':42,'title':'Filme','release_date':'2020-01-01','runtime':120},'movie')
        series=catalog.tmdb_item({'id':42,'name':'Série','number_of_seasons':2},'series')
        self.assertNotEqual(movie['identity_key'],series['identity_key'])
        self.assertEqual(movie['year'],2020)
        self.assertEqual(series['details']['Temporadas'],'2')

    async def test_partial_failure_keeps_other_sources(self):
        async def provider(query, kind, page):
            if kind=='movie': raise APIError('Indisponível')
            return [catalog.media('jikan' if kind=='anime' else 'tmdb' if kind=='series' else 'openlibrary',kind,'42','Título')]
        with patch.object(catalog,'search_one',side_effect=provider):
            items,errors=await catalog.search('teste')
        self.assertEqual(len(items),3)
        self.assertEqual(len(errors),1)
        self.assertIn('Filme',errors[0])

    async def test_search_adapters_preserve_identity(self):
        fixtures={
            'movie':{'results':[{'id':1,'title':'Filme'}]},
            'series':{'results':[{'id':2,'name':'Série'}]},
            'anime':{'data':[{'mal_id':3,'title':'Anime','images':{}}]},
            'book':{'docs':[{'key':'/works/OL4W','title':'Livro','author_name':['Autora'],'first_publish_year':1999}]},
        }
        with patch.dict(os.environ,{'TMDB_READ_TOKEN':'test-only'}):
            for kind,payload in fixtures.items():
                with self.subTest(kind=kind),patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)):
                    result=await catalog.search_one('teste',kind)
                    self.assertEqual(result[0]['media_type'],kind)
                    self.assertTrue(result[0]['external_id'])
                    self.assertTrue(result[0]['identity_key'])

    async def test_external_detail_rejects_invalid_source_and_identifier(self):
        with patch.object(catalog,'fetch',new=AsyncMock()) as fetch:
            for source,kind,identifier in [('evil','book','1'),('tmdb','book','1'),('jikan','anime','../1'),('openlibrary','book','../../secret')]:
                with self.assertRaises(APIError):
                    await catalog.detail(catalog.media(source,kind,identifier,'Título'))
        fetch.assert_not_awaited()

    async def test_book_detail_preserves_metadata(self):
        item=catalog.media('openlibrary','book','OL4W','Livro',details={'Autores':'Autora'})
        with patch.object(catalog,'fetch',new=AsyncMock(return_value={'description':{'value':'Resumo'}})):
            result=await catalog.detail(item)
        self.assertEqual(result['description'],'Resumo')
        self.assertEqual(result['details'],item['details'])


if __name__=='__main__': unittest.main()
