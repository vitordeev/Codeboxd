"""Review modified/untracked project files without staging or printing secret values."""
import json
import re
import subprocess
import sys

from dotenv import dotenv_values
from audit_inventory import ROOT, HERE

sys.path.insert(0, str(ROOT))
from tools.check_staged_secrets import scan_bytes


def main():
    names = set()
    for args in (('diff', '--name-only', '-z'), ('ls-files', '--others', '--exclude-standard', '-z')):
        result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True)
        names.update(x.decode('utf-8') for x in result.stdout.split(b'\0') if x)
    known = [v.encode() for k, v in dotenv_values(ROOT / '.env').items()
             if v and len(v) >= 12 and re.search(r'TOKEN|KEY|SECRET|PASSWORD', k)]
    for private in (ROOT / '.local' / 'credential-rotation').glob('account-*.json'):
        value = json.loads(private.read_text(encoding='utf-8')).get('password')
        if value:
            known.append(value.encode())
    findings = []
    count = 0
    for name in sorted(names):
        path = ROOT / name
        if path.is_file():
            count += 1
            findings.extend(scan_bytes(name, path.read_bytes(), known))
    report = {'mode': 'modified-and-untracked-working-tree', 'scanned_files': count,
              'passed': not findings, 'findings': findings}
    (HERE / 'working-tree-secret-check.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    if findings:
        raise SystemExit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        raise SystemExit('Working tree review failed; private output suppressed') from None
