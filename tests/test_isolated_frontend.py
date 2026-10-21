import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.isolated_frontend import prepare_frontend


class IsolatedFrontendTests(unittest.TestCase):
    def test_generated_files_and_builds_are_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            web = root / '.web'
            for name in ('app', 'node_modules', 'build', 'backend', '.react-router'):
                (web / name).mkdir(parents=True)
                (web / name / 'original.txt').write_text(name)
            package_build=web / 'node_modules/package/build'
            package_build.mkdir(parents=True)
            (package_build / 'index.js').write_text('required package code')
            with patch('tools.isolated_frontend.ROOT', root):
                isolated = prepare_frontend('test-production')
                self.assertEqual((isolated / 'app/original.txt').read_text(), 'app')
                self.assertEqual((isolated / 'node_modules/original.txt').read_text(), 'node_modules')
                (isolated / 'node_modules/original.txt').write_text('new installation')
                self.assertEqual((web / 'node_modules/original.txt').read_text(),'node_modules')
                self.assertEqual((isolated / 'node_modules/package/build/index.js').read_text(),
                                 'required package code')
                for name in ('build', 'backend', '.react-router'):
                    self.assertFalse((isolated / name).exists())
                (isolated / 'app/original.txt').write_text('changed')
                self.assertEqual((web / 'app/original.txt').read_text(), 'app')
                with self.assertRaises(FileExistsError):
                    prepare_frontend('test-production')

    def test_names_cannot_escape_generated_directory(self):
        for name in ('../escape', 'a/b', 'a\\b', '', 'C:drive'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                prepare_frontend(name)
