from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
import unittest
from unittest.mock import patch

from tools.admin_acceptance_guard import GuardRejected, digest
from tools import shared_xano_acceptance as shared


class SharedAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.plan = shared.example(now=1000)

    def rejected(self, plan, code=None):
        with self.assertRaises(GuardRejected) as failure:
            shared.preview(plan, now=1010)
        if code:
            self.assertEqual(str(failure.exception), code)

    def add_fixture(self, table, record):
        self.plan['baseline']['tables'].setdefault(table,{})
        self.plan['current'].setdefault(table,{})[str(record['id'])]=record
        self.plan['receipts'].append({'table':table,'id':record['id'],'run_id':self.plan['run_id'],
            'created_snapshot':deepcopy(record),'created_digest':digest(record),
            'snapshot_digest':digest(record),'identity_digest':shared.row_identity(table,record)})

    def test_existing_shared_workspace_is_valid_without_provisioning(self):
        result=shared.preview(self.plan,now=1010)
        self.assertEqual(self.plan['destination']['workspace'],147717)
        self.assertEqual(result['actions'],1)
        self.assertFalse(result['remote_execution'])
        self.assertFalse(result['baseline_verified_remotely'])
        self.assertFalse(result['approval_checked'])

    def test_foreign_or_ambiguous_destination_is_rejected(self):
        for changes in ({'origin':'https://user:secret@example.invalid'},
                        {'origin':'https://example.invalid/path'}, {'origin':'https://EXAMPLE.invalid'},
                        {'origin':'https://example.invalid:443'}, {'origin':'http://example.invalid'},
                        {'workspace':True},{'branch':''},{'shared':False}):
            plan=deepcopy(self.plan)
            plan['destination'].update(changes)
            self.rejected(plan)
        changed=deepcopy(self.plan)
        changed['destination']['workspace']=9
        self.rejected(changed,'baseline_destination_mismatch')

    def test_preexisting_id_with_matching_marker_is_not_a_fixture(self):
        record=self.plan['current']['post']['43']
        self.plan['baseline']['tables']['post']['43']=digest(record)
        self.rejected(self.plan,'preexisting_record_is_not_fixture')

    def test_marker_without_provisioning_receipt_is_insufficient(self):
        for field in ('created_digest','identity_digest','snapshot_digest','created_snapshot'):
            plan=deepcopy(self.plan)
            plan['receipts'][1].pop(field)
            self.rejected(plan)
        self.plan['receipts'][1]['run_id']='cbshared_aaaaaaaaaaaa'
        self.rejected(self.plan,'foreign_run')

    def test_record_changed_after_preview_is_rejected(self):
        self.plan['current']['post']['43']['body']+=' changed'
        self.rejected(self.plan,'fixture_snapshot_changed')

    def test_operator_must_be_unchanged_original_active_admin(self):
        for change in ({'role':'member'}, {'account_status':'disabled'},{'id':True}):
            plan=deepcopy(self.plan)
            plan['current']['user']['7'].update(change)
            self.rejected(plan,'original_admin_required')

    def test_test_accounts_cannot_be_admin_or_the_operator(self):
        self.plan['current']['user']['42']['role']='admin'
        receipt=self.plan['receipts'][0]
        receipt['snapshot_digest']=digest(self.plan['current']['user']['42'])
        self.rejected(self.plan,'protected_account')

    def test_owned_resource_needs_proven_fixture_owner(self):
        self.plan['receipts']=self.plan['receipts'][1:]
        self.rejected(self.plan,'fixture_owner_not_proven')

    def test_cleanup_blocks_unknown_or_nonempty_references(self):
        for changes in ({'references_complete':False},{'references':{}},
                        {'references':{'post:43':[{'table':'comment','id':77}]}},
                        {'references':{'post:43':None}}):
            plan=deepcopy(self.plan)
            plan.update(changes)
            self.rejected(plan,'empty_reference_inventory_required')

    def test_no_password_roles_email_delete_user_or_arbitrary_endpoints(self):
        for action in ({'method':'DELETE','path':'/admin/users/42','payload':{}},
                       {'method':'POST','path':'/auth/reset/request-reset-link','payload':{}},
                       {'method':'DELETE','path':'/posts/7','payload':{}},
                       {'method':'PUT','path':'/admin/users/42/status','payload':{'role':'admin'}},
                       {'method':'PUT','path':'/admin/users/42/status','payload':{'password':'private-value'}},
                       {'method':'GET','path':'/sandbox/me','payload':{}},
                       {'method':'DELETE','path':'https://example.invalid/posts/43','payload':{}}):
            plan=deepcopy(self.plan)
            plan['actions']=[action]
            self.rejected(plan)

    def test_exact_member_status_update_can_be_previewed(self):
        self.plan['actions']=[{'method':'PUT','path':'/admin/users/42/status',
            'payload':{'account_status':'disabled','reason':self.plan['run_id']+' temporary fixture check'}}]
        result=shared.preview(self.plan,now=1010)
        self.assertFalse(result['remote_execution'])
        self.assertNotIn('payload',result)

    def test_default_lists_cannot_be_deleted_by_generic_planner(self):
        self.add_fixture('user_list',{'id':55,'user_id':42,'title':self.plan['run_id']+' list',
                                     'default_key':'42:planned'})
        self.rejected(self.plan,'default_list_not_supported')

    def test_report_target_and_reporter_must_be_fixtures(self):
        self.add_fixture('report',{'id':61,'reporter_user_id':42,'target_type':'post',
                                  'target_id':999,'description':self.plan['run_id']+' report'})
        self.rejected(self.plan,'report_target_not_fixture')

    def test_operation_budget_duplicates_and_expired_plan_are_rejected(self):
        for actions in ([],self.plan['actions']*2,self.plan['actions']*11):
            plan=deepcopy(self.plan)
            plan['actions']=actions
            self.rejected(plan)
        for changes in ({'expires_at':1001},{'created_at':1011},
                        {'expires_at':3000},{'created_at':True},{'expires_at':float('nan')}):
            plan=deepcopy(self.plan)
            plan.update(changes)
            self.rejected(plan)

    def test_approval_is_bound_to_entire_plan_and_does_not_enable_network(self):
        report=shared.preview(self.plan,now=1010)
        approval={'plan_digest':report['plan_digest'],'reference':'reviewed locally',
                  'reviewed_at':1002,'expires_at':1200}
        result=shared.review_approval(self.plan,approval,now=1010)
        self.assertTrue(result['approval_checked'])
        self.assertFalse(result['remote_execution'])
        changed=deepcopy(self.plan)
        changed['actions']=[{'method':'PUT','path':'/admin/users/42/status',
                            'payload':{'account_status':'disabled','reason':self.plan['run_id']}}]
        with self.assertRaisesRegex(GuardRejected,'approval_digest_mismatch'):
            shared.review_approval(changed,approval,now=1010)
        for changed in ({'expires_at':1009},{'reviewed_at':1011},{'expires_at':2000}):
            with self.assertRaises(GuardRejected):
                shared.review_approval(self.plan,approval|changed,now=1010)

    def test_sanitized_preview_never_echoes_records_or_values(self):
        self.plan['current']['user']['7']['email']='private-operator@example.invalid'
        self.plan['baseline']['tables']['user']['7']=digest(self.plan['current']['user']['7'])
        result=json.dumps(shared.preview(self.plan,now=1010))
        for text in ('private-operator','disposable post','username','operator_id','payload'):
            self.assertNotIn(text,result)

    def test_cli_example_is_offline_and_outputs_only_preview(self):
        with patch('socket.create_connection',side_effect=AssertionError('network_forbidden')), \
             patch('socket.getaddrinfo',side_effect=AssertionError('network_forbidden')):
            output=io.StringIO()
            with redirect_stdout(output):
                status=shared.main(['--example'])
        self.assertEqual(status,0)
        report=json.loads(output.getvalue())
        self.assertFalse(report['remote_execution'])
        self.assertEqual(report['actions'],1)

    def test_private_input_file_errors_are_sanitized(self):
        output=io.StringIO()
        with redirect_stdout(output):
            status=shared.main(['--plan','C:/private-location/secret.json'])
        self.assertEqual(status,1)
        self.assertEqual(json.loads(output.getvalue())['error'],'private_input_required')
        self.assertNotIn('secret.json',output.getvalue())


if __name__=='__main__':
    unittest.main()
