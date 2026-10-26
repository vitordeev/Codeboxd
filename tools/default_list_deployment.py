"""Private backup, scoped preview/deployment and reviewed identity backfill.

Never exports env or records inside the contract export; list/item backups
are private and separate. Publication requires a matching successful preview.
"""
import argparse
import json
from pathlib import Path
import re

import httpx

from tools.default_list_integrity import CHANGE, digest, read_table, reconciliation_plan
from tools.session_revocation import ROOT, blocks, export_workspace, identity, metadata_config

PRIVATE = ROOT / '.local/default-list-integrity/deployment'
FILES = ('xano/table/user_list.xs', 'xano/function/Lists/ensure_default_list.xs',
         'xano/api/authentication/auth/signup_POST.xs', 'xano/api/codeboxd/lists_POST.xs')
EXISTING_GUIDS = {'9VYvnA6iqkXTs0IWM26qVjsJRk0', 'urY15kLDHVGb4vbbHON3_u2xqTk', 'e0SNrmbgrquRIypbGRSj39HFkeI'}
NEW_GUID = 'Waq6O0hSEgPjZrB9CivK4X2fM'
DEFAULTS = {'Quero ver / ler': ('planned', 'Obras para descobrir depois.'),
            'Já assisti / li': ('completed', 'Obras que você já terminou.')}


def legacy_identity_plan(snapshot):
    assignments, seen = [], set()
    for row in snapshot['lists']:
        if row.get('default_key') or row.get('title') not in DEFAULTS: continue
        kind, description = DEFAULTS[row['title']]
        if row.get('description') != description:
            raise ValueError('Legacy title without matching provenance; review manually')
        key = f"{int(row['user_id'])}:{kind}"
        if key in seen: raise ValueError('Ambiguous legacy identity; do not backfill')
        seen.add(key)
        assignments.append(dict(id=int(row['id']), user_id=int(row['user_id']), default_key=key))
    return dict(snapshot_sha256=digest(snapshot), assignments=assignments)


def candidate():
    documents = [(ROOT / path).read_text(encoding='utf-8').strip() for path in FILES]
    if {identity(doc) for doc in documents} != EXISTING_GUIDS | {NEW_GUID}:
        raise ValueError('Unexpected candidate scope')
    if any(re.search(r'^\s*(env|records)\s*{', doc, re.M) for doc in documents):
        raise ValueError('Candidate must contain schema and logic only')
    return '\n---\n'.join(documents) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare-local', 'inventory', 'preview', 'publish', 'backfill'))
    args = parser.parse_args()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    patch = candidate()
    (PRIVATE / 'candidate.xs').write_text(patch, encoding='utf-8')
    if args.action == 'prepare-local':
        print(json.dumps(dict(documents=4, published=False, patch_sha256=digest(patch))))
        return
    base, headers = metadata_config()
    with httpx.Client(timeout=20, follow_redirects=False) as client:
        source = export_workspace(client, base, headers)
        by_guid = {identity(doc): doc for doc in blocks(source)}
        if not EXISTING_GUIDS.issubset(by_guid): raise ValueError('Published contracts differ from expected scope')
        if args.action == 'inventory':
            baseline = PRIVATE / 'baseline.xs'
            if baseline.exists() and baseline.read_text(encoding='utf-8') != source:
                raise ValueError('Preserve previous baseline and review remote drift')
            baseline.write_text(source, encoding='utf-8')
            snapshot = dict(lists=read_table(client, base, headers, 895415),
                            entries=read_table(client, base, headers, 895416))
            backup = PRIVATE / 'backup.json'
            if backup.exists() and json.loads(backup.read_text(encoding='utf-8')) != snapshot:
                raise ValueError('Preserve previous data backup and review drift')
            backup.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
            plan = reconciliation_plan(snapshot['lists'], snapshot['entries'])
            (PRIVATE / 'reconciliation-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
            report = dict(layer='real_xano_read_only', documents=len(by_guid), matched_existing=3,
                          lists=len(snapshot['lists']), entries=len(snapshot['entries']),
                          backup_sha256=digest(snapshot), remote_writes=0)
        elif args.action == 'backfill':
            plan = json.loads((PRIVATE / 'legacy-identities.json').read_text(encoding='utf-8'))
            backup = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
            if digest(backup) != plan['snapshot_sha256']: raise ValueError('Backup mismatch')
            current = dict(lists=read_table(client, base, headers, 895415),
                           entries=read_table(client, base, headers, 895416))
            def without_key(data):
                return dict(lists=[{k:v for k,v in row.items() if k != 'default_key'} for row in data['lists']], entries=data['entries'])
            if without_key(current) != without_key(backup): raise ValueError('Data changed; review required')
            journal = PRIVATE / 'backfill-journal.json'
            if journal.exists(): raise ValueError('Backfill already started; inspect journal before retry')
            changes = []
            journal.write_text(json.dumps(changes), encoding='utf-8')
            for assignment in plan['assignments']:
                old = next(row for row in current['lists'] if row['id'] == assignment['id'])
                if old.get('default_key') is not None: raise ValueError('Unexpected existing identity')
                response = client.put(f"{base}/table/895415/content/{assignment['id']}",
                    headers={**headers, 'x-data-source':'live'}, json={'default_key':assignment['default_key']})
                response.raise_for_status()
                changes.append(assignment)
                journal.write_text(json.dumps(changes), encoding='utf-8')
            after = dict(lists=read_table(client, base, headers, 895415),
                         entries=read_table(client, base, headers, 895416))
            if without_key(after) != without_key(backup): raise ValueError('Data preservation mismatch')
            expected = {row['id']:row['default_key'] for row in plan['assignments']}
            if any(row.get('default_key') != expected.get(row['id']) for row in after['lists']):
                raise ValueError('Backfill identity mismatch')
            report = dict(layer='real_xano_backfill', assignments=len(changes), lists=len(after['lists']),
                          entries=len(after['entries']), records_preserved=True, passed=True)
            (CHANGE / 'validation/backend-backfill.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(json.dumps(report))
            return
        else:
            if (PRIVATE / 'baseline.xs').read_text(encoding='utf-8') != source:
                raise ValueError('Remote drift since backup')
            publish = args.action == 'publish'
            if publish:
                approved = json.loads((PRIVATE / 'preview-approved.json').read_text(encoding='utf-8'))
                if approved.get('sha256') != digest(patch): raise ValueError('Preview does not match candidate')
                backup = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
                now = dict(lists=read_table(client, base, headers, 895415), entries=read_table(client, base, headers, 895416))
                if backup != now: raise ValueError('Data changed since backup')
                plan = legacy_identity_plan(backup)
                (PRIVATE / 'legacy-identities.json').write_text(json.dumps(plan, indent=2), encoding='utf-8')
            response = client.post(base + ('/multidoc' if publish else '/multidoc/dry-run'), headers={**headers, 'Content-Type':'text/x-xanoscript'},
                params={'partial':'true', 'env':'false', 'records':'false', 'delete':'false'}, content=patch.encode())
            response.raise_for_status()
            result = response.json()
            (PRIVATE / ('publish-response.json' if publish else 'preview-response.json')).write_text(json.dumps(result), encoding='utf-8')
            operations = result.get('operations', [])
            report = dict(layer='remote_publication' if publish else 'remote_dry_run', published=publish,
                operations=[{key: op.get(key) for key in ('type','name','action')} for op in operations],
                passed=(publish or bool(operations)) and all(op.get('type') in ('query','table','function')
                    and op.get('action') != 'delete' and 'parse error' not in str(op).lower() for op in operations))
            if not publish:
                expected = {('table','user_list','update'), ('table','user_list','add_field'),
                            ('function','Lists/ensure_default_list','create'),
                            ('query','auth/signup POST','update'), ('query','lists POST','update')}
                report['passed'] = report['passed'] and {(op.get('type'),op.get('name'),op.get('action')) for op in operations} == expected
            if not publish and report['passed']:
                (PRIVATE / 'preview-approved.json').write_text(json.dumps({'sha256':digest(patch)}), encoding='utf-8')
            if publish:
                after = export_workspace(client, base, headers)
                (PRIVATE / 'published.xs').write_text(after, encoding='utf-8')
                after_ids = {identity(doc):doc for doc in blocks(after)}
                unrelated = [key for key in by_guid if key not in EXISTING_GUIDS and by_guid[key] != after_ids.get(key)]
                report.update(unrelated_documents_changed=len(unrelated),
                    new_function_present=NEW_GUID in after_ids,
                    only_expected_function_added=set(after_ids)-set(by_guid)=={NEW_GUID},
                    removed_documents=len(set(by_guid)-set(after_ids)))
                report['passed'] = (report['passed'] and not unrelated and NEW_GUID in after_ids
                                    and report['only_expected_function_added'] and not report['removed_documents'])
        destination = CHANGE / ('validation/backend-inventory.json' if args.action == 'inventory'
                                else 'validation/backend-publication.json' if args.action == 'publish'
                                else 'validation/backend-preview.json')
        destination.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report))


if __name__ == '__main__':
    try: main()
    except httpx.RequestError as exc:
        raise SystemExit('Network unavailable (' + type(exc).__name__ + '); nothing published') from None
