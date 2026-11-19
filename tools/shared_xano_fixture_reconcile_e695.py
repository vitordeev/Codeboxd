"""Reconcile only the interrupted approved run e695fd5320e4, once."""
import argparse
import getpass
import json
from datetime import datetime, timezone
from pathlib import Path
import time

import httpx
from dotenv import dotenv_values

from tools.shared_xano_acceptance import digest
from tools.session_revocation import ROOT, metadata_config

RUN = 'cbshared_e695fd5320e4'
CHANGE = ROOT/'openspec/changes/reconciliar-fixtures-piloto-xano-e695fd5320e4'
OUTPUT = CHANGE/'cleanup-execution.json'
USER_TABLE, LIST_TABLE, ITEM_TABLE = 881681, 895415, 895416
EVENT_TABLE = 881682
USERS = {50: RUN+'_a', 51: RUN+'_b'}
LISTS = {125: (50, RUN+' public'), 126: (50, RUN+' private')}
MIN_INTERVAL = 10.0
MIN_READ_INTERVAL = 1.25
LAST_READ = None


class Stop(RuntimeError):
    pass


def save(state):
    tmp = OUTPUT.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(state, indent=2)+'\n', encoding='utf-8')
    tmp.replace(OUTPUT)


def pace_read():
    global LAST_READ
    if LAST_READ is not None:
        pause=max(0.0,MIN_READ_INTERVAL-(time.monotonic()-LAST_READ))
        if pause: time.sleep(pause)
    LAST_READ=time.monotonic()


def rows(client, base, headers, table_id):
    result, page, total, seen = [], 1, None, set()
    while True:
        if page in seen or len(seen) >= 50:
            raise Stop('pagination_loop_or_budget')
        seen.add(page)
        pace_read()
        response = client.get(f'{base}/table/{table_id}/content', headers={**headers, 'x-data-source':'live'},
                              params={'page':page,'per_page':100})
        if response.status_code != 200:
            raise Stop('inventory_read_http_'+str(response.status_code))
        body = response.json()
        if not isinstance(body,dict) or not isinstance(body.get('items'),list) or type(body.get('itemsTotal')) is not int:
            raise Stop('inventory_shape_unknown')
        if total is None: total = body['itemsTotal']
        elif total != body['itemsTotal']: raise Stop('inventory_changed_during_read')
        result.extend(body['items'])
        nxt = body.get('nextPage')
        if nxt in (None,False,0): break
        if type(nxt) is not int or nxt <= page: raise Stop('invalid_next_page')
        page = nxt
    if len(result) != total or any(not isinstance(r,dict) or type(r.get('id')) is not int for r in result):
        raise Stop('incomplete_or_invalid_inventory')
    return result


def row(client, base, headers, table_id, row_id):
    pace_read()
    response = client.get(f'{base}/table/{table_id}/content/{row_id}',headers={**headers,'x-data-source':'live'})
    if response.status_code != 200: raise Stop('target_read_http_'+str(response.status_code))
    value=response.json()
    if not isinstance(value,dict) or value.get('id') != row_id: raise Stop('target_identity_missing')
    return value


def public_ids(client,social):
    pace_read()
    response=client.get(social+'/lists/public',headers={'x-data-source':'live'},params={'page':1,'per_page':100})
    if response.status_code!=200: raise Stop('public_lists_read_http_'+str(response.status_code))
    value=response.json()
    if isinstance(value,dict): value=value.get('items')
    if not isinstance(value,list): raise Stop('public_lists_shape_unknown')
    return {r.get('id') for r in value if isinstance(r,dict)}


def main():
    global OUTPUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    OUTPUT=args.output.resolve()
    if not OUTPUT.is_relative_to(CHANGE.resolve()): parser.error('Output must remain inside this change.')
    if OUTPUT.exists(): raise Stop('receipt_already_exists_no_retry')
    config=dotenv_values(ROOT/'.env')
    auth,social=config['XANO_AUTH_URL'].rstrip('/'),config['XANO_SOCIAL_URL'].rstrip('/')
    meta,meta_headers=metadata_config()
    baseline=json.loads((ROOT/'.local/shared-xano-preflight-after-run9182-cleanup-escalated/baseline-hashes.json').read_text(encoding='utf-8'))
    tables=baseline['table_ids']
    if (baseline.get('destination',{}).get('workspace')!=147717
            or tables.get('user')!=USER_TABLE or tables.get('user_list')!=LIST_TABLE
            or tables.get('user_list_item')!=ITEM_TABLE or tables.get('event_log')!=EVENT_TABLE):
        raise Stop('reviewed_destination_or_table_ids_mismatch')
    state={'layer':'approved_interrupted_fixture_reconciliation','workspace':147717,'run_id':RUN,
           'passed':False,'remote_writes':0,'write_attempts':[],'checks':[],
           'fixture_ids':{'users':[50,51],'lists':[125,126]},
           'metadata_api_used_for_lists':True,'phase':'read_only_preflight'}
    save(state)
    last_write=None

    def write(client,method,url,headers,body,label,expected=(200,204)):
        nonlocal last_write
        if last_write is not None:
            pause=max(0.0,MIN_INTERVAL-(time.monotonic()-last_write))
            if pause: time.sleep(pause)
        attempt={'action':label,'state':'attempting','started_at':datetime.now(timezone.utc).isoformat()}
        state['write_attempts'].append(attempt);state['remote_writes']+=1;save(state)
        try: response=client.request(method,url,headers=headers,json=body)
        except httpx.RequestError:
            attempt['state']='uncertain_no_retry';save(state);raise Stop(label+'_uncertain_no_retry') from None
        attempt.update(http_status=response.status_code,finished_at=datetime.now(timezone.utc).isoformat())
        if response.status_code not in expected:
            attempt['state']='rejected_no_retry';save(state);raise Stop(label+'_rejected_'+str(response.status_code))
        attempt['state']='accepted';last_write=time.monotonic();save(state)

    try:
        with httpx.Client(timeout=60,follow_redirects=False,trust_env=False) as client:
            users=rows(client,meta,meta_headers,USER_TABLE)
            lists=rows(client,meta,meta_headers,LIST_TABLE)
            items=rows(client,meta,meta_headers,ITEM_TABLE)
            by_user={r['id']:r for r in users};by_list={r['id']:r for r in lists}
            for uid,username in USERS.items():
                u=by_user.get(uid)
                if not u or u.get('username')!=username or u.get('role')!='member' or u.get('account_status')!='active':
                    raise Stop('fixture_user_identity_or_status_mismatch')
            for lid,(owner,title) in LISTS.items():
                listing=by_list.get(lid)
                if (not listing or listing.get('user_id')!=owner or listing.get('title')!=title
                        or listing.get('default_key') is not None or listing.get('is_public') is not False):
                    raise Stop('fixture_list_identity_or_visibility_mismatch')
                if any(it.get('list_id')==lid for it in items): raise Stop('fixture_list_has_references')
            if set(public_ids(client,social)).intersection(LISTS): raise Stop('fixture_list_is_public')
            state['preflight']={'user_hashes':{str(i):digest(by_user[i]) for i in USERS},
                'list_hashes':{str(i):digest(by_list[i]) for i in LISTS},
                'all_list_hashes':{str(r['id']):digest(r) for r in lists},
                'all_item_hashes':{str(r['id']):digest(r) for r in items},
                'list_count':len(lists),'item_count':len(items),
                'references':{'125':[],'126':[]}}
            state['checks'].append({'check':'fixture_identity_private_state_and_empty_references','passed':True});save(state)

            email=input('E-mail do administrador Codeboxd (ID 14): ').strip()
            secret=getpass.getpass('Senha do administrador (entrada oculta): ')
            login=client.post(auth+'/auth/login',headers={'x-data-source':'live'},json={'email':email,'password':secret})
            secret=None
            if login.status_code!=200: raise Stop('admin_login_rejected_before_writes')
            body=login.json();token=body.get('authToken')
            if body.get('user_id')!=14 or not isinstance(token,str): raise Stop('expected_admin_identity_mismatch')
            admin={'Authorization':'Bearer '+token,'x-data-source':'live'}
            pace_read();me=client.get(auth+'/auth/me',headers=admin)
            actor=me.json() if me.status_code==200 else {}
            if actor.get('id')!=14 or actor.get('role')!='admin' or actor.get('account_status')!='active' or str(actor.get('email','')).casefold()!=email.casefold():
                raise Stop('active_admin_confirmation_failed')
            state['admin_confirmed']=True;state['phase']='mutating';save(state)

            before_events=rows(client,meta,meta_headers,EVENT_TABLE)
            event_max=max((r['id'] for r in before_events),default=0)
            state['preflight']['event_log_max_id']=event_max;save(state)

            for lid,(owner,title) in LISTS.items():
                current=row(client,meta,meta_headers,LIST_TABLE,lid)
                current_items=rows(client,meta,meta_headers,ITEM_TABLE)
                if current.get('user_id')!=owner or current.get('title')!=title or current.get('is_public') is not False or any(it.get('list_id')==lid for it in current_items):
                    raise Stop('list_identity_or_references_changed_before_delete')
                write(client,'DELETE',f'{meta}/table/{LIST_TABLE}/content/{lid}',{**meta_headers,'x-data-source':'live'},None,'delete_list_'+str(lid))
                check_lists=rows(client,meta,meta_headers,LIST_TABLE)
                check_items=rows(client,meta,meta_headers,ITEM_TABLE)
                hashes={str(r['id']):digest(r) for r in check_lists}
                expected=dict(state['preflight']['all_list_hashes']);expected.pop(str(lid),None)
                if hashes!=expected or {str(r['id']):digest(r) for r in check_items}!=state['preflight']['all_item_hashes']:
                    raise Stop('post_delete_unrelated_data_changed')
                state['checks'].append({'check':'list_'+str(lid)+'_deleted_other_lists_and_items_preserved','passed':True});save(state)

            for uid in (51,50):
                pace_read()
                lookup=client.get(social+'/admin/users',headers=admin,params={'search':USERS[uid],'page':1,'per_page':25})
                value=lookup.json().get('items',[]) if lookup.status_code==200 else []
                matches=[r for r in value if r.get('id')==uid and r.get('username')==USERS[uid]]
                if len(matches)!=1 or matches[0].get('role')!='member' or matches[0].get('account_status')!='active':
                    raise Stop('fixture_user_admin_identity_or_status_mismatch')
                write(client,'PUT',social+f'/admin/users/{uid}/status',admin,
                    {'account_status':'disabled','reason':RUN+' approved cleanup'},'disable_user_'+str(uid),(200,))
                pace_read()
                verify=client.get(social+'/admin/users',headers=admin,params={'search':USERS[uid],'page':1,'per_page':25})
                found=[r for r in verify.json().get('items',[]) if r.get('id')==uid] if verify.status_code==200 else []
                if len(found)!=1 or found[0].get('account_status')!='disabled': raise Stop('user_disable_verification_failed')
                state['checks'].append({'check':'user_'+str(uid)+'_disabled','passed':True});save(state)

            after_events=rows(client,meta,meta_headers,EVENT_TABLE)
            new_events=[r for r in after_events if r.get('id',0)>event_max]
            audited={r.get('metadata',{}).get('target_user_id') for r in new_events
                     if r.get('user_id')==14 and r.get('action')=='admin_account_status_changed'
                     and r.get('metadata',{}).get('new_status')=='disabled'}
            if not {50,51}.issubset(audited): raise Stop('admin_status_audit_events_missing')
            state['checks'].append({'check':'admin_disable_events_for_50_and_51_preserved','passed':True})
            final_users=rows(client,meta,meta_headers,USER_TABLE)
            final_by={r['id']:r for r in final_users}
            if any(final_by.get(uid,{}).get('account_status')!='disabled' for uid in USERS): raise Stop('final_user_state_mismatch')
            state['audit_events_verified_for']=[50,51]
            state['passed']=all(c['passed'] for c in state['checks']);state['phase']='complete'
            state['completed_at']=datetime.now(timezone.utc).isoformat();save(state)
    except Exception as exc:
        state['failure_reason']=str(exc) if isinstance(exc,Stop) else type(exc).__name__
        state['phase']='interrupted';save(state);raise


if __name__=='__main__': main()
