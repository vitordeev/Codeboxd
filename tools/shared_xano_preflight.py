"""Read-only inventory and contract backup; never provisions or executes a batch."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import secrets
import time
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

from tools.admin_acceptance_guard import digest
from tools.session_revocation import ROOT, metadata_config, blocks

CHANGE = ROOT / 'openspec/changes/validar-integracoes-xano-atual'
REQUIRED = [('auth/signup','POST'), ('auth/login','POST'), ('auth/me','GET'),
            ('lists','POST'), ('lists','GET'), ('lists/{id}','PUT'),
            ('lists/{id}','DELETE'), ('lists/public','GET'),
            ('admin/users/{id}/status','PUT')]


class PreflightStopped(RuntimeError):
    pass


def inventory_hashes(rows):
    if not isinstance(rows, list):
        raise PreflightStopped('invalid_inventory')
    result = {}
    for row in rows:
        if not isinstance(row, dict) or type(row.get('id')) is not int or row['id'] <= 0 or str(row['id']) in result:
            raise PreflightStopped('invalid_or_duplicate_id')
        result[str(row['id'])] = digest(row)
    return result


def configured_target(config):
    urls = [urlsplit(config.get(key, '')) for key in ('XANO_AUTH_URL','XANO_SOCIAL_URL')]
    for url in urls:
        if (url.scheme != 'https' or not url.hostname or not url.hostname.endswith('.xano.io')
                or url.username or url.password or url.query or url.fragment
                or not re.fullmatch(r'/api:[A-Za-z0-9_-]+/?',url.path)):
            raise PreflightStopped('invalid_configured_destination')
    if urls[0].netloc != urls[1].netloc:
        raise PreflightStopped('cross_instance_destination')
    return {'origin':'https://'+urls[0].netloc, 'workspace':147717,
            'branch':'v1', 'data_source':'live',
            'auth_group':urls[0].path.strip('/'), 'social_group':urls[1].path.strip('/')}


class Reads:
    def __init__(self, client, base, headers, *, pause=time.sleep):
        self.client, self.base, self.headers = client, base, headers
        self.calls = 0
        self.pause = pause

    def get(self, path, **params):
        if self.calls >= 150 or not (path in ('','/table','/apigroup','/branch','/multidoc')
                                    or re.fullmatch(r'/table/[1-9][0-9]*/content',path)):
            raise PreflightStopped('read_budget_or_route_rejected')
        if self.calls:
            self.pause(1.1)
        self.calls += 1
        response = self.client.get(self.base+path,headers={**self.headers,'x-data-source':'live'},params=params)
        if response.status_code != 200:
            raise PreflightStopped('metadata_read_http_'+str(response.status_code))
        return response

    def rows(self, table_id):
        rows, total, page, seen = [], None, 1, set()
        while True:
            if page in seen or len(seen) >= 50:
                raise PreflightStopped('pagination_loop_or_budget')
            seen.add(page)
            body = self.get('/table/'+str(table_id)+'/content',page=page,per_page=100).json()
            if not isinstance(body,dict) or not isinstance(body.get('items'),list) or type(body.get('itemsTotal')) is not int:
                raise PreflightStopped('invalid_pagination')
            if total is None:
                total = body['itemsTotal']
            if total != body['itemsTotal']:
                raise PreflightStopped('inventory_changed_during_pagination')
            rows.extend(body['items'])
            next_page = body.get('nextPage')
            if next_page is None or next_page is False or next_page == 0:
                break
            if type(next_page) is not int or next_page <= page:
                raise PreflightStopped('invalid_next_page')
            page = next_page
        hashes = inventory_hashes(rows)
        if len(rows) != total:
            raise PreflightStopped('incomplete_inventory')
        return rows, hashes


def sequence(body):
    if isinstance(body,list):
        return body
    if isinstance(body,dict) and isinstance(body.get('items'),list) and not body.get('nextPage'):
        if 'itemsTotal' in body and body['itemsTotal'] != len(body['items']):
            raise PreflightStopped('incomplete_metadata_listing')
        return body['items']
    raise PreflightStopped('metadata_listing_shape_unknown')


def verify_groups(target, groups):
    result = {}
    for field, name in [('auth_group','Authentication'),('social_group','Codeboxd')]:
        matches = [r for r in groups if 'api:'+str(r.get('canonical')) == target[field]]
        if len(matches) != 1 or matches[0].get('name') != name or matches[0].get('branch') != target['branch']:
            raise PreflightStopped('api_group_or_branch_mismatch')
        result[field] = matches[0]['id']
    return result


def collect(private, output):
    if private.exists() or output.exists():
        raise PreflightStopped('new_evidence_paths_required')
    if not private.resolve().is_relative_to((ROOT/'.local').resolve()):
        raise PreflightStopped('private_directory_required')
    target = configured_target(dotenv_values(ROOT/'.env'))
    base, headers = metadata_config()
    if base != target['origin']+'/api:meta/workspace/147717':
        raise PreflightStopped('metadata_destination_mismatch')
    private.mkdir(parents=True)
    report = {'layer':'real_xano_read_only_preflight','remote_writes':0,
              'fixtures_created':0,'pilot_executed':False,'passed':False,
              'branch_verified':False,'started_at':datetime.now(timezone.utc).isoformat()}
    try:
        with httpx.Client(timeout=35,follow_redirects=False,trust_env=False) as client:
            reader = Reads(client,base,headers)
            source = reader.get('/multidoc',env='false',records='false').text
            (private/'contracts-without-env-records.xs').write_text(source,encoding='utf-8')
            report['contracts_sha256'] = hashlib.sha256(source.encode()).hexdigest()
            docs = {}
            for block in blocks(source):
                match = re.search(r'^query\s+(?:"([^"]+)"|([A-Za-z_]\w*))\s+verb=(\w+)',block,re.M)
                if match:
                    key = (match[1] or match[2],match[3])
                    if key in docs:
                        raise PreflightStopped('ambiguous_route')
                    docs[key] = block
            report['required_contracts'] = {method+' '+path: (path,method) in docs for path,method in REQUIRED}
            groups = sequence(reader.get('/apigroup').json())
            (private/'api-group-descriptors.json').write_text(json.dumps(groups),encoding='utf-8')
            verified_groups = verify_groups(target,groups)
            report.update(branch_verified=True,api_group_ids=verified_groups)
            report['api_group_count'] = len(groups)
            tables = sequence(reader.get('/table').json())
            baseline, counts = {}, {}
            admin_candidates = []
            table_ids = {}
            for table in tables:
                name, table_id = table.get('name'), table.get('id')
                if not isinstance(name,str) or name in table_ids or type(table_id) is not int or table_id <= 0:
                    raise PreflightStopped('invalid_or_duplicate_table')
                rows, hashes = reader.rows(table_id)
                baseline[name], counts[name], table_ids[name] = hashes,len(rows),table_id
                if name == 'user':
                    admin_candidates = [row['id'] for row in rows if row.get('role') == 'admin' and row.get('account_status') == 'active']
                rows = []
            if not {'user','profile','user_list','user_list_item','event_log'} <= baseline.keys():
                raise PreflightStopped('pilot_tables_missing')
            evidence = {'destination':target, 'captured_at':time.time(), 'tables':baseline,
                        'table_ids':table_ids, 'active_admin_candidates':admin_candidates,
                        'complete':True, 'temporal_snapshot_atomic':False}
            (private/'baseline-hashes.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
            run = 'cbshared_'+secrets.token_hex(6)
            manifest = {'run_id':run,'destination':target,'baseline_digest':digest(evidence),
                        'steps':['signup_member_A','signup_member_B','make_four_fixture_default_lists_private','create_public_custom_list_A',
                                 'create_private_custom_list_A','verify_persistence_authorship_privacy',
                                 'delete_two_custom_lists_as_owner','disable_two_members_as_original_admin'],
                        'accounts_to_create':2,'profiles_created_by_signup':2,
                        'default_lists_created_by_signup':4,'custom_lists_to_create':2,
                        'retained_domain_rows':8,'retained_default_lists_visibility':'private','audit_policy':'retain_all',
                        'existing_domain_records_to_mutate':0,'contract_publications':0,
                        'exact_fixture_ids_available':False,'creation_receipts_available':False,
                        'executable':False,'mutating_batch_approved':False}
            (private/'provisioning-preview.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
            report.update(inventory_complete=True,counts=counts,table_count=len(counts),
                          baseline_digest=digest(evidence),provisioning_preview_digest=digest(manifest),
                          run_id=run,active_admin_candidates=len(admin_candidates),requests=reader.calls,
                          passed=all(report['required_contracts'].values()),
                          limitation='Snapshot is not atomic. Refresh inventory and routing before mutation; no fixtures or receipts exist.')
    except (httpx.HTTPError,PreflightStopped,ValueError,KeyError,TypeError) as exc:
        report['failure_type'] = type(exc).__name__
        if isinstance(exc,PreflightStopped):
            report['failure_reason'] = str(exc)
    output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    print(json.dumps(collect(args.private,args.output)))


if __name__ == '__main__':
    main()
