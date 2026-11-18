"""Supervised, single-run Xano fixture pilot. Never retries a write."""
import argparse
from datetime import datetime, timezone
import getpass
import json
from pathlib import Path
import secrets
import string
import time
import tkinter as tk
from tkinter import ttk
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

from tools.shared_xano_acceptance import digest
from tools.shared_xano_preflight import collect, configured_target
from tools.session_revocation import ROOT, metadata_config

RUN = ''
OUT = ROOT/'openspec/changes/validar-integracoes-xano-atual/pilot-execution-final-2026-11-17.json'
MIN_WRITE_INTERVAL_SECONDS = 10.0
MAX_WRITE_INTERVAL_SECONDS = 60.0
RATE_LIMIT_HEADERS = ('retry-after', 'x-ratelimit-limit', 'x-ratelimit-remaining', 'x-ratelimit-reset')


class Stop(RuntimeError):
    pass


def rate_limit_metadata(headers):
    """Return only non-sensitive throttling headers; never persist response bodies."""
    return {name: headers[name] for name in RATE_LIMIT_HEADERS if name in headers}


def validate_minimum_write_interval(value):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not MIN_WRITE_INTERVAL_SECONDS <= value <= MAX_WRITE_INTERVAL_SECONDS):
        raise Stop('minimum_write_interval_out_of_range')
    return float(value)


def validate_review_window(created_at, expires_at, *, now=None):
    now=time.time() if now is None else now
    if (isinstance(created_at,bool) or not isinstance(created_at,(int,float))
            or isinstance(expires_at,bool) or not isinstance(expires_at,(int,float))
            or not created_at <= now < expires_at or not 0 < expires_at-created_at <= 1800):
        raise Stop('review_window_expired_or_invalid')
    return True


def baseline_drift(approved, current):
    return sorted(table for table in set(approved) | set(current)
                  if table != 'event_log' and approved.get(table) != current.get(table))


def list_items(value):
    if isinstance(value,list):
        return value
    if isinstance(value,dict) and isinstance(value.get('items'),list):
        return value['items']
    raise Stop('list_response_shape_unknown')


def run_has_prior_write(receipts_dir, run_id):
    for path in Path(receipts_dir).glob('pilot-execution*.json'):
        try:
            receipt=json.loads(path.read_text(encoding='utf-8'))
        except (OSError,ValueError,UnicodeError):
            raise Stop('existing_pilot_receipt_unreadable') from None
        if receipt.get('run_id')==run_id and type(receipt.get('remote_writes')) is int:
            if receipt['remote_writes']>0 or receipt.get('write_attempts'):
                return True
    return False


def password():
    alphabet=string.ascii_letters+string.digits+'!@#%'
    while True:
        value=''.join(secrets.choice(alphabet) for _ in range(28))
        if any(c.islower() for c in value) and any(c.isupper() for c in value) and any(c.isdigit() for c in value):
            return value


class Pilot:
    def __init__(self,client,auth,social,out,admin_token,admin_id,admin_email,
                 minimum_write_interval_seconds,baseline_path):
        self.client,self.auth,self.social,self.out=client,auth.rstrip('/'),social.rstrip('/'),Path(out)
        self.admin_token,self.admin_id,self.admin_email=admin_token,admin_id,admin_email
        self.minimum_write_interval_seconds=validate_minimum_write_interval(minimum_write_interval_seconds)
        self.baseline_path=Path(baseline_path)
        self.last_write_monotonic=None
        self.state={'layer':'supervised_real_xano_pilot','run_id':RUN,'passed':False,
                    'remote_writes':0,'checks':[],'fixtures':{},'write_attempts':[]}
        self.save()

    def save(self):
        tmp=self.out.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(self.state,indent=2)+'\n',encoding='utf-8')
        tmp.replace(self.out)

    def check(self,name,passed):
        self.state['checks'].append({'check':name,'passed':bool(passed)})
        self.save()
        if not passed: raise Stop('check_failed_'+name)

    def call(self,method,url,token=None,*,params=None,json_body=None,write=False,label='read'):
        if write:
            if self.last_write_monotonic is not None:
                pause=max(0.0,self.minimum_write_interval_seconds-(time.monotonic()-self.last_write_monotonic))
                if pause: time.sleep(pause)
            self.last_write_monotonic=time.monotonic()
            attempt={'action':label,'state':'attempting','started_at':datetime.now(timezone.utc).isoformat()}
            self.state['write_attempts'].append(attempt)
            self.state['remote_writes']+=1
            self.save()
        headers={'x-data-source':'live'}
        if token: headers['Authorization']='Bearer '+token
        try:
            response=self.client.request(method,url,headers=headers,params=params,json=json_body)
        except httpx.RequestError:
            if write:
                attempt['state']='uncertain_no_retry'
                self.save()
            raise Stop('network_uncertain_no_retry') from None
        if write:
            attempt.update(state='response_received',http_status=response.status_code,
                           finished_at=datetime.now(timezone.utc).isoformat())
            throttling=rate_limit_metadata(response.headers)
            if throttling:
                attempt['rate_limit_headers']=throttling
            self.save()
        return response

    def read(self,base,path,token=None,params=None):
        r=self.call('GET',base+path,token,params=params)
        if r.status_code!=200: raise Stop('read_http_'+str(r.status_code))
        try:return r.json()
        except ValueError:raise Stop('invalid_json') from None

    def write(self,method,base,path,token,body,label,expected=(200,)):
        r=self.call(method,base+path,token,json_body=body,write=True,label=label)
        attempt=self.state['write_attempts'][-1]
        if r.status_code not in expected:
            attempt['state']='rejected_no_retry'
            self.save()
            raise Stop('write_rejected_'+str(r.status_code))
        try: data=r.json() if r.content else {}
        except ValueError: raise Stop('write_response_uncertain_no_retry') from None
        attempt['state']='accepted'
        self.save()
        return data,attempt

    def list_rows(self,token):
        value=self.read(self.social,'/lists',token,{'page':1,'per_page':100})
        if isinstance(value,list):
            return value
        if isinstance(value,dict) and isinstance(value.get('items'),list):
            return value['items']
        raise Stop('list_response_shape_unknown')

    def validate(self,users,custom):
        owner_id=users['a']['id']
        owner_rows=self.list_rows(users['a']['token'])
        observed={row.get('id'):row for row in owner_rows if row.get('id') in
                  {custom['public']['id'],custom['private']['id']}}
        public=observed.get(custom['public']['id'])
        private=observed.get(custom['private']['id'])
        if (len(observed)!=2 or not public or not private
                or any(row.get('user_id')!=owner_id for row in (public,private))
                or public.get('title')!=RUN+' public' or public.get('is_public') is not True
                or private.get('title')!=RUN+' private' or private.get('is_public') is not False):
            raise Stop('custom_list_persistence_or_owner_check_failed')
        self.check('custom_lists_persisted_and_owned',True)

        other_rows=self.list_rows(users['b']['token'])
        if any(row.get('id') in (custom['public']['id'],custom['private']['id']) for row in other_rows):
            raise Stop('custom_list_visible_in_other_owner_collection')

        visible=self.read(self.social,'/lists/public',params={'page':1,'per_page':100})
        if not isinstance(visible,list):
            visible=visible.get('items',[]) if isinstance(visible,dict) else []
        visible_ids={row.get('id') for row in visible}
        if custom['public']['id'] not in visible_ids or custom['private']['id'] in visible_ids:
            raise Stop('initial_public_private_visibility_check_failed')
        self.check('public_custom_visible_and_private_custom_hidden',True)

        attempt_response=self.call('PUT',self.social+f"/lists/{custom['public']['id']}",
            users['b']['token'],json_body={'title':public['title'],
            'description':public.get('description',''),'is_public':True},write=True,
            label='cross_user_update_must_be_rejected')
        attempt=self.state['write_attempts'][-1]
        if attempt_response.status_code not in (401,403,404):
            attempt['state']='rejected_no_retry'
            self.save()
            raise Stop('cross_user_mutation_not_rejected_'+str(attempt_response.status_code))
        attempt['state']='expected_rejection'
        self.save()
        unchanged=self.list_rows(users['a']['token'])
        current=next((row for row in unchanged if row.get('id')==custom['public']['id']),None)
        if (current is None or current.get('user_id')!=owner_id
                or current.get('title')!=public['title'] or current.get('is_public') is not True):
            raise Stop('cross_user_rejection_did_not_preserve_owner_snapshot')
        self.check('cross_user_mutation_rejected_without_change',True)

        self.write('PUT',self.social,f"/lists/{custom['public']['id']}",users['a']['token'],
            {'title':public['title'],'description':public.get('description',''),
             'is_public':False},'owner_makes_public_custom_private')
        after_owner=self.list_rows(users['a']['token'])
        after=next((row for row in after_owner if row.get('id')==custom['public']['id']),None)
        after_public=self.read(self.social,'/lists/public',params={'page':1,'per_page':100})
        if not isinstance(after_public,list):
            after_public=after_public.get('items',[]) if isinstance(after_public,dict) else []
        after_public_ids={row.get('id') for row in after_public}
        if (after is None or after.get('user_id')!=owner_id or after.get('is_public') is not False
                or custom['public']['id'] in after_public_ids
                or custom['private']['id'] in after_public_ids):
            raise Stop('owner_privacy_transition_not_persisted')
        self.state['fixtures']['custom']['public']['is_public']=False
        self.save()
        self.check('owner_privacy_change_persisted_and_hidden',True)

    def verify_baseline(self):
        me=self.read(self.auth,'/auth/me',self.admin_token)
        self.check('original_active_admin_confirmed',
                   me.get('id')==self.admin_id and me.get('role')=='admin'
                   and me.get('account_status')=='active'
                   and str(me.get('email','')).casefold()==self.admin_email.casefold())

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true',required=True)
    parser.add_argument('--approval-reference',required=True)
    parser.add_argument('--manifest-digest',required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--console-login',action='store_true',required=True,
                        help='prompt for admin credentials in this PowerShell window; password is masked')
    args=parser.parse_args()
    global RUN,OUT
    OUT=args.output.resolve()
    manifest_path=args.manifest.resolve()
    baseline_path=args.baseline.resolve()
    if (not manifest_path.is_relative_to((ROOT/'.local').resolve())
            or not baseline_path.is_relative_to((ROOT/'.local').resolve())):
        parser.error('Manifest and baseline must remain inside .local.')
    preview=json.loads(manifest_path.read_text(encoding='utf-8'))
    RUN=preview.get('run_id','')
    created_at=preview.get('created_at')
    expires_at=preview.get('expires_at')
    now=time.time()
    try:
        validate_review_window(created_at,expires_at,now=now)
    except Stop as exc:
        parser.error(str(exc))
    if (args.approval_reference!='aprovo '+RUN or args.manifest_digest!=digest(preview)
            or preview.get('approval_status')!='pending_user_review'
            or not RUN.startswith('cbshared_') or args.output.exists()
            or not OUT.is_relative_to((ROOT/'openspec/changes/validar-integracoes-xano-atual').resolve())):
        parser.error('Approval reference or fresh change-local evidence path rejected.')
    if run_has_prior_write(ROOT/'openspec/changes/validar-integracoes-xano-atual',RUN):
        parser.error('This run already has a write attempt; reconcile exact receipts instead of rerunning it.')
    try:
        minimum_write_interval=validate_minimum_write_interval(preview.get('minimum_write_interval_seconds'))
    except Stop as exc:
        parser.error(str(exc))
    if (preview.get('accounts_to_create')!=2 or preview.get('custom_lists_to_create')!=2
            or preview.get('baseline_file')!=baseline_path.name
            or preview.get('batches')!={'provisioning':8,'validation':2,'cleanup':4}
            or preview.get('max_actions_per_batch')!=10
            or preview.get('retained_prior_fixture_rows')!=28
            or preview.get('new_rows_retained_after_cleanup')!=8
            or preview.get('projected_total_test_fixture_rows')!=36):
        parser.error('Reviewed pilot manifest mismatch.')
    auth_base,meta_headers=metadata_config()
    config=dotenv_values(ROOT/'.env')
    auth=urlsplit(config['XANO_AUTH_URL']); social=urlsplit(config['XANO_SOCIAL_URL'])
    if (auth.netloc!=social.netloc or auth.scheme!='https' or social.scheme!='https'
            or configured_target(config)!=preview.get('destination')):
        parser.error('Destination mismatch.')
    baseline=json.loads(baseline_path.read_text(encoding='utf-8'))
    if digest(baseline)!=preview.get('baseline_digest') or baseline.get('active_admin_candidates')!=[14]:
        parser.error('Reviewed baseline or administrator confirmation mismatch.')
    if args.console_login:
        with httpx.Client(timeout=30,follow_redirects=False,trust_env=False) as client:
            email=input('E-mail do administrador Codeboxd (ID 14): ').strip()
            secret=getpass.getpass('Senha do administrador (entrada oculta): ')
            probe=Pilot(client,config['XANO_AUTH_URL'],config['XANO_SOCIAL_URL'],args.output,'',0,email,
                        minimum_write_interval,baseline_path)
            try:
                response=client.post(config['XANO_AUTH_URL'].rstrip('/')+'/auth/login',
                    headers={'x-data-source':'live'},json={'email':email,'password':secret})
                secret=None
                if response.status_code!=200: raise Stop('admin_login_rejected_before_provisioning')
                body=response.json(); admin_token=body.get('authToken'); admin_id=body.get('user_id')
                if not isinstance(admin_token,str) or type(admin_id)is not int:
                    raise Stop('invalid_admin_login_response')
                probe.admin_token=admin_token; probe.admin_id=admin_id
                me=probe.read(config['XANO_AUTH_URL'].rstrip('/'),'/auth/me',admin_token)
                if (admin_id!=14 or me.get('id')!=14 or me.get('role')!='admin'
                        or me.get('account_status')!='active'
                        or str(me.get('email','')).casefold()!=email.casefold()):
                    raise Stop('original_active_admin_confirmation_failed')
                probe.state['admin_confirmed']=True; probe.save()
                probe.run=lambda _: _run_after_admin(probe)
                probe.run(None)
                return
            except Exception as exc:
                probe.state['failure_reason']=str(exc) if isinstance(exc,Stop) else type(exc).__name__
                probe.save()
                raise
    import tkinter as tk
    from tkinter import ttk
    with httpx.Client(timeout=30,follow_redirects=False,trust_env=False) as client:
        window=tk.Tk(); window.title('Piloto Xano controlado')
        frame=ttk.Frame(window,padding=18); frame.pack()
        ttk.Label(frame,text='Informe a conta administradora existente. Ela será usada somente para login e desativação das duas contas novas.').pack()
        fields=[]
        for label,masked in [('E-mail do administrador',False),('Senha do administrador',True)]:
            ttk.Label(frame,text=label).pack(); field=ttk.Entry(frame,width=55,show='*' if masked else ''); field.pack(pady=4); fields.append(field)
        status=tk.StringVar(value='Nenhuma conta de teste criada.')
        ttk.Label(frame,textvariable=status,wraplength=500).pack(pady=8)
        button=ttk.Button(frame,text='Iniciar provisionamento aprovado')
        def start():
            button.configure(state='disabled'); email=fields[0].get().strip(); secret=fields[1].get(); fields[1].delete(0,'end')
            try:
                # Initial admin login is checked before any fixture write.
                probe=Pilot(client,config['XANO_AUTH_URL'],config['XANO_SOCIAL_URL'],args.output,'',0,email,
                            minimum_write_interval,baseline_path)
                response=client.post(config['XANO_AUTH_URL'].rstrip('/')+'/auth/login',headers={'x-data-source':'live'},json={'email':email,'password':secret})
                if response.status_code!=200: raise Stop('admin_login_rejected_before_provisioning')
                body=response.json(); admin_token=body.get('authToken'); admin_id=body.get('user_id')
                if not isinstance(admin_token,str) or type(admin_id)is not int: raise Stop('invalid_admin_login_response')
                probe.admin_token=admin_token; probe.admin_id=admin_id
                me=probe.read(config['XANO_AUTH_URL'].rstrip('/'),'/auth/me',admin_token)
                if (admin_id!=14 or me.get('id')!=14 or me.get('role')!='admin'
                        or me.get('account_status')!='active'
                        or str(me.get('email','')).casefold()!=email.casefold()):
                    raise Stop('original_active_admin_confirmation_failed')
                probe.state['admin_confirmed']=True; probe.save()
                # Resume run after pre-authentication without repeating login.
                probe.run=lambda _: _run_after_admin(probe)
                probe.run(None)
                status.set('Provisionamento, verificacoes e limpeza concluidos. Revise o recibo.')
            except Exception as exc:
                if 'probe' in locals():
                    probe.state['failure_reason']=str(exc) if isinstance(exc,Stop) else type(exc).__name__
                    probe.save()
                status.set('Interrompido: '+(str(exc) if isinstance(exc,Stop) else type(exc).__name__)+'. Sem repeticao automatica.')
        button.configure(command=start); button.pack(pady=8)
        window.mainloop()


def _run_after_admin(p):
    p.refresh_baseline()
    p.verify_baseline()
    users={}
    for suffix in ('a','b'):
        username=RUN+'_'+suffix; email=username+'@example.invalid'; secret=password()
        created,receipt=p.write('POST',p.auth,'/auth/signup',None,{'name':RUN+' fixture','username':username,'email':email,'password':secret},'signup_'+suffix)
        user_id,token=created.get('user_id'),created.get('authToken')
        if type(user_id)is not int or not isinstance(token,str):raise Stop('signup_receipt_missing')
        users[suffix]={'id':user_id,'token':token}
        p.state['fixtures']['user_'+suffix]={'id':user_id,'username':username,'email_sha256':__import__('hashlib').sha256(email.encode()).hexdigest(),'password_sha256':__import__('hashlib').sha256(secret.encode()).hexdigest(),'created_at':receipt['finished_at']};p.save()
        profiles=p.read(p.social,'/profiles',params={'page':1,'per_page':100}); rows=profiles.get('items',profiles if isinstance(profiles,list) else []) if isinstance(profiles,dict) else profiles
        matches=[r for r in rows if r.get('user_id')==user_id]
        lists=p.read(p.social,'/lists',token,{'page':1,'per_page':100}); lr=lists.get('items',lists if isinstance(lists,list) else []) if isinstance(lists,dict) else lists
        defaults=[r for r in lr if r.get('user_id')==user_id and r.get('default_key') in (f'{user_id}:planned',f'{user_id}:completed')]
        if len(matches)!=1 or len(defaults)!=2:raise Stop('signup_related_records_unverified')
        p.state['fixtures']['profile_'+suffix]={'id':matches[0]['id'],'user_id':user_id};p.state['fixtures']['defaults_'+suffix]=[];p.save()
        for row in defaults:
            p.write('PUT',p.social,'/lists/'+str(row['id']),token,{'title':row['title'],'description':row.get('description',''),'is_public':False},'privatize_default_'+suffix)
            p.state['fixtures']['defaults_'+suffix].append({'id':row['id'],'user_id':user_id,'default_key':row['default_key'],'is_public':False});p.save()
    custom={}
    for label,public in [('public',True),('private',False)]:
        row,receipt=p.write('POST',p.social,'/lists',users['a']['token'],{'title':RUN+' '+label,'description':RUN,'is_public':public},'create_'+label)
        if type(row.get('id'))is not int:raise Stop('custom_list_receipt_missing')
        custom[label]={'id':row['id'],'user_id':users['a']['id'],'is_public':public}
        p.state['fixtures']['custom']=custom;p.save()
    p.validate(users,custom)
    p.cleanup(users,custom)
    return p.state


def _refresh_baseline(p):
    suffix=secrets.token_hex(4)
    private=ROOT/'.local'/('shared-xano-refresh-'+suffix)
    output=ROOT/'openspec/changes/validar-integracoes-xano-atual'/('refresh-'+suffix+'.json')
    report=collect(private,output)
    p.state['pre_mutation_read_refresh']={'inventory_complete':report.get('inventory_complete',False),
        'routing_verified':report.get('branch_verified',False),'table_count':report.get('table_count',0),
        'remote_writes':report.get('remote_writes',None),'report_file':output.name}
    p.save()
    if not report.get('inventory_complete') or not report.get('branch_verified'):
        raise Stop('fresh_destination_inventory_failed')
    baseline=json.loads(p.baseline_path.read_text(encoding='utf-8'))['tables']
    current=json.loads((private/'baseline-hashes.json').read_text())['tables']
    differences=baseline_drift(baseline,current)
    p.state['pre_mutation_read_refresh']['existing_table_drift']=sorted(differences)
    p.state['baseline_file']=str(p.baseline_path.relative_to(ROOT))
    p.save()
    if differences:raise Stop('existing_data_changed_since_review')


Pilot.refresh_baseline=_refresh_baseline


def _cleanup(p,users,custom):
    # Each destructive action is limited to a receipt created by this process.
    for label,row in custom.items():
        owner=users['a']
        observed=p.read(p.social,f"/lists/{row['id']}/items",owner['token'],{'page':1,'per_page':100})
        items=list_items(observed)
        if items: raise Stop('custom_fixture_has_references_cleanup_stopped')
        mine=p.read(p.social,'/lists',owner['token'],{'page':1,'per_page':100})
        rows=list_items(mine)
        actual=next((x for x in rows if x.get('id')==row['id']),None)
        if not actual or actual.get('user_id')!=owner['id'] or actual.get('title')!=RUN+' '+label:
            raise Stop('custom_fixture_identity_changed_cleanup_stopped')
        p.write('DELETE',p.social,'/lists/'+str(row['id']),owner['token'],{},'delete_custom_'+label)
        p.state['fixtures']['custom'][label]['deleted']=True;p.save()
        check=p.read(p.social,'/lists',owner['token'],{'page':1,'per_page':100})
        rows=list_items(check)
        p.check('custom_'+label+'_deleted',not any(x.get('id')==row['id'] for x in rows))
    for suffix in ('b','a'):
        user=users[suffix]
        result,_=p.write('PUT',p.social,f"/admin/users/{user['id']}/status",p.admin_token,
            {'account_status':'disabled','reason':RUN+' pilot cleanup'},'disable_fixture_'+suffix)
        p.state['fixtures']['user_'+suffix]['disabled']=True;p.save()
        info=p.read(p.social,f"/admin/users?page=1&per_page=100&search={user['username']}",p.admin_token)
        entries=info.get('items',info if isinstance(info,list) else [])
        found=next((x for x in entries if x.get('id')==user['id']),None)
        p.check('fixture_'+suffix+'_disabled',found is not None and found.get('account_status')=='disabled')
    p.state['phase']='complete';p.state['passed']=all(x['passed'] for x in p.state['checks'])
    p.save()


Pilot.cleanup=_cleanup


if __name__=='__main__':main()
