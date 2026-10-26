"""Auditoria documental local; não importa nem executa o aplicativo."""
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'openspec' / 'config.yaml').exists())
HOME = ROOT / 'openspec'
out = []
broken = []
links = 0
for path in HOME.rglob('*.md'):
    body = path.read_text(encoding='utf-8-sig')
    for raw in re.findall(r'!?\[[^\]]*\]\(([^\n)]+)\)', body):
        target = raw.strip().split(' "')[0].strip('<>')
        if re.match(r'^[a-zA-Z]+://|^#|^mailto:|^app:|^plugin:', target):
            continue
        target = unquote(target.split('#')[0])
        if not target or any(c in target for c in '*{}'):
            continue
        links += 1
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            broken.append({'file': str(path.relative_to(ROOT)), 'target': target})
for path in sorted((HOME / 'changes').glob('**/tasks.md')):
    body = path.read_text(encoding='utf-8-sig')
    checked = re.findall(r'^\s*- \[([ xX])\] (.+)$', body, re.M)
    ids = [re.match(r'(\d+\.\d+)\b', text).group(1) for _, text in checked if re.match(r'(\d+\.\d+)\b', text)]
    out.append({'change': str(path.parent.relative_to(HOME / 'changes')), 'done': sum(x.lower() == 'x' for x, _ in checked), 'open': sum(x == ' ' for x, _ in checked), 'duplicate_ids': sorted({x for x in ids if ids.count(x) > 1}), 'metadata': (path.parent / '.openspec.yaml').exists()})
conflicts = []
for path in HOME.rglob('*.md'):
    if re.search(r'^(?:<{7,}|={7,}|>{7,})', path.read_text(encoding='utf-8-sig'), re.M):
        conflicts.append(str(path.relative_to(ROOT)))
result = {'date': '2026-10-26', 'markdown_files': len(list(HOME.rglob('*.md'))), 'local_links_checked': links, 'broken_links': broken, 'conflict_markers': conflicts, 'checklists': out}
destination = Path(__file__).parent / 'audit.json'
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(broken or conflicts or any(x['duplicate_ids'] or not x['metadata'] for x in out) or any(x['open'] for x in out if x['change'].startswith('archive'))))
