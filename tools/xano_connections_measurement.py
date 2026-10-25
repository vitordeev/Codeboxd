"""Manual member login and bounded read-only comparison of the app's Xano transport."""
import argparse
import asyncio
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path
import statistics
import time

from Codeboxd_main.services import api
from tools.admin_reads_remote import main
from tools.member_reads_remote import MemberProbe
from tools.performance_probe import HttpProbe


class ConnectionProbe(MemberProbe):
    def run(self):
        asyncio.run(self.compare())

    async def compare(self):
        if not self.token:
            raise RuntimeError('member_session_required')
        # Avoid accidentally measuring a different environment than the login.
        if api.base_url('auth') != self.auth or api.base_url('social') != self.social:
            raise RuntimeError('configured_instance_mismatch')
        self.report.update(layer='real-member-xano-transport', samples=[],
                           browser_measured=False, application_cache_measured=False)
        routes = [('profile', f'/profiles/{self.owner}', None),
                  ('library', '/library', {'after_id': 0}),
                  ('feed', '/feed', {'per_page': 20})]
        for index in range(5):
            fingerprints = []
            for pooled in ((False, True) if index % 2 == 0 else (True, False)):
                probe = HttpProbe()
                row = dict(index=index+1, pooled=pooled, reads=[])
                identities, waited = [], 0
                started = time.perf_counter()
                try:
                    with probe.capture():
                        async with (api.api_connection_pool() if pooled else nullcontext()):
                            for name, path, params in routes:
                                # Reserve enough budget for the app's bounded read retries.
                                if self.calls + probe.total + 3 > 40:
                                    raise RuntimeError('request_budget')
                                wait_started = time.perf_counter()
                                await asyncio.sleep(self.pause)
                                waited += time.perf_counter()-wait_started
                                read_started = time.perf_counter()
                                data = await api.request('GET', path, token=self.token, params=params)
                                duration = round((time.perf_counter()-read_started)*1000, 3)
                                if name == 'profile':
                                    valid = (isinstance(data, dict) and isinstance(data.get('profile'), dict)
                                             and data['profile'].get('user_id') == self.owner)
                                elif name == 'library':
                                    valid = (isinstance(data, dict) and isinstance(data.get('items'), list)
                                             and all(item.get('user_id') == self.owner for item in data['items']))
                                else:
                                    valid = isinstance(data, list) or (isinstance(data, dict)
                                                and isinstance(data.get('items'), list))
                                if not valid:
                                    raise RuntimeError('read_contract_failed')
                                identities.append(hashlib.sha256(json.dumps(data, sort_keys=True).encode()).digest())
                                row['reads'].append(dict(name=name, duration_ms=duration))
                                if probe.statuses.get('429'):
                                    raise RuntimeError('remote_rate_limit')
                except Exception as error:
                    row['failure_type'] = type(error).__name__
                    if isinstance(error, api.APIError):
                        row.update(http_status=error.status, retry_after_seconds=error.retry_after)
                finally:
                    row.update(probe.report())
                    row['active_ms'] = round((time.perf_counter()-started-waited)*1000, 3)
                    self.calls += probe.total
                    self.report['requests'].extend(probe.events)
                    self.report['samples'].append(row)
                    self.save()
                if row.get('failure_type'):
                    raise RuntimeError('comparison_interrupted')
                fingerprints.append(identities)
            # Hashes and private values stay in memory; only equality is exported.
            self.check('pair_'+str(index+1)+'_same_content', fingerprints[0] == fingerprints[1])
        self.report['summary'] = {}
        for pooled in (False, True):
            rows = [row for row in self.report['samples'] if row['pooled'] == pooled]
            self.report['summary']['pooled' if pooled else 'legacy'] = dict(
                median_active_ms=statistics.median(row['active_ms'] for row in rows),
                worst_active_ms=max(row['active_ms'] for row in rows),
                calls_per_sample=[row['total_requests'] for row in rows])
        self.report['passed'] = True
        self.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.output, probe_type=ConnectionProbe,
                                     role_label='de membro para comparação de leitura')))
