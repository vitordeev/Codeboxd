"""Verify backups preserve uploads and do not overwrite previous snapshots."""
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from tools.backup_uploads import backup


class UploadBackupTests(unittest.TestCase):
    def test_snapshot_preserves_nested_files_and_can_be_read_back(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'uploads'
            (source / 'profiles').mkdir(parents=True)
            content = b'original upload bytes\x00\xff'
            (source / 'profiles' / 'banner.png').write_bytes(content)
            target = root / 'snapshot.zip'
            result = backup(source, target)
            with ZipFile(target) as archive:
                self.assertEqual(archive.read('uploaded_files/profiles/banner.png'), content)
                self.assertIn('profiles/banner.png', json.loads(archive.read('manifest.json')))
            self.assertEqual((source / 'profiles' / 'banner.png').read_bytes(), content)
            self.assertEqual(result['files'], 1)
            self.assertTrue(result['verified'])

    def test_existing_backup_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'uploads'
            source.mkdir()
            (source / 'image.png').write_bytes(b'upload')
            target = root / 'snapshot.zip'
            target.write_bytes(b'previous backup')
            with self.assertRaises(FileExistsError):
                backup(source, target)
            self.assertEqual(target.read_bytes(), b'previous backup')

    def test_destination_inside_source_is_rejected_without_creating_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            target = source / 'snapshot.zip'
            with self.assertRaises(ValueError):
                backup(source, target)
            self.assertFalse(target.exists())

    def test_empty_source_does_not_produce_false_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'uploads'
            source.mkdir()
            target = Path(directory) / 'snapshot.zip'
            with self.assertRaises(ValueError):
                backup(source, target)
            self.assertFalse(target.exists())
