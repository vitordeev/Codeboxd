"""Execute backend validation lambdas against synthetic data; no database mutations."""
import json
from pathlib import Path
import re
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]/'xano'


class BackendImageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(channel='msedge', headless=True)
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def source(self, path):
        return (ROOT/path).read_text(encoding='utf-8')

    def codes(self, path):
        return [json.loads(code) for code in re.findall(
            r'code = ("(?:[^"\\]|\\.)*")', self.source(path))]

    def evaluate(self, code, inputs, variables=None):
        return self.page.evaluate('(a)=>new Function("$input","$var",a.code)(a.inputs,a.variables)',
                                  {'code': code, 'inputs': inputs, 'variables': variables or {}})

    def record(self, **changes):
        return {'id': 1, 'user_id': 7, 'operation': 'create', 'operation_key': 'a'*32,
                'post_id': 0, 'expected_image_revision': 0, 'state': 'reserved',
                'cloud': 'fixture', 'public_id': 'codeboxd/posts/u7/'+'b'*32, **changes}

    def resource(self, **changes):
        public_id = self.record()['public_id']
        return {'public_id': public_id, 'resource_type': 'image', 'type': 'upload',
                'version': 2, 'asset_id': 'asset', 'format': 'png', 'bytes': 120,
                'width': 10, 'height': 12,
                'secure_url': f'https://res.cloudinary.com/fixture/image/upload/v2/{public_id}.png', **changes}

    def test_operation_validation_does_not_allow_cross_editor_or_invalid_revisions(self):
        code = self.codes('api/codeboxd/post_image_uploads_POST.xs')[0]
        valid = {'operation_key': 'a'*32, 'operation': 'create', 'post_id': 0, 'expected_image_revision': 0}
        self.assertTrue(self.evaluate(code, valid))
        for changed in ({'operation_key': '../bad'}, {'post_id': 2}, {'expected_image_revision': 1},
                        {'operation': 'replace'}, {'operation': 'delete'}):
            self.assertFalse(self.evaluate(code, valid | changed))

    def test_repeated_reserve_returns_committed_creation_but_not_another_replacement(self):
        code = self.codes('api/codeboxd/post_image_uploads_POST.xs')[1]
        request = {'operation': 'create', 'post_id': 0, 'expected_image_revision': 0}
        self.assertTrue(self.evaluate(code, request, {'existing': self.record(post_id=99, state='attached')}))
        self.assertFalse(self.evaluate(code, request | {'operation': 'replace', 'post_id': 18},
                                       {'existing': self.record(operation='replace', post_id=19)}))
        self.assertFalse(self.evaluate(code, request | {'expected_image_revision': 2},
                                       {'existing': self.record()}))

    def test_foreign_namespace_or_deleted_resource_cannot_be_verified(self):
        code = self.codes('function/PostImages/verify_resource.xs')[0]
        self.assertTrue(self.evaluate(code, {'user_id': 7, 'reservation': self.record()}))
        for changes in ({'user_id': 8}, {'public_id': 'codeboxd/posts/u8/'+'b'*32},
                        {'state': 'deleted'}, {'state': 'cleanup_pending'}, {'cloud': 'evil/host'}):
            self.assertFalse(self.evaluate(code, {'user_id': 7, 'reservation': self.record(**changes)}))

    def test_backend_builds_canonical_url_from_authenticated_provider_result(self):
        code = self.codes('function/PostImages/verify_resource.xs')[-1]
        result = self.evaluate(code, {'version': 2, 'reservation': self.record()},
                               {'lookup': self.resource()})
        self.assertEqual(result['url'], self.resource()['secure_url'])
        self.assertEqual(result['asset_id'], 'asset')
        self.assertNotIn('signature', result)
        self.assertNotIn('api_secret', result)

    def test_backend_rejects_replay_version_size_format_url_and_asset_changes(self):
        code = self.codes('function/PostImages/verify_resource.xs')[-1]
        for changed in ({'version': 3}, {'public_id': self.record()['public_id']+'1'},
                        {'bytes': 5242881}, {'bytes': True}, {'width': 0}, {'format': 'svg'},
                        {'type': 'private'}, {'secure_url': 'https://evil.example/img'},
                        {'asset_id': ''}, {'resource_type': 'video'}):
            self.assertIsNone(self.evaluate(code, {'version': 2, 'reservation': self.record()},
                                             {'lookup': self.resource(**changed)}))
        self.assertIsNone(self.evaluate(code, {'version': 2, 'reservation': self.record(asset_id='original')},
                                       {'lookup': self.resource(asset_id='different')}))
        self.assertIsNone(self.evaluate(code, {'version': 2, 'reservation': self.record()}, {'lookup': None}))

    def test_idempotent_commit_uses_lock_transaction_and_returns_existing_post(self):
        source = self.source('function/PostImages/create_post.xs')
        self.assertIn('db.transaction', source)
        self.assertEqual(source.count('lock = true'), 2)
        self.assertLess(source.index('lock = true'), source.index('db.get post_image_asset'))
        self.assertIn('if ($reservation.state == "attached")', source)
        self.assertIn('var.update $result { value = $existing }', source)
        self.assertIn('$existing.image_asset_record_id == $reservation.id', source)
        self.assertIn('$reservation.user_id == $input.user_id', source)
        self.assertIn('state: "attached"', source)
        self.assertIn('image_asset_record_id: $reservation.id', source)
        self.assertNotIn('destroy', source)

    def test_cleanup_is_queued_only_after_unlink_and_never_destroys_remotely(self):
        delete=self.source('api/codeboxd/posts_id_DELETE.xs')
        self.assertLess(delete.index('db.del post {'),delete.index('PostImages/queue_cleanup'))
        queue=self.source('function/PostImages/queue_cleanup.xs')
        self.assertIn('precondition ($references == 0)',queue)
        self.assertIn('add_secs_to_timestamp:86400',queue)
        self.assertIn('state: "cleanup_pending"',queue)
        self.assertNotIn('api.request',queue)
        self.assertNotIn('db.del post_image_asset',delete)

    def test_replace_and_remove_require_revision_inside_the_locked_transaction(self):
        source=self.source('function/PostImages/update_post.xs')
        self.assertIn('lock = true',source)
        self.assertIn('precondition ($revision_matches)',source)
        self.assertIn('$replacement.post_id == $record.id',source)
        self.assertIn('image_revision: $next_revision',source)
        self.assertIn('image_provider: null',source)
        self.assertLess(source.index('image_provider: null'),source.index('PostImages/queue_cleanup'))


if __name__ == '__main__':
    unittest.main()
