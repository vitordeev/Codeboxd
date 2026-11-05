"""Measure actual own-profile handlers on a normally authenticated test account."""
import argparse
import asyncio
import json
from pathlib import Path
import statistics
import time

from dotenv import load_dotenv
import reflex as rx

from Codeboxd_main.services.api import api_connection_pool
from Codeboxd_main.state.social import SocialState
from tools.performance_probe import HttpProbe
from tools.read_only_journey_browser import fixture_credentials, ROOT


async def sample(state, user_id):
    probe = HttpProbe()
    start = time.perf_counter()
    primary = None
    with probe.capture():
        async for _ in state._profile_updates():
            if state.profile.get('user_id') == str(user_id) and state.profile.get('display_name') and primary is None:
                primary = round((time.perf_counter() - start) * 1000, 3)
    complete = (primary is not None and state.user_role == 'member' and not state.notice
                and not state.profile_activity_error and not state.profile_people_error
                and len(state.profile_activity) == 1)
    return dict(primary_ms=primary, complete=complete, activity_count=len(state.profile_activity), **probe.report())


async def run(user):
    report = {'layer': 'real_python_xano_profile_handlers', 'browser_measured': False,
              'samples': [], 'complete': False, 'data_mutation_requests': 0,
              'authentication_audit_events_retained': True, 'between_pair_pause_seconds': 22}
    async with api_connection_pool():
        for index in range(5):
            if index:
                await asyncio.sleep(22)
            root = rx.State(_reflex_internal_init=True)
            root.router.url.path = '/conta'
            state = root.get_substate(SocialState.get_full_name().split('.'))
            state.session_token = user['token']
            for phase in ('cold', 'warm'):
                try:
                    row = await asyncio.wait_for(sample(state, user['id']), timeout=60)
                except Exception as exc:
                    report['failure_type'] = type(exc).__name__
                    return report
                row.update(index=index + 1, phase=phase)
                report['samples'].append(row)
                print(json.dumps({'index': index + 1, 'phase': phase, 'complete': row['complete'],
                                  'requests': row['total_requests'], 'rate_limited': row['rate_limited']}), flush=True)
                if not row['complete'] or row['rate_limited']:
                    report['failure_type'] = 'rate_limit' if row['rate_limited'] else 'partial_content'
                    return report
    report['summary'] = {}
    for phase in ('cold', 'warm'):
        rows = [r for r in report['samples'] if r['phase'] == phase]
        report['summary'][phase] = {key: {'median': statistics.median(r[key] for r in rows),
                                              'worst': max(r[key] for r in rows)}
                                    for key in ('primary_ms', 'elapsed_ms', 'total_requests')}
    report['complete'] = True
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture-journal', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve previous evidence')
    load_dotenv(ROOT / '.env', override=False)
    user = fixture_credentials(args.fixture_journal)
    result = asyncio.run(run(user))
    args.output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'complete': result['complete'], 'samples': len(result['samples']),
                      'failure_type': result.get('failure_type'), 'summary': result.get('summary')}))
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
