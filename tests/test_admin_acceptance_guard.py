"""Synthetic, offline policy checks. No real destination, identity or consent."""
from dataclasses import replace
import unittest
from unittest.mock import patch

from tools.admin_acceptance_guard import (
    Approval, Destination, Fixture, GuardRejected, digest, identity_digest, preview_update,
)


RUN = 'cbh9_012345abcdef'


class AdminAcceptanceGuardTests(unittest.TestCase):
    def setUp(self):
        self.destination = Destination('https://example.invalid', 1, 'v1', 'live',
                                       'api:social', True)
        self.records = {
            'user': dict(id=901, username=RUN + '_b', role='member', account_status='active'),
            'media': dict(id=902, identity_key=RUN + '_movie', external_source='test',
                          external_id='synthetic', media_type='movie', title=RUN + ' movie'),
            'report': dict(id=903, reporter_user_id=901, target_type='message', target_id='synthetic',
                           description=RUN + ' report', status='pending'),
        }
        self.payloads = {
            'user': dict(account_status='disabled', reason=RUN + ' test'),
            'media': dict(title=RUN + ' edited', year=2026),
            'report': dict(status='resolved', decision=RUN + ' decision'),
        }
        self.paths = {'user': '/admin/users/901/status', 'media': '/admin/catalog/902',
                      'report': '/admin/reports/903'}
        self.manifest = tuple(Fixture(table, row['id'], RUN, identity_digest(table, row),
                                     digest(row)) for table, row in self.records.items())
        self.approval = Approval('SYNTHETIC TEST CONSENT ONLY', self.destination, RUN, 900,
                                 frozenset({'A3'}), True,
                                 frozenset((table, self.records[table]['id'], digest(payload))
                                           for table, payload in self.payloads.items()))

    def args(self, table='user', **changes):
        args = dict(destination=self.destination, approval=self.approval,
                    manifest=self.manifest, actor_id=900, method='PUT', path=self.paths[table],
                    payload=self.payloads[table], current_record=self.records[table], confirmed=True)
        return dict(args, **changes)

    def rejects(self, reason, table='user', **changes):
        with self.assertRaisesRegex(GuardRejected, '^' + reason + '$'):
            preview_update(**self.args(table, **changes))

    def test_three_valid_previews_have_no_network_and_no_execution(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')):
            for table in self.records:
                with self.subTest(table=table):
                    result = preview_update(**self.args(table))
                    self.assertEqual(result['mode'], 'offline_preview')
                    self.assertIs(result['remote_execution'], False)
                    self.assertEqual(result['table'], table)
                    self.assertNotIn(RUN, str(result))

    def test_missing_or_blank_approval(self):
        for approval in (None, replace(self.approval, reference=' ')):
            self.rejects('approval_required', approval=approval)

    def test_read_only_authorization_does_not_allow_updates(self):
        for phases in (frozenset(), frozenset({'A0', 'A1'}), frozenset({'A2', 'A4'})):
            self.rejects('phase_not_approved', approval=replace(self.approval, phases=phases))

    def test_cancel_and_absent_confirmation(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')):
            for confirmation in (False, None, 'yes', 1):
                self.rejects('confirmation_required', confirmed=confirmation)

    def test_each_destination_component_is_bound(self):
        for field, value in dict(origin='https://other.invalid', workspace=2, branch='v2',
                                 data_source='other', api_group='api:other', shared=False).items():
            self.rejects('destination_mismatch', destination=replace(self.destination, **{field: value}))

    def test_invalid_origins_and_workspace(self):
        for origin in ('http://example.invalid', 'https://name:private@example.invalid',
                       'https://example.invalid/path', 'https://example.invalid?secret=private',
                       'https://example.invalid#fragment'):
            destination = replace(self.destination, origin=origin)
            self.rejects('invalid_destination', destination=destination,
                         approval=replace(self.approval, destination=destination))
        destination = replace(self.destination, workspace=True)
        self.rejects('invalid_destination', destination=destination,
                     approval=replace(self.approval, destination=destination))

    def test_shared_live_requires_additional_approval_even_if_marked_isolated(self):
        for shared in (True, False):
            destination = replace(self.destination, shared=shared)
            self.rejects('shared_destination_not_approved', destination=destination,
                         approval=replace(self.approval, destination=destination,
                                          shared_destination_approved=False))

    def test_isolated_destination_can_be_previewed_with_its_own_approval(self):
        destination = replace(self.destination, branch='test', data_source='test', shared=False)
        result = preview_update(**self.args(destination=destination,
            approval=replace(self.approval, destination=destination, shared_destination_approved=False)))
        self.assertFalse(result['remote_execution'])

    def test_other_actor_rejected(self):
        for actor_id in (901, True, 0, '900'):
            self.rejects('actor_mismatch', actor_id=actor_id)

    def test_actor_cannot_be_target(self):
        self.rejects('actor_is_target', actor_id=901,
                     approval=replace(self.approval, admin_id=901))

    def test_invalid_run_id(self):
        self.rejects('invalid_run_id', approval=replace(self.approval, run_id='old_run'))

    def test_setup_cleanup_and_other_methods_remain_blocked(self):
        for method, path in [('POST', '/admin/catalog'), ('POST', '/auth/signup'),
                             ('POST', '/table/1/content/bulk/delete'), ('DELETE', '/event_log/1'),
                             ('GET', '/admin/users'), ('PATCH', '/admin/catalog/902')]:
            self.rejects('method_not_supported', method=method, path=path)

    def test_route_bypasses_and_audit_updates_are_blocked(self):
        for path in ('/event_log/1', '/admin/catalog/902?extra=1', '/admin/catalog/0902',
                     '/admin/catalog/%39%30%32', '/admin/catalog/902/',
                     'https://example.invalid/admin/catalog/902', '/admin/catalog/../902'):
            self.rejects('route_not_supported', path=path)

    def test_missing_manifest(self):
        for manifest in (None, (), ('fake',)):
            self.rejects('manifest_required', manifest=manifest)

    def test_duplicate_manifest_id(self):
        self.rejects('duplicate_manifest_id', manifest=self.manifest + (self.manifest[0],))

    def test_foreign_id_and_other_run_are_rejected(self):
        self.rejects('foreign_target', path='/admin/users/999/status')
        self.rejects('foreign_target', manifest=(replace(self.manifest[0], run_id='other'),))

    def test_reloaded_record_must_match_target_id(self):
        self.rejects('record_id_mismatch', current_record=dict(self.records['user'], id=999))

    def test_administrative_and_unknown_account_roles_are_protected(self):
        for role in ('admin', 'moderator', None):
            self.rejects('protected_account', current_record=dict(self.records['user'], role=role))

    def test_marker_alone_never_proves_ownership(self):
        self.rejects('foreign_target', manifest=(self.manifest[1],))
        self.rejects('run_marker_missing', current_record=dict(self.records['user'], username='ordinary'))

    def test_identity_change_is_blocked_even_with_same_marker(self):
        self.rejects('identity_changed', current_record=dict(self.records['user'], username=RUN + '_other'))

    def test_any_snapshot_drift_requires_reconciliation(self):
        self.rejects('snapshot_changed', current_record=dict(self.records['user'], account_status='disabled'))

    def test_identity_and_actor_fields_cannot_be_injected(self):
        for table, field in [('user', 'role'), ('user', 'actor_user_id'),
                             ('media', 'identity_key'), ('media', 'external_id'),
                             ('report', 'reviewer_user_id'), ('report', 'target_id')]:
            self.rejects('payload_fields_not_allowed', table,
                         payload=dict(self.payloads[table], **{field: 'private'}))

    def test_exact_payload_must_be_approved(self):
        self.rejects('update_not_approved', payload=dict(self.payloads['user'], reason=RUN + ' changed'))

    def test_request_marker_is_required_for_all_updates(self):
        for table, field in [('user', 'reason'), ('media', 'title'), ('report', 'decision')]:
            self.rejects('payload_marker_missing', table, payload=dict(self.payloads[table], **{field: ' '}))

    def test_invalid_statuses(self):
        self.rejects('invalid_account_status', payload=dict(self.payloads['user'], account_status='deleted'))
        self.rejects('invalid_report_status', 'report', payload=dict(self.payloads['report'], status='pending'))

    def test_hash_is_stable_and_invalid_json_does_not_leak(self):
        self.assertEqual(digest({'b': 2, 'a': 1}), digest({'a': 1, 'b': 2}))
        with self.assertRaisesRegex(GuardRejected, '^invalid_json$'):
            digest({'private': float('nan')})


if __name__ == '__main__':
    unittest.main()
