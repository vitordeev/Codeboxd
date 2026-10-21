import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class StaleSocialReadsTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.router.url.path='/feed'
        self.state.session_token='fictional-a'

    async def test_late_reference_or_feed_cannot_replace_another_route(self):
        for loader in ('_load_media','_load_people','_refresh_posts'):
            with self.subTest(loader=loader):
                self.state.router.url.path='/feed'
                started,release=asyncio.Event(),asyncio.Event()
                async def call(*args,**kwargs):
                    started.set(); await release.wait()
                    return []
                with patch.object(SocialState,'_call',side_effect=call) as request:
                    task=asyncio.create_task(getattr(self.state,loader)())
                    await started.wait()
                    self.state.router.url.path='/listas'
                    self.state.posts=[{'body':'Current'}]
                    self.state.people=[{'username':'Current'}]
                    self.state.catalog_items=[{'title':'Current'}]
                    release.set(); await task
                self.assertEqual(self.state.posts,[{'body':'Current'}])
                self.assertEqual(self.state.people,[{'username':'Current'}])
                self.assertEqual(self.state.catalog_items,[{'title':'Current'}])
                request.assert_awaited_once()

    async def test_late_list_selection_does_not_replace_new_list_items(self):
        self.state.lists=[{'id':'1'},{'id':'2'}]
        started,release=asyncio.Event(),asyncio.Event()
        async def call(*args,**kwargs):
            started.set(); await release.wait()
            return [{'media_id':99}]
        with patch.object(SocialState,'_call',side_effect=call):
            task=asyncio.create_task(self.state.open_list('1'))
            await started.wait()
            self.state.selected_list={'id':'2'}
            self.state.list_items=[{'title':'New selection'}]
            release.set(); await task
        self.assertEqual(self.state.list_items,[{'title':'New selection'}])

    async def test_late_unauthorized_response_does_not_invalidate_new_session(self):
        started,release=asyncio.Event(),asyncio.Event()
        async def request(*args,**kwargs):
            started.set(); await release.wait()
            raise APIError('Expired old token',401)
        with patch('Codeboxd_main.state.social.request',side_effect=request):
            task=asyncio.create_task(self.state._call('GET','/profiles'))
            await started.wait()
            self.state.session_token='fictional-b'
            self.state._navigation_verified_token='new-validation'
            release.set()
            with self.assertRaises(APIError) as error: await task
        self.assertEqual(error.exception.status,409)
        self.assertEqual(self.state._navigation_verified_token,'new-validation')

    async def test_default_list_preparation_cannot_write_after_account_switch(self):
        started,release=asyncio.Event(),asyncio.Event()
        async def call(*args,**kwargs):
            started.set(); await release.wait()
            return []
        with patch.object(SocialState,'_call',side_effect=call) as request:
            task=asyncio.create_task(self.state._ensure_default_lists())
            await started.wait()
            self.state.session_token='fictional-b'
            release.set()
            with self.assertRaises(APIError): await task
        request.assert_awaited_once_with('GET','/lists')

    async def test_review_read_started_before_write_cannot_restore_old_rating(self):
        self.state._selected_raw={'id':1}
        self.state.user_id=7
        started,release=asyncio.Event(),asyncio.Event()
        async def call(method,*args,**kwargs):
            if method=='GET':
                started.set(); await release.wait()
                return [{'media_id':1,'status':'completed','rating':1,'review':'Old'}]
            return {}
        with patch.object(SocialState,'_call',side_effect=call), \
             patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)):
            task=asyncio.create_task(self.state._load_personal_interaction('1',True))
            await started.wait()
            await self.state.save_interaction({'rating':'4,5','review':'Confirmed'})
            release.set(); await task
        self.assertEqual(self.state.selected_rating,'4.5')
        self.assertEqual(self.state.selected_review,'Confirmed')
