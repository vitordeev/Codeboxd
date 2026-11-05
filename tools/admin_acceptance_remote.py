"""Admin acceptance using ordinary login and strictly disposable member data."""
import argparse
import asyncio
import json
from pathlib import Path

from tools.admin_dashboard_remote import DashboardProbe
from tools.admin_reads_remote import main, page_contract, no_secrets
from tools import list_status_live as live
from tools.default_list_integrity import digest


class AdminAcceptanceProbe(DashboardProbe):
    browser_output = None
    login_notice = ('Valida dashboard e operações administrativas em contas, obras e reports '
                    'descartáveis. Não promove usuários nem altera conteúdo existente.')

    def run(self):
        super().run()
        self.report['passed'] = False
        self.report['layer'] = 'real_admin_api_disposable_acceptance'
        self.save()
        private = live.ROOT / '.local/admin-acceptance-20261104'
        private.mkdir(exist_ok=True)
        live.PRIVATE = private
        run = live.Run()
        admin = {'token': self.token}
        before = {}
        tables = ('user', 'profile', 'user_list', 'user_list_item', 'media', 'post',
                  'user_follow', 'user_media_interaction', 'user_media_list_status', 'report', 'event_log')
        try:
            if run.journal.get('test_users'):
                raise ValueError('Clean previous acceptance fixtures first')
            before = {table: run.rows(table) for table in tables}
            a, b = run.fixture_users()
            marker = run.journal['fixture_marker']
            media = run.bulk_add('media', [{
                'identity_key': marker + ':' + kind + ':' + str(i),
                'external_source': 'test', 'external_id': marker + ':' + kind + ':' + str(i),
                'media_type': kind, 'title': marker + ' ' + kind + ' ' + str(i)}
                for kind in ('movie', 'series', 'book', 'anime') for i in range(2)])
            run.journal['fixture_media_ids'] = media
            run.save()
            mid = media[0]
            post = run.api('POST', 'posts', b, False, json={'body': marker})
            post.raise_for_status()
            pid = post.json()['id']
            for target_type, target_id in (('post', str(pid)), ('media', str(mid)), ('message', marker)):
                response = run.api('POST', 'reports', a, False, json={
                    'target_type': target_type, 'target_id': target_id, 'reason': 'other',
                    'description': marker, 'target_snapshot': {'body': marker}})
                self.check('report_created_' + target_type, response.status_code == 200)
            reports = [r for r in run.rows('report') if r['reporter_user_id'] == a['id']]
            self.check('three_reports_persisted', len(reports) == 3)
            rid = reports[0]['id']
            post_before = next(r for r in run.rows('post') if r['id'] == pid)
            operations = [('GET', 'admin/dashboard', {}), ('GET', 'admin/users', {}),
                          ('GET', 'admin/catalog?media_type=movie', {}), ('GET', 'admin/reports', {}),
                          ('PUT', f"admin/users/{b['id']}/status", {'account_status': 'disabled', 'reason': marker}),
                          ('PUT', f'admin/catalog/{mid}', {'title': marker, 'year': 2020}),
                          ('PUT', f'admin/reports/{rid}', {'status': 'reviewing', 'decision': marker}),
                          ('POST', 'admin/catalog', {'external_source': 'tmdb', 'external_id': '999999999',
                                                   'media_type': 'movie', 'title': marker})]
            for actor, expected, label in ((None, 401, 'guest'), (a, 403, 'member')):
                for method, path, payload in operations:
                    response = run.api(method, path, actor, False, **({'json': payload} if payload else {}))
                    self.check(label + '_denied_' + method + '_' + path.split('?')[0], response.status_code == expected)
            for kind in ('movie', 'series', 'book', 'anime'):
                first = run.api('GET', 'admin/catalog', admin, False,
                                params={'media_type': kind, 'search': marker, 'page': 1, 'per_page': 1})
                self.check('catalog_search_' + kind, first.status_code == 200)
                data = first.json()
                self.check('catalog_page_' + kind, page_contract(data) and data['total'] == 2
                           and all(r['media_type'] == kind and marker in r['title'] for r in data['items']))
                second = run.api('GET', 'admin/catalog', admin, False,
                                 params={'media_type': kind, 'search': marker, 'page': 2, 'per_page': 1}).json()
                self.check('catalog_continuation_' + kind, page_contract(second, page=2)
                           and second['items'][0]['id'] != data['items'][0]['id'])
            media_before = next(r for r in run.rows('media') if r['id'] == mid)
            for payload in ({'title': ''}, {'title': marker, 'cover_url': 'http://invalid.test/cover'},
                            {'title': marker, 'year': 1500}):
                response = run.api('PUT', f'admin/catalog/{mid}', admin, False, json=payload)
                self.check('invalid_catalog_rejected', response.status_code in (400, 422))
                self.check('invalid_catalog_preserved', run.meta('GET', 'media', mid) == media_before)
            response = run.api('PUT', f'admin/catalog/{mid}', admin, False, json={
                'title': marker + ' corrected', 'description': marker, 'year': 2020})
            self.check('catalog_correction', response.status_code == 200)
            corrected = run.meta('GET', 'media', mid)
            self.check('catalog_identity_preserved', all(corrected[k] == media_before[k]
                for k in ('id', 'identity_key', 'external_source', 'external_id', 'media_type'))
                and corrected['title'] == marker + ' corrected')
            for status, previous in (('disabled', 'active'), ('active', 'disabled')):
                response = run.api('PUT', f"admin/users/{b['id']}/status", admin, False, json={
                    'account_status': status, 'reason': marker, 'actor_user_id': a['id']})
                self.check('account_' + status, response.status_code == 200
                           and run.meta('GET', 'user', b['id'])['account_status'] == status)
                protected = run.api('GET', 'interactions', b, False)
                self.check('session_after_' + status, protected.status_code in (401, 403) if status == 'disabled'
                           else protected.status_code == 200)
                logs = [r for r in run.rows('event_log') if (r.get('metadata') or {}).get('reason') == marker]
                self.check('account_audit_' + status, any(r['user_id'] == 14 and r['created_at']
                    and r['action'] == 'admin_account_status_changed'
                    and r['metadata']['target_user_id'] == b['id']
                    and r['metadata']['previous_status'] == previous and r['metadata']['new_status'] == status for r in logs))
            for state in ('pending', 'reviewing', 'resolved', 'rejected'):
                if state != 'pending':
                    previous = run.meta('GET', 'report', rid)['status']
                    response = run.api('PUT', f'admin/reports/{rid}', admin, False, json={
                        'status': state, 'decision': marker, 'reviewer_user_id': a['id']})
                    self.check('report_transition_' + state, response.status_code == 200)
                    logs = [r for r in run.rows('event_log') if (r.get('metadata') or {}).get('report_id') == rid]
                    self.check('report_audit_' + state, any(r['user_id'] == 14 and r['created_at']
                        and r['metadata']['previous_status'] == previous
                        and r['metadata']['new_status'] == state and r['metadata']['decision'] == marker for r in logs))
                response = run.api('GET', 'admin/reports', admin, False,
                                   params={'status': state, 'target_type': 'post', 'reason': 'other', 'per_page': 1})
                data = response.json()
                self.check('report_filter_' + state, response.status_code == 200 and page_contract(data)
                           and no_secrets(data) and all(r['status'] == state and r['target_type'] == 'post'
                           and r['reason'] == 'other' for r in data['items']))
                self.check('report_does_not_change_target_' + state, run.meta('GET', 'post', pid) == post_before)
            self.report['functional_checks_passed'] = True
        finally:
            try:
                users = {u['id'] for u in run.journal.get('test_users', [])}
                owned_reports = [r for r in run.rows('report') if r['reporter_user_id'] in users]
                report_ids = {r['id'] for r in owned_reports}
                logs = [r for r in run.rows('event_log') if r['user_id'] in users
                        or (r.get('metadata') or {}).get('target_user_id') in users
                        or (r.get('metadata') or {}).get('report_id') in report_ids]
                run.bulk_delete('event_log', [r['id'] for r in logs])
                run.bulk_delete('report', sorted(report_ids))
                run.cleanup_fixtures()
                if before:
                    self.check('all_original_records_preserved', all(digest(run.rows(t)) == digest(rows)
                               for t, rows in before.items()))
                self.report['cleanup_passed'] = True
            finally:
                run.client.close()
                self.report['passed'] = bool(self.report.get('functional_checks_passed') and self.report.get('cleanup_passed'))
                self.save()
                if self.browser_output and self.report.get('cleanup_passed'):
                    from tools.admin_browser_real import BrowserProbe
                    browser = BrowserProbe(self.client, self.auth, self.social, self.browser_output, pause=3)
                    browser.token = self.token
                    try:
                        browser.run()
                    except Exception as exc:
                        browser.report['failure_type'] = type(exc).__name__
                        browser.save()
                    finally:
                        browser.token = None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--browser-output', type=Path)
    args = parser.parse_args()
    AdminAcceptanceProbe.browser_output = args.browser_output
    raise SystemExit(asyncio.run(main(args.output, probe_type=AdminAcceptanceProbe)))
