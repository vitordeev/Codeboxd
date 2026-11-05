"""Preview or publish one explicitly selected administrative contract."""
import argparse
import json
from pathlib import Path

from tools import list_status_live as live
from tools.list_status_deployment import fingerprint
from tools.session_revocation import blocks, identity, export_workspace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('preview', 'apply'))
    endpoints = {
        'dashboard': ('admin_dashboard_GET.xs', 'admin/dashboard', 'GET'),
        'catalog': ('admin_catalog_GET.xs', 'admin/catalog', 'GET'),
        'catalog-edit': ('admin_catalog_id_PUT.xs', 'admin/catalog/{id}', 'PUT'),
    }
    parser.add_argument('--endpoint', choices=tuple(endpoints), default='dashboard')
    args = parser.parse_args()
    private = live.ROOT / ('.local/admin-' + args.endpoint + '-20261104')
    private.mkdir(exist_ok=True)
    live.PRIVATE = private
    run = live.Run()
    try:
        filename, endpoint_route, method = endpoints[args.endpoint]
        patch = (live.ROOT / 'xano/api/codeboxd' / filename).read_text(encoding='utf-8')
        docs = blocks(patch)
        if len(docs) != 1 or live.route(docs[0]) != (endpoint_route, method):
            raise ValueError('Unexpected dashboard candidate')
        key = identity(docs[0])
        baseline = export_workspace(run.client, run.base, run.headers)
        previous = {identity(d): d for d in blocks(baseline)}[key]
        backup = private / 'before.xs'
        if args.action == 'preview':
            if backup.exists():
                raise FileExistsError('Preserve previous backup')
            backup.write_text(previous, encoding='utf-8')
            (private / 'baseline.xs').write_text(baseline, encoding='utf-8')
            run.import_docs(patch, 'dashboard', publish=False)
            (private / 'approved.json').write_text(json.dumps({
                'candidate_sha256': fingerprint(patch),
                'baseline_sha256': fingerprint(baseline)}), encoding='utf-8')
            print(json.dumps({'preview_passed': True, 'published': False, 'documents': 1}))
        else:
            approved = json.loads((private / 'approved.json').read_text(encoding='utf-8'))
            if approved != {'candidate_sha256': fingerprint(patch), 'baseline_sha256': fingerprint(baseline)}:
                raise ValueError('Drift after reviewed preview')
            after = run.import_docs(patch, 'dashboard-publication', publish=True)
            run.import_docs(patch, 'dashboard-after', publish=False)
            preview = json.loads((private / 'dashboard-after-preview.json').read_text(encoding='utf-8'))
            if preview.get('operations'):
                raise ValueError('Published candidate still differs')
            report = dict(passed=True, published=True, documents=1,
                          only_endpoint=method + ' ' + endpoint_route, data_written=False,
                          unrelated_contracts_preserved=True, zero_delta=True,
                          candidate_sha256=fingerprint(patch),
                          before_sha256=fingerprint(backup.read_text(encoding='utf-8')),
                          after_sha256=fingerprint(after))
            output = live.ROOT / ('openspec/changes/gerenciamento-website/validation/' + args.endpoint + '-publication-2026-11-04.json')
            if output.exists():
                raise FileExistsError('Preserve previous publication evidence')
            output.write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(json.dumps(report))
    finally:
        run.client.close()


if __name__ == '__main__':
    main()
