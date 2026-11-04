"""Administrative confirmations stay bound to the submitted form and session."""
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.admin import AdminState


class AdminActionContextTests(unittest.IsolatedAsyncioTestCase):
    CASES = (
        ('users', 'confirm_user_status_change', 'user_action', {
            'user_action_id': '22', 'user_action_status': 'disabled',
            'user_action_reason': 'Confirmed reason'}),
        ('catalog', 'save_catalog_edit', 'catalog_edit', {
            'catalog_edit_id': '42', 'catalog_edit_title': 'Original title',
            'catalog_edit_description': 'Original description',
            'catalog_edit_cover': '', 'catalog_edit_year': '2016'}),
        ('reports', 'save_report_review', 'report_review', {
            'report_review_id': '5', 'report_review_status': 'resolved',
            'report_review_decision': 'Confirmed decision'}),
    )

    def prepare(self, fields):
        state = rx.State(_reflex_internal_init=True).get_substate(
            AdminState.get_full_name().split('.'))
        state.session_token = 'original-admin-token'
        for name, value in fields.items():
            setattr(state, name, value)
        return state

    async def test_changed_target_during_authorization_cancels_write(self):
        for section, event, prefix, fields in self.CASES:
            with self.subTest(section=section):
                state = self.prepare(fields)

                async def authorize(*args, **kwargs):
                    setattr(state, prefix + '_id', '999')
                    return {'id': 1, 'role': 'admin'}

                with patch('Codeboxd_main.state.session.request', side_effect=authorize), patch(
                    'Codeboxd_main.state.admin.request', new=AsyncMock()) as request:
                    _ = [item async for item in getattr(state, event)()]
                request.assert_not_awaited()
                self.assertEqual(getattr(state, prefix + '_id'), '999')
                self.assertFalse(getattr(state, prefix + '_loading'))

    async def test_each_changed_form_field_cancels_write(self):
        for section, event, prefix, fields in self.CASES:
            for name in fields:
                with self.subTest(section=section, field=name):
                    state = self.prepare(fields)
                    generator = getattr(state, event)()
                    await anext(generator)
                    setattr(state, name, 'Changed after confirmation')
                    with patch('Codeboxd_main.state.session.request', new=AsyncMock(
                        return_value={'id': 1, 'role': 'admin'})), patch(
                        'Codeboxd_main.state.admin.request', new=AsyncMock()) as request:
                        _ = [item async for item in generator]
                    request.assert_not_awaited()
                    self.assertFalse(getattr(state, prefix + '_loading'))

    async def test_new_session_during_authorization_cancels_write(self):
        for section, event, prefix, fields in self.CASES:
            with self.subTest(section=section):
                state = self.prepare(fields)

                async def authorize(*args, **kwargs):
                    state.session_token = 'new-admin-token'
                    return {'id': 1, 'role': 'admin'}

                with patch('Codeboxd_main.state.session.request', side_effect=authorize), patch(
                    'Codeboxd_main.state.admin.request', new=AsyncMock()) as request:
                    _ = [item async for item in getattr(state, event)()]
                request.assert_not_awaited()
                self.assertEqual(state.session_token, 'new-admin-token')
                self.assertFalse(getattr(state, prefix + '_loading'))

    async def test_late_write_success_preserves_new_editor(self):
        for section, event, prefix, fields in self.CASES:
            with self.subTest(section=section):
                state = self.prepare(fields)

                async def write(*args, **kwargs):
                    setattr(state, prefix + '_id', '999')
                    return {'success': True}

                with patch('Codeboxd_main.state.session.request', new=AsyncMock(
                    return_value={'id': 1, 'role': 'admin'})), patch(
                    'Codeboxd_main.state.admin.request', side_effect=write) as request:
                    _ = [item async for item in getattr(state, event)()]
                self.assertEqual(request.await_count, 1)
                self.assertEqual(request.await_args.kwargs['token'], 'original-admin-token')
                self.assertEqual(getattr(state, prefix + '_id'), '999')
                self.assertEqual(getattr(state, section + '_notice'), '')
                self.assertFalse(getattr(state, prefix + '_loading'))

    async def test_late_write_error_does_not_clear_new_session_or_redirect(self):
        for section, event, prefix, fields in self.CASES:
            for status in (401, 403, 503):
                with self.subTest(section=section, status=status):
                    state = self.prepare(fields)

                    async def write(*args, **kwargs):
                        state.session_token = 'new-admin-token'
                        raise APIError('Old request failed', status)

                    with patch('Codeboxd_main.state.session.request', new=AsyncMock(
                        return_value={'id': 1, 'role': 'admin'})), patch(
                        'Codeboxd_main.state.admin.request', side_effect=write) as request:
                        events = [item async for item in getattr(state, event)()]
                    self.assertFalse(any(item is not None for item in events))
                    request.assert_awaited_once()
                    self.assertEqual(state.session_token, 'new-admin-token')
                    self.assertEqual(getattr(state, section + '_error'), '')
                    self.assertEqual(getattr(state, prefix + '_id'), fields[prefix + '_id'])
                    self.assertFalse(getattr(state, prefix + '_loading'))

    async def test_current_write_error_preserves_draft_and_displays_error(self):
        for section, event, prefix, fields in self.CASES:
            with self.subTest(section=section):
                state = self.prepare(fields)
                with patch('Codeboxd_main.state.session.request', new=AsyncMock(
                    return_value={'id': 1, 'role': 'admin'})), patch(
                    'Codeboxd_main.state.admin.request', new=AsyncMock(
                        side_effect=APIError('Temporary failure', 503))) as request:
                    _ = [item async for item in getattr(state, event)()]
                request.assert_awaited_once()
                self.assertEqual(getattr(state, section + '_error'), 'Temporary failure')
                for name, value in fields.items():
                    self.assertEqual(getattr(state, name), value)
                self.assertFalse(getattr(state, prefix + '_loading'))

    async def test_refresh_error_after_success_remains_visible(self):
        for section, event, prefix, fields in self.CASES:
            with self.subTest(section=section):
                state = self.prepare(fields)
                with patch('Codeboxd_main.state.session.request', new=AsyncMock(
                    return_value={'id': 1, 'role': 'admin'})), patch(
                    'Codeboxd_main.state.admin.request', new=AsyncMock(
                        side_effect=[None, APIError('Refresh failed', 503)])) as request:
                    _ = [item async for item in getattr(state, event)()]
                self.assertEqual(request.await_count, 2)
                self.assertEqual(getattr(state, section + '_error'), 'Refresh failed')
                self.assertTrue(getattr(state, section + '_notice'))
                self.assertEqual(getattr(state, prefix + '_id'), '')

    async def test_expired_current_session_still_redirects(self):
        for section, event, prefix, fields in self.CASES:
            with self.subTest(section=section):
                state = self.prepare(fields)
                with patch('Codeboxd_main.state.session.request', new=AsyncMock(
                    side_effect=APIError('Expired', 401))), patch(
                    'Codeboxd_main.state.admin.request', new=AsyncMock()) as request:
                    events = [item async for item in getattr(state, event)()]
                request.assert_not_awaited()
                self.assertTrue(any(item is not None for item in events))
                self.assertEqual(state.session_token, '')
                self.assertFalse(getattr(state, prefix + '_loading'))
