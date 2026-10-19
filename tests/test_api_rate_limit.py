import unittest
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from unittest.mock import AsyncMock, patch

import httpx

from Codeboxd_main.services import api


class RateLimitTests(unittest.IsolatedAsyncioTestCase):
    async def test_write_is_not_retried_and_exposes_retry_after(self):
        client = AsyncMock()
        client.request.return_value = httpx.Response(429, headers={'Retry-After': '90'},
            request=httpx.Request('POST', 'https://example.com/reports'))
        context = AsyncMock()
        context.__aenter__.return_value = client
        with patch.object(api.httpx, 'AsyncClient', return_value=context), \
             patch.object(api, 'base_url', return_value='https://example.com'), \
             patch.object(api.asyncio, 'sleep', new=AsyncMock()) as sleep:
            with self.assertRaises(api.APIError) as error:
                await api.request('POST', '/reports', data={'target_id': '1'})
        self.assertEqual(error.exception.status, 429)
        self.assertEqual(error.exception.retry_after, 90)
        client.request.assert_awaited_once()
        sleep.assert_not_awaited()

    async def test_read_does_not_retry_before_long_server_deadline(self):
        client = AsyncMock()
        client.request.return_value = httpx.Response(429, headers={'Retry-After': '120'},
            request=httpx.Request('GET', 'https://example.com/media'))
        context = AsyncMock()
        context.__aenter__.return_value = client
        with patch.object(api.httpx, 'AsyncClient', return_value=context), \
             patch.object(api, 'base_url', return_value='https://example.com'), \
             patch.object(api.asyncio, 'sleep', new=AsyncMock()) as sleep:
            with self.assertRaises(api.APIError):
                await api.request('GET', '/media')
        client.request.assert_awaited_once()
        sleep.assert_not_awaited()

    async def test_read_can_retry_short_deadline(self):
        client = AsyncMock()
        request = httpx.Request('GET', 'https://example.com/media')
        client.request.side_effect = [httpx.Response(429, headers={'Retry-After': '1'}, request=request),
                                      httpx.Response(200, json=[], request=request)]
        context = AsyncMock()
        context.__aenter__.return_value = client
        with patch.object(api.httpx, 'AsyncClient', return_value=context), \
             patch.object(api, 'base_url', return_value='https://example.com'), \
             patch.object(api.asyncio, 'sleep', new=AsyncMock()) as sleep:
            self.assertEqual(await api.request('GET', '/media'), [])
        self.assertEqual(client.request.await_count, 2)
        sleep.assert_awaited_once_with(1)

    def test_retry_after_accepts_http_date_and_handles_bad_values(self):
        future = format_datetime(datetime.now(timezone.utc) + timedelta(seconds=120), usegmt=True)
        self.assertIn(api.retry_after_seconds(future), (119, 120))
        for value in ('', 'invalid', 'NaN', 'inf'):
            self.assertEqual(api.retry_after_seconds(value), 30)
