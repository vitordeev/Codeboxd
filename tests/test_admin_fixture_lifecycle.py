"""Cleanup safety using fictional in-memory records only; no transport exists."""
from copy import deepcopy
from dataclasses import replace
import unittest

from tools.admin_fixture_lifecycle import Receipt, cleanup_preview, pilot_plan, _resolve
from tools.admin_acceptance_guard import GuardRejected, digest

RUN = 'cbh9_aabbcc112233'


class PilotLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.plan = pilot_plan(RUN)
        self.ids = {row['symbol']: 100 + index for index, row in enumerate(self.plan['records'])}
        self.current = {table: {} for table in self.plan['counts']}
        self.current.update(event_log={}, user_list_item={})
        self.current['user'][1] = dict(id=1, role='admin', account_status='active', username='original-admin')
        self.current['media'][2] = dict(id=2, title='Original media')
        self.current['event_log'][3] = dict(id=3, user_id=1, action='login', metadata={})
        self.baseline = {table: {key: digest(value) for key, value in rows.items()}
                         for table, rows in self.current.items()}
        for row in self.plan['records']:
            record = {field: _resolve(value, self.ids) for field, value in row['identity'].items()}
            if row['table'] == 'report':
                record['target_id'] = str(record['target_id'])
                record.update(status='resolved', reviewer_user_id=1, decision=RUN + ' reviewed')
            if row['table'] == 'user':
                record.update(role='member', account_status='disabled')
            record['id'] = self.ids[row['symbol']]
            self.current[row['table']][record['id']] = record
            if row['table'] in ('report', 'user'):
                is_user = row['table'] == 'user'
                event_id = 500 + len(self.current['event_log'])
                metadata = {'target_user_id' if is_user else 'report_id': record['id'],
                            'new_status': 'disabled' if is_user else record['status'],
                            'reason' if is_user else 'decision': RUN + (' disabled' if is_user else ' reviewed')}
                self.current['event_log'][event_id] = dict(id=event_id, user_id=1,
                    action='admin_account_status_changed' if is_user else 'admin_report_status_changed',
                    metadata=metadata)
        self.receipts = self.stamps()

    def stamps(self):
        return [Receipt(row['symbol'], row['table'], self.ids[row['symbol']],
                        digest(self.current[row['table']][self.ids[row['symbol']]])) for row in self.plan['records']]

    def preview(self, **changes):
        args = dict(run_id=RUN, receipts=self.receipts, baseline=self.baseline,
                    current=self.current, admin_id=1, inventory_complete=True, references_reviewed=True)
        return cleanup_preview(**(args | changes))

    def test_pilot_is_25_records_with_16_retained_and_9_cleanup_candidates(self):
        self.assertEqual(self.plan['counts'], dict(user=2, profile=2, user_list=4, media=8, post=1, report=8))
        result = self.preview()
        self.assertFalse(result['remote_execution'])
        self.assertFalse(self.plan['final_acceptance_complete'])
        self.assertEqual(sum(map(len, result['delete_ids'].values())), 9)
        self.assertEqual(result['retained_records'], 16)
        self.assertEqual(set(result['delete_ids']), {'post', 'media'})
        self.assertNotIn(2, result['delete_ids']['media'])
        self.assertEqual(result['preserved_audit_events'], 11)

    def test_unknown_inventory_or_unreviewed_cascades_block_cleanup(self):
        for changes in ({'inventory_complete': False}, {'references_reviewed': False}):
            with self.assertRaisesRegex(GuardRejected, 'complete_inventory'):
                self.preview(**changes)

    def test_original_ids_cannot_be_adopted_as_fixtures_even_with_new_receipt(self):
        row = next(row for row in self.receipts if row.table == 'media')
        receipts = [replace(item, row_id=2, snapshot_digest=digest(self.current['media'][2]))
                    if item == row else item for item in self.receipts]
        with self.assertRaisesRegex(GuardRejected, 'original_record'):
            self.preview(receipts=receipts)

    def test_duplicate_receipts_or_missing_resource_block_cleanup(self):
        with self.assertRaises(GuardRejected):
            self.preview(receipts=self.receipts[:-1])
        with self.assertRaises(GuardRejected):
            self.preview(receipts=[*self.receipts[:-1], self.receipts[0]])

    def test_changed_fixture_requires_reconciliation_instead_of_deletion(self):
        self.current['media'][self.ids['M_movie_1']]['title'] = 'Changed elsewhere'
        with self.assertRaisesRegex(GuardRejected, 'snapshot_changed'):
            self.preview()

    def test_foreign_owner_cannot_be_approved_by_refreshing_snapshot(self):
        self.current['post'][self.ids['P']]['user_id'] = 999
        with self.assertRaisesRegex(GuardRejected, 'ownership_changed'):
            self.preview(receipts=self.stamps())

    def test_active_fixture_account_or_unreviewed_report_blocks_cleanup(self):
        self.current['user'][self.ids['B']]['account_status'] = 'active'
        with self.assertRaisesRegex(GuardRejected, 'disabled_member'):
            self.preview(receipts=self.stamps())
        self.current['user'][self.ids['B']]['account_status'] = 'disabled'
        self.current['report'][self.ids['Q1']]['status'] = 'pending'
        with self.assertRaisesRegex(GuardRejected, 'reviewed_report'):
            self.preview(receipts=self.stamps())

    def test_original_or_audit_drift_blocks_cleanup(self):
        for table, key in (('user', 1), ('media', 2), ('event_log', 3)):
            before = deepcopy(self.current[table][key])
            self.current[table][key]['unexpected'] = True
            with self.assertRaisesRegex(GuardRejected, 'original_record_changed'):
                self.preview()
            self.current[table][key] = before

    def test_third_party_reference_to_fixture_blocks_cleanup(self):
        self.current['user_list_item'][900] = dict(id=900, list_id=999, media_id=self.ids['M_movie_1'])
        with self.assertRaisesRegex(GuardRejected, 'external_reference'):
            self.preview()

    def test_third_party_report_blocks_deleting_its_target(self):
        self.current['report'][901] = dict(id=901, reporter_user_id=999,
                                           target_type='post', target_id=str(self.ids['P']))
        with self.assertRaisesRegex(GuardRejected, 'external_report'):
            self.preview()

    def test_missing_or_mismatched_final_audit_blocks_cleanup(self):
        for row in self.current['event_log'].values():
            if row.get('metadata', {}).get('report_id') == self.ids['Q1']:
                row['metadata']['decision'] = RUN + ' different decision'
        with self.assertRaisesRegex(GuardRejected, 'final_fixture_audit_missing'):
            self.preview()

    def test_account_promotion_and_table_inventory_change_block_cleanup(self):
        self.current['user'][self.ids['R']]['role'] = 'admin'
        with self.assertRaisesRegex(GuardRejected, 'disabled_member'):
            self.preview(receipts=self.stamps())
        altered = self.current | {'unexpected_table': {}}
        with self.assertRaisesRegex(GuardRejected, 'tables_changed'):
            self.preview(current=altered)


if __name__ == '__main__':
    unittest.main()
