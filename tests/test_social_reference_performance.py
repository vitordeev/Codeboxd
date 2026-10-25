import asyncio
from copy import deepcopy
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState, present_media


class SocialReferencePerformanceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.router.url.path = '/conta'
        self.state.user_id = 7
        self.state._identity = 7
        self.state.session_token = 'offline-fixture'
        self.profile = dict(profile=dict(user_id=7, username='reader', display_name='Reader'),
                            interactions=[], followers=[dict(follower_id=8)],
                            following=[dict(followed_id=8)])
        self.media = [dict(id=i+1, title=f'Book {i+1}', media_type='book',
                           description='Synopsis', identity_key=f'fixture:book:{i+1}')
                      for i in range(250)]

    async def test_feed_keeps_raw_references_editor_and_suggestions_without_catalog_cards(self):
        self.state.router.url.path = '/feed'
        previous_catalog = [present_media(self.media[0])]
        self.state.catalog_items = deepcopy(previous_catalog)

        async def call(method, path, **kwargs):
            self.assertEqual(method, 'GET')
            return {'/media': self.media,
                    '/profiles': [dict(user_id=8, display_name='Friend')],
                    '/feed': [dict(id=3, user_id=8, media_id=250, body='Post', created_at=0)],
                    '/posts': [], '/likes': []}[path]

        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
             patch.object(SocialState, '_call', side_effect=call), \
             patch('Codeboxd_main.state.social.present_media', wraps=present_media) as transform:
            await self.state.load_feed()
            transform.assert_not_called()
            self.assertEqual(len(self.state._media), 250)
            self.assertEqual(self.state.catalog_items, previous_catalog)
            self.assertEqual(self.state.posts[0]['media_title'], 'Book 250')
            self.assertEqual(self.state.posts[0]['author'], 'Friend')
            self.assertEqual(self.state.suggested_people[0]['display_name'], 'Friend')
            # Editing still obtains the original full media reference.
            self.state.posts[0]['user_id'] = '7'
            self.state.edit_post('3')
            self.assertEqual(self.state._post_media_raw['id'], 250)
            self.assertEqual(self.state.post_media_selected['title'], 'Book 250')

    async def test_default_media_loader_still_prepares_catalog_and_preserves_page_size(self):
        with patch.object(SocialState, '_call', new=AsyncMock(return_value=self.media)) as call:
            await self.state._load_media(per_page=20)
        call.assert_awaited_once_with('GET', '/media', params={'per_page': 20})
        self.assertEqual(self.state.catalog_items, [present_media(m) for m in self.media])

    async def test_feed_reference_mode_ignores_another_routes_late_catalog(self):
        started, release = asyncio.Event(), asyncio.Event()

        async def call(*args, **kwargs):
            started.set()
            await release.wait()
            return self.media

        with patch.object(SocialState, '_call', side_effect=call):
            pending = asyncio.create_task(self.state._load_media(prepare_catalog=False))
            await started.wait()
            self.state.router.url.path = '/listas'
            self.state._media = {'999': {'id': 999}}
            self.state.catalog_items = [{'id': '999'}]
            release.set()
            await pending
        self.assertEqual(self.state._media, {'999': {'id': 999}})
        self.assertEqual(self.state.catalog_items, [{'id': '999'}])

    async def test_empty_profile_keeps_counts_people_and_existing_media_without_catalog_request(self):
        self.state._media = {'999': {'id': 999}}

        async def call(method, path, **kwargs):
            if path == '/profiles/7':
                return self.profile
            self.assertEqual(path, '/profiles')
            return [dict(user_id=8, display_name='Friend')]

        with patch.object(SocialState, '_validate_navigation_session', new=AsyncMock(return_value=True)), \
             patch.object(SocialState, '_call', side_effect=call) as calls:
            updates = self.state._profile_updates()
            await anext(updates)
            self.assertFalse(self.state.profile_activity_loading)
            self.assertEqual(self.state.profile_activity, [])
            async for _ in updates:
                pass
        self.assertEqual(calls.await_count, 2)
        self.assertEqual(self.state._media, {'999': {'id': 999}})
        self.assertEqual(self.state.profile_counts, dict(followers=1, following=1, activities=0))
        self.assertEqual(self.state.followers[0]['display_name'], 'Friend')
        self.assertEqual(self.state.following_ids, ['8'])
        self.assertFalse(self.state.profile_people_loading)
        self.assertEqual(self.state.profile_activity_error, '')

    async def test_other_empty_profile_keeps_current_members_following_state(self):
        self.state.router.url.path = '/perfil/8'

        async def call(method, path, **kwargs):
            if path == '/profiles/8':
                return dict(self.profile, profile=dict(user_id=8, username='friend'))
            if path == '/profiles/7':
                return self.profile
            self.assertEqual(path, '/profiles')
            return [dict(user_id=8, display_name='Friend')]

        with patch.object(SocialState, '_validate_navigation_session', new=AsyncMock(return_value=True)), \
             patch.object(SocialState, '_call', side_effect=call) as calls:
            await self.state.load_profile()
        self.assertEqual(calls.await_count, 3)
        self.assertEqual(self.state.profile['user_id'], '8')
        self.assertEqual(self.state.following_ids, ['8'])

    async def test_guest_empty_profile_does_not_request_own_profile_or_media(self):
        self.state.router.url.path = '/perfil/7'
        self.state.user_id = 0
        self.state.session_token = ''

        async def call(method, path, **kwargs):
            return self.profile if path == '/profiles/7' else []

        with patch.object(SocialState, '_validate_navigation_session', new=AsyncMock(return_value=False)), \
             patch.object(SocialState, '_call', side_effect=call) as calls:
            await self.state.load_profile()
        self.assertEqual([call.args[1] for call in calls.await_args_list], ['/profiles/7', '/profiles'])
        self.assertEqual(self.state.following_ids, [])
        self.assertFalse(self.state.profile_activity_loading)

    async def test_empty_profile_people_failure_does_not_create_activity_error(self):
        async def call(method, path, **kwargs):
            if path == '/profiles/7':
                return self.profile
            self.assertEqual(path, '/profiles')
            raise APIError('People unavailable', 503)

        with patch.object(SocialState, '_validate_navigation_session', new=AsyncMock(return_value=True)), \
             patch.object(SocialState, '_call', side_effect=call):
            await self.state.load_profile()
        self.assertEqual(self.state.profile['username'], 'reader')
        self.assertEqual(self.state.profile_counts['activities'], 0)
        self.assertEqual(self.state.profile_activity_error, '')
        self.assertEqual(self.state.profile_people_error, 'People unavailable')
        self.assertFalse(self.state.profile_activity_loading)
        self.assertFalse(self.state.profile_people_loading)
