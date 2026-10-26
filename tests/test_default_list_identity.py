import asyncio
import os
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class DefaultListIdentityTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.s = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.s.user_id = 7
        self.s.session_token = 'fictional-session'
        self.s.router.url.path = '/listas'
        self.records = [dict(id=1, user_id=7, default_key='7:planned', title='Renomeada', is_public=False),
                        dict(id=2, user_id=7, default_key='7:completed', title='Terminadas', is_public=True)]
        self.env = patch.dict(os.environ, {'DEFAULT_LIST_IDENTITY_ENABLED': 'true'})
        self.env.start()
        self.addCleanup(self.env.stop)

    async def test_renamed_private_defaults_are_reused_without_overwrite(self):
        with patch.object(SocialState, '_call', new=AsyncMock(return_value=self.records)) as call:
            await self.s._ensure_default_lists()
        call.assert_awaited_once_with('GET', '/lists')
        self.assertEqual([row['id'] for row in self.s.quick_lists], ['1', '2'])
        self.assertEqual(self.records[0]['title'], 'Renomeada')
        self.assertFalse(self.records[0]['is_public'])

    async def test_custom_homonym_does_not_impersonate_default(self):
        custom = dict(id=10, user_id=7, title='Quero ver / ler', default_key=None, is_public=False)
        with patch.object(SocialState, '_call', new=AsyncMock(
                side_effect=[[custom, self.records[1]], self.records[0]])) as call:
            await self.s._ensure_default_lists()
        self.assertEqual(call.await_args_list[1].args[2]['default_kind'], 'planned')
        self.assertNotIn('10', [row['id'] for row in self.s.quick_lists])
        self.assertIsNone(custom['default_key'])

    async def test_defaults_after_first_page_are_reused_without_creation(self):
        page = [dict(id=100+i, user_id=7, title=f'Custom {i}') for i in range(100)]
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(
                side_effect=[page, self.records])) as request:
            await self.s._ensure_default_lists()
        self.assertEqual(request.await_count, 2)
        self.assertTrue(all(call.args[0] == 'GET' for call in request.await_args_list))
        self.assertEqual(request.await_args_list[1].kwargs['params'], {'page':2, 'per_page':100})
        self.assertEqual([row['id'] for row in self.s.quick_lists], ['1', '2'])

    async def test_failed_creation_is_not_retried_or_published(self):
        with patch.object(SocialState, '_call', new=AsyncMock(
                side_effect=[[], APIError('Unavailable', 503)])) as call:
            with self.assertRaises(APIError): await self.s._ensure_default_lists()
        self.assertEqual(call.await_count, 2)
        self.assertEqual(self.s.quick_lists, [])

    async def test_account_change_during_creation_cannot_publish_old_lists(self):
        started, release = asyncio.Event(), asyncio.Event()
        async def call(method, *args, **kwargs):
            if method == 'GET': return []
            started.set()
            await release.wait()
            return self.records[0]
        with patch.object(SocialState, '_call', side_effect=call):
            pending = asyncio.create_task(self.s._ensure_default_lists())
            await started.wait()
            self.s.user_id = 8
            self.s.quick_lists = [dict(id='new', title='Outra conta')]
            release.set()
            with self.assertRaises(APIError): await pending
        self.assertEqual(self.s.quick_lists[0]['id'], 'new')

    async def test_ambiguous_identity_and_invalid_server_owner_are_rejected(self):
        for responses in ([self.records + [self.records[0]]],
                          [[], dict(self.records[0], user_id=8)]):
            with self.subTest(responses=len(responses)):
                with patch.object(SocialState, '_call', new=AsyncMock(side_effect=responses)):
                    with self.assertRaises(APIError): await self.s._ensure_default_lists()
