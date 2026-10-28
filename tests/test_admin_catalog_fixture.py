import copy
import unittest
from unittest.mock import patch

from tools import admin_catalog_fixture as fixture


class CatalogFixtureTests(unittest.TestCase):
    def test_get_preserves_actual_filter_and_auth_guard_in_isolated_tables(self):
        generated = fixture.script('get')
        original = fixture.sections(fixture.source('get'))
        self.assertIn(fixture.synthetic_tables(original['stack']), generated)
        self.assertIn('$db.admin_catalog_fixture_media.title ~ $input.search', generated)
        self.assertIn('$actor.account_status == "active" && $actor.role == "admin"', generated)
        self.assertIn('field_value = $input.actor_id', generated)
        self.assertNotIn('$auth.', generated)
        self.assertNotIn('function.run', generated)
        self.assertNotRegex(generated, r'\bdb\.(get|edit|query|add) (user|media)\b')
        self.assertNotIn('table media {', generated)

    def test_put_preserves_actual_validation_and_records_both_snapshots(self):
        generated = fixture.script('put')
        original = fixture.sections(fixture.source('put'))
        self.assertIn(fixture.synthetic_tables(original['stack']), generated)
        self.assertIn('text title filters=trim|min:1|max:500', generated)
        self.assertIn('int year? filters=min:1800|max:2200', generated)
        self.assertIn("u.protocol === 'https:'", generated)
        self.assertLess(generated.index('as $fixture_before'), generated.index('db.edit'))
        self.assertGreater(generated.index('as $fixture_after'), generated.index('db.edit'))
        self.assertNotRegex(generated, r'\bdb\.(get|edit|query|add) (user|media)\b')

    def test_extraction_fails_if_security_boundary_or_layout_changes(self):
        source = fixture.source('get')
        for changed in (source.replace('Security/require_current_session', 'Security/other'),
                        source.replace('db.get user', 'db.query user'),
                        source.replace('$auth.id', '$auth.other')):
            with self.subTest(changed=changed[:30]), self.assertRaises(ValueError):
                fixture.sections(changed)

    def test_manifest_is_explicitly_offline_and_has_required_scenarios(self):
        data = fixture.manifest()
        self.assertFalse(data['xano_executed'])
        self.assertFalse(data['session_validation_covered'])
        names = {case['name'] for case in data['cases']}
        self.assertTrue({'type_movie', 'type_series', 'type_anime', 'type_book',
                         'uppercase', 'literal_symbols', 'empty_result', 'movie_page_3',
                         'valid_edit', 'invalid_title', 'invalid_year', 'invalid_cover',
                         'missing_record', 'get_actor_999', 'put_actor_3'} <= names)
        for digest in data['source_sha256'].values():
            self.assertEqual(len(digest), 64)

    def test_checker_handles_all_types_empty_result_and_literal_search(self):
        for inputs in (dict(media_type=kind) for kind in ('movie', 'series', 'anime', 'book')):
            rows = [dict(row) for row in fixture.MEDIA if row['media_type'] == inputs['media_type']]
            data = dict(items=rows, total=len(rows), page=1, per_page=25, next_page=None)
            self.assertTrue(all(fixture.check_get(data, inputs).values()))
        for term, expected in [('ARRIVAL', [1, 2]), ('%_literal\\movie [Edition]', [3]),
                               ('fixture_no_match', [])]:
            data = dict(items=[dict(row) for row in fixture.MEDIA if row['id'] in expected],
                        total=len(expected), page=1, per_page=25, next_page=None)
            self.assertTrue(all(fixture.check_get(data, dict(media_type='movie', search=term)).values()))

    def test_checker_rejects_wrong_type_false_total_duplicates_and_bad_pagination(self):
        original = dict(items=[dict(fixture.MEDIA[3])], total=1, page=1, per_page=25, next_page=None)
        for changes in (dict(items=[dict(fixture.MEDIA[0])]), dict(total=True),
                        dict(items=[dict(fixture.MEDIA[3])]*2), dict(next_page=2), dict(page=2)):
            self.assertFalse(all(fixture.check_get(original | changes, dict(media_type='book')).values()))
        self.assertFalse(all(fixture.check_get(None, dict(media_type='book')).values()))

    def test_checker_rejects_regex_broadening_for_literal_search(self):
        data = dict(items=[dict(fixture.MEDIA[0])], total=1, page=1, per_page=25, next_page=None)
        self.assertFalse(all(fixture.check_get(data, dict(media_type='movie', search='.*')).values()))

    def test_checker_requires_expected_page_size_and_next_page(self):
        inputs = dict(media_type='movie', per_page=1, page=2)
        data = dict(items=[dict(fixture.MEDIA[0])], total=3, page=2, per_page=1, next_page=3)
        self.assertTrue(all(fixture.check_get(data, inputs).values()))
        self.assertFalse(all(fixture.check_get(data | dict(items=[]), inputs).values()))
        self.assertFalse(all(fixture.check_get(data | dict(next_page=None), inputs).values()))

    def valid_edit(self):
        before = dict(fixture.MEDIA[0], identity_key='fixture:movie:1', external_source='fixture',
                      external_id='1', description='Original', cover_url='', year=2000)
        inputs = dict(id=1, title='Corrected', description='New',
                      cover_url='https://fixture.test/new.jpg', year=2016)
        after = before | inputs
        result = {field: after[field] for field in ('id', *fixture.EDIT_FIELDS, 'media_type')}
        return dict(before=before, after=after, result=result), inputs

    def test_combined_pages_reject_overlap_missing_pages_and_wrong_order(self):
        inputs = dict(media_type='movie', per_page=1)
        pages = [dict(items=[dict(fixture.MEDIA[index])], total=3, page=page,
                      per_page=1, next_page=page+1 if page < 3 else None)
                 for page, index in enumerate((2, 0, 1), 1)]
        self.assertTrue(all(fixture.check_pages(pages, inputs).values()))
        overlap = copy.deepcopy(pages)
        overlap[2]['items'] = copy.deepcopy(overlap[1]['items'])
        self.assertFalse(all(fixture.check_pages(overlap, inputs).values()))
        self.assertFalse(all(fixture.check_pages(pages[:-1], inputs).values()))
        wrong_order = copy.deepcopy(pages)
        wrong_order[0]['items'], wrong_order[1]['items'] = wrong_order[1]['items'], wrong_order[0]['items']
        self.assertFalse(all(fixture.check_pages(wrong_order, inputs).values()))

    def test_malformed_row_id_is_rejected_without_raising(self):
        data = dict(items=[dict(id=[], title='Duna', media_type='book')],
                    total=1, page=1, per_page=25, next_page=None)
        self.assertFalse(all(fixture.check_get(data, dict(media_type='book')).values()))

    def test_put_checker_accepts_edit_and_rejects_each_identity_change(self):
        data, inputs = self.valid_edit()
        self.assertTrue(all(fixture.check_put(data, inputs).values()))
        for field in fixture.IDENTITY_FIELDS:
            changed = copy.deepcopy(data)
            changed['after'][field] = 'wrong'
            self.assertFalse(all(fixture.check_put(changed, inputs).values()))

    def test_put_checker_requires_before_snapshot_and_actual_saved_values(self):
        data, inputs = self.valid_edit()
        for key in ('before', 'after', 'result'):
            changed = copy.deepcopy(data)
            changed.pop(key)
            self.assertFalse(all(fixture.check_put(changed, inputs).values()))
        for key in ('before', 'after', 'result'):
            changed = copy.deepcopy(data)
            changed[key]['id'] = True
            self.assertFalse(all(fixture.check_put(changed, inputs).values()))
        changed = copy.deepcopy(data)
        changed['after']['title'] = 'Not saved'
        self.assertFalse(all(fixture.check_put(changed, inputs).values()))

    def test_cli_does_not_overwrite_existing_file(self):
        # Existing file is never opened for write by this test.
        with patch('sys.argv', ['fixture', '--operation', 'get', '--output', __file__]), \
                self.assertRaises(FileExistsError):
            fixture.main()

    def test_unknown_operation_is_rejected(self):
        with self.assertRaises(ValueError):
            fixture.script('post')


if __name__ == '__main__':
    unittest.main()
