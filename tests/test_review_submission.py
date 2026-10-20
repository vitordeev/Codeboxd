import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class ReviewSubmissionTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.user_id = 1
        self.state._identity = 1
        self.state._selected_raw = {'id': 7}
        self.form = {'status': 'completed', 'rating': '4,5', 'review': 'Minha crítica', 'spoiler': 'on'}

    async def test_one_hundred_identical_submissions_write_once_and_close_form(self):
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)) as auth, \
                patch.object(SocialState, '_call', new=AsyncMock(return_value={})) as call:
            for _ in range(100):
                await self.state.save_interaction(self.form)
        auth.assert_awaited_once()
        call.assert_awaited_once()
        self.assertTrue(self.state.interaction_saved)
        self.assertFalse(self.state.review_editor_open)
        self.assertFalse(self.state.interaction_saving)
        self.assertEqual(self.state.selected_rating, '4.5')
        self.assertEqual(self.state.selected_review, 'Minha crítica')

    async def test_concurrent_submissions_do_not_make_extra_requests(self):
        entered, release = asyncio.Event(), asyncio.Event()
        async def write(*args, **kwargs):
            entered.set()
            await release.wait()
            return {}
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', side_effect=write) as call:
            first = asyncio.create_task(self.state.save_interaction(self.form))
            try:
                await entered.wait()
                await asyncio.gather(*(self.state.save_interaction(self.form) for _ in range(99)))
                call.assert_awaited_once()
                self.assertTrue(self.state.interaction_saving)
            finally:
                release.set()
                await first

    async def test_submit_yields_disabled_state_before_network_and_failure_allows_retry(self):
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock(side_effect=APIError('Falha temporária', 503))) as call:
            sending = self.state.submit_interaction(self.form)
            await anext(sending)
            self.assertTrue(self.state.interaction_saving)
            call.assert_not_awaited()
            async for _ in sending:
                pass
        self.assertFalse(self.state.interaction_saving)
        self.assertFalse(self.state.interaction_saved)
        self.assertTrue(self.state.review_editor_open)
        self.assertEqual(self.state.selected_review, 'Minha crítica')
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock(return_value={})) as call:
            await self.state.save_interaction(self.form)
        call.assert_awaited_once()
        self.assertTrue(self.state.interaction_saved)

    async def test_explicit_edit_updates_same_media_and_identity_reset_clears_saved_state(self):
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock(return_value={})) as call:
            await self.state.save_interaction(self.form)
            self.state.edit_interaction()
            self.assertTrue(self.state.review_editor_open)
            await self.state.save_interaction(dict(self.form, rating='5', review='Atualizada'))
        self.assertEqual(call.await_count, 2)
        self.assertTrue(all(c.args[:2] == ('PUT', '/interactions') for c in call.await_args_list))
        self.assertTrue(all(c.args[2]['media_id'] == 7 for c in call.await_args_list))
        self.state._reset_personal()
        self.assertFalse(self.state._saved_interaction)
        self.assertFalse(self.state.interaction_saved)

    async def test_restored_review_is_closed_and_identical_resubmit_does_not_write(self):
        interaction = dict(media_id=7, status='completed', rating=4.5, review='Minha crítica', spoiler=True)
        with patch.object(SocialState, '_call', new=AsyncMock(return_value=[interaction])):
            await self.state._load_personal_interaction('7', True)
        self.assertFalse(self.state.review_editor_open)
        with patch.object(SocialState, '_call', new=AsyncMock()) as call, \
                patch.object(SocialState, '_require_user', new=AsyncMock()) as auth:
            await self.state.save_interaction(self.form)
        call.assert_not_awaited()
        auth.assert_not_awaited()

    async def test_external_media_restores_existing_review_without_creating_records(self):
        self.state._selected_raw = {'id': 0, 'identity_key': 'tmdb:movie:42'}
        interaction = dict(media_id=7, status='completed', rating=4.5, review='Minha crítica', spoiler=True)
        with patch.object(SocialState, '_call', new=AsyncMock(side_effect=[[
                {'id': 7, 'identity_key': 'tmdb:movie:42'}], [interaction]])) as call:
            await self.state._load_external_interaction(True)
        self.assertEqual(self.state._selected_raw['id'], 7)
        self.assertFalse(self.state.review_editor_open)
        self.assertTrue(all(c.args[0] == 'GET' for c in call.await_args_list))

    async def test_cancelled_submission_releases_busy_flag(self):
        sending = self.state.submit_interaction(self.form)
        await anext(sending)
        self.assertTrue(self.state.interaction_saving)
        await sending.aclose()
        self.assertFalse(self.state.interaction_saving)
