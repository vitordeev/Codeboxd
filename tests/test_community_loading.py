import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class CommunityLoadingTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.router.url.path='/comunidade'

    async def test_guest_reads_people_without_catalog_providers(self):
        async def request(method,path,*args,**kwargs):
            self.assertEqual((method,path),('GET','/profiles'))
            return [{'user_id':7,'username':'reader','display_name':'Reader'}]
        with patch.object(SocialState,'_validate_navigation_session',new=AsyncMock()), \
             patch.object(SocialState,'_call',side_effect=request) as calls, \
             patch.object(SocialState,'load_home',new=AsyncMock()) as home:
            await self.state.load_community()
        home.assert_not_awaited()
        calls.assert_awaited_once()
        self.assertEqual(self.state.people[0]['user_id'],'7')

    async def test_member_keeps_follow_state(self):
        self.state.user_id=2
        async def request(method,path,*args,**kwargs):
            if path=='/profiles': return [{'user_id':7,'username':'reader'}]
            self.assertEqual(path,'/profiles/2')
            return {'following':[{'followed_id':7}]}
        with patch.object(SocialState,'_validate_navigation_session',new=AsyncMock()), \
             patch.object(SocialState,'_call',side_effect=request) as calls:
            await self.state.load_community()
        self.assertEqual(calls.await_count,2)
        self.assertEqual(self.state.following_ids,['7'])

    async def test_late_profile_failure_does_not_replace_current_notice(self):
        started,release=asyncio.Event(),asyncio.Event()
        async def request(*args,**kwargs):
            started.set(); await release.wait()
            raise APIError('Unavailable',503)
        with patch.object(SocialState,'_validate_navigation_session',new=AsyncMock()), \
             patch.object(SocialState,'_call',side_effect=request):
            task=asyncio.create_task(self.state.load_community())
            await started.wait()
            self.state.router.url.path='/listas'
            self.state.notice='Current route'
            release.set(); await task
        self.assertEqual(self.state.notice,'Current route')
