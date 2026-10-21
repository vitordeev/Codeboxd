import unittest
from unittest.mock import AsyncMock, patch

import httpx

from tools.real_login_measurement import normal_network_available, restore_normal_app


class NormalAppRestorationTests(unittest.IsolatedAsyncioTestCase):
    async def test_browser_runner_checks_network_before_touching_generated_app(self):
        from tools.performance_continuation_browser import main
        with patch('tools.performance_continuation_browser.normal_network_available',new=AsyncMock(return_value=False)), \
             patch('tools.performance_continuation_browser.OUTPUT') as output, \
             patch('tools.performance_continuation_browser.subprocess.Popen') as launch:
            with self.assertRaisesRegex(RuntimeError,'Network is blocked'): await main()
        output.mkdir.assert_not_called()
        launch.assert_not_called()

    async def test_blocked_network_does_not_stop_or_replace_existing_app(self):
        with patch('tools.real_login_measurement.normal_network_available',new=AsyncMock(return_value=False)), \
             patch('tools.real_login_measurement.psutil.Process') as process, \
             patch('tools.real_login_measurement.subprocess.Popen') as launch:
            self.assertFalse(await restore_normal_app([(12345,1.0)]))
        process.assert_not_called()
        launch.assert_not_called()

    async def test_preflight_uses_public_head_without_credentials(self):
        client=AsyncMock()
        context=AsyncMock(); context.__aenter__.return_value=client
        with patch('tools.real_login_measurement.httpx.AsyncClient',return_value=context):
            self.assertTrue(await normal_network_available())
        client.head.assert_awaited_once_with('https://api.themoviedb.org')

    async def test_connection_failure_is_reported_as_unavailable(self):
        client=AsyncMock()
        client.head.side_effect=httpx.ConnectError('Fictional network restriction')
        context=AsyncMock(); context.__aenter__.return_value=client
        with patch('tools.real_login_measurement.httpx.AsyncClient',return_value=context):
            self.assertFalse(await normal_network_available())
