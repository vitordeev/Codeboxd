"""Reservation client isolation and read-only independent verification, without network."""
from dataclasses import replace
import hashlib
import os
from pathlib import Path
import unittest
from unittest.mock import AsyncMock, patch

import httpx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.services.cloudinary_uploads import (
    CloudinaryImage, upload_post_image, verify_post_image, recover_post_image, MAX_BYTES)
from Codeboxd_main.services.post_image_reservations import (
    ImageReservation, reserve_image, read_reservation)

ENV = {'CLOUDINARY_UPLOADS_ENABLED': 'true', 'CLOUDINARY_CLOUD_NAME': 'fixture',
       'CLOUDINARY_API_KEY': 'key', 'CLOUDINARY_API_SECRET': 'private-test-secret'}
KEY = 'a' * 32
PUBLIC_ID = 'codeboxd/posts/u7/' + 'b' * 32
ROOT = Path(__file__).resolve().parents[1]


def reservation(**changes):
    return {'contract_version': 1, 'id': 12, 'user_id': 7, 'operation_key': KEY,
            'operation': 'create', 'post_id': 0, 'expected_image_revision': 0,
            'state': 'reserved', 'cloud': 'fixture', 'public_id': PUBLIC_ID, **changes}


def image():
    signature = hashlib.sha256((f'public_id={PUBLIC_ID}&version=1' + ENV['CLOUDINARY_API_SECRET']).encode()).hexdigest()
    return CloudinaryImage('https://res.cloudinary.com/fixture/image/upload/v1/' + PUBLIC_ID + '.png',
                           PUBLIC_ID, 'resource-id', 20, 30, 100, 'png', 1, signature)


def resource(**changes):
    item = image()
    return {'public_id': item.public_id, 'asset_id': item.asset_id, 'width': item.width,
            'height': item.height, 'bytes': item.bytes, 'format': item.format,
            'version': item.version, 'secure_url': item.secure_url,
            'resource_type': 'image', 'type': 'upload', **changes}


class ReservationTests(unittest.IsolatedAsyncioTestCase):
    async def test_reservation_is_recoverable_through_a_fresh_client(self):
        body = reservation()
        with patch('Codeboxd_main.services.post_image_reservations.request',
                   new=AsyncMock(return_value=body)) as api:
            first = await reserve_image(token='session-one', owner_id=7, operation_key=KEY)
            second = await read_reservation(token='session-two', owner_id=7, reservation_id=first.id)
        self.assertEqual(first, second)
        self.assertEqual(api.await_count, 2)
        self.assertEqual(api.await_args_list[0].kwargs['data']['operation_key'], KEY)

    async def test_invalid_context_never_reserves_or_uploads(self):
        for args in ({'token': ''}, {'owner_id': True}, {'owner_id': 0},
                     {'operation_key': '../../resource'}, {'operation': 'delete'},
                     {'post_id': 5}, {'operation': 'replace'}, {'expected_revision': True}):
            with patch('Codeboxd_main.services.post_image_reservations.request', new=AsyncMock()) as api:
                with self.assertRaises(APIError):
                    await reserve_image(**({'token': 'session', 'owner_id': 7, 'operation_key': KEY} | args))
                api.assert_not_awaited()

    async def test_another_owner_or_editor_cannot_reuse_response(self):
        for changes in ({'user_id': 8}, {'operation_key': 'c'*32},
                        {'operation': 'replace', 'post_id': 8}, {'expected_image_revision': 3}):
            with patch('Codeboxd_main.services.post_image_reservations.request',
                       new=AsyncMock(return_value=reservation(**changes))):
                with self.assertRaises(APIError):
                    await reserve_image(token='session', owner_id=7, operation_key=KEY)

    async def test_uncertain_reservation_write_is_not_retried(self):
        with patch('Codeboxd_main.services.post_image_reservations.request',
                   new=AsyncMock(side_effect=APIError('Temporary failure', 503))) as api:
            with self.assertRaises(APIError):
                await reserve_image(token='session', owner_id=7, operation_key=KEY)
            api.assert_awaited_once()

    def test_malformed_or_foreign_reservations_are_rejected(self):
        for changes in ({'id': True}, {'post_id': -1}, {'contract_version': True},
                        {'state': []}, {'cloud': 'evil/host'}, {'public_id': 'codeboxd/posts/u8/'+'b'*32},
                        {'expected_image_revision': -1}, {'operation': 'replace', 'post_id': 0}):
            with self.assertRaises(APIError):
                ImageReservation.parse(reservation(**changes), owner_id=7)

    async def test_read_rejects_mismatched_operation_id(self):
        with patch('Codeboxd_main.services.post_image_reservations.request',
                   new=AsyncMock(return_value=reservation(id=13))):
            with self.assertRaises(APIError):
                await read_reservation(token='session', owner_id=7, reservation_id=12)


class ResourceVerificationTests(unittest.IsolatedAsyncioTestCase):
    async def verify(self, handler, **changes):
        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with patch.dict(os.environ, ENV, clear=True), \
             patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient', return_value=client):
            return await verify_post_image(**({'image': image(), 'owner_id': 7, 'public_id': PUBLIC_ID} | changes))

    async def test_authenticated_lookup_returns_same_version_and_has_no_writes(self):
        calls = []
        def handler(request):
            calls.append(request)
            self.assertEqual(request.method, 'GET')
            self.assertEqual(request.url.host, 'api.cloudinary.com')
            self.assertIn('/resources/image/upload/', request.url.path)
            self.assertTrue(request.headers['authorization'].startswith('Basic '))
            self.assertNotIn('private-test-secret', str(request.url))
            return httpx.Response(200, json=resource())
        self.assertEqual(await self.verify(handler), image())
        self.assertEqual(len(calls), 1)

    async def test_changed_asset_id_version_format_size_or_url_are_rejected(self):
        for changed in ({'asset_id': 'another'}, {'version': 2}, {'format': 'gif'},
                        {'bytes': MAX_BYTES+1}, {'bytes': True}, {'width': 21},
                        {'secure_url': 'https://evil.example/image.png'}, {'type': 'private'},
                        {'resource_type': 'raw'}, {'public_id': PUBLIC_ID+'other'}):
            with self.assertRaises(APIError):
                await self.verify(lambda req: httpx.Response(200, json=resource(**changed)))

    async def test_rate_limit_is_sanitized_and_never_retried(self):
        calls = []
        def handler(request):
            calls.append(request)
            return httpx.Response(429, headers={'Retry-After': '60'}, text='private-test-secret')
        with self.assertRaises(APIError) as failure:
            await self.verify(handler)
        self.assertEqual(failure.exception.status, 429)
        self.assertEqual(failure.exception.retry_after, 60)
        self.assertNotIn('private-test-secret', str(failure.exception))
        self.assertEqual(len(calls), 1)

    async def test_receipt_or_owner_mismatch_never_consumes_provider_quota(self):
        for changes in ({'owner_id': 8}, {'image': replace(image(), signature='forged')},
                        {'public_id': PUBLIC_ID + '/../../'}):
            with patch.dict(os.environ, ENV, clear=True), \
                 patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient') as client:
                with self.assertRaises(APIError):
                    await verify_post_image(**({'image': image(), 'owner_id': 7, 'public_id': PUBLIC_ID} | changes))
                client.assert_not_called()

    async def test_incomplete_network_or_http_results_remain_pending(self):
        def timeout(request):
            raise httpx.ReadTimeout('private-test-secret', request=request)
        for handler in (timeout, lambda req: httpx.Response(500, text='private-test-secret'),
                        lambda req: httpx.Response(404), lambda req: httpx.Response(200, json={}),
                        lambda req: httpx.Response(200, text='not-json')):
            with self.assertRaises(APIError) as failure:
                await self.verify(handler)
            self.assertNotIn('private-test-secret', str(failure.exception))
            self.assertIn('pendente', str(failure.exception))

    async def test_verification_can_reconcile_when_new_uploads_are_disabled(self):
        client = httpx.AsyncClient(transport=httpx.MockTransport(lambda req: httpx.Response(200, json=resource())))
        with patch.dict(os.environ, ENV | {'CLOUDINARY_UPLOADS_ENABLED': 'false'}, clear=True), \
             patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient', return_value=client):
            self.assertEqual(await verify_post_image(image(), owner_id=7, public_id=PUBLIC_ID), image())

    async def test_upload_uses_reserved_identity_without_generating_another_id(self):
        calls = []
        def handler(request):
            calls.append(request)
            self.assertIn(PUBLIC_ID.encode(), request.content)
            return httpx.Response(200, json=resource(signature=image().signature))
        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with patch.dict(os.environ, ENV, clear=True), \
             patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient', return_value=client), \
             patch('Codeboxd_main.services.cloudinary_uploads.uuid.uuid4') as generate:
            result = await upload_post_image(owner_id=7, public_id=PUBLIC_ID,
                content=b'\x89PNG\r\n\x1a\nfixture', mime='image/png')
            generate.assert_not_called()
        self.assertEqual(result.public_id, PUBLIC_ID)
        self.assertEqual(len(calls), 1)

    async def test_lost_upload_receipt_is_recovered_by_read_without_new_upload(self):
        calls=[]
        def handler(request):
            calls.append(request.method)
            return httpx.Response(200,json=resource())
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with patch.dict(os.environ,ENV,clear=True), \
             patch('Codeboxd_main.services.cloudinary_uploads.httpx.AsyncClient',return_value=client):
            result=await recover_post_image(owner_id=7,public_id=PUBLIC_ID)
        self.assertEqual(result,image())
        self.assertEqual(calls,['GET'])


class ReservationSchemaTests(unittest.TestCase):
    def test_journal_has_no_cascade_reference_and_unique_operation_and_resource(self):
        source = (ROOT/'xano/table/post_image_asset.xs').read_text(encoding='utf-8')
        self.assertNotIn('table = "post"', source)
        self.assertIn('field: [{name: "cloud", op: "asc"}, {name: "public_id", op: "asc"}]', source)
        self.assertIn('field: [{name: "user_id", op: "asc"}, {name: "operation_key", op: "asc"}]', source)
        self.assertIn('timestamp? retain_until?', source)
        self.assertIn('"reconciliation_required"', source)
        self.assertIn('"cleanup_pending"', source)

    def test_reserve_and_read_require_full_session_and_owner(self):
        for name in ('post_image_uploads_POST.xs', 'post_image_uploads_id_GET.xs'):
            source = (ROOT/'xano/api/codeboxd'/name).read_text(encoding='utf-8')
            self.assertIn('auth = "user"', source)
            self.assertIn('"Security/require_current_session"', source)
            self.assertIn('allow_reset: false', source)
            self.assertIn('$actor.account_status == "active"', source)
        source = (ROOT/'xano/api/codeboxd/post_image_uploads_id_GET.xs').read_text(encoding='utf-8')
        self.assertIn('$result.user_id == $auth.id', source)
        self.assertNotIn('api_secret', source)


if __name__ == '__main__':
    unittest.main()
