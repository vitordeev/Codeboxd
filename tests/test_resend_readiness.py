import unittest

import httpx

from tools.resend_readiness import provider_error


class ResendReadinessTests(unittest.TestCase):
    def test_restricted_key_is_distinct_from_invalid_key_without_exporting_message(self):
        for name in ('restricted_api_key', 'invalid_api_key'):
            response = httpx.Response(401, json={'name': name, 'message': 'PRIVATE_EMAIL PRIVATE_KEY'})
            self.assertEqual(provider_error(response), name)

    def test_unknown_error_names_or_malformed_bodies_cannot_leak_data(self):
        for body in ({'name': 'PRIVATE_EMAIL'}, {'name': ['PRIVATE_KEY']}, ['PRIVATE_MESSAGE'], {}):
            self.assertEqual(provider_error(httpx.Response(401, json=body)), 'unclassified')
        self.assertEqual(provider_error(httpx.Response(500, text='PRIVATE_BODY')), 'unclassified')

    def test_success_does_not_classify_the_key_as_broken(self):
        self.assertIsNone(provider_error(httpx.Response(200, json={'data': []})))
