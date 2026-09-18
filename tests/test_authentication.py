"""Local authentication regressions. No real accounts or network requests."""
import os
import unittest
from unittest.mock import AsyncMock, patch

import httpx
import reflex as rx

from Codeboxd_main.services import api
from Codeboxd_main.state.session import SessionState


class SessionTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SessionState.get_full_name().split('.'))

    async def test_cookie_presence_does_not_grant_access(self):
        self.state.auth_token = 'unverified'
        self.assertFalse(self.state.is_authenticated)
        self.assertFalse(self.state.is_admin)

    async def test_expired_session_clears_identity_and_both_tokens(self):
        self.state.auth_token = 'expired'
        self.state.session_token = 'expired-tab'
        self.state.user_id = 42
        self.state.user_role = 'admin'
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(side_effect=api.APIError('Expired',401))):
            self.assertFalse(await self.state._validate_session())
        self.assertFalse(self.state.is_authenticated)
        self.assertFalse(self.state.is_admin)
        self.assertEqual(self.state._token(), '')

    async def test_service_failure_fails_closed_but_keeps_token_for_retry(self):
        self.state.auth_token = 'existing'
        self.state.user_id = 42
        self.state.user_role = 'admin'
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(side_effect=api.APIError('Unavailable',503))):
            self.assertFalse(await self.state._validate_session())
        self.assertFalse(self.state.is_admin)
        self.assertEqual(self.state.auth_token, 'existing')

    async def test_member_is_authenticated_but_is_not_admin(self):
        self.state.session_token = 'valid'
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={'id':7,'role':'member','name':'Maria'})):
            self.assertTrue(await self.state._validate_session())
        self.assertTrue(self.state.is_authenticated)
        self.assertFalse(self.state.is_admin)

    async def test_disabled_account_is_denied(self):
        self.state.auth_token = 'valid'
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={'id':7,'role':'admin','account_status':'disabled'})):
            self.assertFalse(await self.state._validate_session())
        self.assertEqual(self.state._token(), '')

    async def test_login_respects_remember_choice(self):
        for remember in (False, True):
            with self.subTest(remember=remember):
                self.state = rx.State(_reflex_internal_init=True).get_substate(SessionState.get_full_name().split('.'))
                mock = AsyncMock(side_effect=[{'authToken':'new-token'}, {'id':7,'role':'member'}])
                with patch('Codeboxd_main.state.session.request', new=mock):
                    events = [event async for event in self.state._authenticate(
                        {'email':' Maria@Example.com ','password':'example1','remember':remember},False)]
                self.assertEqual(bool(self.state.auth_token),remember)
                self.assertEqual(bool(self.state.session_token),not remember)
                self.assertTrue(self.state.is_authenticated)
                self.assertFalse(self.state.is_loading)
                self.assertEqual(mock.call_args_list[0].kwargs['data']['email'],'maria@example.com')
                self.assertGreaterEqual(len(events),2)

    async def test_signup_cannot_use_old_backend_before_migration(self):
        with patch.dict(os.environ,{'XANO_SOCIAL_URL':''}), patch('Codeboxd_main.state.session.request',new=AsyncMock()) as mock:
            async for _ in self.state._authenticate({'email':'maria@example.com','password':'example1'},True):
                pass
        mock.assert_not_awaited()
        self.assertIn('preparação',self.state.error_message)

    async def test_bad_login_has_specific_message(self):
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(side_effect=api.APIError('Denied',401))):
            async for _ in self.state._authenticate({'email':'maria@example.com','password':'example1'},False):
                pass
        self.assertEqual(self.state.error_message,'E-mail ou senha inválidos.')
        self.assertFalse(self.state.is_loading)


class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_rate_limit_retries_without_losing_request(self):
        client=AsyncMock()
        client.request.side_effect=[httpx.Response(429,headers={'Retry-After':'2'}),httpx.Response(200,json={'id':7})]
        context=AsyncMock(); context.__aenter__.return_value=client
        with patch.dict(os.environ,{'XANO_AUTH_URL':'https://example.com/api:auth'}),patch.object(api.httpx,'AsyncClient',return_value=context),patch.object(api.asyncio,'sleep',new=AsyncMock()) as sleep:
            result=await api.request('GET','/auth/me',group='auth',token='test')
        self.assertEqual(result,{'id':7})
        self.assertEqual(client.request.await_count,2)
        sleep.assert_awaited_once_with(2)

    async def run_request(self, response):
        client = AsyncMock()
        client.request.return_value = response
        context = AsyncMock()
        context.__aenter__.return_value = client
        with patch.dict(os.environ,{'XANO_AUTH_URL':'https://example.com/api:auth/'}), patch.object(api.httpx,'AsyncClient',return_value=context):
            result = await api.request('GET','/auth/me',group='auth',token='test-token')
        self.assertEqual(client.request.call_args.args[1],'https://example.com/api:auth/auth/me')
        self.assertEqual(client.request.call_args.kwargs['headers']['Authorization'],'Bearer test-token')
        return result

    async def test_transport_preserves_auth_and_normalizes_base_url(self):
        self.assertEqual(await self.run_request(httpx.Response(200,json={'id':7})),{'id':7})

    async def test_server_errors_do_not_leak_response_body(self):
        with self.assertRaises(api.APIError) as error:
            await self.run_request(httpx.Response(500,text='secret implementation details'))
        self.assertEqual(error.exception.status,500)
        self.assertNotIn('secret',str(error.exception))

    async def test_malformed_response_is_reported(self):
        with self.assertRaises(api.APIError):
            await self.run_request(httpx.Response(200,text='<html>bad gateway</html>'))

    async def test_rejects_absolute_request_path(self):
        with self.assertRaises(ValueError):
            await api.request('GET','https://unexpected.example.com')


if __name__ == '__main__':
    unittest.main()
