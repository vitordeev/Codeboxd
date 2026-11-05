import asyncio
from contextlib import ExitStack
from copy import deepcopy
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


async def finish(event):
    async for _ in event: pass


class FollowFeedListStatusTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.s=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.s.user_id=self.s._identity=7
        self.s.session_token='fixture-session'
        self.s.router.url.path='/media/9'
        self.s._selected_raw={'id':9,'title':'Movie','media_type':'movie'}
        self.s.selected={'id':'9','title':'Movie'}

    def mocks(self, callback):
        stack=ExitStack()
        stack.enter_context(patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)))
        stack.enter_context(patch.object(SocialState,'_call',new=AsyncMock(side_effect=callback)))
        return stack

    async def test_follow_normalizes_ids_and_confirms_follow_unfollow_refollow(self):
        methods=[]
        async def call(method,path,*args,**kwargs):
            self.assertEqual(path,'/follows/2'); methods.append(method)
            return {'follower_id':'7','followed_id':2,'following':method=='PUT'}
        with self.mocks(call):
            for value,expected in ((2,['2']),('002',[]),('2',['2'])):
                await finish(self.s.follow(value))
                self.assertEqual(self.s.following_ids,expected)
        self.assertEqual(methods,['PUT','DELETE','PUT'])
        self.assertEqual(self.s.following_pending,[])

    async def test_follow_uses_actual_response_and_legacy_delete_confirmation(self):
        async def call(method,path,*args,**kwargs):
            return {'follower_id':7,'followed_id':2,'following':False}
        with self.mocks(call): await finish(self.s.follow('2'))
        self.assertEqual(self.s.following_ids,[])
        self.s.following_ids=['2']
        replies=iter([{'success':True},{'following':[]}])
        with self.mocks(lambda *a,**k: next(replies)):
            await finish(self.s.follow('2'))
        self.assertEqual(self.s.following_ids,[])

    async def test_follow_legacy_record_is_confirmed_and_invalid_response_is_not_success(self):
        with self.mocks(lambda *a,**k: {'follower_id':7,'followed_id':2,'id':8}):
            await finish(self.s.follow('2'))
        self.assertEqual(self.s.following_ids,['2'])
        with self.mocks(lambda *a,**k: {}): await finish(self.s.follow('2'))
        self.assertEqual(self.s.following_ids,['2'])
        self.assertIn('confirmar',self.s.notice)

    async def test_follow_errors_and_invalid_targets_preserve_confirmed_state(self):
        for value in ('oops','0','-2',True,'7'):
            with patch.object(SocialState,'_call',new=AsyncMock()) as call:
                await finish(self.s.follow(value))
                call.assert_not_awaited()
        for status in (409,429,503):
            with self.mocks(AsyncMock(side_effect=APIError('Falha visível',status))):
                await finish(self.s.follow('2'))
            self.assertEqual(self.s.following_ids,[])
            self.assertEqual(self.s.notice,'Falha visível')

    async def test_follow_blocks_overlap_and_discards_other_session(self):
        started,release=asyncio.Event(),asyncio.Event()
        async def call(*args,**kwargs):
            started.set(); await release.wait()
            return {'follower_id':7,'followed_id':2,'following':True}
        with self.mocks(call), patch.object(SocialState,'_call',new=AsyncMock(side_effect=call)) as request:
            task=asyncio.create_task(finish(self.s.follow('2')))
            await started.wait(); await finish(self.s.follow('2'))
            self.s.user_id=8; self.s.session_token='other'
            release.set(); await task
        request.assert_awaited_once()
        self.assertEqual(self.s.following_ids,[])

    def post(self):
        return {'id':12,'user_id':2,'body':'Historical post','created_at':1700000000000}

    async def test_feed_new_reader_without_posts_sees_followed_history(self):
        async def call(method,path,*args,**kwargs):
            return [self.post()] if path=='/feed' else []
        with self.mocks(call), patch.object(SocialState,'_load_reference',new=AsyncMock()):
            await self.s.load_feed()
        self.assertEqual([p['id'] for p in self.s.posts],['12'])
        self.assertEqual(self.s.feed_error,'')
        self.assertFalse(self.s.feed_loading)

    async def test_feed_ancillary_errors_do_not_hide_followed_posts(self):
        for failed_path in ('/posts','/likes','references'):
            with self.subTest(path=failed_path):
                async def call(method,path,*args,**kwargs):
                    if path==failed_path: raise APIError('Unavailable',503)
                    return [self.post()] if path=='/feed' else []
                ref=AsyncMock(side_effect=APIError('References',503)) if failed_path=='references' else AsyncMock()
                with self.mocks(call), patch.object(SocialState,'_load_reference',new=ref):
                    await self.s.load_feed()
                self.assertEqual(len(self.s.posts),1)
                self.assertTrue(self.s.feed_warning)
                self.assertEqual(self.s.feed_error,'')

    async def test_feed_error_is_distinct_from_empty_and_retry_succeeds(self):
        async def failed(*args,**kwargs): raise APIError('Feed indisponível',503)
        with self.mocks(failed), patch.object(SocialState,'_load_reference',new=AsyncMock()):
            await self.s.load_feed()
        self.assertEqual(self.s.posts,[])
        self.assertEqual(self.s.feed_error,'Feed indisponível')
        with self.mocks(lambda *a,**k: []), patch.object(SocialState,'_load_reference',new=AsyncMock()):
            await self.s.load_feed()
        self.assertEqual(self.s.feed_error,'')
        self.assertEqual(self.s.posts,[])

    async def test_feed_authorization_failure_is_not_partial_success(self):
        async def call(method,path,*args,**kwargs):
            if path=='/posts': raise APIError('Forbidden',403)
            return [self.post()] if path=='/feed' else []
        with self.mocks(call), patch.object(SocialState,'_load_reference',new=AsyncMock()):
            await self.s.load_feed()
        self.assertEqual(self.s.feed_error,'Forbidden')
        self.assertEqual(self.s.posts,[])

    async def test_switch_and_clear_use_single_status_without_touching_review(self):
        server=None; writes=[]
        async def call(method,path,data=None,**kwargs):
            nonlocal server
            self.assertEqual(path,'/media-list-status/9')
            if method=='PUT': server=data['status']; writes.append(deepcopy(data))
            return {'user_id':7,'media_id':9,'status':server}
        self.s.selected_review='Preserve review'; self.s.selected_rating='4.5'
        self.s.selected_list={'id':'1','user_id':'7','default_key':'7:planned'}
        with self.mocks(call):
            for status,title,expected,lower in (
                ('planned','Quero ver / ler','want_to_watch',['9']),
                ('completed','Já assisti / li','watched',[]),
                ('planned','Quero ver / ler','want_to_watch',['9']),
                ('planned','Quero ver / ler','',[])):
                await finish(self.s.quick_add(status,0,title))
                self.assertEqual(self.s.selected_list_status,expected)
                self.assertEqual([p['id'] for p in self.s.list_items],lower)
        self.assertEqual(writes,[{'status':s} for s in ('want_to_watch','watched','want_to_watch',None)])
        self.assertEqual(self.s.selected_review,'Preserve review')
        self.assertEqual(self.s.selected_rating,'4.5')
        self.assertEqual(self.s.selected_status,'planned')
        self.assertFalse(self.s.list_status_saving)

    async def test_status_load_accepts_string_ids_and_rejects_wrong_contract(self):
        for result in ({'user_id':'7','media_id':'9','status':'watched'},
                       {'user_id':7,'media_id':9,'status':None}):
            with self.mocks(lambda *a,**k: result): await self.s._load_selected_list_status(9)
            self.assertEqual(self.s.selected_list_status,result['status'] or '')
        for result in ({},{'user_id':8,'media_id':9,'status':'watched'},
                       {'user_id':7,'media_id':10,'status':'watched'},
                       {'user_id':7,'media_id':9,'status':'invalid'}):
            self.s.selected_list_status='want_to_watch'
            with self.mocks(lambda *a,**k: result): await self.s._load_selected_list_status(9)
            self.assertEqual(self.s.selected_list_status,'want_to_watch')
            self.assertIn('confirmar',self.s.list_status_error)

    async def test_status_failed_write_keeps_get_confirmation_and_does_not_fallback(self):
        calls=[]
        async def call(method,path,data=None,**kwargs):
            calls.append((method,path))
            if method=='PUT': raise APIError('Não salvou',503)
            return {'user_id':7,'media_id':9,'status':'watched'}
        with self.mocks(call): await finish(self.s.quick_add('planned',0,'Quero ver / ler'))
        self.assertEqual(self.s.selected_list_status,'watched')
        self.assertEqual(self.s.list_status_error,'Não salvou')
        self.assertEqual(calls,[('GET','/media-list-status/9'),('PUT','/media-list-status/9')])

    async def test_status_unknown_backend_blocks_all_legacy_writes(self):
        with self.mocks(AsyncMock(side_effect=APIError('Endpoint indisponível',404))), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=APIError('Endpoint indisponível',404))) as call:
            await finish(self.s.quick_add('completed',0,'Já assisti / li'))
        call.assert_awaited_once_with('GET','/media-list-status/9')
        self.assertEqual(self.s.selected_list_status,'')

    async def test_status_overlap_and_obsolete_response_cannot_change_new_work(self):
        started,release=asyncio.Event(),asyncio.Event()
        async def call(method,*args,**kwargs):
            if method=='PUT': started.set(); await release.wait()
            return {'user_id':7,'media_id':9,'status':'watched' if method=='PUT' else None}
        with self.mocks(call), patch.object(SocialState,'_call',new=AsyncMock(side_effect=call)) as request:
            task=asyncio.create_task(finish(self.s.quick_add('completed',0,'Já assisti / li')))
            await started.wait()
            await finish(self.s.quick_add('planned',0,'Quero ver / ler'))
            self.s._selected_raw={'id':10}; self.s.selected_list_status='want_to_watch'
            release.set(); await task
        self.assertEqual(request.await_count,2)
        self.assertEqual(self.s.selected_list_status,'want_to_watch')

    async def test_late_status_read_cannot_overwrite_newer_mutation(self):
        started,release=asyncio.Event(),asyncio.Event()
        async def slow(*args,**kwargs):
            started.set(); await release.wait()
            return {'user_id':7,'media_id':9,'status':'want_to_watch'}
        with self.mocks(slow):
            task=asyncio.create_task(self.s._load_selected_list_status(9))
            await started.wait()
            with self.mocks(lambda *a,**k: {'user_id':7,'media_id':9,'status':'watched' if a[0]=='PUT' else None}):
                await finish(self.s.quick_add('completed',0,'Já assisti / li'))
            release.set(); await task
        self.assertEqual(self.s.selected_list_status,'watched')

    async def test_picker_default_add_refreshes_status_custom_add_does_not(self):
        self.s.media_list_open=True; self.s.media_list_target='1'
        self.s.media_list_options=[{'id':'1','title':'Default renamed','default_key':'7:completed'}]
        calls=[]
        async def call(method,path,*args,**kwargs):
            calls.append(path)
            return {'user_id':7,'media_id':9,'status':'watched'} if method=='GET' else {'id':1}
        with self.mocks(call): await finish(self.s.add_current_media_to_list())
        self.assertEqual(calls,['/lists/1/items','/media-list-status/9'])
        self.assertEqual(self.s.selected_list_status,'watched')

    async def test_custom_picker_add_preserves_status_and_has_no_new_contract_dependency(self):
        self.s.media_list_open=True; self.s.media_list_target='1'
        self.s.media_list_options=[{'id':'1','title':'Já assisti / li','default_key':''}]
        self.s.selected_list_status='want_to_watch'
        with self.mocks(lambda *a,**k: {'id':1}), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={'id':1})) as call:
            await finish(self.s.add_current_media_to_list())
        call.assert_awaited_once_with('POST','/lists/1/items',{'media_id':9})
        self.assertEqual(self.s.selected_list_status,'want_to_watch')

    async def test_new_feed_load_discards_older_response_on_same_route(self):
        self.s.router.url.path='/feed'
        started,release=asyncio.Event(),asyncio.Event()
        reads=0
        async def call(method,path,*args,**kwargs):
            nonlocal reads
            if path=='/feed':
                reads+=1
                if reads==1:
                    started.set(); await release.wait()
                    return [dict(self.post(),id=11)]
                return [self.post()]
            return []
        with self.mocks(call), patch.object(SocialState,'_load_reference',new=AsyncMock()):
            older=asyncio.create_task(self.s.load_feed())
            await started.wait(); await self.s.load_feed()
            release.set(); await older
        self.assertEqual([p['id'] for p in self.s.posts],['12'])
        self.assertFalse(self.s.feed_loading)

    async def test_successful_refresh_clears_old_feed_error(self):
        self.s.feed_error='Old failure'
        with self.mocks(lambda method,path,**k: [self.post()] if path=='/feed' else []):
            await self.s._refresh_posts()
        self.assertEqual(self.s.feed_error,'')

    async def test_status_switch_account_during_auth_never_writes(self):
        async def switched():
            self.s.user_id=8; self.s.session_token='other-session'
            return True
        with patch.object(SocialState,'_require_user',new=AsyncMock(side_effect=switched)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.quick_add('completed',0,'Já assisti / li'))
        call.assert_not_awaited()
        self.assertFalse(self.s.list_status_saving)

    async def test_status_retry_after_timeout_reconciles_server_before_toggle(self):
        server=None
        async def first(method,path,data=None,**kwargs):
            nonlocal server
            if method=='PUT':
                server=data['status']; raise APIError('Timeout after commit',503)
            return {'user_id':7,'media_id':9,'status':server}
        with self.mocks(first): await finish(self.s.quick_add('completed',0,'Já assisti / li'))
        self.assertEqual(self.s.selected_list_status,'')
        self.assertEqual(server,'watched')
        async def second(method,path,data=None,**kwargs):
            nonlocal server
            if method=='PUT': server=data['status']
            return {'user_id':7,'media_id':9,'status':server}
        with self.mocks(second):
            await self.s._load_selected_list_status(9)
            self.assertEqual(self.s.selected_list_status,'watched')
            await finish(self.s.quick_add('planned',0,'Quero ver / ler'))
        self.assertEqual(server,'want_to_watch')

    def test_controls_bind_to_confirmed_status_and_feed_error(self):
        from Codeboxd_main.pages.social import media_page, feed_page
        media=str(media_page()); feed=str(feed_page())
        self.assertIn('selected_list_status',media)
        self.assertIn('aria-pressed',media)
        self.assertIn('feed_error',feed)
        self.assertIn('Tentar novamente',feed)
