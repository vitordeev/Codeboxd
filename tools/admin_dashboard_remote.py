"""Read-only dashboard acceptance with manual admin login and independent totals."""
import argparse
import asyncio
from pathlib import Path

from tools.admin_reads_remote import Probe, main, no_secrets, page_contract
from tools.session_revocation import metadata_config


class DashboardProbe(Probe):
    def metadata(self, path, params=None):
        response = self.request('GET', self.meta, path, params=params, headers=self.meta_headers)
        self.check('metadata_read', response.status_code == 200, response.status_code)
        return response.json()

    def snapshot(self):
        totals = {}
        for name in ('user', 'post', 'media'):
            data = self.metadata('/table/'+str(self.tables[name])+'/content', {'page': 1, 'per_page': 1})
            total = data.get('itemsTotal')
            self.check('metadata_'+name+'_total', type(total) is int and total >= 0)
            totals[name] = total
        pending, report_ids, seen, page = set(), set(), set(), 1
        report_total = None
        while page is not None:
            if page in seen or len(seen) >= 10:
                raise RuntimeError('metadata_report_page_budget')
            seen.add(page)
            data = self.metadata('/table/'+str(self.tables['report'])+'/content', {'page': page, 'per_page': 100})
            self.check('metadata_report_page', isinstance(data.get('items'), list)
                       and type(data.get('itemsTotal')) is int)
            if report_total is None:
                report_total = data['itemsTotal']
            self.check('metadata_report_total_stable', report_total == data['itemsTotal'])
            for row in data['items']:
                self.check('metadata_report_unique_id', type(row.get('id')) is int and row['id'] not in report_ids)
                report_ids.add(row['id'])
                if row.get('status') == 'pending':
                    pending.add(row['id'])
            page = data.get('nextPage')
        self.check('metadata_reports_complete', len(report_ids) == report_total)
        totals['reports_pending'] = len(pending)
        totals['reports_total'] = report_total
        return totals, pending

    def section(self, data, section, pagination, page=1):
        meta = data.get(pagination)
        self.check(section+'_pagination_present', isinstance(meta, dict))
        payload = dict(meta, items=data.get(section))
        self.check(section+'_pagination_contract', page_contract(payload, page=page))
        return payload

    def run(self):
        if not self.token:
            raise RuntimeError('admin_session_required')
        self.report['layer'] = 'real_admin_dashboard_independent_counts'
        self.meta, self.meta_headers = metadata_config()
        tables = self.metadata('/table')
        rows = tables.get('items', []) if isinstance(tables, dict) else tables
        self.tables = {row['name']: row['id'] for row in rows}
        self.check('metadata_tables_available', all(name in self.tables for name in ('user', 'post', 'media', 'report')))
        before, pending_ids = self.snapshot()
        guest = self.request('GET', self.social, '/admin/dashboard')
        self.check('guest_dashboard_denied', guest.status_code == 401, guest.status_code)
        params = dict(page=1, per_page=1, reports_page=1, reports_per_page=1)
        data = self.get('dashboard', '/admin/dashboard', params)
        self.check('dashboard_no_secrets', no_secrets(data))
        self.check('dashboard_counts_match_storage', all(type(data.get(field)) is int and data[field] == before[table]
            for field, table in [('users_total', 'user'), ('posts_total', 'post'),
                                 ('media_total', 'media'), ('reports_pending', 'reports_pending')]))
        posts = self.section(data, 'recent_posts', 'recent_posts_pagination')
        reports = self.section(data, 'pending_reports', 'pending_reports_pagination')
        self.check('activity_total_matches_storage', posts['total'] == before['post'])
        self.check('pending_total_matches_storage', reports['total'] == before['reports_pending'])
        self.check('activity_minimal_fields', all(set(row) <= {'id', 'user_id', 'created_at'} for row in posts['items']))
        self.check('pending_minimal_fields', all(set(row) <= {'id', 'created_at', 'target_type', 'reason'} for row in reports['items']))
        self.check('only_pending_reports', all(row['id'] in pending_ids for row in reports['items']))
        for section, pagination, page_key, first in (
            ('recent_posts', 'recent_posts_pagination', 'page', posts),
            ('pending_reports', 'pending_reports_pagination', 'reports_page', reports),
        ):
            if first['next_page'] is None:
                self.check(section+'_empty_or_last_page', first['total'] == len(first['items']))
                continue
            following = self.get(section+'_next', '/admin/dashboard', dict(params, **{page_key: first['next_page']}))
            self.check(section+'_next_no_secrets', no_secrets(following))
            next_page = self.section(following, section, pagination, first['next_page'])
            self.check(section+'_continuation', next_page['total'] == first['total']
                and bool(next_page['items']) and not ({row['id'] for row in first['items']}
                    & {row['id'] for row in next_page['items']}))
            if section == 'recent_posts':
                self.check('activity_descending_ids', first['items'][0]['id'] > next_page['items'][0]['id'])
            else:
                self.check('continuation_only_pending', all(row['id'] in pending_ids for row in next_page['items']))
        after, after_pending = self.snapshot()
        self.check('independent_counts_stable', before == after and pending_ids == after_pending)
        self.report['pending_nonempty_real'] = bool(pending_ids)
        self.report['activity_nonempty_real'] = bool(before['post'])
        self.report['passed'] = True
        self.meta_headers.clear()
        self.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.output, probe_type=DashboardProbe)))
