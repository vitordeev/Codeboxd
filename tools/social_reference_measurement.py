"""Measure social reference preparation offline; no browser, server or real API."""
import argparse
import asyncio
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reflex as rx
from Codeboxd_main.state.social import SocialState, present_media


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


async def scenario(kind, size, active):
    samples = []
    for _ in range(5):
        state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        state.router.url.path = '/feed' if kind == 'feed' else '/conta'
        state.session_token = 'offline-fixture'
        state.user_id = 7
        state._identity = 7
        calls = Counter()
        media = [dict(id=i+1, title=f'Fixture {i+1}', media_type='book',
                      description='Fictional synopsis. '*50, year=2020) for i in range(size)]
        post = dict(id=1, user_id=7, media_id=1, body='Fixture post', created_at=1700000000000)
        profile = dict(profile=dict(user_id=7, username='fixture', display_name='Fixture'),
                       interactions=[dict(media_id=1, status='completed', rating=4.5)] if active else [],
                       followers=[dict(follower_id=8)], following=[dict(followed_id=8)])
        responses = {'/media': media, '/profiles/7': profile,
                     '/profiles': [dict(user_id=7, display_name='Fixture'),
                                   dict(user_id=8, display_name='Friend')],
                     '/feed': [post], '/posts': [post], '/likes': []}

        async def request(method, path, **kwargs):
            assert method == 'GET'
            calls[path] += 1
            await asyncio.sleep(0.005)
            return deepcopy(responses[path])

        def snapshot():
            if kind == 'feed':
                return dict(posts=state.posts, people=state.people, liked=state.liked_posts,
                            media_ids=sorted(state._media))
            return dict(profile=state.profile, counts=state.profile_counts,
                        activity=state.profile_activity, stats=state.profile_stats,
                        followers=state.followers, following=state.following,
                        following_ids=state.following_ids,
                        loading=[state.profile_activity_loading, state.profile_people_loading],
                        errors=[state.profile_activity_error, state.profile_people_error])

        load = state.load_feed if kind == 'feed' else state.load_profile
        with patch('Codeboxd_main.state.social.request', side_effect=request), \
             patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
             patch.object(SocialState, '_validate_navigation_session', new=AsyncMock(return_value=True)), \
             patch('Codeboxd_main.state.social.present_media', wraps=present_media) as transform:
            phases = {}
            for phase in ('cold', 'warm'):
                calls.clear()
                transform.reset_mock()
                started = time.perf_counter()
                await load()
                elapsed = (time.perf_counter()-started)*1000
                phases[phase] = dict(milliseconds=round(elapsed, 3), calls=dict(calls),
                                     total_calls=sum(calls.values()), transformations=transform.call_count,
                                     catalog_items=len(state.catalog_items),
                                     catalog_json_bytes=len(json.dumps(state.catalog_items).encode()),
                                     output_fingerprint=fingerprint(snapshot()))
            assert phases['cold']['output_fingerprint'] == phases['warm']['output_fingerprint']
            samples.append(phases)
    summary = {}
    for phase in ('cold', 'warm'):
        values = [sample[phase] for sample in samples]
        summary[phase] = dict(median_ms=statistics.median(row['milliseconds'] for row in values),
                             worst_ms=max(row['milliseconds'] for row in values),
                             calls_per_sample=[row['total_calls'] for row in values],
                             transformations_per_sample=[row['transformations'] for row in values],
                             catalog_json_bytes=values[0]['catalog_json_bytes'])
    return dict(kind=kind, media_count=size, has_activity=active, samples=samples, summary=summary)


async def main(output):
    results = [await scenario(kind, size, active)
               for size in (5, 250)
               for kind, active in (('feed', False), ('profile', False), ('profile', True))]
    output.write_text(json.dumps(dict(layer='offline-synthetic-http', latency_ms=5,
                                     results=results), indent=2)+'\n', encoding='utf-8')
    for row in results:
        print(json.dumps({key: value for key, value in row.items() if key != 'samples'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    asyncio.run(main(parser.parse_args().output))
