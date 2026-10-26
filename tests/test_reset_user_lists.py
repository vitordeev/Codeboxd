from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from tools.reset_user_lists import DEFAULTS, Metadata, apply, prepare, reconcile
from Codeboxd_main.state.social import SocialState


class FakeMetadata:
    scope='fixture-scope'
    def __init__(self):
        self.data={'user':[{'id':1,'password':'private'},{'id':2}],
            'user_list':[{'id':1,'user_id':1,'title':'Custom'}],
            'user_list_item':[{'id':1,'list_id':1,'media_id':10}],
            'media':[{'id':10,'title':'Work'}],
            'user_media_interaction':[{'id':1,'user_id':1,'rating':4.5}]}
        self.writes=[]; self.fail_create=False
    def rows(self,table): return deepcopy(self.data[table])
    def request(self,method,table,record=None,data=None,params=None):
        if self.fail_create and method=='POST': raise RuntimeError('Connection lost')
        self.writes.append((method,table))
        if method=='DELETE':
            self.data[table]=[row for row in self.data[table] if row['id']!=record]
            return None
        result=dict(data,id=max([row['id'] for row in self.data[table]]+[10])+1)
        self.data[table].append(result)
        return result


class ResetTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory=Path(self.temporary.name)
        self.api=FakeMetadata()

    def test_reset_all_accounts_and_preserve_other_data(self):
        plan=prepare(self.api,self.directory)
        self.assertEqual(plan['lists_to_create'],4)
        self.assertNotIn('private',(self.directory/'backup.json').read_text())
        result=apply(self.api,self.directory)
        self.assertEqual(result['status'],'verified')
        self.assertEqual(self.api.data['user_list_item'],[])
        for uid in (1,2):
            self.assertEqual({row['title'] for row in self.api.data['user_list']
                if row['user_id']==uid},{title for title,_ in DEFAULTS})
        self.assertTrue(all(table in ('user_list','user_list_item') for _,table in self.api.writes))
        self.assertEqual(self.api.writes[0],('DELETE','user_list_item'))

    def test_second_execution_cannot_delete_new_custom_lists(self):
        prepare(self.api,self.directory); apply(self.api,self.directory)
        self.api.data['user_list'].append({'id':99,'user_id':1,'title':'New custom'})
        writes=len(self.api.writes)
        with self.assertRaises(FileExistsError): apply(self.api,self.directory)
        self.assertEqual(len(self.api.writes),writes)
        self.assertEqual(self.api.data['user_list'][-1]['title'],'New custom')

    def test_orphan_lists_are_backed_up_and_removed_without_creating_users(self):
        self.api.data['user_list'].append({'id':9,'user_id':999,'title':'Orphan'})
        plan=prepare(self.api,self.directory)
        self.assertEqual(plan['orphan_lists'],1)
        backup=json.loads((self.directory/'backup.json').read_text())
        self.assertEqual(len(backup['data']['lists']),2)
        apply(self.api,self.directory)
        self.assertEqual({r['user_id'] for r in self.api.data['user_list']},{1,2})

    def test_changed_remote_data_stops_before_writes(self):
        prepare(self.api,self.directory)
        self.api.data['user_list'].append({'id':3,'user_id':2,'title':'Concurrent'})
        with self.assertRaisesRegex(ValueError,'changed'): apply(self.api,self.directory)
        self.assertFalse(self.api.writes)

    def test_corrupted_backup_stops_before_writes(self):
        prepare(self.api,self.directory)
        path=self.directory/'backup.json'
        data=json.loads(path.read_text()); data['data']['lists']=[]
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'integrity'): apply(self.api,self.directory)
        self.assertFalse(self.api.writes)

    def test_partial_failure_is_not_retried_and_keeps_backup(self):
        prepare(self.api,self.directory); self.api.fail_create=True
        with self.assertRaises(RuntimeError): apply(self.api,self.directory)
        journal=json.loads((self.directory/'journal.json').read_text())
        self.assertEqual(journal['status'],'failed-review-required')
        self.assertEqual(journal['pending']['method'],'POST')
        self.assertTrue((self.directory/'backup.json').exists())
        with self.assertRaises(FileExistsError): apply(self.api,self.directory)

    def test_recovery_creates_only_missing_lists_and_cannot_run_after_success(self):
        prepare(self.api,self.directory); self.api.fail_create=True
        with self.assertRaises(RuntimeError): apply(self.api,self.directory)
        self.api.fail_create=False
        self.api.data['user_list']=[{'id':30,'user_id':1,'title':DEFAULTS[0][0]}]
        offset=len(self.api.writes)
        self.assertEqual(reconcile(self.api,self.directory)['status'],'verified')
        self.assertEqual(self.api.writes[offset:],[('POST','user_list')]*3)
        with self.assertRaises(ValueError): reconcile(self.api,self.directory)

    def test_recovery_refuses_to_remove_a_concurrent_custom_list(self):
        prepare(self.api,self.directory); self.api.fail_create=True
        with self.assertRaises(RuntimeError): apply(self.api,self.directory)
        self.api.data['user_list']=[{'id':30,'user_id':1,'title':'New custom'}]
        writes=len(self.api.writes)
        with self.assertRaisesRegex(ValueError,'Unexpected'): reconcile(self.api,self.directory)
        self.assertEqual(len(self.api.writes),writes)

    def test_protected_tables_rejected_before_transport(self):
        api=object.__new__(Metadata)
        for table in ('user','media','user_media_interaction'):
            with self.assertRaisesRegex(ValueError,'Only lists'):
                api.request('DELETE',table,1)


class FutureCustomListsTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        legacy = patch.dict('os.environ', {'DEFAULT_LIST_IDENTITY_ENABLED':'false'})
        legacy.start(); self.addCleanup(legacy.stop)

    async def test_navigation_preserves_custom_lists_with_legacy_titles(self):
        state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        lists=[{'id':i+1,'title':title} for i,(title,_) in enumerate(DEFAULTS)]
        lists.extend([{'id':3,'title':'Gostei'},{'id':4,'title':'Não gostei'}])
        with patch.object(SocialState,'_call',new=AsyncMock(return_value=lists)) as request:
            await state._ensure_default_lists()
        request.assert_awaited_once_with('GET','/lists')

    async def test_navigation_keeps_custom_list_after_reset(self):
        state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        state.user_id=1
        lists=[{'id':i+1,'title':title} for i,(title,_) in enumerate(DEFAULTS)]
        async def call(method,path,data=None,**kwargs):
            if method=='POST':
                result=dict(data,id=3)
                lists.append(result)
                return result
            if path=='/media': return []
            if path.endswith('/items'): return []
            return lists
        with patch.object(SocialState,'_call',side_effect=call) as request, \
             patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_validate_navigation_session',new=AsyncMock()):
            async for _ in state.save_list({'title':'Minha lista personalizada','is_public':'on'}):
                pass
            offset=request.await_count
            await state._ensure_default_lists()
        self.assertEqual(sum(c.args[0]=='POST' for c in request.await_args_list),1)
        self.assertEqual(request.await_count,offset+1)
        self.assertEqual(request.await_args_list[-1].args,('GET','/lists'))
        self.assertEqual(lists[-1]['title'],'Minha lista personalizada')
        self.assertEqual(len(state.quick_lists),2)


if __name__=='__main__': unittest.main()
