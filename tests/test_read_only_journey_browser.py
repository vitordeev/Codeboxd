import json
import threading
import time
import unittest
from http.cookiejar import CookieJar
from http.server import ThreadingHTTPServer
from unittest.mock import patch

import httpx

from Codeboxd_main.services.api import _NoCookies
from tools.real_login_measurement import Measurement, VisitCycle
from tools.read_only_journey_browser import allowed_read, preflight_data, proxy_handler, summarize, require_free_port


class ReadOnlyJourneyTests(unittest.TestCase):
    def test_occupied_port_is_refused_instead_of_attaching_to_another_app(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), type('Handler', (), {}))
        try:
            with self.assertRaisesRegex(RuntimeError, '^test_port_in_use$'):
                require_free_port(server.server_port)
        finally:
            server.server_close()

    def test_unknown_port_state_fails_closed(self):
        with patch('tools.read_only_journey_browser.psutil.net_connections', side_effect=OSError):
            with self.assertRaisesRegex(RuntimeError, '^test_port_state_unknown$'):
                require_free_port()

    def test_allowlist_accepts_reads_and_only_login_post(self):
        for path in ('/auth/auth/me', '/social/library?after_id=0', '/social/feed?per_page=20',
                     '/social/media/9', '/social/profiles/7', '/social/lists/public',
                     '/social/lists/12/items', '/social/interactions', '/social/likes'):
            self.assertTrue(allowed_read('GET', path), path)
        self.assertTrue(allowed_read('POST', '/auth/auth/login'))
        for method, path in (('GET', '/auth/reset/request-reset-link'),
                             ('POST', '/social/posts'), ('PUT', '/social/lists/1'),
                             ('DELETE', '/social/posts/1'), ('PATCH', '/social/profile'),
                             ('GET', 'https://other.test/social/feed'), ('GET', '//other.test/social/feed'),
                             ('GET', '/social/feed?private=secret'), ('GET', '/social/../feed'),
                             ('POST', '/auth/auth/login?retry=1')):
            self.assertFalse(allowed_read(method, path), (method, path))

    def test_preflight_refuses_admin_missing_or_legacy_lists_and_requires_existing_movie(self):
        user = dict(id=7, role='member', account_status='active')
        lists = [dict(user_id=7, title=title) for title in ('Quero ver / ler', 'Já assisti / li')]
        media = [dict(id=9, media_type='movie', title='PRIVATE_TITLE')]
        self.assertEqual(preflight_data(user, lists, media), (9, 'PRIVATE_TITLE'))
        for data in ((dict(user, role='admin'), lists, media), (user, lists[:1], media),
                     (user, lists+[dict(user_id=7, title='Jã¡ assisti / li')], media),
                     (user, lists, [])):
            with self.assertRaises(RuntimeError):
                preflight_data(*data)

    def test_stale_snapshot_cannot_complete_cycle_and_raw_content_is_not_retained(self):
        cycle = VisitCycle()
        def frame(data):
            return '42'+json.dumps(['event', {'delta': {'test.social_state': data}}])
        cycle.received(frame({'busy': False, 'profile': {'username': 'PRIVATE_USER'}}))
        self.assertFalse(cycle.metrics()['cycle_finished'])
        cycle.received(frame({'busy': True}))
        cycle.received(frame({'busy': False, 'profile': {'username': 'PRIVATE_USER'}}))
        self.assertTrue(cycle.metrics()['cycle_finished'])
        self.assertNotIn('PRIVATE_USER', str(vars(cycle)))

    def proxy(self, status=200):
        self.seen = []
        def respond(request):
            self.seen.append(request)
            return httpx.Response(status, headers={'Retry-After': '20',
                'Set-Cookie': 'private=fixture; Path=/'}, json={'body': 'PRIVATE_PAYLOAD'})
        outbound = httpx.Client(transport=httpx.MockTransport(respond), cookies=CookieJar(policy=_NoCookies()))
        measurement = Measurement(max_requests=3)
        server = ThreadingHTTPServer(('127.0.0.1', 0), proxy_handler(measurement,
            {'auth': 'https://fixture.test/auth', 'social': 'https://fixture.test/social'}, outbound))
        server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        def cleanup():
            server.shutdown(); server.server_close(); thread.join(timeout=2); outbound.close()
        self.addCleanup(cleanup)
        return 'http://127.0.0.1:'+str(server.server_port), measurement

    def test_proxy_blocks_mutations_before_network_and_preserves_no_payload(self):
        base, measurement = self.proxy()
        response = httpx.post(base+'/social/posts', json={'body': 'PRIVATE_DRAFT'})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.seen)
        self.assertEqual(measurement.stop_reason, 'blocked-non-read-request')
        self.assertNotIn('PRIVATE', json.dumps(measurement.report()))

    def test_proxy_429_stops_further_outbound_requests_and_sanitizes_identity(self):
        base, measurement = self.proxy(429)
        with httpx.Client() as client:
            response = client.get(base+'/social/profiles/77', headers={'Authorization': 'Bearer PRIVATE_TOKEN'})
            self.assertEqual(response.status_code, 429)
            client.get(base+'/social/profiles/77')
        self.assertEqual(len(self.seen), 1)
        self.assertEqual(measurement.stop_reason, 'remote-429')
        report = json.dumps(measurement.report())
        for private in ('PRIVATE', '/profiles/77'):
            self.assertNotIn(private, report)

    def test_proxy_does_not_forward_cookies_or_keep_authorization_between_accounts(self):
        base, measurement = self.proxy()
        with httpx.Client() as client:
            client.get(base+'/social/feed', headers={'Authorization': 'Bearer first', 'Cookie': 'private=browser'})
            client.get(base+'/social/feed', headers={'Authorization': 'Bearer second'})
            client.get(base+'/social/feed')
        self.assertEqual([request.headers.get('Authorization', '') for request in self.seen],
                         ['Bearer first', 'Bearer second', ''])
        self.assertTrue(all('Cookie' not in request.headers for request in self.seen))

    def test_proxy_budget_blocks_before_next_outbound_read(self):
        base, measurement = self.proxy()
        measurement.max_requests = 1
        with httpx.Client() as client:
            self.assertEqual(client.get(base+'/social/feed').status_code, 200)
            self.assertEqual(client.get(base+'/social/feed').status_code, 429)
        self.assertEqual(len(self.seen), 1)
        self.assertEqual(measurement.stop_reason, 'request-budget')

    def test_summary_uses_only_completed_rows_and_does_not_fabricate_five_samples(self):
        rows = [dict(width=390, step='feed', primary_ms=10, finished_ms=20, warning_visible=False),
                dict(width=390, step='feed', primary_ms=20, finished_ms=40, warning_visible=True)]
        summary = summarize(rows)[0]
        self.assertEqual(summary['samples'], 2)
        self.assertEqual(summary['median_finished_ms'], 30)
        self.assertEqual(summary['worst_finished_ms'], 40)
        self.assertEqual(summary['warnings'], 1)
