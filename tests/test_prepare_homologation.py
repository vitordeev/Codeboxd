"""Contracts preparation and destination guards; no remote calls or credentials."""
from pathlib import Path
import tempfile
import unittest

from tools.prepare_homologation import FILES, ROOT, PreparationRejected, build_bundle, sanitize_contract, validate_destination


class HomologationPreparationTests(unittest.TestCase):
    def test_real_bundle_has_only_expected_contracts_and_fresh_api_identity(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            for relative in FILES:
                target = project / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            output = project / '.local/prepared'
            report = build_bundle(project, output)
            self.assertEqual(report['counts'], {'table': 13, 'function': 3, 'api_group': 2, 'query': 14})
            self.assertEqual(report['document_count'], 32)
            self.assertFalse(report['published'])
            self.assertFalse(report['records_included'])
            text = (output / 'contracts.xs').read_text(encoding='utf-8')
            for value in ('guid =', 'canonical =', 'api.request', 'util.send_email', '$env.', 'reset/request-reset-link'):
                self.assertNotIn(value, text)
            self.assertEqual(len(list((output / 'xano').rglob('*.xs'))), len(FILES))
            with self.assertRaisesRegex(PreparationRejected, 'preserve_existing'):
                build_bundle(project, output)

    def test_records_env_extra_documents_and_outgoing_mail_are_rejected(self):
        for value in ('table user { items = [{id:1}] }', 'env { secret="private" }',
                      'table a {}\ntable b {}', 'query a verb=POST { util.send_email {} }',
                      'query a verb=GET { api.request {} }', 'function a { value=$env.KEY }',
                      'table a {}\nenv { key="private" }'):
            with self.subTest(value=value), self.assertRaises(PreparationRejected):
                sanitize_contract(value)

    def test_secret_is_rejected_without_echoing_its_value(self):
        secret = 'private-password-literal'
        with self.assertRaises(PreparationRejected) as failure:
            sanitize_contract('function a { password = "' + secret + '" }')
        self.assertNotIn(secret, str(failure.exception))

    def test_table_response_items_are_not_confused_with_data_import(self):
        kind, text = sanitize_contract('query a verb=GET { response = {items: $items} }')
        self.assertEqual(kind, 'query')
        self.assertIn('items: $items', text)

    def target(self, **changes):
        args = dict(protected_origin='https://source.xano.io', protected_workspace_id=147717,
                    target_origin='https://source.xano.io', target_workspace_id=147717)
        return validate_destination(**(args | changes))

    def test_current_workspace_and_same_origin_sandbox_are_blocked(self):
        with self.assertRaisesRegex(PreparationRejected, 'protected_destination'):
            self.target()
        with self.assertRaisesRegex(PreparationRejected, 'protected_destination'):
            self.target(kind='sandbox')

    def test_separate_identity_is_not_claimed_as_full_isolation_proof(self):
        result = self.target(target_workspace_id=200000)
        self.assertTrue(result['identity_only_not_isolation_proof'])
        self.assertEqual(self.target(kind='sandbox', target_origin='https://isolated.xano.io')['kind'], 'sandbox')

    def test_credentials_non_https_queries_and_boolean_workspace_are_rejected(self):
        for changes in ({'target_origin':'http://isolated.xano.io'},
                        {'target_origin':'https://user:password@isolated.xano.io'},
                        {'target_origin':'https://isolated.xano.io/?token=private'},
                        {'target_origin':'https://source.xano.io.evil.example'},
                        {'target_workspace_id':True}):
            with self.subTest(changes=changes), self.assertRaises(PreparationRejected):
                self.target(**changes)


if __name__ == '__main__':
    unittest.main()
