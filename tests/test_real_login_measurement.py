"""Offline safety/accuracy regressions for the approved real measurement tool."""
from io import BytesIO
import json
import time
import unittest

import httpx

from tools.real_login_measurement import Measurement, VisitCycle, allowed_request, handler_class


class RealMeasurementTests(unittest.TestCase):
    def test_old_hydration_cannot_complete_current_visit(self):
        cycle=VisitCycle()
        def frame(delta):
            return '42'+json.dumps(['event',{'delta':{'root.social_state':delta}}])
        cycle.received(frame({'busy_rx_state_':False,'profile_rx_state_':{'username':'private-old'}}))
        self.assertFalse(cycle.metrics()['cycle_started'])
        self.assertFalse(cycle.metrics()['cycle_finished'])
        self.assertIsNone(cycle.primary_at)
        cycle.received(frame({'busy_rx_state_':True}))
        cycle.received(frame({'profile_rx_state_':{'username':'private-new'}}))
        cycle.received(frame({'busy_rx_state_':False}))
        self.assertTrue(cycle.metrics()['cycle_finished'])
        self.assertIsNotNone(cycle.primary_at)
        self.assertNotIn('private',json.dumps(cycle.metrics()))
        cycle.arm()
        self.assertIsNone(cycle.primary_at)
        self.assertFalse(cycle.metrics()['cycle_finished'])

    def test_only_approved_login_and_profile_reads_are_allowed(self):
        for method,path in [('POST','/auth/auth/login'),('GET','/auth/auth/me'),
                            ('GET','/social/media?page=2&per_page=100'),
                            ('GET','/social/profiles/42')]:
            self.assertTrue(allowed_request(method,path))
        for method,path in [('POST','/social/media'),('GET','/auth/reset/request-reset-link'),
                            ('GET','/social/profiles/7/../8'),('GET','https://other.invalid/social/media'),
                            ('GET','/social/media?token=private'),('PUT','/social/profile')]:
            self.assertFalse(allowed_request(method,path))

    def test_first_rate_limit_blocks_new_requests(self):
        metric=Measurement()
        self.assertTrue(metric.reserve('GET'))
        metric.record('GET','/social/profiles/123',429,time.perf_counter(),'20')
        self.assertFalse(metric.reserve('GET'))
        report=metric.report()
        self.assertEqual(report['stop_reason'],'remote-429')
        self.assertEqual(report['events'][0]['retry_after_seconds'],20)
        self.assertNotIn('123',json.dumps(report))

    def test_login_attempt_and_total_limits(self):
        metric=Measurement(max_requests=2)
        self.assertTrue(metric.reserve('GET'))
        self.assertTrue(metric.reserve('GET'))
        self.assertFalse(metric.reserve('GET'))
        metric=Measurement()
        for _ in range(3): self.assertTrue(metric.reserve('POST'))
        self.assertFalse(metric.reserve('POST'))

    def proxy(self,metric,method,path,transport):
        proxy_type=handler_class(metric,{'auth':'https://example.invalid','social':'https://example.invalid'},transport)
        proxy=proxy_type.__new__(proxy_type)
        proxy.command=method
        proxy.path=path
        body=b'{"password":"private-password"}'
        proxy.headers={'Authorization':'Bearer private-token','Content-Length':str(len(body))}
        proxy.rfile=BytesIO(body)
        replies=[]
        proxy.reply=lambda *args: replies.append(args)
        proxy.forward()
        return replies

    def test_forwarding_does_not_export_credentials_or_response(self):
        metric=Measurement()
        seen=[]
        def upstream(request):
            seen.append(request.headers.get('Authorization'))
            return httpx.Response(200,json={'authToken':'private-response-token'})
        replies=self.proxy(metric,'POST','/auth/auth/login',httpx.MockTransport(upstream))
        self.assertEqual(replies[0][0],200)
        self.assertEqual(seen,['Bearer private-token'])
        output=json.dumps(metric.report())
        for secret in ('private-token','private-password','private-response-token','example.invalid'):
            self.assertNotIn(secret,output)

    def test_unapproved_operation_never_reaches_upstream(self):
        def forbidden(request): self.fail('Unapproved remote request')
        metric=Measurement()
        replies=self.proxy(metric,'POST','/social/media',httpx.MockTransport(forbidden))
        self.assertEqual(replies[0][0],403)
        self.assertEqual(metric.total,0)

    def test_no_follow_redirect_to_another_destination(self):
        calls=[]
        def redirect(request):
            calls.append(True)
            return httpx.Response(302,headers={'Location':'https://other.invalid/secret'})
        replies=self.proxy(Measurement(),'GET','/social/media',httpx.MockTransport(redirect))
        self.assertEqual(replies[0][0],302)
        self.assertEqual(len(calls),1)
