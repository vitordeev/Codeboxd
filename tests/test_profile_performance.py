import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class ProfilePerformanceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        root=rx.State(_reflex_internal_init=True)
        root.router.url.path='/conta'
        self.state=root.get_substate(SocialState.get_full_name().split('.'))
        self.state.user_id=7
        self.state._identity=7
        self.data={'profile':{'user_id':7,'username':'test','display_name':'Test'},
                   'interactions':[{'media_id':9,'status':'completed','rating':1.5}],
                   'followers':[{'follower_id':8}], 'following':[{'followed_id':8}]}

    async def test_partial_failure_keeps_identity_counts_and_people(self):
        async def call(method,path,*args,**kwargs):
            if path=='/profiles/7': return self.data
            if path=='/media': raise APIError('Wait 20 seconds',429,20)
            if path=='/profiles': return [{'user_id':8,'username':'friend','display_name':'Friend'}]
            self.fail('Unexpected path')
        with patch.object(SocialState,'_validate_session',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',side_effect=call):
            updates=self.state._profile_updates()
            await anext(updates)
            self.assertEqual(self.state.profile['username'],'test')
            self.assertTrue(self.state.profile_activity_loading)
            self.assertEqual(self.state.profile_counts,{'followers':1,'following':1,'activities':1})
            async for _ in updates: pass
        self.assertEqual(self.state.followers[0]['username'],'friend')
        self.assertEqual(self.state.following_ids,['8'])
        self.assertTrue(self.state.profile_activity_error)
        self.assertFalse(self.state.profile_people_error)
        self.assertFalse(self.state.profile_activity_loading)

    async def test_activity_survives_people_error(self):
        async def call(method,path,*args,**kwargs):
            if path=='/profiles/7': return self.data
            if path=='/media': return [{'id':9,'title':'Book','media_type':'book'}]
            raise APIError('People unavailable',503)
        with patch.object(SocialState,'_validate_session',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',side_effect=call):
            await self.state.load_profile()
        self.assertEqual(self.state.profile_activity[0]['rating'],'1,5')
        self.assertTrue(self.state.profile_people_error)
        self.assertFalse(self.state.profile_activity_error)

    async def test_route_change_ignores_late_reference_results(self):
        started=asyncio.Event()
        release=asyncio.Event()
        async def call(method,path,*args,**kwargs):
            if path=='/profiles/7': return self.data
            started.set()
            await release.wait()
            return []
        with patch.object(SocialState,'_validate_session',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',side_effect=call):
            task=asyncio.create_task(self.state.load_profile())
            await started.wait()
            self.state.router.url.path='/perfil/8'
            self.state.profile={'user_id':'8','username':'new'}
            release.set()
            await task
        self.assertEqual(self.state.profile['username'],'new')
        self.assertEqual(self.state.profile_activity,[])
