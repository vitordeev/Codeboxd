import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.session import SessionState
from Codeboxd_main.state.social import SocialState


class SessionNavigationTests(unittest.IsolatedAsyncioTestCase):
    async def test_reset_email_cooldown_blocks_repeat_and_resumes_without_login(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(side_effect=[
                APIError('Wait',429,20), {}])) as request, \
             patch('Codeboxd_main.state.session.time.monotonic', return_value=100) as clock:
            await self.session.request_password_reset({'email':'reader@example.invalid'})
            clock.return_value=105
            await self.session.request_password_reset({'email':'READER@example.invalid'})
            self.assertIn('15 segundos', self.session.reset_message)
            request.assert_awaited_once()
            clock.return_value=120
            await self.session.request_password_reset({'email':'reader@example.invalid'})
            self.assertEqual(request.await_count,2)
            self.assertTrue(self.session.reset_success)

    def setUp(self):
        root=rx.State(_reflex_internal_init=True)
        self.session=root.get_substate(SessionState.get_full_name().split('.'))
        self.social=root.get_substate(SocialState.get_full_name().split('.'))
        self.session.session_token='token-a'
        self.member={'id':7,'role':'member','account_status':'active'}

    async def test_navigation_reuses_only_verified_identity_until_expiry(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value=self.member)) as request, \
             patch('Codeboxd_main.state.session.time.monotonic',return_value=100) as clock:
            self.assertTrue(await self.session._validate_session())
            clock.return_value=114.9
            self.assertTrue(await self.social._validate_navigation_session())
            request.assert_awaited_once()
            clock.return_value=115
            self.assertTrue(await self.social._validate_navigation_session())
            self.assertEqual(request.await_count,2)

    async def test_writes_and_admin_guards_do_not_use_navigation_cache(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value=self.member)) as request:
            await self.session._validate_session()
            self.assertTrue(await self.social._require_user())
            self.assertEqual(request.await_count,2)
            await self.session.guard_admin()
            self.assertEqual(request.await_count,3)

    async def test_admin_identity_is_revalidated_even_during_navigation(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value={'id':7,'role':'admin'})) as request:
            await self.session._validate_session()
            await self.social._validate_navigation_session()
            self.assertEqual(request.await_count,2)

    async def test_disabled_account_rejected_on_fresh_check_and_cache_discarded(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(side_effect=[
                self.member,{'id':7,'role':'member','account_status':'disabled'}])):
            await self.session._validate_session()
            self.assertFalse(await self.social._require_user())
        self.assertFalse(self.session.is_authenticated)
        self.assertFalse(self.session._token())
        self.assertFalse(self.session._navigation_verified_token)

    async def test_new_token_does_not_inherit_identity_on_service_failure(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(side_effect=[
                self.member,APIError('outage',503),APIError('outage',503)])):
            await self.session._validate_session()
            await self.session._validate_session()
            self.session.session_token='token-b'
            self.assertFalse(await self.social._validate_navigation_session())
        self.assertEqual(self.session.user_id,0)

    async def test_cooldown_blocks_checks_then_resumes_without_logout(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(side_effect=[
                self.member,APIError('Wait',429,20),self.member])) as request, \
             patch('Codeboxd_main.state.session.time.monotonic',return_value=100) as clock:
            await self.session._validate_session()
            self.assertFalse(await self.session._validate_session())
            clock.return_value=105
            self.assertFalse(await self.social._validate_navigation_session())
            self.assertFalse(await self.session._validate_session())
            self.assertEqual(request.await_count,2)
            self.assertIn('15 segundos',self.session.error_message)
            self.assertEqual(self.session.user_id,7)
            self.assertEqual(self.session._token(),'token-a')
            clock.return_value=120
            self.assertTrue(await self.session._validate_session())
            self.assertEqual(request.await_count,3)
            self.assertFalse(self.session.error_message)

    async def test_logout_and_new_session_do_not_reuse_validation(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value=self.member)) as request:
            await self.session._validate_session()
            self.session._clear_session()
            self.session.session_token='token-a'
            await self.session._validate_navigation_session()
            other=rx.State(_reflex_internal_init=True).get_substate(SessionState.get_full_name().split('.'))
            other.session_token='token-a'
            await other._validate_navigation_session()
            self.assertEqual(request.await_count,3)

    async def test_profile_cache_invalidates_on_write_and_cannot_be_repopulated_by_old_read(self):
        started=asyncio.Event()
        release=asyncio.Event()
        async def call(method,path,**kwargs):
            if method=='GET':
                started.set()
                await release.wait()
                return {'profile':{'username':'old'}}
            return {}
        with patch('Codeboxd_main.state.social.request',side_effect=call):
            pending=asyncio.create_task(self.social._call('GET','/profiles/7'))
            await started.wait()
            await self.social._call('PUT','/profile',{'username':'new'})
            release.set()
            await pending
        self.assertEqual(self.social._navigation_reads,{})

    async def test_profile_cache_reuses_copies_and_refreshes_after_write(self):
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(return_value={'profile':{'username':'old'}})) as request:
            first=await self.social._call('GET','/profiles/7')
            first['profile']['username']='mutated'
            second=await self.social._call('GET','/profiles/7')
            self.assertEqual(second['profile']['username'],'old')
            request.assert_awaited_once()
            await self.social._call('PUT','/profile',{'username':'new'})
            request.return_value={'profile':{'username':'new'}}
            self.assertEqual((await self.social._call('GET','/profiles/7'))['profile']['username'],'new')

    async def test_unauthorized_data_response_discards_identity_reuse(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value=self.member)):
            await self.session._validate_session()
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=APIError('Denied',403))):
            with self.assertRaises(APIError): await self.social._call('GET','/profiles/7')
        self.assertFalse(self.session._navigation_verified_token)
