import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import read_only_journey_browser as runner


class FixtureLoginTests(unittest.TestCase):
    def test_only_prepared_generated_reader_can_log_in_automatically(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, 'ROOT', Path(directory)):
            path = Path(directory) / '.local/fixture.json'
            path.parent.mkdir()
            marker = 'cbst_123456abcdef'
            journal = {'fixture_marker': marker, 'browser_fixture_ready': True, 'test_users': [
                {'id': 1, 'username': marker + '_a', 'email': marker + '_a@example.invalid', 'password': 'synthetic'},
                {'id': 2}]}
            path.write_text(json.dumps(journal), encoding='utf-8')
            self.assertEqual(runner.fixture_credentials(path)['id'], 1)
            for field, value in (('email', 'existing@example.com'), ('username', 'existing'),
                                 ('id', 0), ('password', '')):
                invalid = json.loads(json.dumps(journal))
                invalid['test_users'][0][field] = value
                path.write_text(json.dumps(invalid), encoding='utf-8')
                with self.subTest(field=field), self.assertRaises(ValueError):
                    runner.fixture_credentials(path)
            journal['browser_fixture_ready'] = False
            path.write_text(json.dumps(journal), encoding='utf-8')
            with self.assertRaises(ValueError):
                runner.fixture_credentials(path)

    def test_path_outside_private_workspace_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, 'ROOT', Path(directory)):
            with self.assertRaises(ValueError):
                runner.fixture_credentials(Path(directory) / 'outside.json')
