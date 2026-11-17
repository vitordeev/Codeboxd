import asyncio
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState

ROOT = Path(__file__).resolve().parents[1]


class AddressableListTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(
            SocialState.get_full_name().split('.'))
        self.state.router.url.path = '/lista'
        self.state.router.url.query_parameters = {'id': '84', 'page': '1'}
        self.state._media = {'9': {
            'id': 9, 'title': 'Obra de teste', 'media_type': 'movie',
            'external_source': 'tmdb', 'external_id': '9',
        }}

    async def load(self):
        async for _ in self.state.load_addressable_list():
            pass

    @staticmethod
    def public_record():
        return {
            'id': 84, 'user_id': 7, 'title': 'Lista pública',
            'description': 'Descrição pública.', 'is_public': True,
            'creator': {
                'user_id': 7, 'username': 'joana', 'display_name': 'Joana',
                'avatar_url': '',
            },
        }

    async def test_direct_public_detail_loads_only_summary_and_requested_items_page(self):
        self.state.router.url.query_parameters = {'id': '84', 'page': '2'}
        calls = []

        async def request(method, path, **kwargs):
            calls.append((method, path, kwargs.get('params') or {}))
            if path == '/lists/public/84':
                return self.public_record()
            if path == '/lists/public/84/items':
                return [{'id': 21, 'list_id': 84, 'media_id': 9}]
            raise AssertionError(f'unexpected_request:{path}')

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)), \
             patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(return_value=True)):
            await self.load()

        self.assertEqual([call[1] for call in calls], [
            '/lists/public/84', '/lists/public/84/items'])
        self.assertEqual(calls[1][2], {'page': 2, 'per_page': 20})
        self.assertEqual(self.state.selected_list['title'], 'Lista pública')
        self.assertEqual(self.state.list_detail_creator['user_id'], '7')
        self.assertEqual(self.state.list_detail_page, 2)
        self.assertEqual(self.state.list_items[0]['title'], 'Obra de teste')
        self.assertFalse(self.state.list_detail_has_more)
        self.assertEqual(self.state.list_detail_error, '')

    async def test_visitor_detail_load_survives_personal_state_reset_during_validation(self):
        async def request(method, path, **kwargs):
            if path == '/lists/public/84':
                return self.public_record()
            if path == '/lists/public/84/items':
                return []
            raise AssertionError(f'unexpected_request:{path}')

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)) as api:
            await self.load()

        self.assertEqual([call.args[1] for call in api.await_args_list], [
            '/lists/public/84', '/lists/public/84/items'])
        self.assertEqual(self.state.selected_list['title'], 'Lista pública')
        self.assertFalse(self.state.list_detail_loading)

    async def test_detail_load_survives_trailing_slash_normalization(self):
        calls = []

        async def request(method, path, **kwargs):
            calls.append(path)
            if path == '/lists/public/84':
                return self.public_record()
            if path == '/lists/public/84/items':
                return []
            raise AssertionError(f'unexpected_request:{path}')

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)), \
             patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(return_value=True)):
            stream = self.state.load_addressable_list()
            await anext(stream)
            self.state.router.url.path = '/lista/'
            async for _ in stream:
                pass

        self.assertEqual(calls, ['/lists/public/84', '/lists/public/84/items'])
        self.assertEqual(self.state.selected_list['title'], 'Lista pública')

    async def test_query_change_discards_delayed_detail_response(self):
        gate = asyncio.Event()

        async def request(method, path, **kwargs):
            if path == '/lists/public/84':
                await gate.wait()
                return self.public_record()
            raise AssertionError(f'unexpected_request:{path}')

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)), \
             patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(return_value=True)):
            task = asyncio.create_task(self.load())
            await asyncio.sleep(0)
            self.state.router.url.query_parameters = {'id': '85', 'page': '1'}
            gate.set()
            await task

        self.assertEqual(self.state.selected_list['id'], '')
        self.assertEqual(self.state.list_items, [])
        self.assertFalse(self.state.list_detail_loading)

    async def test_session_validation_error_clears_previous_detail(self):
        self.state.selected_list = {
            'id': '83', 'title': 'Lista anterior', 'description': 'Privada',
            'user_id': '6', 'is_public': 'False',
        }
        self.state.list_items = [{'id': '1', 'title': 'Obra privada'}]

        with patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(side_effect=APIError('Sessão indisponível.', 503))):
            await self.load()

        self.assertEqual(self.state.selected_list['id'], '')
        self.assertEqual(self.state.list_items, [])
        self.assertEqual(self.state.list_detail_error, 'Sessão indisponível.')
        self.assertFalse(self.state.list_detail_loading)

    async def test_private_list_is_available_only_through_authenticated_owner_contract(self):
        self.state.user_id = 7
        self.state.session_token = 'fixture-session'
        calls = []

        async def request(method, path, **kwargs):
            calls.append(path)
            if path == '/lists/public/84':
                raise APIError('Registro não encontrado.', 404)
            if path == '/lists/84':
                record = self.public_record()
                record['is_public'] = False
                return record
            if path == '/lists/84/items':
                return []
            raise AssertionError(f'unexpected_request:{path}')

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)), \
             patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(return_value=True)):
            await self.load()

        self.assertEqual(calls, ['/lists/public/84', '/lists/84', '/lists/84/items'])
        self.assertTrue(self.state.owns_list)
        self.assertEqual(self.state.selected_list['is_public'], 'False')
        self.assertEqual(self.state.selected_list['title'], 'Lista pública')

    async def test_private_or_missing_list_from_another_account_has_no_metadata(self):
        self.state.user_id = 8
        self.state.session_token = 'other-session'

        async def request(method, path, **kwargs):
            raise APIError('Registro não encontrado.', 404)

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)), \
             patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(return_value=True)):
            await self.load()

        self.assertEqual(self.state.selected_list['id'], '')
        self.assertEqual(self.state.list_items, [])
        self.assertEqual(self.state.list_detail_error, 'Esta lista não está disponível.')

    async def test_visibility_change_between_summary_and_items_clears_public_state(self):
        async def request(method, path, **kwargs):
            if path == '/lists/public/84':
                return self.public_record()
            if path == '/lists/public/84/items':
                raise APIError('Registro não encontrado.', 404)
            raise AssertionError(f'unexpected_request:{path}')

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)), \
             patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(return_value=True)):
            await self.load()

        self.assertEqual(self.state.selected_list['id'], '')
        self.assertEqual(self.state.list_items, [])
        self.assertEqual(self.state.list_detail_error, 'Esta lista não está disponível.')

    async def test_account_change_discards_delayed_detail_response(self):
        gate = asyncio.Event()

        async def request(method, path, **kwargs):
            if path == '/lists/public/84':
                await gate.wait()
                return self.public_record()
            raise AssertionError(f'unexpected_request:{path}')

        self.state.user_id = 7
        self.state.session_token = 'first-session'
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=request)), \
             patch.object(SocialState, '_validate_navigation_session',
                          new=AsyncMock(return_value=True)):
            task = asyncio.create_task(self.load())
            await asyncio.sleep(0)
            self.state.session_token = 'second-session'
            gate.set()
            await task

        self.assertEqual(self.state.selected_list['id'], '')
        self.assertEqual(self.state.list_items, [])


class ListDetailContractTests(unittest.TestCase):
    def read(self, name):
        return (ROOT / 'xano/api/codeboxd' / name).read_text(encoding='utf-8')

    def test_public_detail_hides_private_lists_with_not_found_and_projects_public_fields(self):
        source = self.read('lists_public_id_GET.xs')
        self.assertNotIn('auth = "user"', source)
        self.assertIn('precondition ($record.is_public == true)', source)
        self.assertEqual(source.count('error_type = "notfound"'), 2)
        self.assertIn('output = ["id", "user_id", "title", "description", "is_public"]', source)
        self.assertIn('output = ["user_id", "username", "display_name", "avatar_url"]', source)
        self.assertNotRegex(source, r'(?i)email|password|account_status|role')

    def test_owner_detail_requires_current_session_and_matches_owner_before_projection(self):
        source = self.read('lists_id_GET.xs')
        self.assertIn('auth = "user"', source)
        self.assertIn('"Security/require_current_session"', source)
        self.assertIn('precondition ($record != null && $record.user_id == $auth.id)', source)
        self.assertIn('error_type = "notfound"', source)
        self.assertNotRegex(source.split('api.lambda', 1)[1],
                            r'(?i)email|password|account_status|role')

    def test_public_items_make_private_and_missing_lists_indistinguishable(self):
        source = self.read('lists_public_id_items_GET.xs')
        self.assertEqual(source.count('error_type = "notfound"'), 2)
        self.assertNotIn('error_type = "accessdenied"', source)


if __name__ == '__main__':
    unittest.main()
