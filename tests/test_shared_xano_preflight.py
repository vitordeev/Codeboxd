import json
import unittest
import httpx

from tools.shared_xano_preflight import Reads, PreflightStopped, inventory_hashes, configured_target, sequence, verify_groups


class PreflightTests(unittest.TestCase):
    def test_baseline_contains_only_ids_and_hashes(self):
        result = inventory_hashes([{'id':7,'email':'private@example.invalid','password':'private-value'}])
        self.assertEqual(set(result),{'7'})
        self.assertEqual(len(result['7']),64)
        self.assertNotIn('private',json.dumps(result))

    def test_duplicate_and_boolean_ids_rejected(self):
        for rows in [[{'id':True}], [{'id':7},{'id':7}], [{'id':0}]]:
            with self.assertRaises(PreflightStopped):
                inventory_hashes(rows)

    def test_destination_rejects_mixed_origins_credentials_and_query(self):
        good = {'XANO_AUTH_URL':'https://fixture.xano.io/api:auth','XANO_SOCIAL_URL':'https://fixture.xano.io/api:social'}
        self.assertEqual(configured_target(good)['workspace'],147717)
        for other in ['https://foreign.xano.io/api:social','https://user:pass@fixture.xano.io/api:social','https://fixture.xano.io/api:social?branch=other']:
            with self.assertRaises(PreflightStopped):
                configured_target({**good,'XANO_SOCIAL_URL':other})

    def reader(self, pages):
        calls = []
        def handle(request):
            calls.append(request)
            return httpx.Response(200,json=pages[len(calls)-1])
        client = httpx.Client(transport=httpx.MockTransport(handle))
        self.addCleanup(client.close)
        return Reads(client,'https://fixture.invalid/api:meta/workspace/147717',{},pause=lambda _:None),calls

    def test_complete_pagination_is_read_only_and_source_is_explicit(self):
        reader,calls = self.reader([{'items':[{'id':1}],'itemsTotal':2,'nextPage':2},
                                   {'items':[{'id':2}],'itemsTotal':2,'nextPage':None}])
        rows,hashes = reader.rows(10)
        self.assertEqual(len(rows),2)
        self.assertEqual(set(hashes),{'1','2'})
        self.assertTrue(all(r.method=='GET' and r.headers['x-data-source']=='live' for r in calls))

    def test_drift_loop_and_truncation_rejected(self):
        for pages in [[{'items':[{'id':1}],'itemsTotal':2,'nextPage':1}],
                      [{'items':[{'id':1}],'itemsTotal':2,'nextPage':None}],
                      [{'items':[{'id':1}],'itemsTotal':2,'nextPage':2},
                       {'items':[{'id':2}],'itemsTotal':3,'nextPage':None}]]:
            reader,_ = self.reader(pages)
            with self.assertRaises(PreflightStopped):
                reader.rows(10)

    def test_unapproved_routes_fail_before_network(self):
        reader,calls = self.reader([])
        for route in ['/table/10/content/1','/multidoc/import','/table/10/content/bulk/delete']:
            with self.assertRaises(PreflightStopped):
                reader.get(route)
        self.assertEqual(calls,[])

    def test_incomplete_table_listing_is_not_accepted(self):
        with self.assertRaises(PreflightStopped):
            sequence({'items':[{'id':1}],'itemsTotal':2})

    def test_group_and_branch_must_match_independent_metadata(self):
        target = {'auth_group':'api:auth','social_group':'api:social','branch':'v1'}
        groups = [{'id':1,'canonical':'auth','name':'Authentication','branch':'v1'},
                  {'id':2,'canonical':'social','name':'Codeboxd','branch':'v1'}]
        self.assertEqual(verify_groups(target,groups),{'auth_group':1,'social_group':2})
        for bad in [groups+[groups[0]], [groups[0],{**groups[1],'branch':'other'}], groups[:1]]:
            with self.assertRaises(PreflightStopped):
                verify_groups(target,bad)
