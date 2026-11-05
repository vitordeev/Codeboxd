import asyncio
import unittest
from unittest.mock import AsyncMock, call, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


async def finish(events):
    async for _ in events:
        pass


class ListItemRemovalTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.router.url.path = '/listas'
        self.state.session_token = 'fixture-session'
        self.state.user_id = 7
        self.state.selected_list = {'id': '12', 'user_id': '7', 'title': 'Minha lista'}
        self.state.lists = [dict(self.state.selected_list)]
        self.state.list_items = [{'id': '9', 'title': 'Obra preservada'}]

    async def test_pending_removal_yields_feedback_and_blocks_duplicate_delete(self):
        entered, release = asyncio.Event(), asyncio.Event()
        async def write(*args):
            entered.set()
            await release.wait()
            return []
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', side_effect=write) as request:
            events = self.state.remove_list_item('9')
            await anext(events)
            self.assertTrue(self.state.list_item_saving)
            request.assert_not_called()
            first = asyncio.create_task(finish(events))
            await entered.wait()
            await asyncio.gather(*(finish(self.state.remove_list_item('9')) for _ in range(10)))
            release.set()
            await first
        request.assert_has_awaits([call('DELETE', '/lists/12/items/9'), call('GET', '/lists/12/items')])
        self.assertEqual(request.await_count, 2)
        self.assertFalse(self.state.list_item_saving)

    async def test_selection_or_session_change_during_auth_prevents_write(self):
        for change in ('list', 'session'):
            with self.subTest(change=change):
                self.setUp()
                async def auth():
                    if change == 'list': self.state.selected_list = {'id': '13', 'user_id': '7'}
                    else: self.state.session_token = 'new-session'
                    return True
                with patch.object(SocialState, '_require_user', side_effect=auth), \
                        patch.object(SocialState, '_call', new=AsyncMock()) as call:
                    await finish(self.state.remove_list_item('9'))
                call.assert_not_called()
                self.assertFalse(self.state.list_item_saving)

    async def test_late_success_or_failure_cannot_refresh_or_overwrite_new_list(self):
        for fail in (False, True):
            with self.subTest(fail=fail):
                self.setUp()
                async def write(*args):
                    self.state.selected_list = {'id': '13', 'user_id': '7'}
                    self.state.notice = 'Lista atual'
                    if fail: raise APIError('Erro antigo', 503)
                with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                        patch.object(SocialState, '_call', side_effect=write), \
                        patch.object(SocialState, 'open_list', new=AsyncMock()) as refresh:
                    await finish(self.state.remove_list_item('9'))
                refresh.assert_not_called()
                self.assertEqual(self.state.notice, 'Lista atual')
                self.assertEqual(self.state.list_items[0]['id'], '9')

    async def test_failed_delete_preserves_items_and_does_not_retry(self):
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock(side_effect=APIError('Tente novamente', 503))) as call, \
                patch.object(SocialState, 'open_list', new=AsyncMock()) as refresh:
            await finish(self.state.remove_list_item('9'))
        call.assert_awaited_once()
        refresh.assert_not_called()
        self.assertEqual(self.state.list_items[0]['id'], '9')
        self.assertIn('Tente novamente', self.state.notice)
        self.assertFalse(self.state.list_item_saving)

    async def test_invalid_ids_and_foreign_lists_do_not_authorize_or_send(self):
        for lid, mid, owner in (('0', '9', '7'), ('12', '-1', '7'), ('12', 'invalid', '7'), ('12', '9', '8')):
            with self.subTest(lid=lid, mid=mid, owner=owner):
                self.state.selected_list = {'id': lid, 'user_id': owner}
                with patch.object(SocialState, '_require_user', new=AsyncMock()) as auth, \
                        patch.object(SocialState, '_call', new=AsyncMock()) as call:
                    await finish(self.state.remove_list_item(mid))
                auth.assert_not_called()
                call.assert_not_called()

    async def test_cancelled_generator_releases_pending_flag(self):
        events = self.state.remove_list_item('9')
        await anext(events)
        self.assertTrue(self.state.list_item_saving)
        await events.aclose()
        self.assertFalse(self.state.list_item_saving)

    async def test_expired_session_redirects_without_deleting(self):
        async def expired():
            self.state.session_token = ''
            return False
        with patch.object(SocialState, '_require_user', side_effect=expired), \
                patch.object(SocialState, '_call', new=AsyncMock()) as request:
            events = [event async for event in self.state.remove_list_item('9')]
        request.assert_not_called()
        self.assertEqual(len([event for event in events if event is not None]), 1)
        self.assertFalse(self.state.list_item_saving)
