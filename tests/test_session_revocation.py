"""Execute the actual claim validator and check every protected Xano contract."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

from tools.session_revocation import GUARD_NAME, guard_call, transform

ROOT = Path(__file__).resolve().parents[1]


class SessionRevocationTests(unittest.TestCase):
    def test_actual_javascript_rejects_legacy_stale_and_wrong_purpose(self):
        source = (ROOT / 'xano/function/security/require_current_session.xs').read_text(encoding='utf-8')
        code = json.loads(re.search(r'code = ("[^\n]+")', source)[1])
        cases = []
        for extras, version, allow, expected in (
                ({}, 0, False, False),
                ({'session_version': 0, 'purpose': 'session'}, None, False, True),
                ({'session_version': 0, 'purpose': 'session'}, 1, False, False),
                ({'session_version': '1', 'purpose': 'session'}, 1, False, False),
                ({'session_version': True, 'purpose': 'session'}, 1, False, False),
                ({'session_version': -1, 'purpose': 'session'}, -1, False, False),
                ({'session_version': 1, 'purpose': 'password_reset'}, 1, False, False),
                ({'session_version': 1, 'purpose': 'password_reset'}, 1, True, True),
                ({'session_version': 1, 'purpose': 'password_reset'}, 2, True, False),
                ({'session_version': 1, 'purpose': 'admin'}, 1, True, False),
                ({'session_version': 2, 'purpose': 'session'}, 2, False, True)):
            cases.append({'input': {'extras': extras, 'allow_reset': allow},
                          'var': {'session_user': {'session_version': version}}, 'expected': expected})
        node = shutil.which('node')
        self.assertIsNotNone(node, 'Node is required to execute the real Xano JavaScript policy')
        script = 'const f = new Function("$input", "$var", ' + json.dumps(code) + ');\n'
        script += 'const cases = ' + json.dumps(cases) + ';\n'
        script += 'if (!cases.every(c => f(c.input, c.var) === c.expected)) process.exit(1);'
        result = subprocess.run([node, '-e', script], capture_output=True)
        self.assertEqual(result.returncode, 0, 'Session claim policy failed')

    def test_every_authenticated_query_checks_session_before_any_action(self):
        count = 0
        for path in (ROOT / 'xano/api').rglob('*.xs'):
            source = path.read_text(encoding='utf-8')
            if re.search(r'\bauth\s*=\s*"user"', source):
                count += 1
                stack = source.split('stack {', 1)[1].lstrip()
                self.assertTrue(stack.startswith('function.run "' + GUARD_NAME + '"'), path.name)
                allowed = 'allow_reset: true' if 'reset/update_password' in source else 'allow_reset: false'
                self.assertIn(allowed, stack.split('}', 2)[0], path.name)
        self.assertEqual(count, 40)  # 39 remote endpoints and local /likes, not published.

    def test_guard_insertion_preserves_existing_authorization(self):
        before = 'query "x/{id}" verb=DELETE {\n auth = "user"\n stack {\n precondition ($user.role == "admin") { error_type = "accessdenied" }\n }\n}'
        after = transform(before)
        self.assertEqual(after.replace(guard_call(False) + '\n', '', 1), before)
        self.assertEqual(transform(after), after)

    def test_password_revalidation_occurs_under_lock_before_update(self):
        source = (ROOT / 'xano/api/authentication/reset/update_password_POST.xs').read_text(encoding='utf-8')
        transactional = source.split('db.transaction {', 1)[1]
        locked = transactional.index('as $locked_user')
        guarded = transactional.index(GUARD_NAME)
        changed = transactional.index('password: $input.password, session_version: $next_session_version')
        self.assertLess(locked, guarded)
        self.assertLess(guarded, changed)
        self.assertEqual(source.count(GUARD_NAME), 2)
