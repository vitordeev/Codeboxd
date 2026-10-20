"""Opt-in HTTP measurements for isolated local diagnostic processes.

Does not import or modify the application. Never install in a shared server:
the temporary patch observes all httpx async sends in the current process.
Run the offline example with: python -m tools.performance_probe --demo
"""
import argparse
import asyncio
from collections import Counter
from contextlib import contextmanager
import json
import time
from urllib.parse import urlsplit
from unittest.mock import patch

import httpx


_SEGMENTS = frozenset('auth me login signup reset request-reset-link magic-link-login '
    'update_password media profiles profile interactions lists public items posts '
    'feed likes comments follows discussion like reports admin users dashboard '
    'stats activity catalog movies series movie tv anime search discover popular '
    'top_rated now_playing upcoming recommendations videos watch providers '
    'api edge works editions subjects translate v2'.split())


def safe_endpoint(url: str) -> str:
    """Keep known route words only; omit host, query and all identifiers."""
    parts = urlsplit(str(url)).path.split('/')
    return '/' + '/'.join(part if part in _SEGMENTS else '{value}'
                          for part in parts if part)


def service_name(url: str) -> str:
    host = (urlsplit(str(url)).hostname or '').lower()
    for domain, name in (('xano.io', 'xano'), ('xano.com', 'xano'),
                         ('themoviedb.org', 'tmdb'), ('kitsu.io', 'kitsu'),
                         ('openlibrary.org', 'open-library'), ('deepl.com', 'deepl')):
        if host == domain or host.endswith('.' + domain):
            return name
    return 'other'


class HttpProbe:
    """Count physical httpx sends, including application-level retries.

    No headers, payloads, raw URLs, response bodies or exception messages are
    retained. Redirect hops inside one send are not counted separately. Metrics
    are in-memory only; duration includes body reading for non-streamed sends.
    """

    def __init__(self, max_events: int = 2000):
        if max_events < 1:
            raise ValueError('max_events must be positive')
        self.max_events = max_events
        self.events = []
        self.total = 0
        self.counts = Counter()
        self.statuses = Counter()
        self.started = None
        self.elapsed_ms = 0.0

    @contextmanager
    def capture(self):
        if self.started is not None:
            raise RuntimeError('Use a new probe for each capture')
        self.started = time.perf_counter()
        original = httpx.AsyncClient.send

        async def measured(client, request, *args, **kwargs):
            start = time.perf_counter()
            # Sanitize immediately; never retain the request or raw URL.
            service = service_name(str(request.url))
            endpoint = safe_endpoint(str(request.url))
            method = request.method if request.method in (
                'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS') else 'OTHER'
            status = 0
            outcome = 'interrupted'
            try:
                response = await original(client, request, *args, **kwargs)
                status = response.status_code
                outcome = 'response'
                return response
            except httpx.RequestError:
                outcome = 'network-error'
                raise
            finally:
                self.total += 1
                self.counts[service] += 1
                self.statuses[str(status)] += 1
                if len(self.events) < self.max_events:
                    self.events.append(dict(service=service, endpoint=endpoint,
                        method=method, status=status, outcome=outcome,
                        offset_ms=round((start-self.started)*1000, 3),
                        duration_ms=round((time.perf_counter()-start)*1000, 3)))

        try:
            with patch.object(httpx.AsyncClient, 'send', measured):
                yield self
        finally:
            self.elapsed_ms = (time.perf_counter()-self.started)*1000

    def report(self):
        return dict(schema_version=1, scope='isolated-process-httpx',
            elapsed_ms=round(self.elapsed_ms, 3), total_requests=self.total,
            rate_limited=self.statuses['429'], services=dict(self.counts),
            statuses=dict(self.statuses), dropped_events=self.total-len(self.events),
            events=[dict(event) for event in self.events])


async def demo():
    """Two synthetic responses; no DNS, account, email or network access."""
    attempts = 0

    async def respond(request):
        nonlocal attempts
        attempts += 1
        return httpx.Response(429 if attempts == 1 else 200, json={})

    probe = HttpProbe()
    with probe.capture():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            await client.get('https://example.invalid/media')
            await client.get('https://example.invalid/media')
    return {'validation_layer': 'simulated', **probe.report()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true', required=True,
                        help='Run offline example and print sanitized JSON')
    parser.parse_args()
    print(json.dumps(asyncio.run(demo()), indent=2))
