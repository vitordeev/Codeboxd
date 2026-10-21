"""One-time, backed-up Xano list reset. Never imported by the application.

prepare writes private data under .local; apply requires that exact backup and
refuses repeated execution. No automatic retry of writes or partial migrations.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time

import httpx

WORKSPACE = 147717
TABLES = {'user':881681, 'user_list':895415, 'user_list_item':895416,
          'media':895410, 'user_media_interaction':895417}
DEFAULTS = (('Quero ver / ler','Obras para descobrir depois.'),
            ('Já assisti / li','Obras que você já terminou.'))
ROOT = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,
                                    separators=(',',':')).encode()).hexdigest()


def write_json(path, value):
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    temporary.replace(path)


class Metadata:
    def __init__(self):
        source=(Path.home()/'.xano/credentials.yaml').read_text(encoding='utf-8')
        def field(name):
            values=re.findall(r'(?m)^\s+'+name+r':\s*(.+)$',source)
            if len(values)!=1:
                raise ValueError('Migration requires one unambiguous Xano profile')
            return values[0].strip().strip('"').strip("'")
        origin=field('instance_origin').rstrip('/')
        if not origin.startswith('https://'): raise ValueError('HTTPS is required')
        self.scope=digest({'origin':origin,'workspace':WORKSPACE,'source':'live'})
        self.client=httpx.Client(base_url=origin+'/api:meta',timeout=30,
            headers={'Authorization':'Bearer '+field('access_token'),'x-data-source':'live'})

    def request(self, method, table, record=None, data=None, params=None):
        if table not in TABLES: raise ValueError('Unknown table')
        if method!='GET' and table not in ('user_list','user_list_item'):
            raise ValueError('Only lists and list items may be mutated')
        path=f'/workspace/{WORKSPACE}/table/{TABLES[table]}/content'
        if record is not None: path+='/'+str(int(record))
        # Keep metadata/database calls below the observed shared write burst.
        time.sleep(1.5)
        response=self.client.request(method,path,json=data,params=params)
        if not response.is_success:
            raise RuntimeError(f'Metadata {method} {table}: HTTP {response.status_code}; stopped without retry')
        return response.json() if response.content else None

    def rows(self, table):
        result=[]; page=1; seen=set(); total=None
        while True:
            if page in seen: raise ValueError('Repeated page')
            seen.add(page)
            batch=self.request('GET',table,params={'page':page,'per_page':100})
            if not isinstance(batch,dict) or not isinstance(batch.get('items'),list):
                raise ValueError('Unexpected pagination response')
            if total is None: total=batch['itemsTotal']
            if batch['itemsTotal']!=total: raise ValueError('Table changed during pagination')
            result.extend(batch['items'])
            if not batch.get('nextPage'): break
            page=int(batch['nextPage'])
        if len(result)!=total or len({r['id'] for r in result})!=total:
            raise ValueError('Incomplete or duplicated snapshot')
        return sorted(result,key=lambda r:r['id'])


def snapshot(api):
    # User records exist only in memory; persist IDs, never passwords or emails.
    users=[r['id'] for r in api.rows('user')]
    return dict(user_ids=users,lists=api.rows('user_list'),items=api.rows('user_list_item'),
        protected={name:digest(api.rows(name)) for name in ('media','user_media_interaction')})


def prepare(api, directory):
    directory.mkdir(parents=True,exist_ok=True)
    if (directory/'backup.json').exists() or (directory/'journal.json').exists():
        raise FileExistsError('Preserve previous migration evidence')
    data=snapshot(api)
    if not data['user_ids']: raise ValueError('No users; refuse destructive reset')
    backup=dict(scope=api.scope,created_at=datetime.now(timezone.utc).isoformat(),data=data)
    write_json(directory/'backup.json',backup)
    write_json(directory/'manifest.json',dict(backup_sha256=digest(backup),
        users=len(data['user_ids']),lists_to_delete=len(data['lists']),
        items_to_delete=len(data['items']),lists_to_create=2*len(data['user_ids']),
        orphan_lists=sum(row['user_id'] not in data['user_ids'] for row in data['lists'])))
    return json.loads((directory/'manifest.json').read_text(encoding='utf-8'))


def apply(api, directory):
    backup=json.loads((directory/'backup.json').read_text(encoding='utf-8'))
    manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if api.scope!=backup['scope'] or digest(backup)!=manifest['backup_sha256']:
        raise ValueError('Backup integrity or remote scope mismatch')
    if (directory/'journal.json').exists():
        raise FileExistsError('Already started; inspect journal rather than resetting again')
    before=backup['data']
    if snapshot(api)!=before: raise ValueError('Remote data changed since backup; no mutation performed')
    journal=dict(status='started',completed=[],pending=None)
    # Exclusive creation is the durable one-time execution guard.
    with (directory/'journal.json').open('x',encoding='utf-8') as file:
        json.dump(journal,file)
    def mutate(method,table,record=None,data=None):
        journal['pending']=dict(method=method,table=table,id=record)
        write_json(directory/'journal.json',journal)
        result=api.request(method,table,record,data)
        journal['completed'].append(dict(journal['pending'],result_id=result.get('id')
            if isinstance(result,dict) else None))
        journal['pending']=None
        write_json(directory/'journal.json',journal)
        return result
    try:
        for row in before['items']: mutate('DELETE','user_list_item',row['id'])
        for row in before['lists']: mutate('DELETE','user_list',row['id'])
        for uid in before['user_ids']:
            for title,description in DEFAULTS:
                result=mutate('POST','user_list',data=dict(user_id=uid,title=title,
                    description=description,is_public=True))
                if not isinstance(result,dict) or not result.get('id'):
                    raise ValueError('Unconfirmed list creation; inspect journal')
        after=snapshot(api)
        expected=Counter((uid,title) for uid in before['user_ids'] for title,_ in DEFAULTS)
        actual=Counter((row['user_id'],row['title']) for row in after['lists'])
        if (after['user_ids']!=before['user_ids'] or after['items'] or actual!=expected
                or after['protected']!=before['protected']):
            raise ValueError('Post-migration verification failed')
        journal['status']='verified'
        write_json(directory/'after.json',after)
    except Exception:
        journal['status']='failed-review-required'
        raise
    finally:
        write_json(directory/'journal.json',journal)
    return dict(users=len(after['user_ids']),lists=len(after['lists']),items=0,
                protected_unchanged=True,status=journal['status'])


def reconcile(api, directory):
    """Explicit recovery: read first, create missing defaults only, never delete."""
    backup=json.loads((directory/'backup.json').read_text(encoding='utf-8'))
    manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    journal=json.loads((directory/'journal.json').read_text(encoding='utf-8'))
    if api.scope!=backup['scope'] or digest(backup)!=manifest['backup_sha256']:
        raise ValueError('Backup integrity or remote scope mismatch')
    if journal['status']!='failed-review-required':
        raise ValueError('Explicit recovery requires a failed migration')
    before=backup['data']; current=snapshot(api)
    expected={(uid,title) for uid in before['user_ids'] for title,_ in DEFAULTS}
    actual=[(row['user_id'],row['title']) for row in current['lists']]
    deleted={(entry['table'],entry['id']) for entry in journal['completed'] if entry['method']=='DELETE'}
    required={('user_list',row['id']) for row in before['lists']}
    required.update(('user_list_item',row['id']) for row in before['items'])
    if (not required.issubset(deleted) or current['items'] or
            current['user_ids']!=before['user_ids'] or current['protected']!=before['protected']
            or not set(actual).issubset(expected) or len(set(actual))!=len(actual)):
        raise ValueError('Unexpected remote data; recovery cannot mutate it')
    journal['recovery_started_at']=datetime.now(timezone.utc).isoformat()
    try:
        for uid in before['user_ids']:
            for title,description in DEFAULTS:
                if (uid,title) in actual: continue
                journal['pending']=dict(method='POST',table='user_list',user_id=uid,title=title)
                write_json(directory/'journal.json',journal)
                result=api.request('POST','user_list',data=dict(user_id=uid,title=title,
                    description=description,is_public=True))
                if not isinstance(result,dict) or not result.get('id'):
                    raise ValueError('Unconfirmed creation; inspect remote before recovery')
                journal['completed'].append(dict(journal['pending'],result_id=result['id']))
                journal['pending']=None
                write_json(directory/'journal.json',journal)
        after=snapshot(api)
        observed=Counter((row['user_id'],row['title']) for row in after['lists'])
        if (observed!=Counter(expected) or after['items'] or after['user_ids']!=before['user_ids']
                or after['protected']!=before['protected']):
            raise ValueError('Post-recovery verification failed')
        journal['status']='verified'
        write_json(directory/'after.json',after)
    finally:
        write_json(directory/'journal.json',journal)
    return dict(users=len(after['user_ids']),lists=len(after['lists']),items=0,
                protected_unchanged=True,status=journal['status'],recovered=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','apply','reconcile'))
    parser.add_argument('--directory',type=Path,required=True)
    args=parser.parse_args()
    directory=args.directory.resolve()
    if not directory.is_relative_to(ROOT/'.local'):
        raise ValueError('Private migration evidence must stay in .local')
    api=Metadata()
    try:
        result={'prepare':prepare,'apply':apply,'reconcile':reconcile}[args.action](api,directory)
        print(json.dumps(result,ensure_ascii=True))
    finally: api.client.close()


if __name__=='__main__': main()
