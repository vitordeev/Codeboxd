"""Finish only the approved admin-status actions after list deletion receipt verification."""
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

RUN='cbshared_e695fd5320e4'
CHANGE=ROOT/'openspec/changes/reconciliar-fixtures-piloto-xano-e695fd5320e4'
SOURCE=CHANGE/'cleanup-execution-after-read-429.json'
USER_TABLE,LIST_TABLE,ITEM_TABLE,EVENT_TABLE=881681,895415,895416,881682
USERS={50:RUN+'_a',51:RUN+'_b'}
LIST_IDS=(125,126)
READ_GAP=1.25
WRITE_GAP=10.0


class Stop(RuntimeError): pass


def rows(client,base,headers,table_id):
    result=[];page=1;total=None;seen=set()
    while True:
        if page in seen or len(seen)>=50: raise Stop('pagination_budget')
        seen.add(page)
        if getattr(rows,'last',None) is not None:
            pause=max(0,READ_GAP-(time.monotonic()-rows.last))
            if pause: time.sleep(pause)
        rows.last=time.monotonic()
        response=client.get(f'{base}/table/{table_id}/content',headers={**headers,'x-data-source':'live'},params={'page':page,'per_page':100})
        if response.status_code!=200: raise Stop('inventory_read_http_'+str(response.status_code))
        body=response.json()
        if not isinstance(body,dict) or not isinstance(body.get('items'),list) or type(body.get('itemsTotal')) is not int: raise Stop('inventory_shape_unknown')
        if total is None: total=body['itemsTotal']
        elif total!=body['itemsTotal']: raise Stop('inventory_changed_during_read')
        result.extend(body['items']);nxt=body.get('nextPage')
        if nxt in (None,False,0): break
        if type(nxt)is not int or nxt<=page: raise Stop('invalid_next_page')
        page=nxt
    if len(result)!=total or any(not isinstance(r,dict) or type(r.get('id'))is not int for r in result): raise Stop('incomplete_inventory')
    return result


def save(path,state):
    tmp=path.with_suffix('.json.tmp');tmp.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8');tmp.replace(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();out=args.output.resolve()
    if not out.is_relative_to(CHANGE.resolve()) or out.exists(): parser.error('fresh change-local output required')
    source=json.loads(SOURCE.read_text(encoding='utf-8'))
    accepted=[a.get('action') for a in source.get('write_attempts',[]) if a.get('state')=='accepted']
    if (source.get('run_id')!=RUN or source.get('remote_writes')!=2
            or accepted!=['delete_list_125','delete_list_126']
            or source.get('failure_reason')!='post_delete_unrelated_data_changed'):
        parser.error('partial list cleanup receipt mismatch')
    baseline=source['preflight'];meta,meta_headers=metadata_config()
    config=dotenv_values(ROOT/'.env');auth=config['XANO_AUTH_URL'].rstrip('/');social=config['XANO_SOCIAL_URL'].rstrip('/')
    state={'layer':'approved_fixture_admin_cleanup_resume','workspace':147717,'run_id':RUN,'passed':False,
           'remote_writes':0,'checks':[],'write_attempts':[],'fixture_ids':{'users':[50,51],'deleted_lists':[125,126]},
           'phase':'verify_prior_list_cleanup'}
    save(out,state);last_write=None
    try:
        with httpx.Client(timeout=60,follow_redirects=False,trust_env=False) as client:
            lists=rows(client,meta,meta_headers,LIST_TABLE);items=rows(client,meta,meta_headers,ITEM_TABLE);users=rows(client,meta,meta_headers,USER_TABLE)
            list_hashes={str(r['id']):digest(r) for r in lists};expected=dict(baseline['all_list_hashes'])
            for lid in LIST_IDS: expected.pop(str(lid),None)
            if list_hashes!=expected or {str(r['id']):digest(r) for r in items}!=baseline['all_item_hashes']:
                raise Stop('list_cleanup_preservation_recheck_failed')
            if any(any(r.get('id')==lid for r in lists) for lid in LIST_IDS): raise Stop('deleted_list_reappeared')
            by={r['id']:r for r in users}
            for uid,username in USERS.items():
                u=by.get(uid)
                if not u or u.get('username')!=username or u.get('role')!='member' or u.get('account_status')!='active':
                    raise Stop('fixture_user_identity_or_status_mismatch')
            state['checks'].append({'check':'deleted_lists_absent_and_other_lists_items_unchanged','passed':True})
            state['checks'].append({'check':'users_50_51_identity_and_active_status','passed':True});state['phase']='admin_login';save(out,state)
            email=input('E-mail do administrador Codeboxd (ID 14): ').strip();secret=getpass.getpass('Senha do administrador (entrada oculta): ')
            login=client.post(auth+'/auth/login',headers={'x-data-source':'live'},json={'email':email,'password':secret});secret=None
            if login.status_code!=200: raise Stop('admin_login_rejected_before_writes')
            data=login.json();token=data.get('authToken')
            if data.get('user_id')!=14 or not isinstance(token,str): raise Stop('expected_admin_identity_mismatch')
            headers={'Authorization':'Bearer '+token,'x-data-source':'live'}
            response=client.get(auth+'/auth/me',headers=headers);actor=response.json() if response.status_code==200 else {}
            if actor.get('id')!=14 or actor.get('role')!='admin' or actor.get('account_status')!='active' or str(actor.get('email','')).casefold()!=email.casefold(): raise Stop('active_admin_confirmation_failed')
            state['admin_confirmed']=True;state['phase']='disable_accounts';save(out,state)
            events=rows(client,meta,meta_headers,EVENT_TABLE);event_max=max((r['id'] for r in events),default=0)
            for uid in (51,50):
                if last_write is not None:
                    pause=max(0,WRITE_GAP-(time.monotonic()-last_write))
                    if pause: time.sleep(pause)
                # Search/confirm exact target immediately before writing.
                response=client.get(social+'/admin/users',headers=headers,params={'search':USERS[uid],'page':1,'per_page':25})
                found=response.json().get('items',[]) if response.status_code==200 else []
                matches=[r for r in found if r.get('id')==uid and r.get('username')==USERS[uid]]
                if len(matches)!=1 or matches[0].get('role')!='member' or matches[0].get('account_status')!='active': raise Stop('admin_fixture_identity_or_status_mismatch')
                attempt={'action':'disable_user_'+str(uid),'state':'attempting','started_at':datetime.now(timezone.utc).isoformat()}
                state['write_attempts'].append(attempt);state['remote_writes']+=1;save(out,state)
                try: result=client.put(social+f'/admin/users/{uid}/status',headers=headers,json={'account_status':'disabled','reason':RUN+' approved cleanup'})
                except httpx.RequestError:
                    attempt['state']='uncertain_no_retry';save(out,state);raise Stop('disable_uncertain_no_retry') from None
                attempt.update(http_status=result.status_code,finished_at=datetime.now(timezone.utc).isoformat())
                if result.status_code!=200:
                    attempt['state']='rejected_no_retry';save(out,state);raise Stop('disable_rejected_'+str(result.status_code))
                attempt['state']='accepted';last_write=time.monotonic();save(out,state)
                verify=client.get(social+'/admin/users',headers=headers,params={'search':USERS[uid],'page':1,'per_page':25})
                matches=[r for r in verify.json().get('items',[]) if r.get('id')==uid] if verify.status_code==200 else []
                if len(matches)!=1 or matches[0].get('account_status')!='disabled': raise Stop('disable_verification_failed')
                state['checks'].append({'check':'user_'+str(uid)+'_disabled','passed':True});save(out,state)
            events=rows(client,meta,meta_headers,EVENT_TABLE)
            new=[r for r in events if r.get('id',0)>event_max]
            audited={r.get('metadata',{}).get('target_user_id') for r in new if r.get('user_id')==14 and r.get('action')=='admin_account_status_changed' and r.get('metadata',{}).get('new_status')=='disabled'}
            if not {50,51}.issubset(audited): raise Stop('admin_status_audit_events_missing')
            state['checks'].append({'check':'admin_disable_audit_events_for_50_and_51','passed':True})
            state['audit_events_verified_for']=[50,51];state['passed']=all(c['passed'] for c in state['checks']);state['phase']='complete';state['completed_at']=datetime.now(timezone.utc).isoformat();save(out,state)
    except Exception as exc:
        state['failure_reason']=str(exc) if isinstance(exc,Stop) else type(exc).__name__;state['phase']='interrupted';save(out,state);raise


if __name__=='__main__':main()
