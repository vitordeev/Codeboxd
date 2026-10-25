"""Offline comparison of feed revisits; never contacts Xano or starts a server."""
import argparse
import asyncio
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import statistics
import sys
import time
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reflex as rx
from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


async def measure(missing_likes=False):
    samples = []
    for _ in range(5):
        state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        state.router.url.path = '/feed'
        state.session_token = 'offline-fixture'
        state.user_id = 7
        calls = Counter()
        post = dict(id=1, user_id=7, body='Fixture', created_at=1700000000000,
                    media_id=9, likes_count=1, comments_count=2)
        responses = {
            '/media': [dict(id=9, title='Fixture', media_type='movie')],
            '/profiles': [dict(user_id=7, display_name='Fixture')],
            '/feed': [post], '/posts': [post], '/likes': [dict(post_id=1)],
        }

        async def request(method, path, **kwargs):
            assert method == 'GET'
            calls[path] += 1
            await asyncio.sleep(0.01)
            if missing_likes and path == '/likes':
                raise APIError('Unavailable route', 404)
            return deepcopy(responses[path])

        with patch('Codeboxd_main.state.social.request', side_effect=request), \
             patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)):
            await state.load_feed()
            expected = deepcopy(state.posts)
            calls.clear()
            started = time.perf_counter()
            for _ in range(5):
                await state.load_feed()
                assert state.posts == expected
            samples.append(dict(milliseconds=round((time.perf_counter()-started)*1000, 3),
                                calls=dict(calls), total_calls=sum(calls.values())))
    times = [sample['milliseconds'] for sample in samples]
    return dict(layer='offline-synthetic-http', simulated_latency_ms=10,
                revisits_per_sample=5, missing_likes=missing_likes,
                samples=samples, median_ms=statistics.median(times), worst_ms=max(times),
                posts_unchanged=True)


async def main(output):
    results = [await measure(), await measure(missing_likes=True)]
    output.write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
    for row in results:
        print(json.dumps({k: v for k, v in row.items() if k != 'samples'} | {
            'calls_per_sample': [sample['total_calls'] for sample in row['samples']]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    asyncio.run(main(parser.parse_args().output))
