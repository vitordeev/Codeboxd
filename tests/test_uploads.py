"""Upload transport contract: multipart data and safe, readable errors."""
import unittest
from unittest.mock import patch

import httpx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.services.uploads import upload_file


class UploadTests(unittest.IsolatedAsyncioTestCase):
    async def send(self, handler):
        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with patch('Codeboxd_main.services.uploads.httpx.AsyncClient', return_value=client), \
                patch('Codeboxd_main.services.uploads.base_url', return_value='https://service.example'):
            return await upload_file('/posts', token='test-token', data={'body': 'Legenda'},
                                     field='image', filename='cover.png', content=b'image-bytes', mime='image/png')

    async def test_upload_sends_authenticated_multipart_and_reads_result(self):
        def handler(request):
            self.assertEqual(request.url.path, '/posts')
            self.assertEqual(request.headers['Authorization'], 'Bearer test-token')
            self.assertIn('multipart/form-data', request.headers['Content-Type'])
            self.assertIn(b'name="image"; filename="cover.png"', request.content)
            self.assertIn(b'Content-Type: image/png', request.content)
            self.assertIn(b'image-bytes', request.content)
            self.assertIn(b'Legenda', request.content)
            return httpx.Response(200, json={'id': 7})

        self.assertEqual(await self.send(handler), {'id': 7})

    async def test_http_failures_are_readable_preserve_status_and_hide_provider_body(self):
        for status in (400, 401, 403, 404, 413, 422, 429, 500):
            with self.subTest(status=status):
                with self.assertRaises(APIError) as failure:
                    await self.send(lambda request: httpx.Response(status, text='internal-secret'))
                self.assertEqual(failure.exception.status, status)
                self.assertNotIn('\\u', str(failure.exception))
                self.assertNotIn('internal-secret', str(failure.exception))

    async def test_connection_failure_is_readable(self):
        def handler(request):
            raise httpx.ConnectError('internal-network-detail', request=request)

        with self.assertRaises(APIError) as failure:
            await self.send(handler)
        self.assertIn('Não foi possível', str(failure.exception))
        self.assertNotIn('internal-network-detail', str(failure.exception))

    async def test_invalid_success_body_returns_readable_service_error(self):
        with self.assertRaises(APIError) as failure:
            await self.send(lambda request: httpx.Response(200, text='invalid-json'))
        self.assertIn('serviço', str(failure.exception))
        self.assertNotIn('\\u', str(failure.exception))
