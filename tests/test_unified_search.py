import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class UnifiedSearchTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(
            SocialState.get_full_name().split('.'))
        self.state.router.url.path = '/buscar'

    async def load(self):
        async for _ in self.state.load_unified_search():
            pass

    async def test_empty_url_does_not_query_any_search_domain(self):
        self.state.router.url.query_parameters = {'tipo': 'listas', 'page': '1'}
        with patch('Codeboxd_main.state.social.request', new=AsyncMock()) as api, \
             patch('Codeboxd_main.state.social.catalog.search', new=AsyncMock()) as catalog_search:
            await self.load()
        api.assert_not_awaited()
        catalog_search.assert_not_awaited()
        self.assertEqual(self.state.unified_search_scope, 'listas')
        self.assertEqual(self.state.unified_search_query, '')

    async def test_people_scope_uses_only_public_paginated_profile_contract(self):
        self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'Jo', 'page': '2'}
        response = {
            'items': [{'user_id': 9, 'username': 'joana', 'display_name': 'Joana',
                       'avatar_url': '', 'email': 'must-not-leak'}],
            'total': 21, 'page': 2, 'per_page': 20, 'next_page': None,
        }
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=response)) as api, \
             patch('Codeboxd_main.state.social.catalog.search', new=AsyncMock()) as catalog_search:
            await self.load()
        api.assert_awaited_once()
        self.assertEqual(api.await_args.args[:2], ('GET', '/profiles'))
        self.assertEqual(api.await_args.kwargs['params'], {'q': 'Jo', 'page': 2, 'per_page': 20})
        self.assertEqual(api.await_args.kwargs['token'], '')
        catalog_search.assert_not_awaited()
        self.assertEqual(self.state.unified_search_total, 21)
        self.assertEqual(self.state.unified_search_people_results, [{
            'user_id': '9', 'username': 'joana', 'display_name': 'Joana', 'avatar_url': '',
        }])

    async def test_public_list_scope_sends_visible_filters_without_profile_fanout(self):
        self.state.router.url.query_parameters = {
            'tipo': 'listas', 'q': 'ficção', 'page': '3',
            'creator_id': '42', 'search_in': 'title_description',
        }
        response = {
            'items': [{
                'id': 12, 'title': 'Ficção', 'description': 'Leituras',
                'items_count': 7,
                'creator': {'user_id': 42, 'username': 'leitora',
                            'display_name': 'Leitora', 'email': 'must-not-leak'},
            }],
            'total': 41, 'page': 3, 'per_page': 20, 'next_page': None,
        }
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=response)) as api, \
             patch('Codeboxd_main.state.social.catalog.search', new=AsyncMock()) as catalog_search:
            await self.load()
        api.assert_awaited_once()
        self.assertEqual(api.await_args.args[:2], ('GET', '/lists/public'))
        self.assertEqual(api.await_args.kwargs['params'], {
            'q': 'ficção', 'page': 3, 'per_page': 20,
            'search_in': 'title_description', 'creator_id': 42,
        })
        catalog_search.assert_not_awaited()
        self.assertEqual(self.state.unified_search_total, 41)
        self.assertEqual(self.state.unified_search_list_results, [{
            'id': '12', 'title': 'Ficção', 'description': 'Leituras', 'items_count': '7',
            'creator_user_id': '42', 'creator_display_name': 'Leitora',
        }])

    async def test_submitted_works_search_reuses_multiformat_catalog_only(self):
        self.state.router.url.query_parameters = {'tipo': 'obras', 'q': 'Duna', 'page': '2'}
        item = {
            'identity_key': 'tmdb:movie:42', 'id': 5, 'title': 'Duna',
            'media_type': 'movie', 'external_source': 'tmdb', 'external_id': '42',
        }
        with patch('Codeboxd_main.state.social.catalog.search',
                   new=AsyncMock(return_value=([item], []))) as catalog_search, \
             patch('Codeboxd_main.state.social.request', new=AsyncMock()) as api:
            await self.load()
        catalog_search.assert_awaited_once_with('Duna', 'all', 2)
        api.assert_not_awaited()
        self.assertEqual(self.state.search_results[0]['title'], 'Duna')

    async def test_typing_does_not_submit_or_change_pagination_context(self):
        self.state.unified_search_query = 'Duna'
        self.state.unified_search_page = 4
        self.state.update_unified_search_draft('Duna 2')
        self.assertEqual(self.state.unified_search_draft, 'Duna 2')
        self.assertEqual(self.state.unified_search_query, 'Duna')
        self.assertEqual(self.state.unified_search_page, 4)

    async def test_array_response_is_rejected_instead_of_client_filtering(self):
        self.state.router.url.query_parameters = {'tipo': 'listas', 'q': 'privada'}
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=[
            {'id': 1, 'title': 'Lista não filtrada'}])) as api:
            await self.load()
        api.assert_awaited_once()
        self.assertEqual(self.state.unified_search_list_results, [])
        self.assertIn('sem paginação', self.state.unified_search_error)

    async def test_rate_limit_is_distinct_from_empty_results(self):
        self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'Jo'}
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(
                side_effect=APIError('Muitas solicitações. Tente novamente em 30 segundos.', 429, 30))):
            await self.load()
        self.assertEqual(self.state.unified_search_people_results, [])
        self.assertIn('30', self.state.unified_search_error)
        self.assertFalse(self.state.unified_search_busy)

    async def test_public_list_rate_limit_does_not_query_other_scopes(self):
        self.state.router.url.query_parameters = {'tipo': 'listas', 'q': 'Coleção'}
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(
                side_effect=APIError('Muitas solicitações. Tente novamente em 30 segundos.', 429, 30))) as api, \
             patch('Codeboxd_main.state.social.catalog.search', new=AsyncMock()) as catalog_search:
            await self.load()
        api.assert_awaited_once()
        self.assertEqual(api.await_args.args[:2], ('GET', '/lists/public'))
        self.assertEqual(self.state.unified_search_list_results, [])
        self.assertIn('30', self.state.unified_search_error)
        self.assertFalse(self.state.unified_search_busy)
        catalog_search.assert_not_awaited()

    async def test_rate_limit_cooldown_suppresses_same_scope_but_not_other_scope(self):
        calls = []

        async def respond(method, path, **kwargs):
            calls.append(path)
            if path == '/profiles':
                raise APIError('Muitas solicitações. Tente novamente em 30 segundos.', 429, 30)
            return {
                'items': [{
                    'id': 12, 'title': 'Lista disponível', 'items_count': 1,
                    'creator': {'user_id': 9, 'username': 'joana',
                                'display_name': 'Joana'},
                }],
                'total': 1, 'page': 1, 'per_page': 20, 'next_page': None,
            }

        with patch('Codeboxd_main.state.social.request',
                   new=AsyncMock(side_effect=respond)) as api:
            self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'Jo'}
            await self.load()
            self.assertIn('30 segundos', self.state.unified_search_error)

            self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'Joana'}
            await self.load()
            self.assertIn('30 segundos', self.state.unified_search_error)

            self.state.router.url.query_parameters = {'tipo': 'listas', 'q': 'Joana'}
            await self.load()

        self.assertEqual(calls, ['/profiles', '/lists/public'])
        self.assertEqual(api.await_count, 2)
        self.assertEqual(self.state.unified_search_list_results[0]['title'], 'Lista disponível')

    async def test_long_public_names_are_preserved_without_private_fields_or_fanout(self):
        long_name = 'Nome público ' + ('com muitas palavras ' * 8)
        long_title = 'Lista ' + ('de leituras extensas ' * 7)
        creator_name = 'Criadora ' + ('de listas públicas ' * 8)
        responses = [
            {
                'items': [{
                    'user_id': 9, 'username': 'leitora', 'display_name': long_name,
                    'avatar_url': '', 'email': 'must-not-leak',
                }],
                'total': 1, 'page': 1, 'per_page': 20, 'next_page': None,
            },
            {
                'items': [{
                    'id': 12, 'title': long_title, 'description': 'Descrição',
                    'items_count': 3,
                    'creator': {
                        'user_id': 9, 'username': 'leitora',
                        'display_name': creator_name, 'email': 'must-not-leak',
                    },
                }],
                'total': 1, 'page': 1, 'per_page': 20, 'next_page': None,
            },
        ]
        with patch('Codeboxd_main.state.social.request',
                   new=AsyncMock(side_effect=responses)) as api, \
             patch('Codeboxd_main.state.social.catalog.search', new=AsyncMock()) as catalog_search:
            self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'leitora'}
            await self.load()
            self.assertEqual(self.state.unified_search_people_results[0]['display_name'], long_name.strip())
            self.assertNotIn('email', self.state.unified_search_people_results[0])

            self.state.router.url.query_parameters = {'tipo': 'listas', 'q': 'leitora'}
            await self.load()

        self.assertEqual(self.state.unified_search_list_results[0]['title'], long_title.strip())
        self.assertEqual(self.state.unified_search_list_results[0]['creator_display_name'],
                         creator_name.strip())
        self.assertEqual([call.args[1] for call in api.await_args_list],
                         ['/profiles', '/lists/public'])
        self.assertNotIn('email', self.state.unified_search_list_results[0])
        catalog_search.assert_not_awaited()

    async def test_scope_switch_discards_delayed_response_from_previous_domain(self):
        self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'jo'}
        gate = asyncio.Event()
        calls = []

        async def respond(method, path, **kwargs):
            calls.append(path)
            if path == '/profiles':
                await gate.wait()
                return {
                    'items': [{'user_id': 9, 'username': 'joana', 'display_name': 'Joana'}],
                    'total': 1, 'page': 1, 'per_page': 20, 'next_page': None,
                }
            return {
                'items': [{
                    'id': 12, 'title': 'Lista atual', 'items_count': 1,
                    'creator': {'user_id': 9, 'username': 'joana',
                                'display_name': 'Joana'},
                }],
                'total': 1, 'page': 1, 'per_page': 20, 'next_page': None,
            }

        with patch('Codeboxd_main.state.social.request',
                   new=AsyncMock(side_effect=respond)):
            old_search = asyncio.create_task(self.load())
            await asyncio.sleep(.01)
            self.state.router.url.query_parameters = {'tipo': 'listas', 'q': 'jo'}
            await self.load()
            gate.set()
            await old_search

        self.assertEqual(calls, ['/profiles', '/lists/public'])
        self.assertEqual(self.state.unified_search_scope, 'listas')
        self.assertEqual(self.state.unified_search_people_results, [])
        self.assertEqual(self.state.unified_search_list_results[0]['title'], 'Lista atual')
        self.assertFalse(self.state.unified_search_busy)

    async def test_failed_scope_can_recover_without_leaking_its_results_or_error(self):
        self.state.router.url.query_parameters = {'tipo': 'listas', 'q': 'ficção'}
        calls = []

        async def respond(method, path, **kwargs):
            calls.append(path)
            if path == '/lists/public':
                raise APIError('Serviço de listas indisponível.', 503)
            return {
                'items': [{'user_id': 9, 'username': 'leitora',
                           'display_name': 'Leitora'}],
                'total': 1, 'page': 1, 'per_page': 20, 'next_page': None,
            }

        with patch('Codeboxd_main.state.social.request',
                   new=AsyncMock(side_effect=respond)):
            await self.load()
            self.assertIn('indisponível', self.state.unified_search_error)
            self.assertEqual(self.state.unified_search_list_results, [])
            self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'ficção'}
            await self.load()

        self.assertEqual(calls, ['/lists/public', '/profiles'])
        self.assertEqual(self.state.unified_search_error, '')
        self.assertEqual(self.state.unified_search_people_results[0]['display_name'], 'Leitora')

    async def test_account_change_discards_delayed_search_result(self):
        self.state.router.url.query_parameters = {'tipo': 'pessoas', 'q': 'Jo'}
        gate = asyncio.Event()
        response = {
            'items': [{'user_id': 9, 'username': 'joana', 'display_name': 'Joana'}],
            'total': 1, 'page': 1, 'per_page': 20, 'next_page': None,
        }

        async def delayed(*args, **kwargs):
            await gate.wait()
            return response

        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=delayed)):
            task = asyncio.create_task(self.load())
            await asyncio.sleep(0)
            self.state.session_token = 'different-session'
            gate.set()
            await task
        self.assertEqual(self.state.unified_search_people_results, [])


if __name__ == '__main__':
    unittest.main()
