"""Measure public home handlers in isolation; no account or running server."""
import argparse
import asyncio
import json
import logging
from pathlib import Path
import statistics
import time
from unittest.mock import AsyncMock, patch

from dotenv import load_dotenv
import reflex as rx

from Codeboxd_main.services import catalog
from Codeboxd_main.state.social import SocialState
from tools.performance_probe import HttpProbe

ROOT = Path(__file__).resolve().parents[1]


async def sample():
    root = rx.State(_reflex_internal_init=True)
    root.router.url.path = '/'
    state = root.get_substate(SocialState.get_full_name().split('.'))
    probe = HttpProbe()
    started = time.perf_counter()
    primary_ms = None
    # Scope deliberately excludes Xano/community and authorization, which need
    # separate measurements. All catalog calls still use the actual transport.
    with probe.capture(), \
            patch.object(SocialState, '_validate_navigation_session', new=AsyncMock()), \
            patch.object(SocialState, '_load_media', new=AsyncMock()):
        async for _ in state._home_updates():
            if state.featured_items and primary_ms is None:
                primary_ms = round((time.perf_counter()-started)*1000, 3)
    counts = {key: len(value) for key, value in state.home_collections.items()}
    return dict(primary_ms=primary_ms, finished=state.home_loaded,
                complete=bool(primary_ms is not None and not state.notice
                              and not state.home_collection_errors
                              and all(key in counts for key in catalog.HOME_COLLECTIONS)),
                shelves=counts, failed_shelves=len(state.home_collection_errors),
                warning=bool(state.notice), **probe.report())


async def run(samples=5, timeout=90):
    if not 1 <= samples <= 5:
        raise ValueError('Use one to five sample pairs')
    report = dict(layer='real-public-provider-handlers', browser_measured=False,
                  xano_measured=False, samples=[], complete=False)
    for index in range(samples):
        catalog._public_cache.clear()
        catalog._kitsu_cache.clear()
        for phase in ('cold', 'warm'):
            try:
                row = await asyncio.wait_for(sample(), timeout=timeout)
            except Exception as error:
                report['failure_type'] = type(error).__name__
                return report
            row.update(index=index+1, phase=phase)
            report['samples'].append(row)
            if row['rate_limited'] or not row['complete']:
                report['failure_type'] = 'rate_limit' if row['rate_limited'] else 'partial_content'
                return report
    report['complete'] = True
    report['summary'] = {}
    for phase in ('cold', 'warm'):
        rows = [row for row in report['samples'] if row['phase'] == phase]
        report['summary'][phase] = {
            metric: dict(median=statistics.median(row[metric] for row in rows),
                         worst=max(row[metric] for row in rows))
            for metric in ('primary_ms', 'elapsed_ms', 'total_requests')}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--samples', type=int, choices=range(1, 6), default=5)
    args = parser.parse_args()
    # Reserve evidence before making requests; never overwrite prior runs.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as output:
        load_dotenv(ROOT/'.env', override=False)
        logging.getLogger('Codeboxd_main.services.catalog').setLevel(logging.CRITICAL)
        result = asyncio.run(run(args.samples))
        output.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(complete=result['complete'], samples=len(result['samples']),
                          failure_type=result.get('failure_type'), summary=result.get('summary'))))
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
