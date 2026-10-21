import json
from pathlib import Path
import tempfile
import unittest

from tools.performance_inventory import inventory


class InventoryTests(unittest.TestCase):
    def test_collects_without_importing_and_keeps_nested_calls_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / 'Codeboxd_main'
            package.mkdir()
            (package / 'sample.py').write_text('''raise RuntimeError("must not import")
app.add_page(page, route="/example", on_load=S.visit("profile"))
class Example:
    @rx.event
    async def load(self):
        async def child():
            await request("GET", f"/profiles/{uid}")
        button("Save", self.save, on_click=self.save)
        await self._call("POST", "/lists")
''', encoding='utf-8')
            report = inventory(directory)
            self.assertEqual(report['routes'][0]['route'], '/example')
            self.assertEqual(report['routes'][0]['on_load'], "S.visit('profile')")
            functions = {f['name']: f for f in report['functions']}
            self.assertNotIn('request', [c['target'] for c in functions['Example.load']['calls']])
            self.assertEqual(functions['Example.load.child']['calls'][0]['target'], 'request')
            self.assertTrue(any(b['handler'] == 'self.save' for b in report['bindings']))
            self.assertEqual(len(report['files'][0]['sha256']), 64)
            json.dumps(report)

    def test_repository_routes_and_handlers_are_covered_deterministically(self):
        root = Path(__file__).resolve().parents[1]
        report = inventory(root)
        self.assertEqual(report, inventory(root))
        routes = {r['route'] for r in report['routes']}
        self.assertTrue({'/login', '/biblioteca', '/admin', '/admin/reports', '/admin/demo'} <= routes)
        functions = {f['name'] for f in report['functions']}
        self.assertTrue({'SocialState.load_library', 'SessionState.login', 'AdminState.load_dashboard'} <= functions)
        self.assertTrue(any(b['trigger'] == 'on_submit' for b in report['bindings']))
