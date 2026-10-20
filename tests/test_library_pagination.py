import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


def item(identifier, **overrides):
    return dict(id=identifier,user_id=7,media_id=identifier,status='completed',
                rating=3.5,review='Review',spoiler=True,media_title=f'Work {identifier}',
                media_type='book',media_cover_url='',media_year=2020,**overrides)


class LibraryPaginationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        root=rx.State(_reflex_internal_init=True)
        root.router.url.path='/biblioteca'
        self.state=root.get_substate(SocialState.get_full_name().split('.'))
        self.state.user_id=7; self.state._identity=7
        self.state.auth_token='fictional-token'
        self.flag=patch.dict('os.environ',{'LIBRARY_PAGINATION_ENABLED':'true'})
        self.flag.start(); self.addCleanup(self.flag.stop)
        self.auth=patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True))
        self.auth.start(); self.addCleanup(self.auth.stop)

    async def more(self):
        async for _ in self.state.show_more_library(): pass

    async def test_large_collection_is_bounded_and_all_items_reachable(self):
        calls=[]
        async def call(method,path,**kwargs):
            self.assertEqual((method,path,kwargs['paginate']),('GET','/library',False))
            cursor=kwargs['params']['after_id']; calls.append(cursor)
            return {'items':[item(i) for i in range(cursor+1,min(cursor+20,250)+1)],
                    'has_more':cursor+20<250}
        with patch.object(SocialState,'_call',side_effect=call):
            await self.state.load_library()
            self.assertEqual(len(self.state.library),20)
            self.assertEqual(calls,[0])
            while self.state.library_has_more: await self.more()
        self.assertEqual([i['id'] for i in self.state.visible_library],[str(i) for i in range(1,251)])
        self.assertEqual(calls,list(range(0,250,20)))
        self.assertEqual(self.state.catalog_items,[])
        self.assertEqual(self.state.library[0]['rating'],'3,5')
        self.assertEqual(self.state.library[0]['spoiler'],'True')

    async def test_failure_preserves_cards_cursor_and_manual_retry(self):
        call=AsyncMock(side_effect=[{'items':[item(i) for i in range(1,21)],'has_more':True},
            APIError('Unavailable',503),{'items':[item(21)],'has_more':False}])
        with patch.object(SocialState,'_call',call):
            await self.state.load_library(); await self.more()
            self.assertEqual(len(self.state.library),20)
            self.assertEqual(self.state._library_cursor,20)
            self.assertTrue(self.state.library_error)
            self.assertFalse(self.state.library_loading)
            await self.more()
        self.assertEqual(len(self.state.library),21)
        self.assertFalse(self.state.library_error)
        self.assertEqual(call.call_args_list[1].kwargs,call.call_args_list[2].kwargs)

    async def test_empty_and_exact_twenty_need_no_extra_request(self):
        for size in (0,20):
            call=AsyncMock(return_value={'items':[item(i) for i in range(1,size+1)],'has_more':False})
            with patch.object(SocialState,'_call',call):
                await self.state.load_library(); await self.more()
            self.assertEqual(len(self.state.library),size)
            self.assertEqual(call.await_count,1)

    async def test_bad_pages_are_atomic_and_retryable(self):
        bad_pages=[None,{'items':[],'has_more':'false'},
            {'items':[item(i) for i in range(1,22)],'has_more':False},
            {'items':[item(1),item(1)],'has_more':False},
            {'items':[dict(item(1),user_id=8)],'has_more':False},
            {'items':[item(2),item(1)],'has_more':False},
            {'items':[],'has_more':True}]
        for data in bad_pages:
            with self.subTest(data=data),patch.object(SocialState,'_call',AsyncMock(return_value=data)):
                await self.state.load_library()
                self.assertEqual(self.state.library,[])
                self.assertEqual(self.state._library_cursor,0)
                self.assertTrue(self.state.library_error)
                self.assertTrue(self.state.library_has_more)

    async def test_deduplicates_media_without_losing_cursor(self):
        data={'items':[item(1),dict(item(2),media_id=1)],'has_more':False}
        with patch.object(SocialState,'_call',AsyncMock(return_value=data)):
            await self.state.load_library()
        self.assertEqual(len(self.state.library),1)
        self.assertEqual(self.state._library_cursor,2)

    async def test_missing_media_remains_accessible_without_extra_fetch(self):
        data={'items':[dict(item(1),media_title=None)],'has_more':False}
        with patch.object(SocialState,'_call',AsyncMock(return_value=data)) as call:
            await self.state.load_library()
        self.assertEqual(self.state.library[0]['title'],'Obra indisponível')
        self.assertEqual(self.state.library[0]['id'],'1')
        self.assertEqual(call.await_count,1)

    async def test_late_account_route_and_reset_results_are_discarded(self):
        for change in ('account','token','route','reset'):
            started=asyncio.Event(); release=asyncio.Event()
            async def call(*args,**kwargs):
                started.set(); await release.wait()
                return {'items':[item(1)],'has_more':False}
            self.setUpStateForLateResult()
            with patch.object(SocialState,'_call',side_effect=call):
                task=asyncio.create_task(self.state._load_library_page())
                await started.wait()
                if change=='account': self.state.user_id=8
                elif change=='token': self.state.auth_token='other-token'
                elif change=='route': self.state.router.url.path='/listas'
                else: self.state._reset_personal()
                release.set(); await task
            self.assertEqual(self.state.library,[])
            self.assertFalse(self.state.library_loading)

    def setUpStateForLateResult(self):
        self.state.user_id=7; self.state.auth_token='fictional-token'
        self.state.router.url.path='/biblioteca'
        self.state._library_owner=self.state._token()
        self.state.library_has_more=True

    async def test_concurrent_read_is_suppressed(self):
        self.setUpStateForLateResult()
        started=asyncio.Event(); release=asyncio.Event()
        async def call(*args,**kwargs):
            started.set(); await release.wait()
            return {'items':[item(1)],'has_more':False}
        with patch.object(SocialState,'_call',side_effect=call) as mocked:
            task=asyncio.create_task(self.state._load_library_page())
            await started.wait(); await self.more()
            release.set(); await task
        self.assertEqual(mocked.await_count,1)

    async def test_cooldown_blocks_network_until_expiry(self):
        call=AsyncMock(side_effect=[APIError('Wait 20 seconds',429,20),{'items':[],'has_more':False}])
        with patch.object(SocialState,'_call',call),patch('Codeboxd_main.state.social.time.monotonic',return_value=100):
            await self.state.load_library(); await self.more()
            self.assertEqual(call.await_count,1)
            self.assertTrue(self.state.library_error)
        with patch.object(SocialState,'_call',call),patch('Codeboxd_main.state.social.time.monotonic',return_value=121):
            await self.more()
        self.assertEqual(call.await_count,2)

    async def test_rejected_authorization_clears_visible_private_items(self):
        for status in (401,403):
            with patch.object(SocialState,'_call',AsyncMock(side_effect=[
                {'items':[item(i) for i in range(1,21)],'has_more':True},APIError('Denied',status)])):
                await self.state.load_library(); await self.more()
            self.assertFalse(self.state.library)
            self.assertFalse(self.state.library_has_more)

    async def test_disabled_flag_uses_legacy_only(self):
        with patch.dict('os.environ',{'LIBRARY_PAGINATION_ENABLED':'false'}), \
             patch.object(SocialState,'_load_media',AsyncMock()) as media, \
             patch.object(SocialState,'_call',AsyncMock(return_value=[])) as call:
            await self.state.load_library(); await self.more()
        self.assertFalse(self.state.library_paginated)
        media.assert_awaited_once()
        call.assert_awaited_once_with('GET','/interactions')
        self.assertEqual(self.state.visible_count,40)

    async def test_transport_boundary_fetches_only_requested_page(self):
        response={'items':[item(i) for i in range(1,21)],'has_more':True}
        with patch('Codeboxd_main.state.social.request',AsyncMock(return_value=response)) as request:
            await self.state.load_library()
        request.assert_awaited_once_with('GET','/library',token='fictional-token',data=None,params={'after_id':0})
        self.assertEqual(len(self.state.visible_library),20)
