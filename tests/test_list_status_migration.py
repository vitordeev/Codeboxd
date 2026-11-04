from copy import deepcopy
import unittest

from tools.list_status_migration import migration_plan, verify_preservation


class ListStatusMigrationTests(unittest.TestCase):
    def fixture(self):
        return {
            'user': [{'id': 1}, {'id': 2}], 'media': [{'id': 10}, {'id': 11}],
            'user_list': [
                {'id': 1, 'user_id': 1, 'default_key': '1:planned', 'title': 'Renamed'},
                {'id': 2, 'user_id': 1, 'default_key': '1:completed', 'is_public': False},
                {'id': 3, 'user_id': 1, 'default_key': None, 'title': 'Já assisti / li'}],
            'user_list_item': [
                {'id': 1, 'list_id': 1, 'media_id': 10},
                {'id': 2, 'list_id': 2, 'media_id': 10},
                {'id': 3, 'list_id': 3, 'media_id': 10},
                {'id': 4, 'list_id': 99, 'media_id': 11}],
            'user_follow': [{'id': 1, 'follower_id': 1, 'followed_id': 2, 'identity_key': '1:2'}],
            'user_media_interaction': [{'id': 1, 'rating': 4.5, 'review': 'Keep review', 'spoiler': True}],
        }

    def migrated(self, snapshot, plan):
        after = deepcopy(snapshot)
        after['user_list_item'] = [r for r in after['user_list_item'] if r['id'] not in plan['legacy_item_ids']]
        after['user_media_list_status'] = [dict(r, id=i+1) for i,r in enumerate(plan['statuses'])]
        return after

    def test_watched_wins_and_custom_homonym_and_orphans_are_preserved(self):
        data = self.fixture()
        plan = migration_plan(data)
        self.assertEqual(plan['statuses'], [{'user_id': 1, 'media_id': 10, 'status': 'watched'}])
        self.assertEqual(plan['legacy_item_ids'], [1, 2])
        self.assertEqual(plan['conflicts_resolved'], 1)
        self.assertTrue(verify_preservation(data, self.migrated(data, plan), plan))

    def test_review_and_custom_metadata_changes_fail_preservation(self):
        data = self.fixture()
        plan = migration_plan(data)
        for table, field, value in (('user_media_interaction', 'rating', 0),
                                     ('user_media_interaction', 'review', ''),
                                     ('user_list', 'title', 'Overwritten'),
                                     ('user_list_item', 'media_id', 11)):
            with self.subTest(table=table, field=field):
                after = self.migrated(data, plan)
                after[table][0][field] = value
                with self.assertRaises(ValueError):
                    verify_preservation(data, after, plan)

    def test_cross_owner_default_key_is_rejected(self):
        data = self.fixture()
        data['user_list'][0]['default_key'] = '2:planned'
        with self.assertRaises(ValueError):
            migration_plan(data)

    def test_empty_default_key_is_not_treated_as_custom(self):
        data = self.fixture()
        data['user_list'][0]['default_key'] = ''
        with self.assertRaises(ValueError):
            migration_plan(data)

    def test_default_orphan_is_rejected_without_a_plan_to_delete_it(self):
        data = self.fixture()
        data['user_list_item'][0]['media_id'] = 999
        with self.assertRaises(ValueError):
            migration_plan(data)

    def test_changed_snapshot_cannot_use_previous_plan(self):
        data = self.fixture()
        plan = migration_plan(data)
        data['user_media_interaction'][0]['review'] = 'New review'
        with self.assertRaises(ValueError):
            verify_preservation(data, self.migrated(data, plan), plan)

    def test_more_than_a_hundred_items_are_not_truncated(self):
        data = self.fixture()
        data['media'] = [{'id': i} for i in range(1, 252)]
        data['user_list_item'] = [{'id': i, 'list_id': 1, 'media_id': i} for i in range(1,252)]
        plan = migration_plan(data)
        self.assertEqual(len(plan['statuses']), 251)
        self.assertTrue(verify_preservation(data, self.migrated(data, plan), plan))

    def test_repeated_planning_preserves_existing_watched_and_is_deterministic(self):
        data = self.fixture()
        data['user_list_item'] = data['user_list_item'][:1]
        data['user_media_list_status'] = [{'id': 1, 'user_id': 1, 'media_id': 10, 'status': 'watched'}]
        first = migration_plan(data)
        self.assertEqual(first, migration_plan(data))
        self.assertEqual(first['statuses'][0]['status'], 'watched')

    def test_follow_dedup_keeps_lowest_id_and_rejects_cross_pair_key(self):
        data = self.fixture()
        data['user_follow'].append({'id': 2, 'follower_id': 1, 'followed_id': 2, 'identity_key': 'old'})
        self.assertEqual(migration_plan(data)['follow_delete_ids'], [2])
        data['user_follow'][0]['identity_key'] = 'bad'
        data['user_follow'].append({'id': 3, 'follower_id': 2, 'followed_id': 1, 'identity_key': '1:2'})
        with self.assertRaises(ValueError):
            migration_plan(data)

    def test_duplicate_orphan_follow_requires_review(self):
        data = self.fixture()
        data['user_follow'] = [{'id': i, 'follower_id': 999, 'followed_id': 2, 'identity_key': str(i)} for i in (1,2)]
        with self.assertRaises(ValueError):
            migration_plan(data)

    def test_extra_or_duplicate_status_fails_preservation(self):
        data = self.fixture()
        plan = migration_plan(data)
        after = self.migrated(data, plan)
        after['user_media_list_status'].append(deepcopy(after['user_media_list_status'][0]))
        with self.assertRaises(ValueError):
            verify_preservation(data, after, plan)
