from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import httpx

from tools.main_journey_browser import Audit, TABLES, metadata_token


class MetadataProfileTests(unittest.TestCase):
    def credentials(self, default='project'):
        raw = ("profiles:\n"
               "  default:\n"
               "    access_token: PRIVATE_OTHER_TOKEN\n"
               "    instance_origin: https://other.example.test\n"
               "    expires_at: 123\n"
               "  project:\n"
               "    access_token: 'PRIVATE_PROJECT_TOKEN'\n"
               "    instance_origin: https://project.example.test/\n")
        return raw + (f'default: {default}\n' if default is not None else '')

    def test_declared_default_selects_matching_origin_not_first_token(self):
        self.assertEqual(metadata_token(self.credentials(), 'https://project.example.test'),
                         'PRIVATE_PROJECT_TOKEN')

    def test_no_default_requires_unique_origin_match(self):
        self.assertEqual(metadata_token(self.credentials(None), 'https://project.example.test'),
                         'PRIVATE_PROJECT_TOKEN')
        raw = self.credentials(None).replace('https://other.example.test', 'https://project.example.test')
        with self.assertRaisesRegex(RuntimeError, '^metadata_profile_ambiguous$'):
            metadata_token(raw, 'https://project.example.test')

    def test_default_with_wrong_origin_never_falls_back_to_other_token(self):
        with self.assertRaisesRegex(RuntimeError, '^metadata_profile_origin$'):
            metadata_token(self.credentials('default'), 'https://project.example.test')

    def test_unknown_default_fails_without_disclosing_names_or_tokens(self):
        with self.assertRaisesRegex(RuntimeError, '^metadata_profile_ambiguous$') as caught:
            metadata_token(self.credentials('PRIVATE_MISSING_PROFILE'), 'https://project.example.test')
        self.assertNotIn('PRIVATE', str(caught.exception))

    def test_quoted_url_profile_names_are_supported(self):
        raw = self.credentials().replace('  project:', '  "https://project.example.test":')
        raw = raw.replace('default: project', 'default: "https://project.example.test"')
        self.assertEqual(metadata_token(raw, 'https://project.example.test'), 'PRIVATE_PROJECT_TOKEN')

    def test_duplicate_profiles_fields_and_defaults_fail_closed(self):
        variants = [self.credentials() + 'default: project\n',
                    self.credentials().replace('    expires_at:', '    access_token:'),
                    self.credentials().replace("    access_token: 'PRIVATE_PROJECT_TOKEN'",
                                               "    access_token: 'PRIVATE_PROJECT_TOKEN'\n    access_token:"),
                    self.credentials().replace('  project:', '  default:')]
        for raw in variants:
            with self.subTest(variant=variants.index(raw)), self.assertRaises(RuntimeError):
                metadata_token(raw, 'https://project.example.test')

    def test_missing_token_and_non_https_origin_fail_closed(self):
        raw = self.credentials().replace("    access_token: 'PRIVATE_PROJECT_TOKEN'\n", '')
        with self.assertRaises(RuntimeError):
            metadata_token(raw, 'https://project.example.test')
        with self.assertRaisesRegex(RuntimeError, '^metadata_profile_origin$'):
            metadata_token(self.credentials(), 'http://project.example.test')


class JourneyAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data = {
            'user_list': [dict(id=1, user_id=7, title='PRIVATE_LIST')],
            'user_list_item': [dict(id=1, list_id=1, media_id=2)],
            'post': [dict(id=1, user_id=7, body='PRIVATE_POST')],
            'user_media_interaction': [dict(id=1, user_id=7, media_id=2, review='PRIVATE_REVIEW')],
            'media': [dict(id=1, title='Movie', identity_key='tmdb:movie:603', external_source='tmdb',
                           external_id='603', media_type='movie'),
                      dict(id=2, title='Other', identity_key='tmdb:movie:2', external_source='tmdb',
                           external_id='2', media_type='movie')],
        }
        self.ids = {name: index+1 for index, name in enumerate(self.data)}
        self.deleted = []
        def handler(request):
            path = request.url.path
            if path == '/auth/me': return httpx.Response(200, json=dict(id=7, role='member', account_status='active'))
            if path == '/meta/table': return httpx.Response(200, json=[dict(name=name, id=tid) for name, tid in self.ids.items()])
            parts = path.split('/')
            name = next(name for name, tid in self.ids.items() if tid == int(parts[3]))
            if len(parts) == 5:
                return httpx.Response(200, json={'items': deepcopy(self.data[name]), 'nextPage': None})
            rid = int(parts[5])
            row = next(row for row in self.data[name] if row['id'] == rid)
            if request.method == 'GET': return httpx.Response(200, json=deepcopy(row))
            self.deleted.append((name, rid))
            self.data[name].remove(row)
            return httpx.Response(204)
        self.client = httpx.Client(transport=httpx.MockTransport(handler))
        self.addCleanup(self.client.close)
        self.report = dict(verification_requests=[], cleanup=[])
        self.audit = Audit(self.client, 'https://example.test', 'https://example.test',
                           'https://example.test/meta', 'PRIVATE_META_TOKEN', self.report, pause=0)
        self.audit.token = 'PRIVATE_MEMBER_TOKEN'
        self.audit.journal = Path(self.tmp.name)/'journal.json'

    def test_existing_review_is_excluded_and_no_credentials_exported(self):
        self.audit.prepare()
        self.assertEqual(self.audit.mid, 1)
        self.assertTrue(self.audit.ready)
        output = json.dumps(self.report)+self.audit.journal.read_text()
        for private in ('PRIVATE_META_TOKEN', 'PRIVATE_MEMBER_TOKEN', 'PRIVATE_LIST', 'PRIVATE_POST', 'PRIVATE_REVIEW'):
            self.assertNotIn(private, output)
        self.assertFalse(self.deleted)

    def test_cleanup_only_removes_new_owned_marked_records(self):
        self.audit.prepare()
        marker = self.audit.marker
        fixtures = {
            'user_list': dict(id=12, user_id=7, title=marker+' list'),
            'user_list_item': dict(id=12, list_id=12, media_id=1),
            'post': dict(id=12, user_id=7, body=marker+' post'),
            'user_media_interaction': dict(id=12, user_id=7, media_id=1, review=marker+' review'),
        }
        for table, row in fixtures.items(): self.data[table].append(row)
        self.data['post'].append(dict(id=99, user_id=8, body=marker+' foreign'))
        self.audit.cleanup()
        self.assertEqual(set(self.deleted), {(table, 12) for table in TABLES})
        self.assertTrue(self.report['cleanup_complete'])
        self.assertTrue(all(self.report['existing_records_unchanged'].values()))
        self.assertTrue(any(row['id'] == 99 for row in self.data['post']))

    def test_original_ids_cannot_be_deleted_even_with_matching_marker(self):
        self.audit.prepare()
        self.assertFalse(self.audit.fixture('post', dict(id=1, user_id=7, body=self.audit.marker)))
        self.assertFalse(self.audit.fixture('user_media_interaction',
            dict(id=1, user_id=7, media_id=1, review=self.audit.marker)))

    def test_changed_existing_record_fails_storage_comparison_without_deleting_it(self):
        self.audit.prepare()
        self.data['post'][0]['body'] = 'External legitimate edit'
        with self.assertRaisesRegex(RuntimeError, 'storage_comparison_failed'):
            self.audit.cleanup()
        self.assertFalse(self.deleted)
        self.assertFalse(self.report['existing_records_unchanged']['post'])

    def test_rate_limit_is_not_retried_and_records_only_sanitized_metrics(self):
        calls = []
        def limited(request):
            calls.append(request)
            return httpx.Response(429, headers={'Retry-After': '20'})
        with httpx.Client(transport=httpx.MockTransport(limited)) as client:
            self.audit.client = client
            with self.assertRaisesRegex(RuntimeError, 'verification_rate_limit'):
                self.audit.api('/profiles/7', {'search': 'PRIVATE_QUERY'})
        self.assertEqual(len(calls), 1)
        self.assertNotIn('PRIVATE_QUERY', json.dumps(self.report))
        self.assertNotIn('/profiles/7', json.dumps(self.report))
        self.assertGreater(self.audit.retry_until, 0)

    def test_cleanup_before_preflight_cannot_delete_anything(self):
        self.audit.cleanup()
        self.assertFalse(self.deleted)
