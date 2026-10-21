"""Integration tests for the offline measurement harness, not browser benchmarks."""
import json
import unittest

from tools.login_performance_scenario import run_sample


class LoginScenarioTests(unittest.IsolatedAsyncioTestCase):
    async def test_success_records_five_calls_and_one_session_check(self):
        result = await run_sample()
        self.assertEqual(result['total_requests'], 5)
        self.assertEqual(sum(e['endpoint'] == '/auth/me' for e in result['events']), 1)
        self.assertTrue(result['profile_loaded'])
        self.assertFalse(result['busy_after'])
        self.assertFalse(result['error_visible'])
        for secret in ('synthetic-token', 'synthetic-user', 'synthetic-password', 'example.invalid'):
            self.assertNotIn(secret, json.dumps(result))

    async def test_profile_detail_is_published_before_slow_references(self):
        result = await run_sample('slow-references', delay_ms=30)
        events = result['events']
        detail = next(e for e in events if e['endpoint'] == '/profiles/{value}')
        for event in events:
            if event['endpoint'] in ('/media', '/profiles'):
                self.assertLess(detail['offset_ms'],event['offset_ms'])
        self.assertLess(result['milestones']['profile_primary_ms'],
                        result['milestones']['login_to_profile_handler_ms'])
        self.assertTrue(result['profile_loaded'])

    async def test_login_rate_limit_does_not_retry_or_navigate(self):
        result = await run_sample('login-429')
        self.assertEqual(result['total_requests'], 1)
        self.assertEqual(result['rate_limited'], 1)
        self.assertFalse(result['redirected'])
        self.assertFalse(result['profile_loaded'])
        self.assertTrue(result['error_visible'])

    async def test_session_rate_limit_keeps_identity_and_still_loads_profile(self):
        result = await run_sample('profile-session-429')
        self.assertTrue(result['identity_retained'])
        self.assertTrue(result['profile_loaded'])
        self.assertTrue(result['error_visible'])
        self.assertEqual(result['rate_limited'], 1)
        self.assertEqual(result['total_requests'], 6)

    async def test_reference_rate_limit_preserves_profile_without_retries(self):
        result = await run_sample('references-429')
        self.assertTrue(result['profile_loaded'])
        self.assertTrue(result['error_visible'])
        self.assertFalse(result['busy_after'])
        self.assertEqual(result['total_requests'], 5)
        self.assertEqual(result['rate_limited'], 1)

    async def test_five_quick_profile_visits_reuse_identity_and_detail(self):
        result=await run_sample(visits=5)
        self.assertEqual(result['total_requests'],5)
        self.assertEqual(sum(e['endpoint']=='/auth/me' for e in result['events']),1)
        self.assertEqual(sum(e['endpoint']=='/profiles/{value}' for e in result['events']),1)
