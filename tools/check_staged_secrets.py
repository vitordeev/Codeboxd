"""Check staged Git content without printing credentials. No network or Git writes."""
import argparse
import json
from pathlib import Path
import re
import subprocess

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'jwt': re.compile(rb'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'),
    'aws_access_key': re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'github_token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),
    'resend_key': re.compile(rb'\bre_[A-Za-z0-9_]{20,}\b'),
    'deepl_key': re.compile(rb'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}:fx\b'),
    'private_key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
}
PRIVATE_DIRS = {'.local', '.aws', '.xano', '.venv', 'venv', '.states', '.web', 'uploaded_files'}


def private_path(path):
    parts = Path(path).parts
    name = parts[-1] if parts else ''
    if name.endswith('.env.example') or name == '.env.example':
        return any(part in PRIVATE_DIRS for part in parts[:-1])
    return (any(part in PRIVATE_DIRS for part in parts) or name == '.env'
            or name.startswith('.env.') or name.endswith('.env'))


def safe_path(path, known_values):
    if '@' in path or any(value and value.decode('utf-8', errors='replace') in path for value in known_values):
        return '[private-path]'
    return path


def scan_bytes(path, content, known_values=()):
    findings = []
    label = safe_path(path, known_values)
    if private_path(path):
        findings.append({'path': label, 'rule': 'private_file'})
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(content):
            findings.append({'path': label, 'rule': name, 'line': content.count(b'\n', 0, match.start()) + 1})
    for value in known_values:
        if value and value in content:
            findings.append({'path': label, 'rule': 'configured_secret'})
    return findings


def git(repo, *args):
    result = subprocess.run(['git', *args], cwd=repo, capture_output=True)
    if result.returncode:
        raise RuntimeError('Git check failed; raw output suppressed')
    return result.stdout


def check_index(repo=ROOT, all_index=False):
    config = dotenv_values(repo / '.env') if (repo / '.env').exists() else {}
    known = [v.encode() for k, v in config.items() if v and len(v) >= 12
             and re.search(r'TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY', k, re.I)]
    selected = None if all_index else set(git(repo, 'diff', '--cached', '--name-only', '--diff-filter=ACMRT', '-z').split(b'\0'))
    findings = []
    scanned = 0
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        if selected is not None and name not in selected:
            continue
        mode, oid, stage = metadata.decode().split()
        path = name.decode('utf-8', errors='replace')
        if stage != '0':
            findings.append({'path': safe_path(path, known), 'rule': 'unmerged_index'})
            continue
        if mode == '160000':
            findings.append({'path': safe_path(path, known), 'rule': 'submodule_not_inspected'})
            continue
        scanned += 1
        content = git(repo, 'cat-file', 'blob', oid)
        findings.extend(scan_bytes(path, content, known))
    return {'scanned_files': scanned, 'mode': 'all-index' if all_index else 'staged-changes',
            'passed': not findings, 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all-index', action='store_true', help='Also inspect unchanged indexed files')
    args = parser.parse_args()
    try:
        result = check_index(all_index=args.all_index)
    except Exception:
        print('Secret check failed; private details suppressed')
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
