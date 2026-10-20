import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services import catalog
from Codeboxd_main.state.social import SocialState


class ReviewIdentityTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.user_id = 1
        self.state._identity = 1
        self.state._selected_raw = catalog.media('tmdb', 'movie', '222', 'Segunda obra')

    async def test_unfiltered_media_response_uses_only_exact_identity(self):
        response = [{'id': 1, 'identity_key': 'openlibrary:book:OL1W'},
                    {'id': 7, 'identity_key': 'tmdb:movie:111'},
                    {'id': 8, 'identity_key': 'tmdb:movie:222'}]
        interactions = [{'media_id': 7, 'status': 'completed', 'rating': 5, 'review': 'Primeiro filme'},
                        {'media_id': 8, 'status': 'completed', 'rating': 3, 'review': 'Segundo filme'}]
        with patch.object(SocialState, '_call', new=AsyncMock(side_effect=[response, interactions])):
            await self.state._load_external_interaction(True)
        self.assertEqual(self.state._selected_raw['id'], 8)
        self.assertEqual(self.state.selected_review, 'Segundo filme')
        self.assertEqual(self.state.selected_rating, '3')

    async def test_no_match_does_not_reuse_previous_review_or_assign_another_id(self):
        self.state.selected_review = 'Crítica de outra obra'
        self.state.interaction_saved = True
        self.state.review_editor_open = False
        with patch.object(SocialState, '_call', new=AsyncMock(return_value=[
                {'id': 7, 'identity_key': 'tmdb:movie:111'}])) as call:
            await self.state._load_external_interaction(True)
        call.assert_awaited_once()
        self.assertEqual(self.state._selected_raw['id'], 0)
        self.assertEqual(self.state.selected_review, '')
        self.assertEqual(self.state.selected_rating, '0')
        self.assertFalse(self.state.interaction_saved)
        self.assertTrue(self.state.review_editor_open)

    async def test_internal_media_without_review_does_not_keep_previous_one(self):
        self.state.selected_review = 'Crítica anterior'
        self.state.selected_rating = '5'
        with patch.object(SocialState, '_call', new=AsyncMock(return_value=[
                {'media_id': 7, 'status': 'completed', 'rating': 5, 'review': 'Outra obra'}])):
            await self.state._load_personal_interaction('8', True)
        self.assertEqual(self.state.selected_review, '')
        self.assertEqual(self.state.selected_rating, '0')

    async def test_old_form_cannot_write_to_current_movie(self):
        with patch.object(SocialState, '_call', new=AsyncMock()) as call, \
                patch.object(SocialState, '_require_user', new=AsyncMock()) as auth:
            await self.state.save_interaction({'media_key': 'tmdb:movie:111', 'rating': '5', 'review': 'Antiga'})
        call.assert_not_awaited()
        auth.assert_not_awaited()
        self.assertIn('A obra mudou', self.state.notice)

    async def test_wrong_cached_internal_id_is_replaced_before_saving(self):
        self.state._selected_raw['id'] = 7
        correct = dict(self.state._selected_raw, id=8)
        with patch.object(SocialState, '_call', new=AsyncMock(side_effect=[
                {'id': 7, 'identity_key': 'tmdb:movie:111'}, correct])) as call:
            mid = await self.state._persist_selected()
        self.assertEqual(mid, 8)
        self.assertEqual(call.await_args_list[0].args, ('GET', '/media/7'))
        self.assertEqual(call.await_args_list[1].args[0:2], ('POST', '/media'))
        self.assertEqual(call.await_args_list[1].args[2]['external_id'], '222')
