"""Real report validation using disposable member data and exact cleanup.

Never elevates an account or prints credentials. Existing target data is read
only. No write is retried automatically. Metadata access is used for evidence
and removal of this run's marked fixtures, never to impersonate an admin.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import secrets
import time
from urllib.parse import urlsplit
import uuid

import httpx
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]


class Probe:
    def __init__(self, client, output):
        self.client, self.output = client, output
        config = dotenv_values(ROOT / '.env')
        self.auth = config['XANO_AUTH_URL'].rstrip('/')
        self.social = config['XANO_SOCIAL_URL'].rstrip('/')
        origin = urlsplit(self.auth)
        self.meta = f'{origin.scheme}://{origin.netloc}/api:meta/workspace/147717'
        raw = (Path.home()/'.xano/credentials.yaml').read_text(encoding='utf-8')
        tokens = re.findall(r'^\s*access_token:\s*(.*?)\s*$', raw, re.M)
        if len(tokens) != 1:
            raise RuntimeError('metadata_profile_ambiguous')
        self.metadata_headers = {'Authorization': 'Bearer '+tokens[0].strip().strip("'\"")}
        self.marker = 'cbadmin_'+uuid.uuid4().hex[:20]
        self.journal = ROOT/'.local'/('admin-reports-'+self.marker+'.json')
        self.journal.write_text(json.dumps({'marker': self.marker, 'workspace': 147717}), encoding='utf-8')
        self.uid = None
        self.tables = {}
        self.before = {}
        self.report = dict(layer='real_api_disposable_member', passed=False,
                           started_at=datetime.now(timezone.utc).isoformat(), checks=[], cleanup=[])

    def save(self):
        self.output.write_text(json.dumps(self.report, indent=2)+'\n', encoding='utf-8')

    def check(self, name, condition, response=None):
        row = dict(scenario=name, passed=bool(condition))
        if response is not None:
            row['http_status'] = response.status_code
        self.report['checks'].append(row)
        self.save()
        print(json.dumps(row), flush=True)
        if not condition:
            raise RuntimeError(name)

    def request(self, method, url, **kwargs):
        time.sleep(1.1)
        response = self.client.request(method, url, **kwargs)
        if method == 'GET':
            for _ in range(2):
                if response.status_code != 429:
                    break
                delay = response.headers.get('Retry-After', '5')
                delay = min(15, max(1, int(delay))) if delay.isdigit() else 5
                time.sleep(delay)
                response = self.client.request(method, url, **kwargs)
        return response

    def rows(self, table):
        page, seen, rows = 1, set(), []
        while page is not None:
            if page in seen or len(seen) >= 100:
                raise RuntimeError('metadata_pagination_limit')
            seen.add(page)
            response = self.request('GET', f'{self.meta}/table/{self.tables[table]}/content',
                                    params=dict(page=page, per_page=100), headers=self.metadata_headers)
            if response.status_code != 200:
                raise RuntimeError('metadata_read_failed')
            data = response.json()
            rows.extend(data['items'])
            page = data['nextPage']
        return rows

    @staticmethod
    def hashes(rows):
        return {str(row['id']): hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
                for row in rows}

    def run(self):
        tables = self.request('GET', self.meta+'/table', headers=self.metadata_headers)
        tables.raise_for_status()
        data = tables.json()
        self.tables = {row['name']: row['id'] for row in (data['items'] if isinstance(data, dict) else data)}
        for table in ('user', 'profile', 'user_list', 'user_list_item', 'post', 'comment', 'report', 'media'):
            self.before[table] = self.hashes(self.rows(table))
        assert all('2147483647' not in self.before[table] for table in ('user', 'media', 'report'))
        try:
            password = 'CbTest!'+secrets.token_urlsafe(24)
            response = self.request('POST', self.auth+'/auth/signup', json=dict(
                email=self.marker+'@example.invalid', password=password, name=self.marker,
                username=self.marker))
            self.check('temporary_member_signup', response.status_code == 200, response)
            session = response.json()
            self.uid = session['user_id']
            headers = {'Authorization': 'Bearer '+session['authToken']}
            me = self.request('GET', self.auth+'/auth/me', headers=headers)
            self.check('member_role_server_confirmed', me.status_code == 200
                       and me.json().get('id') == self.uid and me.json().get('role') == 'member', me)
            post = self.request('POST', self.social+'/posts', headers=headers, json={'body': self.marker})
            self.check('own_post_fixture_created', post.status_code == 200, post)
            post_id = post.json()['id']
            comment = self.request('POST', self.social+'/comments', headers=headers,
                                   json={'post_id': post_id, 'body': self.marker})
            self.check('own_comment_fixture_created', comment.status_code == 200, comment)
            comment_id = comment.json()['id']
            media = self.request('GET', self.social+'/media', params={'per_page': 1})
            media.raise_for_status()
            data = media.json()
            media_id = (data['items'] if isinstance(data, dict) else data)[0]['id']
            targets_before = {table: self.hashes(self.rows(table)) for table in ('post', 'comment', 'profile', 'media')}
            base = dict(target_type='media', target_id=str(media_id), reason='other', description=self.marker)
            invalids = [('missing_target', 'target_id', None), ('invalid_reason', 'reason', 'invalid'),
                        ('missing_description', 'description', None), ('empty_description', 'description', ''),
                        ('whitespace_description', 'description', ' \t\n ')]
            for label, key, value in invalids:
                payload = dict(base)
                if value is None:
                    payload.pop(key)
                else:
                    payload[key] = value
                rejected = self.request('POST', self.social+'/reports', headers=headers, json=payload)
                self.check('reject_'+label, rejected.status_code == 400, rejected)
            invalid_message = dict(base, target_type='message', target_id=self.marker, target_snapshot={})
            rejected = self.request('POST', self.social+'/reports', headers=headers, json=invalid_message)
            self.check('reject_message_without_context', rejected.status_code == 400, rejected)
            self.check('invalid_reports_not_inserted', self.before['report'] == self.hashes(self.rows('report')))
            cases = [('post', post_id), ('comment', comment_id), ('profile', self.uid),
                     ('media', media_id), ('message', self.marker)]
            for kind, target in cases:
                payload = dict(base, target_type=kind, target_id=str(target),
                               target_snapshot={'body': self.marker, 'sender_name': 'Teste',
                                                'sent_at': '2026-10-22', 'secret_fixture': 'discard'})
                created = self.request('POST', self.social+'/reports', headers=headers, json=payload)
                self.check('create_report_'+kind, created.status_code == 200, created)
                report_id = created.json()['id']
                stored = self.request('GET', f'{self.meta}/table/{self.tables["report"]}/content/{report_id}',
                                      headers=self.metadata_headers)
                stored.raise_for_status()
                row = stored.json()
                self.check('persist_report_'+kind, row.get('reporter_user_id') == self.uid
                           and row.get('target_type') == kind and str(row.get('target_id')) == str(target)
                           and row.get('status') == 'pending' and row.get('description') == self.marker
                           and bool(row.get('created_at')) and bool(row.get('target_snapshot')))
                snapshot = row.get('target_snapshot') or {}
                self.check('safe_snapshot_'+kind, 'secret_fixture' not in snapshot
                           and (kind == 'message' or snapshot.get('body') != self.marker or kind in ('post', 'comment')))
                if kind == 'message':
                    self.check('message_context_without_live_message', snapshot == {
                        'body': self.marker, 'sender_name': 'Teste', 'sent_at': '2026-10-22'})
            targets_after = {table: self.hashes(self.rows(table)) for table in targets_before}
            self.check('reports_preserve_all_target_records', targets_before == targets_after)
            endpoints = [('GET', '/admin/dashboard', {}), ('GET', '/admin/users', {'params': {'search': self.marker}}),
                         ('GET', '/admin/catalog', {'params': {'media_type': 'movie'}}), ('GET', '/admin/reports', {}),
                         ('PUT', '/admin/users/2147483647/status', {'json': {'account_status': 'disabled'}}),
                         ('PUT', '/admin/catalog/2147483647', {'json': {'title': self.marker,
                             'description': self.marker, 'cover_url': '', 'year': 2020}}),
                         ('POST', '/admin/catalog', {'json': {'media_type': 'movie', 'external_source': 'tmdb',
                             'external_id': self.marker, 'title': self.marker}}),
                         ('PUT', '/admin/reports/2147483647', {'json': {'status': 'resolved', 'decision': self.marker}})]
            for role, role_headers, statuses in [('guest', {}, (401,)), ('member', headers, (403,))]:
                for method, path, kwargs in endpoints:
                    denied = self.request(method, self.social+path, headers=role_headers, **kwargs)
                    self.check(role+'_'+method+'_'+path.split('/')[2]+'_denied', denied.status_code in statuses, denied)
        finally:
            self.cleanup()

    def cleanup(self):
        # Also recover fixtures after a timeout with an unknown signup response.
        if not self.tables:
            return
        for row in self.rows('user'):
            if row.get('username') == self.marker and row.get('email') == self.marker+'@example.invalid':
                self.uid = row['id']
        if self.uid:
            rules = (
                ('report', lambda r: r.get('reporter_user_id') == self.uid and r.get('description') == self.marker),
                ('comment', lambda r: r.get('user_id') == self.uid and r.get('body') == self.marker),
                ('post', lambda r: r.get('user_id') == self.uid and r.get('body') == self.marker),
                ('media', lambda r: r.get('title') == self.marker and r.get('external_id') == self.marker),
                ('user_list', lambda r: r.get('user_id') == self.uid),
                ('profile', lambda r: r.get('user_id') == self.uid and r.get('username') == self.marker),
                ('event_log', lambda r: r.get('user_id') == self.uid),
                ('user', lambda r: r.get('id') == self.uid and r.get('username') == self.marker),
            )
            for table, owned in rules:
                for row in self.rows(table):
                    if owned(row) and str(row['id']) not in self.before.get(table, {}):
                        response = self.request('DELETE', f'{self.meta}/table/{self.tables[table]}/content/{row["id"]}',
                                                headers=self.metadata_headers)
                        result = dict(table=table, passed=response.status_code in (200, 204))
                        self.report['cleanup'].append(result)
                        self.save()
                        if not result['passed']:
                            raise RuntimeError('fixture_cleanup_failed')
        self.report['existing_storage_unchanged'] = {
            table: before == self.hashes(self.rows(table)) for table, before in self.before.items()}
        self.save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Use another output path to preserve evidence')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=25, follow_redirects=False) as client:
        probe = Probe(client, args.output)
        try:
            probe.run()
            probe.report['passed'] = (all(x['passed'] for x in probe.report['checks'])
                                      and all(probe.report['existing_storage_unchanged'].values()))
        except Exception as error:
            probe.report['failure_type'] = type(error).__name__
        finally:
            probe.save()
    print(json.dumps({'passed': probe.report['passed'], 'checks': len(probe.report['checks']),
                      'storage_unchanged': probe.report.get('existing_storage_unchanged', {})}), flush=True)
    return 0 if probe.report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
