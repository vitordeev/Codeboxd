"""Read-only default-list inventory and reviewable reconciliation plans.

Never deletes, creates or edits remote records. Titles alone never establish a
system-list identity. Raw lists/items stay in an ignored private backup.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import uuid

import httpx

from tools.session_revocation import ROOT, metadata_config

DEFAULT_KINDS = ('planned', 'completed')
CHANGE = ROOT / 'openspec/changes/corrigir-duplicacao-listas-padrao'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def reconciliation_plan(lists, entries):
    """Produce a plan only; merging requires a separate reviewed operation."""
    by_id = {int(row['id']): row for row in lists}
    if len(by_id) != len(lists): raise ValueError('Duplicate list IDs in snapshot')
    groups, items = defaultdict(list), defaultdict(set)
    legacy, conflicts, merges = [], [], []
    for entry in entries:
        lid = int(entry['list_id'])
        if lid not in by_id: raise ValueError('Orphan list item; stop for review')
        items[lid].add(int(entry['media_id']))
    for row in lists:
        key = row.get('default_key')
        if not key:
            if str(row.get('title', '')).strip().casefold() in ('quero ver / ler', 'já assisti / li'):
                legacy.append(int(row['id']))
            continue
        owner = int(row['user_id'])
        if key not in [f'{owner}:{kind}' for kind in DEFAULT_KINDS]:
            conflicts.append(dict(list_id=int(row['id']), reason='identity_owner_or_kind_mismatch'))
            continue
        groups[key].append(row)
    for key, group in sorted(groups.items()):
        if len(group) < 2: continue
        group = sorted(group, key=lambda row: int(row['id']))
        union = set().union(*(items[int(row['id'])] for row in group))
        if any(not isinstance(row.get('is_public'), bool) for row in group):
            conflicts.append(dict(list_ids=[int(r['id']) for r in group], reason='unknown_privacy'))
            continue
        metadata_conflict = len({(row.get('title', ''), row.get('description', '')) for row in group}) > 1
        merges.append(dict(default_key=key, user_id=int(group[0]['user_id']),
            canonical_id=int(group[0]['id']), duplicate_ids=[int(r['id']) for r in group[1:]],
            media_ids=sorted(union), is_public=all(row['is_public'] for row in group),
            preserve_metadata=[dict(id=int(r['id']), title=r.get('title', ''),
                                    description=r.get('description', '')) for r in group],
            requires_metadata_review=metadata_conflict))
    return dict(snapshot_sha256=digest(dict(lists=lists, entries=entries)),
                mode='plan_only_no_writes', merges=merges, conflicts=conflicts,
                legacy_candidates_require_identity_review=legacy,
                cleanup_required=bool(merges), executable=False)


def read_table(client, base, headers, table):
    result, seen, page, total = [], set(), 1, None
    while True:
        if page in seen: raise ValueError('Repeated page')
        seen.add(page)
        response = client.get(f'{base}/table/{table}/content', headers={**headers, 'x-data-source': 'live'},
                              params={'page': page, 'per_page': 100})
        response.raise_for_status()
        batch = response.json()
        if not isinstance(batch, dict) or not isinstance(batch.get('items'), list):
            raise ValueError('Unexpected pagination')
        if total is None: total = batch['itemsTotal']
        if total != batch['itemsTotal']: raise ValueError('Remote table changed during pagination')
        result.extend(batch['items'])
        if not batch.get('nextPage'): break
        page = int(batch['nextPage'])
    if len(result) != total or len({row['id'] for row in result}) != total:
        raise ValueError('Incomplete snapshot')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--remote', action='store_true')
    source.add_argument('--snapshot', type=Path)
    args = parser.parse_args()
    if args.remote:
        base, headers = metadata_config()
        with httpx.Client(timeout=20, follow_redirects=False) as client:
            data = dict(lists=read_table(client, base, headers, 895415),
                        entries=read_table(client, base, headers, 895416))
    else:
        data = json.loads(args.snapshot.read_text(encoding='utf-8'))
    plan = reconciliation_plan(data['lists'], data['entries'])
    private = ROOT / '.local/default-list-integrity' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8])
    private.mkdir(parents=True)
    (private / 'backup.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    (private / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    report = dict(layer='real_xano_read_only' if args.remote else 'local_snapshot',
                  lists=len(data['lists']), entries=len(data['entries']),
                  duplicate_default_groups=len(plan['merges']), conflicts=len(plan['conflicts']),
                  legacy_candidates=len(plan['legacy_candidates_require_identity_review']),
                  cleanup_required=plan['cleanup_required'], remote_writes=0,
                  backup_sha256=plan['snapshot_sha256'])
    print(json.dumps(report))
    if args.remote:
        (CHANGE / 'validation/integridade-remote.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    try: main()
    except httpx.RequestError as exc:
        raise SystemExit('Network unavailable (' + type(exc).__name__ + '); no writes performed') from None
