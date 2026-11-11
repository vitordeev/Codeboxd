"""Transport probe tests: local MockTransport only, no real assets."""
import contextlib
import io
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs

import httpx

from tools import cloudinary_acceptance_probe as probe

CONFIG = {'CLOUDINARY_CLOUD_NAME': 'fixture', 'CLOUDINARY_API_KEY': 'fixture-key',
          'CLOUDINARY_API_SECRET': 'fixture-secret'}
PUBLIC_ID = 'codeboxd/acceptance/' + 'a' * 32


def uploaded(**overrides):
    return {'public_id': PUBLIC_ID, 'asset_id': 'fixture-asset', 'resource_type': 'image',
            'type': 'upload', 'format': 'png', 'width': 2, 'height': 2,
            'secure_url': 'https://res.cloudinary.com/fixture/image/upload/v1/' + PUBLIC_ID + '.png',
            **overrides}


class CloudinaryProbeTests(unittest.TestCase):
    def exercise(self, handler):
        report, journals = {}, []
        def save(value):
            journals.append(dict(value))
        with httpx.Client(transport=httpx.MockTransport(handler)) as client, \
                patch.object(probe.uuid, 'uuid4', return_value=SimpleNamespace(hex='a'*32)):
            probe.run(client, CONFIG, report, save)
        return report, journals

    def test_preview_never_opens_client(self):
        with patch.object(probe.httpx, 'Client') as client, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(probe.main([]), 0)
            client.assert_not_called()

    def test_complete_flow_signs_only_known_asset_and_verifies_download(self):
        calls = []
        def handler(request):
            calls.append(request)
            self.assertNotIn(CONFIG['CLOUDINARY_API_SECRET'].encode(), request.content)
            if request.url.path.endswith('/upload'):
                return httpx.Response(200, json=uploaded())
            if request.method == 'GET':
                return httpx.Response(200, content=probe.png())
            data = parse_qs(request.content.decode())
            self.assertEqual(data['public_id'], [PUBLIC_ID])
            self.assertEqual(data['invalidate'], ['true'])
            return httpx.Response(200, json={'result': 'ok'})
        report, journals = self.exercise(handler)
        self.assertTrue(report['passed'])
        self.assertEqual([r.method for r in calls], ['POST', 'GET', 'POST'])
        self.assertEqual(journals[0]['upload'], 'not_started')
        self.assertEqual(journals[0]['public_id'], PUBLIC_ID)
        self.assertEqual(report['cleanup'], 'provider_confirmed_deleted')

    def test_foreign_asset_or_url_never_downloaded_or_deleted(self):
        for overrides in ({'public_id': 'someone-elses-image'},
                          {'secure_url': 'https://foreign.invalid/image.png'},
                          {'asset_id': ''}):
            calls = []
            def handler(request):
                calls.append(request)
                return httpx.Response(200, json=uploaded(**overrides))
            report, _ = self.exercise(handler)
            self.assertEqual(len(calls), 1)
            self.assertFalse(report['passed'])
            self.assertEqual(report['cleanup'], 'not_started')

    def test_upload_timeout_is_uncertain_without_retry_or_cleanup(self):
        calls = []
        def handler(request):
            calls.append(request)
            raise httpx.ReadTimeout('private raw message', request=request)
        report, _ = self.exercise(handler)
        self.assertEqual(len(calls), 1)
        self.assertEqual(report['upload'], 'outcome_uncertain')
        self.assertEqual(report['cleanup'], 'not_started')
        self.assertNotIn('private raw message', str(report))

    def test_download_failure_still_cleans_confirmed_own_asset(self):
        def handler(request):
            if request.url.path.endswith('/upload'):
                return httpx.Response(200, json=uploaded())
            if request.method == 'GET':
                return httpx.Response(200, content=b'wrong bytes')
            return httpx.Response(200, json={'result': 'ok'})
        report, _ = self.exercise(handler)
        self.assertFalse(report['passed'])
        self.assertEqual(report['cleanup'], 'provider_confirmed_deleted')

    def test_cleanup_timeout_does_not_retry_or_claim_success(self):
        calls = []
        def handler(request):
            calls.append(request)
            if request.url.path.endswith('/upload'):
                return httpx.Response(200, json=uploaded())
            if request.method == 'GET':
                return httpx.Response(200, content=probe.png())
            raise httpx.ReadTimeout('private', request=request)
        report, _ = self.exercise(handler)
        self.assertFalse(report['passed'])
        self.assertEqual(report['cleanup'], 'outcome_uncertain')
        self.assertEqual(len(calls), 3)
