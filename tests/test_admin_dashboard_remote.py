import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import httpx

from tools.admin_dashboard_remote import DashboardProbe


class DashboardAcceptanceTests(unittest.TestCase):
    def exercise(self, change=None, pending=True, incomplete_inventory=False):
        def handler(request):
            if request.url.host == 'metadata.test':
                if request.url.path == '/table':
                    return httpx.Response(200, json=[dict(id=i, name=name) for i, name in
                        enumerate(('user', 'post', 'media', 'report'), 1)])
                table = int(request.url.path.split('/')[2])
                items = [dict(id=11, status='pending'), dict(id=12, status='pending'),
                         dict(id=13, status='resolved')] if pending else []
                totals = {1: 3, 2: 2, 3: 5, 4: len(items)}
                if table == 4 and incomplete_inventory:
                    items = []
                return httpx.Response(200, json=dict(items=items if table == 4 else
                    [{'password': 'PRIVATE_METADATA_HASH'}], itemsTotal=totals[table], nextPage=None))
            if 'Authorization' not in request.headers:
                return httpx.Response(401, json={})
            page = int(request.url.params.get('page', 1))
            reports_page = int(request.url.params.get('reports_page', 1))
            payload = dict(users_total=3, posts_total=2, media_total=5, reports_pending=2 if pending else 0,
                recent_posts=[dict(id=3-page, user_id=7, created_at=1000)],
                pending_reports=[dict(id=13-reports_page, created_at=1000, target_type='post', reason='spam')] if pending else [],
                recent_posts_pagination=dict(total=2, page=page, per_page=1, next_page=2 if page == 1 else None),
                pending_reports_pagination=dict(total=2 if pending else 0, page=reports_page,
                    per_page=1, next_page=2 if pending and reports_page == 1 else None))
            if change:
                change(payload)
            return httpx.Response(200, json=payload)
        with tempfile.TemporaryDirectory() as tmp, httpx.Client(transport=httpx.MockTransport(handler)) as client:
            path = Path(tmp)/'report.json'
            probe = DashboardProbe(client, 'https://auth.test', 'https://social.test', path, pause=0)
            probe.token = 'PRIVATE_AUTH_TOKEN'
            with patch('tools.admin_dashboard_remote.metadata_config', return_value=(
                'https://metadata.test', {'Authorization': 'Bearer PRIVATE_METADATA_TOKEN'})):
                error = None
                try:
                    probe.run()
                except RuntimeError as caught:
                    error = str(caught)
            saved = path.read_text()
            self.assertNotIn('PRIVATE', saved)
            return json.loads(saved), error

    def test_totals_pages_and_independent_inventory_pass_without_exporting_payload(self):
        report, error = self.exercise()
        self.assertIsNone(error)
        self.assertTrue(report['passed'])
        self.assertTrue(report['pending_nonempty_real'])
        self.assertTrue(all(row['method'] == 'GET' for row in report['requests']))
        self.assertTrue(any(row['scenario'] == 'independent_counts_stable' for row in report['checks']))

    def test_real_empty_queue_is_distinguished_from_nonempty_pagination(self):
        report, error = self.exercise(pending=False)
        self.assertIsNone(error)
        self.assertTrue(report['passed'])
        self.assertFalse(report['pending_nonempty_real'])

    def test_wrong_or_boolean_counts_cannot_be_accepted(self):
        for wrong in (999, False):
            with self.subTest(wrong=wrong):
                report, error = self.exercise(lambda data: data.update(users_total=wrong))
                self.assertEqual(error, 'contract_check_failed')
                self.assertFalse(report['passed'])
                self.assertEqual(report['checks'][-1]['scenario'], 'dashboard_counts_match_storage')

    def test_old_unpaged_endpoint_cannot_pass(self):
        report, error = self.exercise(lambda data: data.pop('recent_posts_pagination'))
        self.assertEqual(error, 'contract_check_failed')
        self.assertFalse(report['passed'])
        self.assertEqual(report['checks'][-1]['scenario'], 'recent_posts_pagination_present')

    def test_incomplete_inventory_cannot_look_like_an_empty_pending_queue(self):
        report, error = self.exercise(incomplete_inventory=True)
        self.assertEqual(error, 'contract_check_failed')
        self.assertFalse(report['passed'])
        self.assertEqual(report['checks'][-1]['scenario'], 'metadata_reports_complete')

    def test_secret_payload_is_rejected_without_exporting_secret(self):
        report, error = self.exercise(lambda data: data.update(password='PRIVATE_RESPONSE_PASSWORD'))
        self.assertEqual(error, 'contract_check_failed')
        self.assertFalse(report['passed'])
        self.assertEqual(report['checks'][-1]['scenario'], 'dashboard_no_secrets')
