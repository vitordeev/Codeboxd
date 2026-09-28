from pathlib import Path
p=Path('tests/test_catalog.py'); s=p.read_text(encoding='utf8')
s=s.replace('class CatalogTests(unittest.IsolatedAsyncioTestCase):','class CatalogTests(unittest.IsolatedAsyncioTestCase):\n    def setUp(self):\n        catalog._kitsu_cache.clear()\n')
s=s.replace("'anime':{'data':[{'mal_id':3,'title':'Anime','images':{}}]}","'anime':{'data':[{'id':'3','type':'anime','attributes':{'canonicalTitle':'Anime'}}]}")
a=s.index('    async def test_anime_search_uses_jikan'); b=s.index('    async def test_external_detail',a)
s=s[:a]+'''    async def test_anime_search_uses_kitsu_and_page_offsets(self):
        payload={'data':[{'id':'91','type':'anime','attributes':{'canonicalTitle':'Anime de teste'}}]}
        with patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)) as fetch:
            items=await catalog.search_one('Anime de teste','anime',page=2)
        self.assertEqual(items[0]['external_source'],'kitsu')
        self.assertEqual(items[0]['external_id'],'91')
        self.assertEqual(fetch.call_args.args[0],catalog.KITSU_URL+'/anime')
        self.assertEqual(fetch.call_args.kwargs['params']['filter[text]'],'Anime de teste')
        self.assertEqual(fetch.call_args.kwargs['params']['page[offset]'],12)

''' + s[b:]
a=s.index('    async def test_jikan_detail'); b=s.index('    async def test_tmdb_detail',a)
s=s[:a]+'''    async def test_old_jikan_detail_resolves_mapping_without_changing_identity(self):
        item=catalog.media('jikan','anime','91','Anime')
        mapping={'data':[{'attributes':{'externalSite':'myanimelist/anime','externalId':'91'},
            'relationships':{'item':{'data':{'type':'anime','id':'456'}}}}]}
        payload={'data':{'id':'456','type':'anime','attributes':{'canonicalTitle':'Anime','synopsis':'Resumo'}}}
        with patch.object(catalog,'fetch',new=AsyncMock(side_effect=[mapping,payload])) as fetch:
            result=await catalog.detail(item)
        self.assertEqual(fetch.await_args_list[1].args[0],catalog.KITSU_URL+'/anime/456')
        self.assertEqual(result['external_source'],'jikan')
        self.assertEqual(result['external_id'],'91')
        self.assertEqual(result['details']['Kitsu ID'],'456')
        self.assertEqual(result['description'],'Resumo')

''' + s[b:]
a=s.index('    async def test_recommendations_use_provider'); b=s.index('    async def test_public_reviews',a)
s=s[:a]+'''    async def test_recommendations_use_provider_data_without_extra_credentials(self):
        tmdb=catalog.media('tmdb','series','42','Série')
        anime=catalog.media('kitsu','anime','7','Anime')
        with patch.dict(os.environ,{'TMDB_READ_TOKEN':'test-only'}), patch.object(catalog,'fetch',new=AsyncMock(side_effect=[
            {'results':[{'id':43,'name':'Outra série'}]},
            {'data':[{'relationships':{'destination':{'data':{'type':'anime','id':'8'}}}}],
             'included':[{'id':'8','type':'anime','attributes':{'canonicalTitle':'Outro anime'}}]}
        ])) as fetch:
            tv=await catalog.recommendations(tmdb)
            anime_results=await catalog.recommendations(anime)
        self.assertEqual(tv[0]['external_id'],'43')
        self.assertEqual(anime_results[0]['external_id'],'8')
        self.assertEqual(fetch.await_count,2)

''' + s[b:]
p.write_text(s,encoding='utf8')
p=Path('tests/test_home_catalog.py'); s=p.read_text(encoding='utf8').replace('class HomeCatalogTests(unittest.IsolatedAsyncioTestCase):','class HomeCatalogTests(unittest.IsolatedAsyncioTestCase):\n    def setUp(self):\n        catalog._kitsu_cache.clear()\n')
s=s.replace("{'data':[{'mal_id':1,'title':'Anime'}]}","{'data':[{'id':'1','type':'anime','attributes':{'canonicalTitle':'Anime'}}]}")
s=s.replace("'https://api.jikan.moe/v4/top/anime'","catalog.KITSU_URL+'/anime'").replace("self.assertEqual(fetch.call_args.kwargs['params']['sfw'],'true')","self.assertEqual(fetch.call_args.kwargs['params']['sort'],'-averageRating')").replace("items[0]['external_source'],'jikan'","items[0]['external_source'],'kitsu'")
p.write_text(s,encoding='utf8')
p=Path('xano/api/codeboxd/media_POST.xs'); s=p.read_text(encoding='utf8')
s=s.replace("i.external_source === 'jikan' &&", "['jikan','kitsu'].includes(i.external_source) &&")
p.write_text(s,encoding='utf8')
