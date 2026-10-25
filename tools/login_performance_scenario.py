"""Offline login-to-profile scenario using real state handlers and HTTP transport.

Run from repository root: python -B -m tools.login_performance_scenario
No server, browser, credentials, environment edits or network are required.
"""
import argparse
import asyncio
from collections import Counter
import json
import statistics
import time
from unittest.mock import patch

import httpx
import reflex as rx

from Codeboxd_main.services import api
from Codeboxd_main.state.session import SessionState
from Codeboxd_main.state.social import SocialState
from tools.performance_probe import HttpProbe


CASES = ('success', 'slow-references', 'login-429', 'profile-session-429', 'references-429')


async def run_sample(case='success', delay_ms=50, visits=1):
    if case not in CASES or not 0 <= delay_ms <= 1000:
        raise ValueError('Invalid scenario configuration')
    root = rx.State(_reflex_internal_init=True)
    session = root.get_substate(SessionState.get_full_name().split('.'))
    social = root.get_substate(SocialState.get_full_name().split('.'))
    root.router.url.path = '/conta'
    hits = Counter()
    probe = HttpProbe()
    original_client = httpx.AsyncClient

    async def respond(request):
        path = request.url.path
        hits[path] += 1
        limited = ((case == 'login-429' and path == '/auth/login') or
                   (case == 'profile-session-429' and path == '/auth/me' and hits[path] == 2) or
                   (case == 'references-429' and path == '/media'))
        if case == 'slow-references' and path in ('/media', '/profiles'):
            await asyncio.sleep(delay_ms / 1000)
        if limited:
            return httpx.Response(429, headers={'Retry-After': '20'}, json={})
        payloads = {
            '/auth/login': {'authToken': 'synthetic-token'},
            '/auth/me': {'id': 7, 'role': 'member', 'username': 'synthetic-user'},
            '/media': [], '/profiles': [],
            '/profiles/7': {'profile': {'user_id': 7, 'username': 'synthetic-user',
                'display_name': 'Synthetic'},
                # A media-reference failure is only relevant when activities
                # actually need those references; empty profiles skip /media.
                'interactions': [{'media_id': 9, 'status': 'completed', 'rating': 4.5}]
                    if case == 'references-429' else [],
                'followers': [], 'following': []},
        }
        if path not in payloads:
            raise AssertionError('Unexpected synthetic endpoint')
        return httpx.Response(200, json=payloads[path])

    def local_client(*args, **kwargs):
        # Every application-created client uses MockTransport, including retries.
        kwargs['transport'] = httpx.MockTransport(respond)
        return original_client(*args, **kwargs)

    milestones = {}
    with probe.capture(), patch.object(api, 'base_url', return_value='https://scenario.xano.io'), \
            patch.object(api.httpx, 'AsyncClient', side_effect=local_client):
        started = time.perf_counter()
        redirected = False
        async for event in session.login({'email': 'synthetic@example.invalid',
                                         'password': 'synthetic-password', 'remember': True}):
            if event is not None:
                redirected = True
        milestones['login_handler_ms'] = round((time.perf_counter()-started)*1000, 3)
        if case=='profile-session-429':
            # Exercise revalidation after expiry, rather than the cached post-login visit.
            session._navigation_verified_until=0.0
        if redirected:
            for _ in range(visits):
                async for _ in social.visit('profile'):
                    if social.profile.get('username') and 'profile_primary_ms' not in milestones:
                        milestones['profile_primary_ms']=round((time.perf_counter()-started)*1000,3)
        milestones['login_to_profile_handler_ms'] = round((time.perf_counter()-started)*1000, 3)

    # Export booleans, not identity, credentials or profile contents.
    return dict(case=case, validation_layer='simulated-handlers', cache='cold',
        injected_reference_delay_ms=delay_ms if case == 'slow-references' else 0,
        milestones=milestones, redirected=redirected,
        profile_loaded=bool(social.profile.get('username')),
        identity_retained=bool(session.user_id),
        error_visible=bool(session.error_message or social.notice or social.profile_activity_error or social.profile_people_error),
        busy_after=social.busy, **probe.report())


async def run_suite(samples=5, delay_ms=50):
    if not 1 <= samples <= 20:
        raise ValueError('samples must be between 1 and 20')
    results = []
    for case in CASES:
        rows = [await run_sample(case, delay_ms) for _ in range(samples)]
        times = [row['milestones']['login_to_profile_handler_ms'] for row in rows]
        results.append(dict(case=case, median_ms=statistics.median(times),
                            worst_ms=max(times), samples=rows))
    return dict(validation_layer='simulated-handlers', browser_measured=False,
                remote_measured=False, cases=results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=5, choices=range(1, 21))
    parser.add_argument('--delay-ms', type=int, default=50, choices=range(0, 1001))
    args = parser.parse_args()
    print(json.dumps(asyncio.run(run_suite(args.samples, args.delay_ms)), indent=2))
