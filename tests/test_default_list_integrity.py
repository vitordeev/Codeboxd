from copy import deepcopy
import unittest

from tools.default_list_integrity import reconciliation_plan


class DefaultListIntegrityTests(unittest.TestCase):
    def test_no_duplicates_does_not_propose_cleanup_or_mutate_snapshot(self):
        lists = [dict(id=1, user_id=7, default_key='7:planned', title='Quero ver / ler', is_public=True),
                 dict(id=2, user_id=7, default_key='7:completed', title='Já assisti / li', is_public=True)]
        before = deepcopy(lists)
        plan = reconciliation_plan(lists, [])
        self.assertFalse(plan['cleanup_required'])
        self.assertEqual(plan['merges'], [])
        self.assertFalse(plan['executable'])
        self.assertEqual(lists, before)

    def test_union_and_restrictive_privacy_preserve_owner_and_metadata(self):
        lists = [dict(id=i, user_id=7, default_key='7:planned', title='Minha seleção',
                      description='Personalizada', is_public=i == 1) for i in (1, 2)]
        entries = [dict(list_id=1, media_id=10), dict(list_id=2, media_id=10), dict(list_id=2, media_id=11)]
        plan = reconciliation_plan(lists, entries)
        group = plan['merges'][0]
        self.assertEqual(group['canonical_id'], 1)
        self.assertEqual(group['duplicate_ids'], [2])
        self.assertEqual(group['media_ids'], [10, 11])
        self.assertFalse(group['is_public'])
        self.assertEqual(len(group['preserve_metadata']), 2)

    def test_titles_alone_never_merge_or_reclassify_custom_lists(self):
        lists = [dict(id=i, user_id=7, title='Quero ver / ler', is_public=True) for i in (1, 2)]
        plan = reconciliation_plan(lists, [])
        self.assertFalse(plan['cleanup_required'])
        self.assertEqual(plan['legacy_candidates_require_identity_review'], [1, 2])

    def test_cross_owner_identity_and_unknown_privacy_stop_for_review(self):
        lists = [dict(id=1, user_id=8, default_key='7:planned'),
                 dict(id=2, user_id=7, default_key='7:completed', is_public=True),
                 dict(id=3, user_id=7, default_key='7:completed')]
        plan = reconciliation_plan(lists, [])
        self.assertEqual(len(plan['conflicts']), 2)
        self.assertEqual(plan['merges'], [])

    def test_different_metadata_requires_review(self):
        lists = [dict(id=i, user_id=7, default_key='7:planned', title=f'Personalizado {i}', is_public=True)
                 for i in (1, 2)]
        self.assertTrue(reconciliation_plan(lists, [])['merges'][0]['requires_metadata_review'])

    def test_orphan_items_and_duplicate_snapshot_ids_are_rejected(self):
        with self.assertRaises(ValueError): reconciliation_plan([], [dict(list_id=1, media_id=5)])
        with self.assertRaises(ValueError): reconciliation_plan([dict(id=1), dict(id=1)], [])
