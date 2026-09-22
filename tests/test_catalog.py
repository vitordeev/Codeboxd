import os
import unittest
from unittest.mock import AsyncMock, patch
import httpx

from Codeboxd_main.services import catalog
from Codeboxd_main.services.api import APIError


class CatalogTests(unittest.IsolatedAsyncioTestCase):
    async def test_provider_fetch_retries_transient_http_status(self):
        client=AsyncMock()
        request=httpx.Request('GET','https://provider.example/test')
        client.get.side_effect=[httpx.Response(503,request=request),httpx.Response(200,json={'ok':True},request=request)]
        context=AsyncMock(); context.__aenter__.return_value=client
        with patch.object(catalog.httpx,'AsyncClient',return_value=context),patch.object(catalog.asyncio,'sleep',new=AsyncMock()) as sleep:
            result=await catalog.fetch('https://provider.example/test')
        self.assertEqual(result,{'ok':True})
        self.assertEqual(client.get.await_count,2)
        sleep.assert_awaited_once_with(0.5)

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
            return [catalog.media('jikan' if kind=='anime' else 'tmdb' if kind=='series' else 'openlibrary',kind,'42','Título de teste')]
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

    async def test_anime_search_uses_jikan_v4_and_keeps_jikan_identity(self):
        payload={'data':[{'mal_id':91,'title':'Anime de teste','images':{}}]}
        with patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)) as fetch:
            items=await catalog.search_one('Anime de teste','anime')
        self.assertEqual(items[0]['media_type'],'anime')
        self.assertEqual(items[0]['external_source'],'jikan')
        self.assertEqual(items[0]['external_id'],'91')
        fetch.assert_awaited_once_with('https://api.jikan.moe/v4/anime',
            params={'q':'Anime de teste','page':1,'limit':12,'sfw':'true'})

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

    async def test_jikan_detail_uses_v4_full_endpoint_and_preserves_source(self):
        item=catalog.media('jikan','anime','91','Anime')
        payload={'data':{'mal_id':91,'title':'Anime','synopsis':'Resumo','images':{},'episodes':12}}
        with patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)) as fetch:
            result=await catalog.detail(item)
        fetch.assert_awaited_once_with('https://api.jikan.moe/v4/anime/91/full')
        self.assertEqual(result['external_source'],'jikan')
        self.assertEqual(result['external_id'],'91')
        self.assertEqual(result['description'],'Resumo')

    async def test_tmdb_detail_enriches_director_and_cast(self):
        item=catalog.media('tmdb','movie','42','Filme')
        replies=[{'id':42,'title':'Filme','backdrop_path':'/wide.jpg','genres':[{'name':'Drama'}]},
                 {'crew':[{'job':'Director','name':'Diretora'}], 'cast':[{'name':'Atriz'}]}]
        with patch.dict(os.environ,{'TMDB_READ_TOKEN':'test-only'}), patch.object(catalog,'fetch',new=AsyncMock(side_effect=replies)):
            result=await catalog.detail(item)
        self.assertIn('Diretora',result['details']['Direção'])
        self.assertIn('Atriz',result['details']['Elenco principal'])
        self.assertEqual(result['backdrop_url'],'https://image.tmdb.org/t/p/w1280/wide.jpg')

    async def test_recommendations_use_provider_data_without_extra_credentials(self):
        tmdb=catalog.media('tmdb','series','42','Série')
        anime=catalog.media('jikan','anime','7','Anime')
        with patch.dict(os.environ,{'TMDB_READ_TOKEN':'test-only'}), patch.object(catalog,'fetch',new=AsyncMock(side_effect=[
            {'results':[{'id':43,'name':'Outra série'}]}, {'data':[{'entry':{'mal_id':8,'title':'Outro anime','images':{}}}]}
        ])) as fetch:
            tv=await catalog.recommendations(tmdb)
            anime_results=await catalog.recommendations(anime)
        self.assertEqual(tv[0]['external_id'],'43')
        self.assertEqual(anime_results[0]['external_id'],'8')
        self.assertEqual(fetch.await_count,2)

    async def test_public_reviews_are_normalized_when_provider_supplies_them(self):
        movie=catalog.media('tmdb','movie','42','Filme')
        with patch.dict(os.environ,{'TMDB_READ_TOKEN':'test-only'}), patch.object(catalog,'fetch',new=AsyncMock(return_value={
            'results':[{'author':'Crítica','content':'Boa história.','created_at':'2025-03-01T00:00:00Z',
                        'author_details':{'rating':8}}]})):
            result=await catalog.reviews(movie)
        self.assertEqual(result[0]['author'],'Crítica')
        self.assertEqual(result[0]['rating'],'8')
        self.assertEqual(result[0]['body'],'Boa história.')


    async def test_tmdb_trailers_filter_and_embed_only_youtube_trailers(self):
        movie=catalog.media('tmdb','movie','42','Filme')
        videos={'results':[{'site':'YouTube','type':'Trailer','key':'abcDEF_123','name':'Official','official':True},
            {'site':'Vimeo','type':'Trailer','key':'abcDEF_456'},
            {'site':'YouTube','type':'Behind the Scenes','key':'abcDEF_789'},
            {'site':'YouTube','type':'Teaser','key':'bad key'}]}
        with patch.dict(os.environ,{'TMDB_READ_TOKEN':'test-only'}), patch.object(catalog,'fetch',new=AsyncMock(return_value=videos)) as fetch:
            result=await catalog.trailers(movie)
        fetch.assert_awaited_once_with('https://api.themoviedb.org/3/movie/42/videos',params={'language':'pt-BR'},
            headers={'Authorization':'Bearer test-only'})
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['embed_url'],'https://www.youtube-nocookie.com/embed/abcDEF_123')

    async def test_tmdb_trailers_fallback_to_english_when_localized_list_empty(self):
        series=catalog.media('tmdb','series','42','Série')
        with patch.dict(os.environ,{'TMDB_READ_TOKEN':'test-only'}), patch.object(catalog,'fetch',new=AsyncMock(
                side_effect=[{'results':[]},{'results':[{'site':'YouTube','type':'Trailer','key':'abcDEF_123'}]}])) as fetch:
            result=await catalog.trailers(series)
        self.assertEqual(len(result),1)
        self.assertEqual(fetch.await_args_list[1].kwargs['params'],{'language':'en-US'})


if __name__=='__main__': unittest.main()
