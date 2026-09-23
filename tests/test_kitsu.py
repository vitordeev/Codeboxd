import unittest
from unittest.mock import AsyncMock, patch
import httpx
from Codeboxd_main.services import catalog
from Codeboxd_main.services.api import APIError


def anime(identifier='1', **attrs):
    return {'id':identifier,'type':'anime','attributes':{'canonicalTitle':'Cowboy Bebop',**attrs}}


class KitsuTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        catalog._kitsu_cache.clear()

    def test_normalizes_missing_images_titles_and_rating(self):
        item=catalog.kitsu_item(anime(posterImage=None,coverImage=None,startDate='1998-04-03',
            titles={'en':'Cowboy Bebop','ja_jp':'Japanese title'},averageRating='82.27',episodeCount=26))
        self.assertEqual(item['cover_url'],'')
        self.assertEqual(item['year'],1998)
        self.assertEqual(item['details']['Nota Kitsu'],'82.27/100')
        self.assertGreater(catalog.title_score('Japanese title',item),0)

    def test_filters_adult_content_and_non_anime_resources(self):
        payload={'data':[anime(),anime('2',nsfw=True),anime('3',ageRating='R18'),{'type':'manga','id':'4'}]}
        self.assertEqual([i['external_id'] for i in catalog.kitsu_items(payload)],['1'])

    def test_mapping_is_linked_to_the_correct_anime(self):
        item=anime('10')
        item['relationships']={'mappings':{'data':[{'type':'mappings','id':'100'}]}}
        included=[{'id':'100','type':'mappings','attributes':{'externalSite':'myanimelist/anime','externalId':'99'}},
                  {'id':'101','type':'mappings','attributes':{'externalSite':'myanimelist/anime','externalId':'88'}}]
        self.assertEqual(catalog.kitsu_item(item,included)['details']['MyAnimeList ID'],'99')

    async def test_unmapped_legacy_record_does_not_guess_kitsu_id(self):
        with patch.object(catalog,'fetch',new=AsyncMock(return_value={'data':[]})) as fetch:
            with self.assertRaises(APIError):
                await catalog.detail(catalog.media('jikan','anime','123','Old anime'))
        self.assertEqual(fetch.await_count,1)
        self.assertTrue(fetch.call_args.args[0].endswith('/mappings'))

    async def test_cache_reuses_success_without_sharing_mutations(self):
        with patch.object(catalog,'fetch',new=AsyncMock(return_value={'data':[anime()]})) as fetch:
            first=await catalog.kitsu_fetch('/anime',sort='-userCount')
            first['data'].clear()
            second=await catalog.kitsu_fetch('/anime',sort='-userCount')
        self.assertEqual(len(second['data']),1)
        self.assertEqual(fetch.await_count,1)

    async def test_cache_expires_and_never_stores_failures(self):
        with patch.object(catalog,'fetch',new=AsyncMock(side_effect=[APIError('offline'),{'data':[anime()]},{'data':[]}])) as fetch:
            with self.assertRaises(APIError): await catalog.kitsu_fetch('/anime')
            await catalog.kitsu_fetch('/anime')
            key=next(iter(catalog._kitsu_cache))
            stamp,payload=catalog._kitsu_cache[key]
            catalog._kitsu_cache[key]=(stamp-301,payload)
            self.assertEqual((await catalog.kitsu_fetch('/anime'))['data'],[])
        self.assertEqual(fetch.await_count,3)

    async def test_invalid_provider_body_is_not_cached(self):
        with patch.object(catalog,'fetch',new=AsyncMock(return_value={'errors':[{'detail':'bad request'}]})):
            with self.assertRaises(APIError): await catalog.kitsu_fetch('/anime')
        self.assertFalse(catalog._kitsu_cache)

    async def test_invalid_source_or_id_is_rejected_before_network(self):
        with patch.object(catalog,'fetch',new=AsyncMock()) as fetch:
            for source,kind,identifier in [('kitsu','book','1'),('kitsu','anime','../1')]:
                with self.assertRaises(APIError): await catalog.detail(catalog.media(source,kind,identifier,'Invalid'))
        fetch.assert_not_awaited()

    async def test_trailer_uses_only_valid_youtube_id(self):
        item=catalog.kitsu_item(anime(youtubeVideoId='abcDEF_123'))
        with patch.object(catalog,'fetch',new=AsyncMock()) as fetch:
            result=await catalog.trailers(item)
        self.assertEqual(result[0]['embed_url'],'https://www.youtube-nocookie.com/embed/abcDEF_123')
        fetch.assert_not_awaited()
        self.assertNotIn('YouTube ID',catalog.kitsu_item(anime(youtubeVideoId='https://evil.test'))['details'])

    async def test_errors_keep_http_status_and_log_public_provider_reason(self):
        request=httpx.Request('GET',catalog.KITSU_URL+'/anime')
        client=AsyncMock()
        client.get.return_value=httpx.Response(504,json={'message':'Provider upstream unavailable'},request=request)
        context=AsyncMock(); context.__aenter__.return_value=client
        with patch.object(catalog.httpx,'AsyncClient',return_value=context), \
             patch.object(catalog.asyncio,'sleep',new=AsyncMock()), self.assertLogs(catalog.logger,level='WARNING') as logs:
            with self.assertRaises(APIError) as error: await catalog.fetch(catalog.KITSU_URL+'/anime')
        self.assertEqual(error.exception.status,504)
        self.assertIn('HTTP 504',str(error.exception))
        self.assertIn('Provider upstream unavailable',logs.output[0])

    async def test_network_and_format_errors_are_distinguished(self):
        request=httpx.Request('GET',catalog.KITSU_URL+'/anime')
        for reply,expected in [(httpx.ReadTimeout('slow',request=request),'tempo de resposta'),
                               (httpx.ConnectError('blocked',request=request),'conectar')]:
            client=AsyncMock(); client.get.side_effect=reply
            context=AsyncMock(); context.__aenter__.return_value=client
            with patch.object(catalog.httpx,'AsyncClient',return_value=context):
                with self.assertRaises(APIError) as error: await catalog.fetch(catalog.KITSU_URL+'/anime')
            self.assertIn(expected,str(error.exception))

    def test_search_deduplicates_verified_legacy_identity(self):
        new=catalog.media('kitsu','anime','11','Naruto',details={'MyAnimeList ID':'20'})
        old=catalog.media('jikan','anime','20','Naruto')
        distinct=catalog.media('jikan','anime','11','Naruto Special')
        self.assertEqual(catalog.relevant_results('Naruto',[new,old,distinct]),[new,distinct])

    async def test_long_rate_limit_does_not_retry_too_early(self):
        client=AsyncMock()
        client.get.return_value=httpx.Response(429,headers={'Retry-After':'60'},
            request=httpx.Request('GET',catalog.KITSU_URL+'/anime'))
        context=AsyncMock(); context.__aenter__.return_value=client
        with patch.object(catalog.httpx,'AsyncClient',return_value=context), patch.object(catalog.asyncio,'sleep',new=AsyncMock()) as sleep:
            with self.assertRaises(APIError) as error: await catalog.fetch(catalog.KITSU_URL+'/anime')
        self.assertEqual(error.exception.status,429)
        self.assertEqual(client.get.await_count,1)
        sleep.assert_not_awaited()

    def test_provider_identifiers_are_not_shown_in_media_facts(self):
        from Codeboxd_main.state.social import present_media
        item=catalog.media('kitsu','anime','11','Naruto',details={
            'Kitsu ID':'11','MyAnimeList ID':'20','YouTube ID':'abcDEF_123','Fonte':'Kitsu','Episódios':'220'})
        facts=present_media(item)['details']
        self.assertIn('Fonte: Kitsu',facts)
        self.assertNotIn(' ID:',facts)
        self.assertIn('Episódios: 220',facts)
