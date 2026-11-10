"""Prepared upload transport contracts; no network or real Cloudinary account."""
import hashlib
import os
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.services.cloudinary_uploads import upload_post_image, upload_config, MAX_BYTES

ENV = {'CLOUDINARY_UPLOADS_ENABLED': 'true', 'CLOUDINARY_CLOUD_NAME': 'demo-test',
       'CLOUDINARY_API_KEY': 'dummy-key', 'CLOUDINARY_API_SECRET': 'dummy-secret'}
PUBLIC_ID = 'codeboxd/posts/u7/fixed-id'
PNG = b'\x89PNG\r\n\x1a\n' + b'fictional-image'


def image():
    return {'secure_url': 'https://res.cloudinary.com/demo-test/image/upload/v1/' + PUBLIC_ID + '.png',
            'public_id': PUBLIC_ID, 'asset_id': 'test-asset', 'resource_type': 'image', 'type': 'upload',
            'width': 40, 'height': 30, 'bytes': 100, 'format': 'png', 'api_key': 'provider-extra-field'}


class CloudinaryUploadTests(unittest.IsolatedAsyncioTestCase):
    async def send(self, handler, **kwargs):
        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with patch.dict(os.environ, ENV, clear=True), \
             patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient', return_value=client), \
             patch('Codeboxd_main.services.cloudinary_uploads.time.time', return_value=1700000000), \
             patch('Codeboxd_main.services.cloudinary_uploads.uuid.uuid4', return_value=SimpleNamespace(hex='fixed-id')):
            return await upload_post_image(**({'owner_id': 7, 'content': PNG, 'mime': 'image/png'} | kwargs))

    async def test_signed_upload_keeps_secret_private_and_returns_only_asset_metadata(self):
        def handler(request):
            self.assertEqual(str(request.url), 'https://api.cloudinary.com/v1_1/demo-test/image/upload')
            expected = hashlib.sha256(('overwrite=false&public_id=' + PUBLIC_ID + '&timestamp=1700000000dummy-secret').encode()).hexdigest()
            self.assertIn(expected.encode(), request.content)
            self.assertNotIn(b'dummy-secret', request.content)
            self.assertIn(b'dummy-key', request.content)
            self.assertIn(b'name="file"; filename="image.png"', request.content)
            self.assertIn(PNG, request.content)
            return httpx.Response(200, json=image())
        result = await self.send(handler)
        self.assertEqual(result.public_id, PUBLIC_ID)
        self.assertNotIn('provider-extra-field', repr(result))

    async def test_disabled_and_incomplete_configuration_never_call_network(self):
        for env in ({}, {**ENV, 'CLOUDINARY_UPLOADS_ENABLED': 'false'}, {**ENV, 'CLOUDINARY_API_SECRET': ''},
                    {**ENV, 'CLOUDINARY_CLOUD_NAME': 'bad/host'}):
            with patch.dict(os.environ, env, clear=True), patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient') as client:
                with self.assertRaises(APIError):
                    await upload_post_image(owner_id=7, content=PNG, mime='image/png')
                client.assert_not_called()

    async def test_invalid_owner_size_and_format_rejected_before_network(self):
        for kwargs in ({'owner_id': 0}, {'owner_id': True}, {'content': b''}, {'content': b'x' * (MAX_BYTES + 1)},
                       {'content': b'<svg>image</svg>', 'mime': 'image/svg+xml'}, {'content': b'not a png'},
                       {'content': b'RIFFbad', 'mime': 'image/webp'}):
            with patch.dict(os.environ, ENV, clear=True), patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient') as client:
                with self.assertRaises(APIError):
                    await upload_post_image(**({'owner_id': 7, 'content': PNG, 'mime': 'image/png'} | kwargs))
                client.assert_not_called()

    async def test_provider_errors_are_sanitized_and_not_retried(self):
        for status in (301, 400, 401, 403, 413, 429, 500):
            requests = []
            def handler(request):
                requests.append(request)
                return httpx.Response(status, json={'error': 'dummy-secret internal detail'})
            with self.assertRaises(APIError) as failure:
                await self.send(handler)
            self.assertNotIn('dummy-secret', str(failure.exception))
            self.assertEqual(len(requests), 1)

    async def test_untrusted_or_incomplete_success_response_is_rejected(self):
        for changes in ({'secure_url': 'http://res.cloudinary.com/demo-test/image.png'},
                        {'secure_url': 'https://evil.example/image.png'},
                        {'secure_url': 'https://res.cloudinary.com/other-cloud/image.png'},
                        {'public_id': 'someone-elses-asset'}, {'width': True}, {'bytes': MAX_BYTES + 1},
                        {'resource_type': 'video'}, {'asset_id': ''}):
            with self.assertRaises(APIError):
                await self.send(lambda request: httpx.Response(200, json=image() | changes))

    async def test_network_and_invalid_json_do_not_expose_provider_details(self):
        def failed(request):
            raise httpx.ReadTimeout('internal-secret', request=request)
        for handler in (failed, lambda request: httpx.Response(200, text='internal-secret')):
            with self.assertRaises(APIError) as failure:
                await self.send(handler)
            self.assertNotIn('internal-secret', str(failure.exception))

    def test_configuration_repr_does_not_expose_credentials(self):
        with patch.dict(os.environ, ENV, clear=True):
            self.assertNotIn('dummy-secret', repr(upload_config()))
            self.assertNotIn('dummy-key', repr(upload_config()))
