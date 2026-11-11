"""Exercise config selection before any login, socket, browser or remote request."""
import tempfile
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx

from tools import admin_reads_remote, admin_browser_real


class BootstrapStopped(RuntimeError):
    pass


class AdminWorktreeConfigTests(unittest.IsolatedAsyncioTestCase):
    def test_proxy_evidence_preserves_login_and_separates_local_errors(self):
        login = [{'method': 'POST', 'endpoint': '/auth/login', 'status': 200}]
        probe = SimpleNamespace(report={'requests': login})
        proxy = [{'endpoint': '/admin/dashboard', 'status': 200},
                 {'endpoint': '/admin/dashboard', 'status': 503}]
        admin_browser_real.record_proxy_stats(probe, {'requests': proxy,
            'upstream_requests': 1, 'injected_failures': 1, 'rate_limits': 0})
        self.assertEqual(probe.report['requests'], login)
        self.assertEqual(probe.report['proxy_requests'], proxy)
        self.assertEqual(probe.report['proxy_upstream_requests'], 1)
        self.assertEqual(probe.report['injected_failures'], 1)

    async def test_login_and_proxy_share_explicit_configuration_without_copying_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = root / 'private.env'
            config.write_text('XANO_AUTH_URL=https://auth.invalid\nXANO_SOCIAL_URL=https://social.invalid\n', encoding='utf-8')
            calls = []

            def bootstrap(probe, role_label):
                self.assertEqual(probe.auth, 'https://auth.invalid')
                self.assertEqual(probe.social, 'https://social.invalid')
                self.assertEqual(probe.config_path, config)
                calls.append(probe.config_path)
                raise BootstrapStopped()

            client = httpx.Client(transport=httpx.MockTransport(lambda request: self.fail('Unexpected network request')))
            with patch.object(admin_reads_remote.httpx, 'Client', return_value=client), \
                    patch.object(admin_reads_remote, 'login_server', side_effect=bootstrap), \
                    self.assertRaises(BootstrapStopped):
                await admin_reads_remote.main(root / 'result.json', config_path=config)
            self.assertEqual(calls, [config])
            self.assertFalse((root / '.env').exists())

    async def test_browser_proxy_reads_same_path_before_opening_socket(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = root / 'external.env'
            probe = SimpleNamespace(private_dir=root / 'private', config_path=config)
            with patch.object(admin_browser_real, 'dotenv_values', return_value={}) as values, \
                    patch.object(admin_browser_real.socket, 'socket', side_effect=BootstrapStopped), \
                    self.assertRaises(BootstrapStopped):
                await admin_browser_real.validate(probe)
            values.assert_called_once_with(config)


if __name__ == '__main__':
    unittest.main()
