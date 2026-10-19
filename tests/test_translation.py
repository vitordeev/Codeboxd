import asyncio
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

import httpx

from Codeboxd_main.services import catalog, translation


class TranslationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        for target in (patch.object(translation, 'CACHE_PATH', Path(directory.name) / 'cache.sqlite3'),
                       patch.dict(os.environ, {'DEEPL_API_KEY': 'test-only:fx'})):
            target.start()
            self.addCleanup(target.stop)
        translation._blocked_until = 0
        self.addCleanup(setattr, translation, '_blocked_until', 0)
        self.client = AsyncMock()
        context = AsyncMock()
        context.__aenter__.return_value = self.client
        factory = patch.object(translation.httpx, 'AsyncClient', return_value=context)
        factory.start()
        self.addCleanup(factory.stop)

    def response(self, status=200, payload=None):
        return httpx.Response(status, request=httpx.Request('POST', 'https://api-free.deepl.com/v2/translate'),
                              json=payload if payload is not None else {'translations': [{'text': 'Uma aventura.', 'detected_source_language': 'EN'}]})

    async def test_concurrent_requests_and_later_calls_reuse_disk_cache(self):
        self.client.post.return_value = self.response()
        results = await asyncio.gather(*(translation.translate_description('An adventure.') for _ in range(4)))
        self.assertEqual(results, ['Uma aventura.'] * 4)
        translation._locks.clear()
        self.assertEqual(await translation.translate_description('An adventure.'), 'Uma aventura.')
        self.client.post.assert_awaited_once()
        self.assertEqual(self.client.post.call_args.kwargs['json']['target_lang'], 'PT-BR')
        self.assertEqual(self.client.post.call_args.args[0], 'https://api-free.deepl.com/v2/translate')
        await translation.translate_description('A different adventure.')
        self.assertEqual(self.client.post.await_count, 2)

    async def test_detected_portuguese_keeps_original(self):
        self.client.post.return_value = self.response(payload={'translations': [{'text': 'Reformulado.', 'detected_source_language': 'PT'}]})
        self.assertEqual(await translation.translate_description('Uma história.'), 'Uma história.')

    async def test_missing_key_empty_and_oversized_do_not_call_provider(self):
        with patch.dict(os.environ, {'DEEPL_API_KEY': ''}):
            self.assertEqual(await translation.translate_description('Story'), 'Story')
        for original in ('', '  ', 'a' * 20001):
            self.assertEqual(await translation.translate_description(original), original)
        self.client.post.assert_not_awaited()

    async def test_http_errors_keep_original_and_apply_cooldown_without_secret_logs(self):
        for status in (403, 429, 456, 500):
            with self.subTest(status=status):
                translation._blocked_until = 0
                self.client.post.reset_mock()
                self.client.post.return_value = self.response(status)
                with self.assertLogs(translation.logger, level='WARNING') as logs:
                    self.assertEqual(await translation.translate_description('Original'), 'Original')
                self.assertNotIn('test-only', ''.join(logs.output))
                self.assertEqual(await translation.translate_description('Original'), 'Original')
                self.client.post.assert_awaited_once()

    async def test_network_and_malformed_response_keep_original(self):
        for failure in ('network', 'invalid', 'empty'):
            translation._blocked_until = 0
            self.client.post.side_effect = httpx.ConnectError('private-error') if failure == 'network' else None
            self.client.post.return_value = self.response(payload={} if failure == 'invalid' else {'translations': [{'text': ''}]})
            with self.assertLogs(translation.logger, level='WARNING'):
                self.assertEqual(await translation.translate_description('Original'), 'Original')

    async def test_cache_failure_does_not_spend_quota(self):
        with patch.object(translation, '_cache', side_effect=OSError), self.assertLogs(translation.logger, level='WARNING'):
            self.assertEqual(await translation.translate_description('Original'), 'Original')
        self.client.post.assert_not_awaited()

    async def test_book_and_anime_detail_translate_without_changing_identity(self):
        fixtures = [
            ({'external_source': 'openlibrary', 'media_type': 'book', 'external_id': 'OL1W', 'title': 'Title', 'identity_key': 'openlibrary:book:OL1W'},
             {'title': 'Title', 'description': {'value': 'Story'}}),
            ({'external_source': 'kitsu', 'media_type': 'anime', 'external_id': '1'},
             {'data': {'id': '1', 'type': 'anime', 'attributes': {'canonicalTitle': 'Title', 'synopsis': 'Story'}}}),
            ({'external_source': 'jikan', 'media_type': 'anime', 'external_id': '2', 'id': 7},
             {'data': {'id': '1', 'type': 'anime', 'attributes': {'canonicalTitle': 'Title', 'synopsis': 'Story'}}}),
        ]
        for item, payload in fixtures:
            with patch.object(catalog, 'fetch', new=AsyncMock(return_value=payload)), \
                 patch.object(catalog, 'kitsu_fetch', new=AsyncMock(return_value=payload)), \
                 patch.object(catalog, 'kitsu_identifier', new=AsyncMock(return_value='1')), \
                 patch.object(catalog, 'translate_description', new=AsyncMock(return_value='História')) as translate:
                result = await catalog.detail(item)
            self.assertEqual(result['description'], 'História')
            self.assertEqual(result['external_source'], item['external_source'])
            self.assertEqual(result['external_id'], item['external_id'])
            self.assertEqual(result['title'], 'Title')
            translate.assert_awaited_once_with('Story')

    async def test_tmdb_does_not_call_translation(self):
        with patch.object(catalog, 'fetch', new=AsyncMock(return_value={'id': 1, 'title': 'Filme', 'overview': 'Original'})), \
             patch.object(catalog, 'translate_description', new=AsyncMock()) as translate:
            result = await catalog.detail({'external_source': 'tmdb', 'media_type': 'movie', 'external_id': '1'})
        self.assertEqual(result['description'], 'Original')
        translate.assert_not_awaited()
