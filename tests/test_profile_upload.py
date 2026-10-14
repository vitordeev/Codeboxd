"""Banner uploads must persist real URLs and clean up rejected files."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class ProfileUploadTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.user_id = 1
        self.state.profile = {'user_id': '1', 'username': 'member', 'display_name': 'Member',
                              'bio': '', 'avatar_url': '', 'banner_url': 'https://old.example/banner.png'}
        self.image = SimpleNamespace(read=AsyncMock(return_value=b'\x89PNG\r\n\x1a\nimage-bytes'))

    async def test_banner_payload_contains_real_url_with_backend_prefix(self):
        async def update(method, path, data):
            self.assertEqual((method, path), ('PUT', '/profile'))
            self.assertIsInstance(data['banner_url'], str)
            self.assertTrue(data['banner_url'].startswith('https://backend.example/api/_upload/profiles/1/banner-'))
            return {'user_id': 1, **data}

        config = SimpleNamespace(api_url='https://backend.example', prepend_backend_path=lambda path: '/api'+path)
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock(side_effect=update)), \
                patch('Codeboxd_main.state.social.rx.get_upload_dir', return_value=Path(directory)), \
                patch('reflex_base.config.get_config', return_value=config):
            await self.state.upload_profile_banner([self.image])
            files = list(Path(directory).rglob('*.png'))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].read_bytes(), b'\x89PNG\r\n\x1a\nimage-bytes')
            self.assertTrue(self.state.profile['banner_url'].endswith(files[0].name))

    async def test_rejected_banner_is_removed_without_removing_previous_image(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock(side_effect=APIError('Rejected', 422))), \
                patch('Codeboxd_main.state.social.rx.get_upload_dir', return_value=Path(directory)):
            previous = Path(directory) / 'previous.png'
            previous.write_bytes(b'previous-image')
            await self.state.upload_profile_banner([self.image])
            self.assertEqual(list(Path(directory).rglob('*.png')), [previous])
            self.assertEqual(previous.read_bytes(), b'previous-image')
            self.assertEqual(self.state.profile['banner_url'], 'https://old.example/banner.png')

    async def test_other_profile_owner_cannot_write_banner(self):
        self.state.profile['user_id'] = '2'
        with patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                patch.object(SocialState, '_call', new=AsyncMock()) as update:
            await self.state.upload_profile_banner([self.image])
        self.image.read.assert_not_awaited()
        update.assert_not_awaited()
