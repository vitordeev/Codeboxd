"""Scoped previews and rollback preparation. This CLI never publishes contracts."""
import argparse
import hashlib
import json
import re

import httpx

from tools.default_list_integrity import digest
from tools.list_status_contracts import candidate, FILES, ROOT
from tools.list_status_migration import PRIVATE, migration_plan
from tools.session_revocation import blocks, identity, metadata_config, export_workspace


def fingerprint(text):
    return hashlib.sha256(text.encode()).hexdigest()


def expected_operations(patch, baseline):
    existing = {identity(doc) for doc in blocks(baseline)}
    expected = set()
    for doc in blocks(patch):
        match = re.search(r'^(table|function|query)\s+(?:"([^"]+)"|([\w/-]+))(?:\s+verb=(\w+))?', doc, re.M)
        if not match:
            raise ValueError('Unexpected candidate document')
        kind, name = match[1], match[2] or match[3]
        if kind == 'query':
            name += ' ' + match[4]
        expected.add((kind, name, 'update' if identity(doc) in existing else 'create'))
    return expected


def rollback_bundle(baseline, patch, snapshot):
    before = {identity(doc): doc for doc in blocks(baseline)}
    affected = {identity(doc) for doc in blocks(patch)}
    plan = migration_plan(snapshot)
    rollback = '\n---\n'.join(before[key] for key in sorted(affected & before.keys())) + '\n'
    records = {
        'snapshot_sha256': digest(snapshot),
        'restore_default_items': [row for row in snapshot['user_list_item'] if row['id'] in plan['legacy_item_ids']],
        'restore_follows': [row for row in snapshot['user_follow'] if row['id'] in
                           set(plan['follow_delete_ids']) | {r['id'] for r in plan['follow_rewrites']}],
        'new_object_guids_review_before_removal': sorted(affected - before.keys()),
        'requires_writers_blocked': True,
        'refuse_automatic_rollback_after_release': True,
    }
    return rollback, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('preview', 'prepare-rollback'))
    args = parser.parse_args()
    if not (ROOT / 'openspec/changes/corrigir-conexoes-feed-listas').is_dir():
        parser.error('Change is no longer active; do not overwrite historical evidence')
    baseline = (PRIVATE / 'baseline.xs').read_text(encoding='utf-8')
    patch = candidate()
    if len(blocks(patch)) != len(FILES):
        raise ValueError('Candidate document count mismatch')
    (PRIVATE / 'candidate.xs').write_text(patch, encoding='utf-8')
    if args.action == 'prepare-rollback':
        snapshot = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
        source, records = rollback_bundle(baseline, patch, snapshot)
        (PRIVATE / 'rollback-contracts.xs').write_text(source, encoding='utf-8')
        (PRIVATE / 'rollback-records.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
        print(json.dumps({'rollback_documents': len(blocks(source)),
                          'restore_default_items': len(records['restore_default_items']),
                          'restore_follows': len(records['restore_follows']), 'remote_writes': 0}))
        return
    base, headers = metadata_config()
    with httpx.Client(timeout=40, follow_redirects=False) as client:
        if export_workspace(client, base, headers) != baseline:
            raise ValueError('Remote drift since backup; preserve and review before preview')
        response = client.post(base + '/multidoc/dry-run',
            headers={**headers, 'Content-Type': 'text/x-xanoscript'},
            params={'partial': 'true', 'env': 'false', 'records': 'false', 'delete': 'false'},
            content=patch.encode())
        (PRIVATE / 'preview-final-response.json').write_text(response.text, encoding='utf-8')
        if response.status_code != 200:
            raise ValueError('Remote preview failed; inspect private response')
        result = response.json()
        operations = result.get('operations', [])
        actual = {(r.get('type'), r.get('name'), r.get('action')) for r in operations}
        passed = (actual == expected_operations(patch, baseline)
                  and not result.get('has_records') and not result.get('has_env')
                  and not result.get('warnings') and
                  all('parse error' not in str(row).lower() for row in operations))
        report = {'passed': passed, 'published': False, 'candidate_sha256': fingerprint(patch),
                  'baseline_sha256': fingerprint(baseline),
                  'operations': [{key: row.get(key) for key in ('type', 'name', 'action')} for row in operations]}
        (PRIVATE / 'preview-approved.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        evidence = ROOT / 'openspec/changes/corrigir-conexoes-feed-listas/validation'
        evidence.mkdir(exist_ok=True)
        (evidence / 'preview-2026-11-03.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report))
        if not passed:
            raise ValueError('Unexpected preview scope; publication forbidden')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, httpx.HTTPError) as exc:
        raise SystemExit('Preparation failed (' + type(exc).__name__ + '); nothing published') from None
