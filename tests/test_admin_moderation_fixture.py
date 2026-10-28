"""Offline generator/checker regressions, not executions of Xano contracts."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import admin_moderation_fixture as fixture


def synthetic_result(case):
    """Construct a checker input; this helper does not simulate a backend."""
    reports = [dict(id=i, created_at=1000+i, reporter_user_id=2, target_type=target,
                    target_id="1", reason=reason, description="Synthetic report "+str(i),
                    target_snapshot={"body": fixture.TARGET["body"]}, status=status)
               for i, (status, target, reason) in enumerate(fixture.ROWS, 1)]
    data = dict(targets=[deepcopy(fixture.TARGET)], reports_after=reports, audit=[])
    if case.get("review"):
        status = case["inputs"]["status"]
        reports[0].update(status=status, reviewer_user_id=1, decision="Synthetic review", reviewed_at=2000)
        data["result"] = dict(success=True, report_id=1, previous_status="pending", status=status,
                              reviewer_user_id=1, decision="Synthetic review")
        data["audit"] = [dict(user_id=1, action="admin_report_status_changed", created_at=2000,
                              metadata=dict(report_id=1, target_type="post", target_id="1",
                                            previous_status="pending", new_status=status, decision="Synthetic review"))]
    else:
        inputs, total = case["inputs"], case["total"]
        page, size = inputs.get("page", 1), inputs.get("per_page", 25)
        data["result"] = dict(items=[deepcopy(reports[i-1]) for i in case["ids"]], total=total,
                              page=page, per_page=size, next_page=page+1 if page*size < total else None)
    return data


class ModerationFixtureTests(unittest.TestCase):
    def test_generated_script_is_isolated_and_reuses_production_stacks(self):
        source = fixture.script()
        self.assertIn('precondition ($actor != null && $actor.account_status == "active" && $actor.role == "admin")', source)
        self.assertIn('previous_status: $current.status', source)
        self.assertIn('db.transaction {', source)
        self.assertIn('db.edit moderation_fixture_report', source)
        self.assertIn('db.add moderation_fixture_event_log', source)
        self.assertNotIn('$auth', source)
        self.assertNotIn('Security/require_current_session', source)
        for table in ('user', 'post', 'report', 'event_log'):
            for operation in ('get', 'query', 'add', 'edit', 'del'):
                self.assertNotRegex(source, r'\bdb\.'+operation+r'\s+'+table+r'\b')

    def test_unexpected_production_dependency_fails_closed(self):
        original = Path.read_text

        def changed(path, *args, **kwargs):
            return original(path, *args, **kwargs).replace('db.query report {', 'db.query private_records {')

        with patch.object(Path, 'read_text', changed):
            with self.assertRaisesRegex(ValueError, 'dependency'):
                fixture.script()

    def test_removed_session_guard_requires_review_instead_of_silent_drift(self):
        original = Path.read_text

        def changed(path, *args, **kwargs):
            return original(path, *args, **kwargs).replace('Security/require_current_session', 'Security/new_guard')

        with patch.object(Path, 'read_text', changed):
            with self.assertRaisesRegex(ValueError, 'dependency'):
                fixture.script()

    def test_checker_accepts_explicit_synthetic_reference_results(self):
        cases = fixture.cases()
        self.assertEqual(len(cases), 22)
        self.assertEqual(len({case['name'] for case in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case['name']):
                checks = fixture.check_result(synthetic_result(case), case)
                self.assertTrue(checks)
                self.assertTrue(all(checks.values()), checks)

    def test_checker_rejects_wrong_page_total_and_private_fields(self):
        case = next(case for case in fixture.cases() if case['name'] == 'second_page')
        for mutate in (lambda d: d['result'].update(total=0),
                       lambda d: d['result'].update(next_page=None),
                       lambda d: d['result']['items'].reverse(),
                       lambda d: d['result']['items'][0].pop('target_snapshot'),
                       lambda d: d['result']['items'][0].update(auth_token='synthetic-invalid')):
            data = synthetic_result(case)
            mutate(data)
            self.assertFalse(all(fixture.check_result(data, case).values()))

    def test_checker_rejects_missing_or_spoofed_audit_and_target_changes(self):
        case = next(case for case in fixture.cases() if case['name'] == 'decision_resolved')
        for mutate in (lambda d: d.update(audit=[]),
                       lambda d: d['audit'][0].update(user_id=2),
                       lambda d: d['audit'][0]['metadata'].update(previous_status='resolved'),
                       lambda d: d['targets'][0].update(body='changed'),
                       lambda d: d['reports_after'][1].update(status='resolved'),
                       lambda d: d['reports_after'][0].update(target_snapshot={}),
                       lambda d: d['reports_after'][0].update(reviewed_at=None)):
            data = synthetic_result(case)
            mutate(data)
            self.assertFalse(all(fixture.check_result(data, case).values()))

    def test_missing_or_malformed_results_fail_without_success(self):
        case = fixture.cases()[0]
        for data in (None, {}, {'result': []}, {'result': {}, 'reports_after': [None]}):
            self.assertFalse(all(fixture.check_result(data, case).values()))

    def test_boolean_ids_totals_and_actors_do_not_pass_as_integer_one(self):
        case = next(case for case in fixture.cases() if case['name'] == 'combined')
        for mutate in (lambda d: d['result'].update(total=True),
                       lambda d: d['result'].update(page=True),
                       lambda d: d['result']['items'][0].update(id=True),
                       lambda d: d['targets'][0].update(id=True),
                       lambda d: d['reports_after'][0].update(id=True)):
            data = synthetic_result(case)
            mutate(data)
            self.assertFalse(all(fixture.check_result(data, case).values()))
        case = next(case for case in fixture.cases() if case['name'] == 'decision_resolved')
        for mutate in (lambda d: d['result'].update(report_id=True),
                       lambda d: d['result'].update(reviewer_user_id=True),
                       lambda d: d['reports_after'][0].update(reviewer_user_id=True),
                       lambda d: d['audit'][0].update(user_id=True),
                       lambda d: d['audit'][0]['metadata'].update(report_id=True)):
            data = synthetic_result(case)
            mutate(data)
            self.assertFalse(all(fixture.check_result(data, case).values()))

    def test_offline_cli_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)/'fixture'
            with patch('sys.argv', ['fixture', '--output', str(output)]):
                fixture.main()
                self.assertTrue((output/'fixture.xs').is_file())
                self.assertTrue((output/'cases.json').is_file())
                with self.assertRaises(FileExistsError):
                    fixture.main()

    def test_checker_rejects_invalid_audit_and_review_timestamps(self):
        case = next(case for case in fixture.cases() if case['name'] == 'decision_resolved')
        invalid = (None, True, False, [], [2000], {}, {'timestamp': 2000},
                   float('nan'), float('inf'), float('-inf'), 0, -1, 0.0, -0.1,
                   '', '2000', '2026-10-28T12:00:00Z')
        for location, field, check in (('audit', 'created_at', 'audit'),
                                       ('reports_after', 'reviewed_at', 'stored_decision')):
            for value in invalid:
                with self.subTest(location=location, value=value):
                    data = synthetic_result(case)
                    data[location][0][field] = value
                    self.assertFalse(fixture.check_result(data, case)[check])

    def test_checker_accepts_positive_finite_numeric_timestamps(self):
        case = next(case for case in fixture.cases() if case['name'] == 'decision_resolved')
        for timestamp in (2000, 2000.5, 1793188800000):
            with self.subTest(timestamp=timestamp):
                data = synthetic_result(case)
                data['audit'][0]['created_at'] = timestamp
                data['reports_after'][0]['reviewed_at'] = timestamp
                self.assertTrue(all(fixture.check_result(data, case).values()))


if __name__ == '__main__':
    unittest.main()
