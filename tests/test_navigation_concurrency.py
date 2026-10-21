import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState, _NAVIGATION_IN_FLIGHT


def state():
    result = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
    result.session_token = 'fixture-a'
    return result


class NavigationConcurrencyTests(unittest.IsolatedAsyncioTestCase):
    async def test_account_change_before_task_starts_cannot_use_new_credentials(self):
        current = state()
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=[])) as transport:
            pending = asyncio.create_task(current._call('GET', '/media'))
            # _call creates the child task and yields before its first request.
            await asyncio.sleep(0)
            current.session_token = 'fixture-b'
            with self.assertRaises(APIError): await pending
        transport.assert_not_awaited()

    async def test_equivalent_concurrent_reads_send_once_and_return_independent_copies(self):
        current = state()
        started, release = asyncio.Event(), asyncio.Event()
        async def request(*args, **kwargs):
            started.set()
            await release.wait()
            return [{'id': 1, 'nested': {'title': 'Original'}}]
        with patch('Codeboxd_main.state.social.request', side_effect=request) as transport:
            first = asyncio.create_task(current._call('GET', '/media'))
            await started.wait()
            second = asyncio.create_task(current._call('GET', '/media'))
            await asyncio.sleep(0)
            release.set()
            a, b = await asyncio.gather(first, second)
            a[0]['nested']['title'] = 'Changed'
            self.assertEqual(b[0]['nested']['title'], 'Original')
            self.assertEqual((await current._call('GET', '/media'))[0]['nested']['title'], 'Original')
        transport.assert_awaited_once()
        self.assertFalse(_NAVIGATION_IN_FLIGHT)

    async def test_distinct_pages_sessions_and_credentials_do_not_share_pending_reads(self):
        first, other = state(), state()
        started, release = asyncio.Event(), asyncio.Event()
        async def request(*args, **kwargs):
            started.set()
            await release.wait()
            return []
        with patch('Codeboxd_main.state.social.request', side_effect=request) as transport:
            pending = [asyncio.create_task(first._call('GET', '/media', params={'page': 1}))]
            await started.wait()
            pending += [asyncio.create_task(first._call('GET', '/media', params={'page': 2})),
                        asyncio.create_task(other._call('GET', '/media', params={'page': 1}))]
            # Let each request capture its credentials before switching account.
            for _ in range(4): await asyncio.sleep(0)
            first.session_token = 'fixture-b'
            pending.append(asyncio.create_task(first._call('GET', '/media', params={'page': 1})))
            for _ in range(4): await asyncio.sleep(0)
            release.set()
            results = await asyncio.gather(*pending, return_exceptions=True)
        self.assertEqual(transport.await_count, 4)
        self.assertIsInstance(results[0], APIError)
        self.assertEqual(results[-1], [])

    async def test_cancelled_waiter_does_not_cancel_remaining_consumer(self):
        current = state()
        started, release = asyncio.Event(), asyncio.Event()
        async def request(*args, **kwargs):
            started.set()
            await release.wait()
            return []
        with patch('Codeboxd_main.state.social.request', side_effect=request) as transport:
            first = asyncio.create_task(current._call('GET', '/lists'))
            await started.wait()
            second = asyncio.create_task(current._call('GET', '/lists'))
            await asyncio.sleep(0)
            first.cancel()
            with self.assertRaises(asyncio.CancelledError): await first
            release.set()
            self.assertEqual(await second, [])
        transport.assert_awaited_once()
        self.assertFalse(_NAVIGATION_IN_FLIGHT)

    async def test_shared_error_is_not_cached_and_can_be_retried(self):
        current = state()
        started, release = asyncio.Event(), asyncio.Event()
        async def request(*args, **kwargs):
            started.set()
            await release.wait()
            raise APIError('Unavailable', 503)
        with patch('Codeboxd_main.state.social.request', side_effect=request) as transport:
            first = asyncio.create_task(current._call('GET', '/profiles'))
            await started.wait()
            second = asyncio.create_task(current._call('GET', '/profiles'))
            await asyncio.sleep(0)
            release.set()
            results = await asyncio.gather(first, second, return_exceptions=True)
        self.assertTrue(all(isinstance(result, APIError) for result in results))
        transport.assert_awaited_once()
        self.assertFalse(current._navigation_reads)
        self.assertFalse(_NAVIGATION_IN_FLIGHT)
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=[])) as retry:
            await current._call('GET', '/profiles')
        retry.assert_awaited_once()

    async def test_failed_mutation_prevents_reuse_of_read_started_before_write(self):
        current = state()
        started, release = asyncio.Event(), asyncio.Event()
        async def request(method, path, **kwargs):
            if method == 'PUT': raise APIError('Write failed', 503)
            started.set()
            await release.wait()
            return [{'user_id': 7}]
        with patch('Codeboxd_main.state.social.request', side_effect=request) as transport:
            old = asyncio.create_task(current._call('GET', '/profiles'))
            await started.wait()
            with self.assertRaises(APIError): await current._call('PUT', '/profile')
            fresh = asyncio.create_task(current._call('GET', '/profiles'))
            for _ in range(3): await asyncio.sleep(0)
            release.set()
            await asyncio.gather(old, fresh)
        self.assertEqual(transport.await_count, 3)

    async def test_account_change_cannot_fetch_second_page_under_new_token(self):
        current = state()
        async def request(*args, **kwargs):
            current.session_token = 'fixture-b'
            return [{'id': i} for i in range(100)]
        with patch('Codeboxd_main.state.social.request', side_effect=request) as transport:
            with self.assertRaises(APIError): await current._call('GET', '/media')
        transport.assert_awaited_once()
        self.assertFalse(current._navigation_reads)

    async def test_writes_are_never_shared(self):
        current = state()
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value={})) as transport:
            await asyncio.gather(current._call('POST', '/lists'), current._call('POST', '/lists'))
        self.assertEqual(transport.await_count, 2)
