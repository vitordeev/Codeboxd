import asyncio
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.state.social import SocialState
from Codeboxd_main.services.api import APIError
from Codeboxd_main.pages.social import feed_page, post_image_picker


def media(kind='movie', mid=0):
    return dict(id=mid, identity_key='fixture:'+kind, external_source='fixture',
                external_id=kind, media_type=kind, title='Matrix '+kind,
                description='Fixture', cover_url='', year=2020, details={})


async def finish(event):
    async for _ in event:
        pass


class FeedListWorkflowTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.s=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.s.user_id=7; self.s._identity=7; self.s.session_token='fictional-session'
        self.s.selected_list={'id':'12','user_id':'7','title':'Favoritos','description':'','is_public':'False'}

    def post(self, mid='0'):
        self.s.posts=[dict(id='55',user_id='7',body='Original',media_id=mid,
                           spoiler='False',media_title='Matrix',image_url='/image.png')]
        self.s.edit_post('55')

    def test_post_image_picker_starts_upload_on_selection(self):
        picker=post_image_picker()
        upload=picker.children[1].children[0]
        hooks=' '.join(upload.special_props[0]._var_data.hooks)
        self.assertIn('stage_post_image',hooks)
        self.assertIn('on_drop_',hooks)
        self.assertNotIn('Carregar imagem',str(picker))
        self.assertIn('Descartar',str(picker))
        page=str(feed_page())
        self.assertIn('disabled:pyOr',page)
        self.assertIn('filesById["post_image_upload"]',page)

    async def test_selected_post_image_is_staged_and_cleared_after_success(self):
        from types import SimpleNamespace

        image=SimpleNamespace(name='fixture.png',read=AsyncMock(return_value=b'\x89PNG\r\n\x1a\nfixture'))
        with TemporaryDirectory() as directory, \
             patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch('Codeboxd_main.state.social.rx.get_upload_dir',return_value=Path(directory)):
            await finish(self.s.stage_post_image([image]))
            self.assertFalse(self.s.post_image_staging)
            self.assertEqual(self.s.post_image_mime,'image/png')
            self.assertTrue(Path(self.s._post_image_path).is_file())
            self.assertEqual(Path(self.s._post_image_path).read_bytes(),b'\x89PNG\r\n\x1a\nfixture')

    async def test_edit_keeps_id_with_without_replaced_and_removed_media(self):
        for action in ('none','keep','replace','remove'):
            with self.subTest(action=action):
                self.post('0' if action=='none' else '9')
                if action=='replace': self.s._post_media_raw={'id':10}
                if action=='remove': self.s.clear_post_media()
                with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
                     patch.object(SocialState,'_call',new=AsyncMock(return_value={})) as call, \
                     patch.object(SocialState,'_refresh_posts',new=AsyncMock()):
                    await finish(self.s.save_post({'body':'Edited','post_id':'55'}))
                self.assertEqual(call.await_args.args[:2],('PUT','/posts/55'))
                self.assertEqual(call.await_args.args[2]['media_id'],{'none':0,'keep':9,'replace':10,'remove':0}[action])
                self.assertNotIn('image',call.await_args.args[2])

    async def test_edit_losing_identity_during_auth_never_creates_post(self):
        self.post()
        async def reset():
            self.s.edit_post_id=''
            return True
        with patch.object(SocialState,'_require_user',new=AsyncMock(side_effect=reset)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.save_post({'body':'Edit','post_id':'55'}))
        call.assert_not_awaited()

    async def test_saving_locks_editor_and_stale_submit_is_rejected(self):
        self.post()
        token=self.s.post_editor_token
        event=self.s.save_post({'body':'Edit','post_id':'55','editor_token':token})
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={})) as call, \
             patch.object(SocialState,'_refresh_posts',new=AsyncMock()):
            await anext(event)
            self.s.set_post_editor_open(False); self.s.new_post()
            self.assertEqual(self.s.edit_post_id,'55')
            await finish(event)
            await finish(self.s.save_post({'body':'Edit','post_id':'55','editor_token':token}))
        self.assertEqual(call.await_count,1)

    async def test_duplicate_create_form_does_not_create_twice(self):
        self.s.new_post()
        form={'body':'Story','post_id':'','editor_token':self.s.post_editor_token}
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={})) as call, \
             patch.object(SocialState,'_refresh_posts',new=AsyncMock()):
            await finish(self.s.save_post(form)); await finish(self.s.save_post(form))
        self.assertEqual(call.await_count,1)

    async def test_failed_edit_keeps_draft_and_image_upload_uses_put(self):
        self.post('9')
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=APIError('Unavailable',503))):
            await finish(self.s.save_post({'body':'Draft'}))
        self.assertEqual(self.s.edit_post_id,'55')
        self.assertTrue(self.s.post_editor_open)
        with TemporaryDirectory() as directory:
            path=Path(directory)/'cover.png'; path.write_bytes(b'fictional-image')
            self.s._post_image_path=str(path); self.s.post_image_mime='image/png'
            with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
                 patch('Codeboxd_main.state.social.upload_file',new=AsyncMock()) as upload, \
                 patch.object(SocialState,'_refresh_posts',new=AsyncMock()):
                await finish(self.s.save_post({'body':'With image'}))
            self.assertEqual(upload.await_args.args[0],'/posts/55')
            self.assertEqual(upload.await_args.kwargs['method'],'PUT')

    async def test_search_lists_all_types_and_add_external_only_once(self):
        self.s.list_media_query='Matrix'
        items=[media(kind) for kind in ('movie','series','anime','book')]
        with patch('Codeboxd_main.state.social.catalog.search',new=AsyncMock(return_value=(items,[]))):
            await finish(self.s.search_list_media())
        self.assertEqual(len(self.s.list_media_results),4)
        async def call(method,path,data=None):
            return dict(items[0],id=88) if path=='/media' else {'id':91}
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=call)) as request:
            await finish(self.s.add_list_result(items[0]['identity_key']))
            await finish(self.s.add_list_result(items[0]['identity_key']))
        self.assertEqual([(x.args[0],x.args[1]) for x in request.await_args_list],
                         [('POST','/media'),('POST','/lists/12/items')])
        self.assertEqual(self.s.list_items[0]['id'],'88')

    async def test_obsolete_search_empty_and_failed_search(self):
        self.s.list_media_query='Matrix'
        async def obsolete(*args):
            self.s.update_list_media_query('Other')
            return [media()],[]
        with patch('Codeboxd_main.state.social.catalog.search',new=AsyncMock(side_effect=obsolete)):
            await finish(self.s.search_list_media())
        self.assertEqual(self.s.list_media_results,[])
        with patch('Codeboxd_main.state.social.catalog.search',new=AsyncMock(return_value=([],[]))):
            await finish(self.s.search_list_media())
        self.assertIn('Nenhuma',self.s.list_media_error)
        with patch('Codeboxd_main.state.social.catalog.search',new=AsyncMock(side_effect=APIError('Provider failure',503))):
            await finish(self.s.search_list_media())
        self.assertIn('Provider failure',self.s.list_media_error)

    async def test_add_cannot_cross_list_or_ownership_boundary(self):
        self.s._list_media_candidates={'fixture:movie':media()}
        async def persist(item):
            self.s.selected_list={'id':'13','user_id':'7'}
            return dict(item,id=88)
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_persist_list_candidate',new=AsyncMock(side_effect=persist)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.add_list_result('fixture:movie'))
        call.assert_not_awaited()
        self.s.selected_list={'id':'14','user_id':'8'}
        with patch.object(SocialState,'_require_user',new=AsyncMock()) as auth:
            await finish(self.s.add_list_result('fixture:movie'))
        auth.assert_not_awaited()

    async def test_details_picker_only_own_public_private_and_no_interaction_write(self):
        self.s._selected_raw=media(mid=9)
        lists=[dict(id=12,user_id=7,title='Private',is_public=False),
               dict(id=13,user_id=7,title='Public',is_public=True),
               dict(id=14,user_id=8,title='Other',is_public=True)]
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value=lists)):
            await finish(self.s.open_media_lists())
        self.assertEqual([x['id'] for x in self.s.media_list_options],['12','13'])
        self.s.select_media_list('14'); self.assertEqual(self.s.media_list_target,'')
        self.s.select_media_list('12')
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_persist_selected',new=AsyncMock(return_value=9)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={})) as call:
            await finish(self.s.add_current_media_to_list())
        call.assert_awaited_once_with('POST','/lists/12/items',{'media_id':9})

    async def test_details_changed_during_persist_does_not_add_wrong_work(self):
        self.s._selected_raw=media(mid=9)
        self.s.media_list_open=True; self.s.media_list_target='12'
        self.s.media_list_options=[{'id':'12','title':'Private','is_public':'False'}]
        async def changed():
            self.s._selected_raw=media('book',11)
            return 9
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_persist_selected',new=AsyncMock(side_effect=changed)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.add_current_media_to_list())
        call.assert_not_awaited()

    async def test_rejected_session_cannot_write_an_edit(self):
        self.post()
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=False)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.save_post({'body':'Edit','post_id':'55'}))
        call.assert_not_awaited()
        self.assertFalse(self.s.post_saving)

    async def test_failed_list_add_preserves_search_and_existing_items(self):
        item=media(mid=9)
        self.s._list_media_candidates={'fixture:movie':item}
        self.s.list_media_results=[{'key':'fixture:movie','title':'Matrix movie'}]
        self.s.list_items=[{'id':'8','title':'Existing'}]
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=APIError('Unavailable',503))):
            await finish(self.s.add_list_result('fixture:movie'))
        self.assertEqual(self.s.list_items,[{'id':'8','title':'Existing'}])
        self.assertEqual(len(self.s.list_media_results),1)
        self.assertEqual(self.s.selected_list['id'],'12')
        self.assertFalse(self.s.list_item_saving)
        self.assertIn('Unavailable',self.s.list_media_error)

    async def test_failed_picker_load_and_account_change_never_write(self):
        self.s._selected_raw=media(mid=9)
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=APIError('Unavailable',503))):
            await finish(self.s.open_media_lists())
        self.assertTrue(self.s.media_list_open)
        self.assertFalse(self.s.media_list_loading)
        self.assertIn('Unavailable',self.s.media_list_error)
        self.s.media_list_options=[{'id':'12','title':'Private','is_public':'False'}]
        self.s.media_list_target='12'
        async def switched():
            self.s.user_id=8
            return True
        with patch.object(SocialState,'_require_user',new=AsyncMock(side_effect=switched)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.add_current_media_to_list())
        call.assert_not_awaited()


if __name__=='__main__':
    unittest.main()
