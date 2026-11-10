"""Run the actual Xano password policy JavaScript, including Unicode boundaries."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


class ResetPasswordPolicyTests(unittest.TestCase):
    def test_backend_policy_boundaries_and_character_rules(self):
        source = (Path(__file__).resolve().parents[1] / 'xano/api/authentication/reset/update_password_POST.xs').read_text(encoding='utf-8')
        code = json.loads(re.search(r'code = ("[^\n]+")', source)[1])
        cases = [(p, expected) for p, expected in (
            ('Abc1234', False), ('Abc12345', True), ('A1' + 'x' * 126, True),
            ('A1' + 'x' * 127, False), ('A1' + 'é' * 126, True),
            ('abcdefgh', False), ('12345678', False), ('abcdefg١', False),
            ('  Ab1234  ', True), ('Abcdef1😀', True))]
        node = shutil.which('node')
        self.assertIsNotNone(node)
        script = 'const f=new Function("$input",' + json.dumps(code) + ');\n'
        script += 'const cases=' + json.dumps(cases) + ';\n'
        script += 'if(!cases.every(([password,want])=>f({password})===want))process.exit(1);'
        result = subprocess.run([node, '-e', script], capture_output=True)
        self.assertEqual(result.returncode, 0, 'Backend password policy rejected a contract case')
