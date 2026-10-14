"""Recovery form contracts; all provider requests are controlled test doubles."""
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.session import SessionState


class PasswordRecoveryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SessionState.get_full_name().split('.'))
        self.form = {'email': 'Member@Example.com', 'code': '123456',
                     'password': 'replacement123', 'confirm_password': 'replacement123'}

    async def test_invalid_codes_never_reach_provider(self):
        for code in ('', '12345', '1234567', 'abcdef', '12 456', '１２３４５６',
                     '123e45', 'c92a23e5-8aa0-4b78-81b3-d5e149a72d89'):
            with self.subTest(code=code), patch('Codeboxd_main.state.session.request', new=AsyncMock()) as request:
                await self.state.reset_password({**self.form, 'code': code})
                request.assert_not_awaited()
                self.assertFalse(self.state.reset_success)
                self.assertIn('6 dígitos', self.state.reset_message)

    async def test_valid_six_digits_with_leading_zero_are_preserved(self):
        mock = AsyncMock(side_effect=[{'authToken': 'temporary-reset'}, {'message': {'success': True}}])
        with patch('Codeboxd_main.state.session.request', new=mock):
            await self.state.reset_password({**self.form, 'code': ' 012345 '})
        self.assertEqual(mock.await_args_list[0].kwargs['data'],
                         {'email': 'member@example.com', 'magic_token': '012345'})
        self.assertEqual(mock.await_args_list[1].kwargs['token'], 'temporary-reset')
        self.assertEqual(self.state._token(), '')
        self.assertFalse(self.state.is_authenticated)
        self.assertTrue(self.state.reset_success)
        self.assertFalse(self.state.is_loading)

    async def test_mismatched_or_weak_password_does_not_consume_code(self):
        for password, confirmation in (('short1', 'short1'), ('withoutnumbers', 'withoutnumbers'),
                                       ('replacement123', 'different123')):
            with self.subTest(password=password), patch('Codeboxd_main.state.session.request', new=AsyncMock()) as request:
                await self.state.reset_password({**self.form, 'password': password, 'confirm_password': confirmation})
                request.assert_not_awaited()

    async def test_rejected_code_does_not_update_password(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(side_effect=APIError('Rejected', 401))) as request:
            await self.state.reset_password(self.form)
        self.assertEqual(request.await_count, 1)
        self.assertIn('inválido ou expirado', self.state.reset_message)
        self.assertFalse(self.state.reset_success)

    async def test_request_response_is_generic_for_registered_and_missing_accounts(self):
        messages = []
        for response in ({'message': {'success': True}}, APIError('Not found', 404)):
            mock = AsyncMock(side_effect=response) if isinstance(response, APIError) else AsyncMock(return_value=response)
            with patch('Codeboxd_main.state.session.request', new=mock):
                await self.state.request_password_reset({'email': 'Member@Example.com'})
            self.assertTrue(self.state.reset_success)
            self.assertIn('6 dígitos', self.state.reset_message)
            self.assertIn('15 minutos', self.state.reset_message)
            messages.append(self.state.reset_message)
        self.assertEqual(messages[0], messages[1])

    async def test_concurrent_submission_is_ignored(self):
        self.state.is_loading = True
        with patch('Codeboxd_main.state.session.request', new=AsyncMock()) as request:
            await self.state.request_password_reset({'email': 'member@example.com'})
            await self.state.reset_password(self.form)
        request.assert_not_awaited()

    async def test_password_update_failure_never_persists_reset_token(self):
        mock = AsyncMock(side_effect=[{'authToken': 'temporary-reset'}, APIError('Unavailable', 503)])
        with patch('Codeboxd_main.state.session.request', new=mock):
            await self.state.reset_password(self.form)
        self.assertEqual(self.state._token(), '')
        self.assertFalse(self.state.reset_success)
        self.assertFalse(self.state.is_loading)
