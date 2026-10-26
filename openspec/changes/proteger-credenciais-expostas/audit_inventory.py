"""Read-only heuristic inventory; never emit matched values or raw Git output."""
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LIMIT = 2_000_000


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    if result.returncode:
        raise RuntimeError('Git inventory operation failed; raw output suppressed')
    return result.stdout


def safe_path(path):
    if '@' in path:
        return '[private-path]'
    return path


def inventory():
    configured = {}
    local_summary = []
    for name, value in dotenv_values(ROOT / '.env').items():
        if re.search(r'TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY', name, re.I):
            local_summary.append({'variable': name, 'configured': bool(value)})
            if value and len(value) >= 12:
                configured[name] = value

    patterns = {
        'jwt_candidate': re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'),
        'aws_access_id_candidate': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
        'github_token_candidate': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),
        'resend_key_candidate': re.compile(r'\bre_[A-Za-z0-9]{20,}\b'),
        'deepl_key_candidate': re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}:fx\b'),
        'private_key_candidate': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        'password_literal_candidate': re.compile(r'''["']?(?:password|senha|aws_secret_access_key)["']?\s*[:=]\s*["']([^"'\r\n]{8,})["']''', re.I),
    }
    findings = []
    scanned = Counter()
    skipped = Counter()
    sensitive_paths = []

    def inspect(data, scope, path, obj=''):
        if len(data) > LIMIT or b'\0' in data[:8000]:
            skipped[scope] += 1
            return
        scanned[scope] += 1
        text = data.decode('utf-8', errors='replace')
        for category, regex in patterns.items():
            matches = list(regex.finditer(text))
            if matches:
                findings.append({'scope': scope, 'path': safe_path(path), 'object': obj,
                                 'category': category, 'lines': sorted({text.count('\n', 0, m.start()) + 1 for m in matches})})
        for name, value in configured.items():
            pos = text.find(value)
            if pos >= 0:
                findings.append({'scope': scope, 'path': safe_path(path), 'object': obj,
                                 'category': 'exact_local_value:' + name,
                                 'lines': [text.count('\n', 0, pos) + 1]})

    # Unique reachable objects; paths are Git's representative path per object.
    objects = git('rev-list', '--objects', '--all').decode('utf-8', errors='replace').splitlines()
    batch = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    blobs = 0
    try:
        for entry in objects:
            oid, _, path = entry.partition(' ')
            batch.stdin.write((oid + '\n').encode())
            batch.stdin.flush()
            header = batch.stdout.readline().split()
            if len(header) != 3:
                raise RuntimeError('Unexpected Git object header; content suppressed')
            size = int(header[2])
            data = batch.stdout.read(size)
            batch.stdout.read(1)
            if header[1] != b'blob':
                continue
            blobs += 1
            if path == '.env' or path.startswith('.aws/') or re.search(r'(?:account|conta|credential)', path, re.I):
                sensitive_paths.append({'scope': 'history', 'path': safe_path(path), 'object': oid})
            inspect(data, 'history', path, oid)
    finally:
        batch.stdin.close()
        batch.wait()

    for entry in git('ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        metadata, path_bytes = entry.split(b'\t', 1)
        mode, oid, stage = metadata.decode().split()
        if mode == '160000':
            skipped['index_submodule'] += 1
            continue
        inspect(git('cat-file', 'blob', oid), 'index', path_bytes.decode('utf-8', errors='replace'), oid)

    # Current project files including ignored local artifacts; dependencies/builds excluded.
    exclude = {'.git', '.venv', 'venv', '.web', '.states', 'node_modules', '__pycache__',
               'uploaded_files', '.pytest_cache', '.agents', '.codex', 'Imagens'}
    import os
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in exclude and not (Path(base) == ROOT and d == '.local')]
        for filename in files:
            path = Path(base) / filename
            if path.is_symlink():
                skipped['worktree_symlink'] += 1
                continue
            if path.stat().st_size > LIMIT:
                skipped['worktree'] += 1
                continue
            inspect(path.read_bytes(), 'worktree', path.relative_to(ROOT).as_posix())

    # Include ignored .local text/log/JSON artifacts, excluding generated frontends/builds.
    for path in (ROOT / '.local').glob('*'):
        if path.is_file() and not path.is_symlink() and path.stat().st_size <= LIMIT:
            inspect(path.read_bytes(), 'local_top_level', '.local/' + path.name)
    for path in (ROOT / '.local').glob('xano-before-*/*.json'):
        if path.is_file() and not path.is_symlink() and path.stat().st_size <= LIMIT:
            inspect(path.read_bytes(), 'local_xano_backup', '.local/[xano-backup]/' + path.name)

    output = {'commits': int(git('rev-list', '--all', '--count')), 'shallow': git('rev-parse', '--is-shallow-repository').decode().strip(),
              'reachable_blobs': blobs, 'scanned': dict(scanned), 'skipped': dict(skipped),
              'local_configuration': local_summary, 'sensitive_paths': sensitive_paths, 'findings': findings,
              'limitations': ['No remote fetch or provider validation', 'No reflog/unreachable objects',
                              'Binary and >2MB content excluded', 'Generated directories and nested .local builds excluded',
                              'Heuristic candidates require triage; representative path per history object',
                              'No secret values or fingerprints persisted']}
    (HERE / 'inventory.json').write_text(json.dumps(output, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    print(json.dumps({'commits': output['commits'], 'reachable_blobs': blobs, 'scanned': dict(scanned),
                      'skipped': dict(skipped), 'categories': dict(Counter(f['category'] for f in findings)),
                      'configured_variable_names': [x['variable'] for x in local_summary]}, indent=2))


if __name__ == '__main__':
    try:
        inventory()
    except Exception:
        raise SystemExit('Inventory failed; raw exception suppressed to protect private content') from None
