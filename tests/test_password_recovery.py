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

    async def test_request_for_active_account_advances_to_code(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={'message': {'success': True}})):
            await self.state.request_password_reset({'email': 'Member@Example.com'})
        self.assertTrue(self.state.reset_success)
        self.assertTrue(self.state.reset_code_requested)
        self.assertIn('6 dígitos', self.state.reset_message)
        self.assertIn('15 minutos', self.state.reset_message)

    async def test_missing_account_stays_on_email_step_and_preserves_address(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(side_effect=APIError('Not found', 404))):
            await self.state.request_password_reset({'email': 'Missing@Example.com'})
        self.assertFalse(self.state.reset_success)
        self.assertFalse(self.state.reset_code_requested)
        self.assertEqual(self.state.reset_email, 'missing@example.com')
        self.assertIn('Não encontramos uma conta ativa', self.state.reset_message)
        self.assertEqual(self.state._reset_retry_at, 0)

    async def test_provider_error_does_not_advance_or_report_success(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(side_effect=APIError('Send failed', 400))):
            await self.state.request_password_reset({'email': 'member@example.com'})
        self.assertFalse(self.state.reset_success)
        self.assertFalse(self.state.reset_code_requested)
        self.assertIn('Não foi possível enviar', self.state.reset_message)

    async def test_password_boundaries_are_checked_before_consuming_code(self):
        for password in ('Abc1234', 'A1' + 'x' * 127, 'abcdefgh', '12345678', 'abcdefg١'):
            with self.subTest(length=len(password)), patch('Codeboxd_main.state.session.request', new=AsyncMock()) as request:
                await self.state.reset_password({**self.form, 'password': password, 'confirm_password': password})
                request.assert_not_awaited()
                self.assertIn('8 a 128', self.state.reset_message)
        for password in ('Abc12345', 'A1' + 'é' * 126, '  Ab1234  '):
            self.state.reset_completed = False
            mock = AsyncMock(side_effect=[{'authToken': 'reset'}, {}])
            with patch('Codeboxd_main.state.session.request', new=mock):
                await self.state.reset_password({**self.form, 'password': password, 'confirm_password': password})
            self.assertTrue(self.state.reset_completed)
            self.assertEqual(mock.await_args_list[1].kwargs['data']['password'], password)

    async def test_password_rejection_after_code_acceptance_has_specific_feedback(self):
        mock = AsyncMock(side_effect=[{'authToken': 'reset'}, APIError('Rejected', 400)])
        with patch('Codeboxd_main.state.session.request', new=mock):
            await self.state.reset_password(self.form)
        self.assertIn('diferente da atual', self.state.reset_message)
        self.assertNotIn('Código inválido', self.state.reset_message)
        self.assertEqual(self.state._token(), '')

    async def test_expired_reset_authorization_is_not_reported_as_wrong_code(self):
        mock = AsyncMock(side_effect=[{'authToken': 'reset'}, APIError('Expired', 401)])
        with patch('Codeboxd_main.state.session.request', new=mock):
            await self.state.reset_password(self.form)
        self.assertIn('autorização de recuperação', self.state.reset_message)
        self.assertNotIn('Código inválido', self.state.reset_message)

    async def test_success_clears_only_session_of_recovered_account(self):
        for recovered, expected_user in ((7, 0), (8, 7)):
            self.state.reset_completed = False
            self.state.user_id = 7
            self.state.auth_token = 'existing-session'
            mock = AsyncMock(side_effect=[{'authToken': 'reset', 'user_id': recovered}, {}])
            with patch('Codeboxd_main.state.session.request', new=mock):
                await self.state.reset_password(self.form)
            self.assertEqual(self.state.user_id, expected_user)
            self.assertEqual(self.state._token(), '' if expected_user == 0 else 'existing-session')

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

    async def test_repeated_submit_after_success_preserves_confirmation(self):
        mock = AsyncMock(side_effect=[{'authToken': 'temporary-reset'}, {'message': {'success': True}}])
        with patch('Codeboxd_main.state.session.request', new=mock):
            await self.state.reset_password(self.form)
            confirmation = self.state.reset_message
            await self.state.reset_password(self.form)
        self.assertEqual(mock.await_count, 2)
        self.assertTrue(self.state.reset_completed)
        self.assertTrue(self.state.reset_success)
        self.assertEqual(self.state.reset_message, confirmation)

    async def test_new_request_starts_another_recovery_after_completion(self):
        self.state.reset_completed = True
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={})) as request:
            await self.state.request_password_reset({'email': 'member@example.com'})
        request.assert_awaited_once()
        self.assertFalse(self.state.reset_completed)

    async def test_progressive_form_uses_requested_email_without_second_field(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={})):
            await self.state.request_password_reset({'email': 'Member@Example.com'})
        self.assertTrue(self.state.reset_code_requested)
        self.assertEqual(self.state.reset_email, 'member@example.com')
        mock = AsyncMock(side_effect=[{'authToken': 'temporary-reset'}, {}])
        with patch('Codeboxd_main.state.session.request', new=mock):
            await self.state.reset_password({k: v for k, v in self.form.items() if k != 'email'})
        self.assertEqual(mock.await_args_list[0].kwargs['data']['email'], 'member@example.com')
        self.assertTrue(self.state.reset_completed)

    async def test_change_email_returns_to_initial_step_without_request(self):
        self.state.reset_email = 'member@example.com'
        self.state.reset_code_requested = True
        self.state.reset_message = 'previous message'
        with patch('Codeboxd_main.state.session.request', new=AsyncMock()) as request:
            self.state.change_reset_email()
        request.assert_not_awaited()
        self.assertFalse(self.state.reset_code_requested)
        self.assertEqual(self.state.reset_message, '')

    async def test_resend_keeps_email_and_failure_keeps_current_step(self):
        self.state.reset_email = 'member@example.com'
        self.state.reset_code_requested = True
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(side_effect=APIError('Unavailable', 503))) as request:
            await self.state.resend_reset_code()
        self.assertEqual(request.await_args.kwargs['params'], {'email': 'member@example.com'})
        self.assertTrue(self.state.reset_code_requested)
        self.assertFalse(self.state.reset_success)

    async def test_request_publishes_loading_before_waiting_for_network(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={})) as request:
            event = self.state.submit_password_reset({'email': 'member@example.com'})
            await anext(event)
            self.assertTrue(self.state.reset_sending)
            request.assert_not_awaited()
            duplicate = self.state.submit_password_reset({'email': 'member@example.com'})
            with self.assertRaises(StopAsyncIteration):
                await anext(duplicate)
            with self.assertRaises(StopAsyncIteration):
                await anext(event)
        request.assert_awaited_once()
        self.assertFalse(self.state.reset_sending)

    async def test_successful_request_blocks_immediate_resend_without_network(self):
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={})) as request:
            await self.state.request_password_reset({'email': 'member@example.com'})
            await self.state.resend_reset_code()
        request.assert_awaited_once()
        self.assertIn('segundos', self.state.reset_message)
        self.assertTrue(self.state.reset_code_requested)
