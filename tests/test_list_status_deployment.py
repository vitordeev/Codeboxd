import unittest

from tools.list_status_deployment import expected_operations, rollback_bundle


class ListStatusDeploymentTests(unittest.TestCase):
    def test_preview_scope_distinguishes_additions_from_updates(self):
        old = 'query "lists/{id}" verb=DELETE { guid = "existing" }'
        new = 'table user_media_list_status { guid = "new" }'
        self.assertEqual(expected_operations(old + '\n---\n' + new, old), {
            ('query', 'lists/{id} DELETE', 'update'),
            ('table', 'user_media_list_status', 'create')})

    def test_rollback_only_contains_touched_original_contracts_and_rows(self):
        original = 'query "original" verb=GET { guid = "old" }'
        unrelated = 'table other { guid = "unrelated" }'
        added = 'table user_media_list_status { guid = "new" }'
        snapshot = {
            'user': [{'id': 1}], 'media': [{'id': 10}], 'user_follow': [],
            'user_list': [{'id': 1, 'user_id': 1, 'default_key': '1:planned'},
                          {'id': 2, 'user_id': 1, 'default_key': None}],
            'user_list_item': [{'id': 7, 'list_id': 1, 'media_id': 10},
                               {'id': 8, 'list_id': 2, 'media_id': 10}],
        }
        contracts, records = rollback_bundle(original + '\n---\n' + unrelated,
                                               original + '\n---\n' + added, snapshot)
        self.assertIn(original, contracts)
        self.assertNotIn(unrelated, contracts)
        self.assertEqual([r['id'] for r in records['restore_default_items']], [7])
        self.assertEqual(records['new_object_guids_review_before_removal'], ['new'])
        self.assertTrue(records['requires_writers_blocked'])
        self.assertTrue(records['refuse_automatic_rollback_after_release'])
