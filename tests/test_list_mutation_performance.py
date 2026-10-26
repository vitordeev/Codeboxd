import asyncio
from copy import deepcopy
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import DEFAULT_MEDIA_LISTS, SocialState


async def finish(events):
    async for _ in events:
        pass


class ListMutationPerformanceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        legacy = patch.dict('os.environ', {'DEFAULT_LIST_IDENTITY_ENABLED':'false'})
        legacy.start(); self.addCleanup(legacy.stop)
        self.s = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.s.router.url.path = '/listas'
        self.s.user_id = self.s._identity = 7
        self.s.session_token = 'fictional-session'
        self.s.selected_list = dict(id='12', title='Original', description='Draft', user_id='7', is_public='False')
        self.s.list_editor_open = True
        self.records = [dict(id=index, title=title, description=description, user_id=7, is_public=True)
                        for index, (title, description) in enumerate(DEFAULT_MEDIA_LISTS, 1)]
        self.records.append(dict(id=12, title='Original', description='Draft', user_id=7, is_public=False))
        self.s.lists = [{key: str(value) for key, value in row.items()} for row in self.records]
        self.s._media = {'9': dict(id=9, title='Existing work', media_type='book')}
        self.calls = []

    async def call(self, method, path, data=None, **kwargs):
        self.calls.append((method, path))
        if path == '/media': return list(self.s._media.values())
        if method == 'GET':
            if path == '/lists': return deepcopy(self.records)
            if path == '/lists/public': return []
            if path.endswith('/items'): return [{'media_id': int(next(iter(self.s._media)))}]
        if method == 'DELETE':
            self.records = [row for row in self.records if str(row['id']) != path.rsplit('/', 1)[-1]]
            return {}
        if method == 'POST':
            result = dict(data, id=13, user_id=7)
            self.records.append(result)
            return result
        if method == 'PUT':
            result = next(row for row in self.records if str(row['id']) == path.rsplit('/', 1)[-1])
            result.update(data)
            return deepcopy(result)
        raise AssertionError('Unexpected call')

    def patches(self):
        from contextlib import ExitStack
        stack = ExitStack()
        stack.enter_context(patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)))
        stack.enter_context(patch.object(SocialState, '_validate_navigation_session', new=AsyncMock(return_value=True)))
        stack.enter_context(patch.object(SocialState, '_call', side_effect=self.call))
        return stack

    async def test_edit_skips_catalog_but_confirms_directory_and_items(self):
        for size in (5, 250):
            self.s._media = {str(i): dict(id=i, title=f'Work {i}', media_type='book') for i in range(1, size+1)}
            self.calls.clear()
            with self.patches():
                await finish(self.s.save_list({'title': 'Edited', 'description': 'Saved'}))
            self.assertNotIn(('GET', '/media'), self.calls)
            self.assertEqual(self.calls.count(('PUT', '/lists/12')), 1)
            self.assertIn(('GET', '/lists/12/items'), self.calls)
            self.assertEqual(len(self.s._media), size)
            self.assertEqual(self.s.selected_list['title'], 'Edited')
            self.assertEqual(self.s.list_items[0]['title'], 'Work 1')
            self.assertFalse(self.s.list_editor_open)
            self.assertFalse(self.s.list_saving)

    async def test_creation_and_deletion_preserve_default_lists_and_catalog(self):
        with self.patches():
            self.s.new_list()
            await finish(self.s.save_list({'title': 'Created', 'is_public': 'on'}))
            self.assertEqual(self.s.selected_list['id'], '13')
            await finish(self.s.remove_list())
        self.assertNotIn(('GET', '/media'), self.calls)
        self.assertEqual(self.calls.count(('POST', '/lists')), 1)
        self.assertEqual(self.calls.count(('DELETE', '/lists/13')), 1)
        self.assertEqual(len(self.s.quick_lists), 2)
        self.assertIn('9', self.s._media)
        self.assertEqual(self.s.notice, 'Lista removida.')

    async def test_normal_screen_entry_still_refreshes_catalog(self):
        with self.patches():
            await self.s.load_lists()
        self.assertIn(('GET', '/media'), self.calls)

    async def test_five_samples_compare_reconstructed_previous_flow_with_optimized_flow(self):
        for size in (5, 250):
            before, after = [], []
            for _ in range(5):
                self.setUp()
                self.s._media = {str(i): dict(id=i, title=f'Work {i}', media_type='book') for i in range(1, size+1)}
                with self.patches():
                    # Original save flow: write, full screen reload, reopen list.
                    await self.call('PUT', '/lists/12', dict(title='Edited', description='', is_public=False))
                    await self.s.load_lists()
                    await self.s.open_list('12')
                before.append(len(self.calls))
                self.calls.clear()
                with self.patches():
                    await finish(self.s.save_list({'title': 'Edited'}))
                after.append(len(self.calls))
                self.assertEqual(len(self.s._media), size)
            # Both paths now omit the unrelated public directory request.
            self.assertEqual(before, [5]*5)
            self.assertEqual(after, [4]*5)

    async def test_failed_write_preserves_editor_and_draft_without_retry(self):
        original = deepcopy(self.s.selected_list)
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock(side_effect=APIError('Unavailable', 503))) as call:
            await finish(self.s.save_list({'title': 'Edited'}))
        call.assert_awaited_once()
        self.assertEqual(self.s.selected_list, original)
        self.assertTrue(self.s.list_editor_open)
        self.assertFalse(self.s.list_saving)
        self.assertIn('Unavailable', self.s.notice)

    async def test_duplicate_save_and_delete_are_blocked_during_pending_write(self):
        started, release = asyncio.Event(), asyncio.Event()
        original = self.call
        async def delayed(*args, **kwargs):
            if args[0] == 'PUT':
                started.set()
                await release.wait()
            return await original(*args, **kwargs)
        self.call = delayed
        with self.patches():
            task = asyncio.create_task(finish(self.s.save_list({'title': 'Edited'})))
            await started.wait()
            try:
                self.assertTrue(self.s.list_saving)
                await finish(self.s.save_list({'title': 'Duplicate'}))
                await finish(self.s.remove_list())
            finally:
                release.set()
                await task
        self.assertEqual(sum(method != 'GET' for method, _ in self.calls), 1)

    async def test_late_write_cannot_replace_new_selection_or_account(self):
        for change in ('selection', 'account'):
            with self.subTest(change=change):
                self.setUp()
                started, release = asyncio.Event(), asyncio.Event()
                async def delayed(*args, **kwargs):
                    started.set()
                    await release.wait()
                    return {'id': 12}
                with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                        patch.object(SocialState, '_call', side_effect=delayed) as call:
                    task = asyncio.create_task(finish(self.s.save_list({'title': 'Old result'})))
                    await started.wait()
                    if change == 'selection': self.s.new_list()
                    else: self.s.session_token = 'new-account'
                    self.s.notice = 'Current view'
                    release.set()
                    await task
                call.assert_awaited_once()
                self.assertEqual(self.s.notice, 'Current view')
                self.assertTrue(self.s.list_editor_open)

    async def test_directory_failure_keeps_editor_instead_of_false_success(self):
        original = self.call
        async def fail_directory(method, path, *args, **kwargs):
            if method == 'GET': raise APIError('Refresh failed', 503)
            return await original(method, path, *args, **kwargs)
        self.call = fail_directory
        with self.patches():
            await finish(self.s.save_list({'title': 'Saved remotely'}))
        self.assertTrue(self.s.list_editor_open)
        self.assertEqual(self.s.selected_list['title'], 'Original')
        self.assertEqual(self.s.notice, 'Refresh failed')
