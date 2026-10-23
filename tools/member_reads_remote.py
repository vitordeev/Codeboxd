"""Bounded member API measurements with a manual login; exports no payloads."""
import argparse
import asyncio
from pathlib import Path
import statistics

from tools.admin_reads_remote import Probe, main


class MemberProbe(Probe):
    def authenticate(self, email, password):
        response = self.request('POST', self.auth, '/auth/login',
                                json=dict(email=email, password=password))
        if response.status_code != 200:
            return False
        token = response.json().get('authToken')
        if not isinstance(token, str) or not token:
            return False
        me = self.request('GET', self.auth, '/auth/me',
                          headers={'Authorization': 'Bearer '+token})
        user = me.json() if me.status_code == 200 else {}
        if (type(user.get('id')) is int and user['id'] > 0
                and user.get('role') == 'member' and user.get('account_status') == 'active'):
            self.token, self.owner = token, user['id']
            self.report['layer'] = 'real_member_api_reads'
            return True
        return False

    def run(self):
        if not self.token:
            raise RuntimeError('member_session_required')
        routes = [
            ('profile', f'/profiles/{self.owner}', None),
            ('library', '/library', {'after_id': 0}),
            ('lists', '/lists', {'per_page': 20}),
            ('public_lists', '/lists/public', {'per_page': 20}),
            ('feed', '/feed', {'per_page': 20}),
            ('posts', '/posts', {'user_id': self.owner, 'per_page': 20}),
            ('community', '/profiles', {'per_page': 20}),
        ]
        times = {name: [] for name, _, _ in routes}
        for index in range(5):
            for name, path, params in routes:
                data = self.get(name+'_'+str(index+1), path, params)
                # Only validate envelope shape; never persist the returned values.
                if name == 'profile':
                    valid = (isinstance(data, dict) and isinstance(data.get('profile'), dict)
                             and data['profile'].get('user_id') == self.owner)
                elif name == 'library':
                    valid = (isinstance(data, dict) and isinstance(data.get('items'), list)
                             and all(item.get('user_id') == self.owner for item in data['items']))
                else:
                    valid = isinstance(data, list) or (isinstance(data, dict)
                                                       and isinstance(data.get('items'), list))
                self.check(name+'_'+str(index+1)+'_shape', valid)
                times[name].append(self.report['requests'][-1]['duration_ms'])
        self.report['summary'] = {
            name: dict(samples=values, median_ms=statistics.median(values), worst_ms=max(values))
            for name, values in times.items()}
        self.report['browser_measured'] = False
        self.report['application_cache_measured'] = False
        self.report['passed'] = True
        self.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.output, probe_type=MemberProbe, role_label='de membro ativa')))
