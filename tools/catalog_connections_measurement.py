"""Compare real public TMDB transport with/without pooling; no accounts or writes."""
import argparse
import asyncio
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path
import statistics
import time

from Codeboxd_main.services import catalog
from tools.performance_probe import HttpProbe


async def measure(samples=5):
    if not 1 <= samples <= 5:
        raise ValueError('Use one to five pairs')
    report = dict(layer='real-public-tmdb-transport', browser_measured=False,
                  samples=[], complete=False)
    for index in range(samples):
        fingerprints = []
        # Alternate order to avoid always giving either mode the first network visit.
        for pooled in ((False, True) if index % 2 == 0 else (True, False)):
            catalog._public_cache.clear()
            probe = HttpProbe()
            started = time.perf_counter()
            row = dict(index=index+1, pooled=pooled, selections={})
            identities = {}
            try:
                async with (catalog.catalog_connection_pool() if pooled else nullcontext()):
                    with probe.capture():
                        for key in ('movies_now', 'movies_rated', 'movies_upcoming'):
                            items = await catalog.home_collection(key)
                            if not items:
                                raise RuntimeError('empty_selection')
                            row['selections'][key] = len(items)
                            identities[key] = [item['identity_key'] for item in items]
                            if probe.statuses.get('429'):
                                raise RuntimeError('rate_limit')
            except Exception as error:
                row['failure_type'] = type(error).__name__
            row.update(probe.report())
            row['elapsed_ms'] = round((time.perf_counter()-started)*1000, 3)
            row['content_fingerprint'] = hashlib.sha256(json.dumps(identities, sort_keys=True).encode()).hexdigest()
            report['samples'].append(row)
            if row.get('failure_type'):
                return report
            fingerprints.append(row['content_fingerprint'])
        if len(set(fingerprints)) != 1:
            report['failure_type'] = 'content_changed_between_modes'
            return report
    report['complete'] = True
    report['summary'] = {}
    for pooled in (False, True):
        rows = [row for row in report['samples'] if row['pooled'] == pooled]
        report['summary']['pooled' if pooled else 'legacy'] = dict(
            median_ms=statistics.median(row['elapsed_ms'] for row in rows),
            worst_ms=max(row['elapsed_ms'] for row in rows),
            calls_per_sample=[row['total_requests'] for row in rows])
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x', encoding='utf-8') as output:
        result = asyncio.run(measure())
        output.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(complete=result['complete'], summary=result.get('summary'),
                          failure_type=result.get('failure_type'))))
    raise SystemExit(0 if result['complete'] else 1)
