"""Synthetic cases only; temporary Git repositories never contain real secrets."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.check_staged_secrets import check_index, scan_bytes


class StagedSecretTests(unittest.TestCase):
    def test_patterns_report_locations_without_values(self):
        samples = [b'eyJ' + b'A' * 20 + b'.' + b'B' * 30 + b'.' + b'C' * 30,
                   b'AKIA' + b'Z' * 16, b'ghp_' + b'X' * 36,
                   b're_' + b'X' * 24, b'01234567-' + b'0123-0123-0123-0123456789ab:fx',
                   b'-----BEGIN ' + b'PRIVATE KEY-----']
        for sample in samples:
            with self.subTest(prefix=sample[:3]):
                result = scan_bytes('config.txt', b'prefix\n' + sample)
                self.assertTrue(result)
                self.assertEqual(result[0]['line'], 2)
                self.assertNotIn(sample.decode(), json.dumps(result))

    def test_binary_known_secret_and_filename_are_redacted(self):
        secret = b'private-synthetic-value-123'
        result = scan_bytes(secret.decode() + '.bin', b'\0' + secret, [secret])
        self.assertNotIn(secret.decode(), json.dumps(result))
        self.assertEqual(result[0]['path'], '[private-path]')

    def test_private_files_and_public_placeholders(self):
        for path in ('.env', '.env.production', '.aws/credentials', '.local/rotation.json', '.xano/credentials.yaml'):
            self.assertEqual(scan_bytes(path, b'')[0]['rule'], 'private_file')
        for path in ('.env.example', 'deploy/production.env.example'):
            self.assertEqual(scan_bytes(path, b'TMDB_READ_TOKEN=\nXANO_AUTH_URL=https://YOUR-INSTANCE.xano.io/api:AUTH'), [])

    def test_reads_staged_blob_not_modified_worktree_and_ignores_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            def git(*args):
                subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True)
            git('init', '-q')
            sample = 're_' + 'Q' * 30
            file = repo / 'settings.txt'
            file.write_text(sample)
            git('add', 'settings.txt')
            file.write_text('safe worktree')
            result = check_index(repo)
            self.assertFalse(result['passed'])
            self.assertNotIn(sample, json.dumps(result))
            git('add', 'settings.txt')
            self.assertTrue(check_index(repo)['passed'])
            git('-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid', 'commit', '-qm', 'fixture')
            file.unlink()
            git('add', '-u')
            self.assertEqual(check_index(repo)['scanned_files'], 0)
