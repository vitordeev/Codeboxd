import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.state.social import SocialState


class PersonalListsTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.s = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.s.router.url.path = '/listas'
        self.s.user_id = self.s._identity = 7
        self.s.session_token = 'fictional-a'
        self.records = [dict(id=1, user_id=7, title='Quero ver / ler', is_public=True),
                        dict(id=2, user_id=7, title='Já assisti / li', is_public=True),
                        dict(id=3, user_id=7, title='Minha coleção', is_public=False),
                        dict(id=4, user_id=8, title='Quero ver / ler', is_public=True)]

    def patches(self, call):
        from contextlib import ExitStack
        stack = ExitStack()
        stack.enter_context(patch.object(SocialState, '_validate_navigation_session', new=AsyncMock()))
        stack.enter_context(patch.object(SocialState, '_ensure_default_lists', new=AsyncMock()))
        stack.enter_context(patch.object(SocialState, '_call', side_effect=call))
        return stack

    async def test_personal_collection_preserves_private_custom_lists_and_excludes_other_owners(self):
        calls = []
        async def call(method, path, **kwargs):
            calls.append(path)
            return self.records
        with self.patches(call):
            await self.s.load_lists(refresh_media=False)
        self.assertEqual([x['id'] for x in self.s.lists], ['1', '2', '3'])
        self.assertEqual(calls, ['/lists'])

    async def test_public_discovery_and_foreign_items_use_public_routes(self):
        calls = []
        async def call(method, path, **kwargs):
            calls.append(path)
            return self.records if path == '/lists/public' else []
        with self.patches(call):
            await self.s.change_list_scope('public')
            self.assertEqual([x['id'] for x in self.s.lists], ['1', '2', '4'])
            await self.s.open_list('4')
        self.assertFalse(self.s.owns_list)
        self.assertEqual(calls, ['/lists/public', '/profiles', '/lists/public/4/items'])

    async def test_visitor_gets_only_public_discovery(self):
        self.s.user_id = 0
        self.s.session_token = ''
        async def call(*args, **kwargs): return self.records
        with self.patches(call):
            await self.s.load_lists(refresh_media=False)
        self.assertEqual([x['id'] for x in self.s.lists], ['1', '2', '4'])

    async def test_normal_entry_returns_to_personal_collection_after_discovery(self):
        self.s.list_scope = 'public'
        async def call(*args, **kwargs): return self.records
        with self.patches(call), patch.object(SocialState, '_load_media', new=AsyncMock()):
            await self.s.load_lists()
        self.assertEqual(self.s.list_scope, 'own')
        self.assertEqual([x['id'] for x in self.s.lists], ['1', '2', '3'])

    async def test_public_lists_group_under_correct_author_with_one_profile_lookup(self):
        calls = []
        records = [self.records[0], self.records[3], self.records[1]]
        profiles = [dict(user_id=7, display_name='Ana', avatar_url='https://example.org/ana.png'),
                    dict(user_id=8, display_name='Bruno', avatar_url='https://example.org/bruno.png')]
        async def call(method, path, **kwargs):
            calls.append(path)
            return profiles if path == '/profiles' else records
        with self.patches(call):
            await self.s.change_list_scope('public')
        groups = self.s.public_list_groups
        self.assertEqual([g['display_name'] for g in groups], ['Ana', 'Bruno'])
        self.assertEqual([[i['id'] for i in g['lists']] for g in groups], [['1', '2'], ['4']])
        self.assertEqual(groups[0]['avatar_url'], profiles[0]['avatar_url'])
        self.assertEqual(calls, ['/lists/public', '/profiles'])

    async def test_missing_or_failed_profile_preserves_public_lists_with_neutral_fallback(self):
        from Codeboxd_main.services.api import APIError
        for failed in (False, True):
            with self.subTest(failed=failed):
                async def call(method, path, **kwargs):
                    if path == '/profiles':
                        if failed: raise APIError('Unavailable', 503)
                        return []
                    return [self.records[3]]
                with self.patches(call):
                    await self.s.change_list_scope('public')
                group = self.s.public_list_groups[0]
                self.assertEqual(group['user_id'], '8')
                self.assertEqual(group['display_name'], 'Usuário')
                self.assertEqual(group['avatar_url'], '')
                self.assertEqual([i['id'] for i in group['lists']], ['4'])

    async def test_late_account_or_scope_response_is_ignored(self):
        for change in ('account', 'scope'):
            with self.subTest(change=change):
                self.setUp()
                started, release = asyncio.Event(), asyncio.Event()
                async def call(*args, **kwargs):
                    started.set()
                    await release.wait()
                    return self.records
                with self.patches(call):
                    pending = asyncio.create_task(self.s.load_lists(refresh_media=False))
                    await started.wait()
                    if change == 'account':
                        self.s.user_id = 8
                        self.s.session_token = 'fictional-b'
                    else:
                        self.s.list_scope = 'public'
                    self.s.lists = [{'id': 'current'}]
                    release.set()
                    await pending
                self.assertEqual(self.s.lists, [{'id': 'current'}])
