"""Verify all admin routes reject guests/members using disposable targets."""
import argparse
import json
from pathlib import Path

from tools import list_status_live as live
from tools.default_list_integrity import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve previous evidence')
    private = live.ROOT / '.local/admin-authorization-20261104'
    private.mkdir(exist_ok=True)
    live.PRIVATE = private
    run = live.Run()
    report = {'layer': 'real_admin_guest_member_authorization', 'passed': False, 'checks': []}
    before = {}

    def check(name, condition, status=None):
        row = {'scenario': name, 'passed': bool(condition)}
        if status is not None:
            row['http_status'] = status
        report['checks'].append(row)
        args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
        if not condition:
            raise ValueError(name)

    try:
        if run.journal.get('test_users'):
            raise ValueError('Recover previous fixtures before rerunning')
        tables = ('user', 'profile', 'user_list', 'user_list_item', 'media', 'post',
                  'user_follow', 'user_media_interaction', 'user_media_list_status', 'report', 'event_log')
        before = {table: run.rows(table) for table in tables}
        a, b = run.fixture_users()
        marker = run.journal['fixture_marker']
        run.journal['fixture_media_ids'] = run.bulk_add('media', [{
            'identity_key': marker, 'external_source': 'test', 'external_id': marker,
            'media_type': 'movie', 'title': marker}])
        run.save()
        mid = run.journal['fixture_media_ids'][0]
        post = run.api('POST', 'posts', b, False, json={'body': marker})
        post.raise_for_status()
        response = run.api('POST', 'reports', a, False, json={
            'target_type': 'post', 'target_id': str(post.json()['id']), 'reason': 'other', 'description': marker})
        response.raise_for_status()
        rid = response.json()['id']
        operations = [('GET', 'admin/dashboard', {}), ('GET', 'admin/users', {}),
                      ('GET', 'admin/catalog?media_type=movie', {}), ('GET', 'admin/reports', {}),
                      ('PUT', f"admin/users/{b['id']}/status", {'account_status': 'disabled', 'reason': marker}),
                      ('PUT', f'admin/catalog/{mid}', {'title': marker, 'year': 2020}),
                      ('PUT', f'admin/reports/{rid}', {'status': 'reviewing', 'decision': marker}),
                      ('POST', 'admin/catalog', {'external_source': 'tmdb', 'external_id': '999999999',
                                               'media_type': 'movie', 'title': marker})]
        for actor, expected, label in ((None, 401, 'guest'), (a, 403, 'member')):
            for index, (method, path, payload) in enumerate(operations):
                response = run.api(method, path, actor, False, **({'json': payload} if payload else {}))
                if method == 'POST' and response.status_code == 200 and response.json().get('created'):
                    run.journal['fixture_media_ids'].append(response.json()['item']['id'])
                    run.save()
                check(label + '_' + str(index + 1) + '_' + method, response.status_code == expected, response.status_code)
        report['authorization_passed'] = True
    except Exception as exc:
        report['failure_type'] = type(exc).__name__
    finally:
        try:
            users = {u['id'] for u in run.journal.get('test_users', [])}
            reports = [r for r in run.rows('report') if r['reporter_user_id'] in users]
            ids = {r['id'] for r in reports}
            logs = [r for r in run.rows('event_log') if r['user_id'] in users
                    or (r.get('metadata') or {}).get('target_user_id') in users
                    or (r.get('metadata') or {}).get('report_id') in ids]
            run.bulk_delete('event_log', [r['id'] for r in logs])
            run.bulk_delete('report', sorted(ids))
            run.cleanup_fixtures()
            check('all_original_records_preserved', bool(before) and all(
                digest(sorted(run.rows(t), key=lambda r: r['id'])) == digest(sorted(rows, key=lambda r: r['id']))
                for t, rows in before.items()))
            report['cleanup_passed'] = True
        except Exception as exc:
            report['cleanup_failure_type'] = type(exc).__name__
        finally:
            run.client.close()
            report['passed'] = bool(report.get('authorization_passed') and report.get('cleanup_passed'))
            args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
