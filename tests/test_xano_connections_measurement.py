import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import httpx

from Codeboxd_main.services import api
from tools.xano_connections_measurement import ConnectionProbe


class XanoComparisonTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.client = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200)))
        self.addCleanup(self.client.close)
        self.probe = ConnectionProbe(self.client, 'https://fixture.test/auth', 'https://fixture.test/social',
                                     Path(self.tmp.name)/'result.json', pause=0)
        self.probe.token, self.probe.owner = 'PRIVATE_TOKEN', 7
        self.original = httpx.AsyncClient
        self.requests = []
        self.wrong_owner = False

    def factory(self, *args, **kwargs):
        def respond(request):
            self.requests.append(request)
            if request.url.path.endswith('/profiles/7'):
                data = {'profile': {'user_id': 7, 'email': 'PRIVATE_EMAIL'}}
            elif request.url.path.endswith('/library'):
                data = {'items': [{'user_id': 8 if self.wrong_owner else 7, 'review': 'PRIVATE_REVIEW'}]}
            else:
                data = [{'body': 'PRIVATE_POST'}]
            return httpx.Response(200, json=data)
        kwargs['transport'] = httpx.MockTransport(respond)
        return self.original(*args, **kwargs)

    def base(self, group):
        return 'https://fixture.test/'+('auth' if group == 'auth' else 'social')

    async def test_five_pairs_preserve_content_export_no_values_and_count_physical_reads(self):
        with patch.object(api, 'base_url', side_effect=self.base), \
             patch.object(api, '_new_api_client', side_effect=self.factory):
            await self.probe.compare()
        self.assertTrue(self.probe.report['passed'])
        self.assertEqual(self.probe.calls, 30)
        self.assertEqual(len(self.requests), 30)
        self.assertTrue(all(request.method == 'GET' for request in self.requests))
        self.assertEqual(len(self.probe.report['checks']), 5)
        self.assertNotIn('PRIVATE', json.dumps(self.probe.report))
        self.assertEqual(self.probe.report['summary']['pooled']['calls_per_sample'], [3]*5)

    async def test_request_budget_stops_before_network(self):
        self.probe.calls = 39
        with patch.object(api, 'base_url', side_effect=self.base), \
             patch.object(api, '_new_api_client', side_effect=self.factory):
            with self.assertRaises(RuntimeError):
                await self.probe.compare()
        self.assertFalse(self.requests)
        self.assertFalse(self.probe.report['passed'])

    async def test_wrong_owner_stops_without_exporting_private_payload_or_continuing(self):
        self.wrong_owner = True
        with patch.object(api, 'base_url', side_effect=self.base), \
             patch.object(api, '_new_api_client', side_effect=self.factory):
            with self.assertRaises(RuntimeError):
                await self.probe.compare()
        self.assertEqual(len(self.requests), 2)
        self.assertFalse(self.probe.report['passed'])
        self.assertNotIn('PRIVATE', json.dumps(self.probe.report))
