import asyncio
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


def state():
    result = rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
    result.router.url.path = '/feed'
    result.session_token = 'fixture-a'
    result.user_id = 7
    return result


class FeedNavigationPerformanceTests(unittest.IsolatedAsyncioTestCase):
    async def test_revisit_keeps_posts_order_images_counts_and_likes_without_new_reads(self):
        current = state()
        post = dict(id=2, user_id=7, media_id=9, body='Own', created_at=1700000000000,
                    image='https://example.com/image.png', likes_count=3, comments_count=2)
        data = {'/media': [dict(id=9, title='Movie', media_type='movie')],
                '/profiles': [dict(user_id=7, display_name='Reader')],
                '/feed': [post, dict(post, id=1, body='Older', created_at=1600000000000)],
                '/posts': [post], '/likes': [dict(post_id=2)]}

        async def request(method, path, **kwargs):
            self.assertEqual(method, 'GET')
            return deepcopy(data[path])

        with patch('Codeboxd_main.state.social.request', side_effect=request) as transport, \
             patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)):
            await current.load_feed()
            expected = deepcopy(current.posts)
            self.assertEqual([p['id'] for p in expected], ['2', '1'])
            self.assertEqual(expected[0]['image_url'], post['image'])
            self.assertEqual(expected[0]['likes_count'], '3')
            self.assertEqual(transport.await_count, 5)
            for _ in range(5):
                await current.load_feed()
                self.assertEqual(current.posts, expected)
                self.assertEqual(current.liked_posts, ['2'])
            self.assertEqual(transport.await_count, 5)

    async def test_feed_routes_expire_and_return_independent_copies(self):
        current = state()
        for path in ('/feed', '/posts', '/likes'):
            with self.subTest(path=path), \
                 patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=[{'id': 1}])) as transport:
                first = await current._call('GET', path)
                first[0]['id'] = 99
                self.assertEqual(await current._call('GET', path), [{'id': 1}])
                transport.assert_awaited_once()
                current._navigation_reads = {key: (0, value[1])
                                             for key, value in current._navigation_reads.items()}
                await current._call('GET', path)
                self.assertEqual(transport.await_count, 2)

    async def test_pages_accounts_and_sessions_do_not_reuse_private_posts(self):
        current, other = state(), state()
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=[])) as transport:
            await current._call('GET', '/posts', params={'user_id': 7, 'page': 1})
            await current._call('GET', '/posts', params={'user_id': 7, 'page': 2})
            await current._call('GET', '/posts', params={'user_id': 8, 'page': 1})
            await other._call('GET', '/posts', params={'user_id': 7, 'page': 1})
            current.session_token = 'fixture-b'
            await current._call('GET', '/posts', params={'user_id': 7, 'page': 1})
            self.assertEqual(transport.await_count, 5)

    async def test_feed_errors_and_missing_likes_are_not_cached(self):
        for path, status in (('/feed', 429), ('/posts', 503), ('/likes', 404)):
            with self.subTest(path=path):
                current = state()
                with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=APIError('Fixture', status))) as transport:
                    for _ in range(2):
                        with self.assertRaises(APIError):
                            await current._call('GET', path)
                    self.assertEqual(transport.await_count, 2)
                    self.assertFalse(current._navigation_reads)

    async def test_social_writes_refresh_cached_feed_even_if_write_fails(self):
        for method, path in (('POST', '/posts'), ('PUT', '/posts/1'), ('DELETE', '/posts/1'),
                             ('PUT', '/posts/1/like'), ('POST', '/comments'),
                             ('PUT', '/follows/8'), ('DELETE', '/follows/8')):
            for fails in (False, True):
                with self.subTest(method=method, path=path, fails=fails):
                    current = state()
                    reads = 0

                    async def request(verb, route, **kwargs):
                        nonlocal reads
                        if verb == 'GET':
                            reads += 1
                            return [{'id': reads}]
                        if fails:
                            raise APIError('Uncertain write', 503)
                        return {}

                    with patch('Codeboxd_main.state.social.request', side_effect=request):
                        await current._call('GET', '/feed')
                        if fails:
                            with self.assertRaises(APIError):
                                await current._call(method, path)
                        else:
                            await current._call(method, path)
                        self.assertEqual(await current._call('GET', '/feed'), [{'id': 2}])

    async def test_inflight_feed_before_write_cannot_repopulate_cache(self):
        current = state()
        started, release = asyncio.Event(), asyncio.Event()
        reads = 0

        async def request(method, path, **kwargs):
            nonlocal reads
            if method != 'GET':
                return {}
            reads += 1
            if reads == 1:
                started.set()
                await release.wait()
                return [{'id': 1}]
            return [{'id': 2}]

        with patch('Codeboxd_main.state.social.request', side_effect=request):
            pending = asyncio.create_task(current._call('GET', '/feed'))
            await started.wait()
            await current._call('POST', '/posts')
            release.set()
            await pending
            self.assertEqual(await current._call('GET', '/feed'), [{'id': 2}])
            self.assertEqual(reads, 2)

    async def test_image_upload_invalidates_before_and_after_and_preserves_failed_draft(self):
        for fails in (False, True):
            with self.subTest(fails=fails), TemporaryDirectory() as directory:
                current = state()
                current.new_post()
                current.edit_post_body = 'Draft with image'
                image = Path(directory) / 'fixture.png'
                image.write_bytes(b'fixture-image')
                current._post_image_path = str(image)
                current.post_image_mime = 'image/png'
                reads = 0

                async def request(*args, **kwargs):
                    nonlocal reads
                    reads += 1
                    return [{'id': reads}]

                async def upload(*args, **kwargs):
                    self.assertFalse(current._navigation_reads)
                    # A read arriving during the multipart write is also invalidated.
                    await current._call('GET', '/feed')
                    if fails:
                        raise APIError('Upload unavailable', 503)
                    return {'id': 1}

                with patch('Codeboxd_main.state.social.request', side_effect=request), \
                     patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
                     patch.object(SocialState, '_refresh_posts', new=AsyncMock()), \
                     patch('Codeboxd_main.state.social.upload_file', side_effect=upload) as uploads:
                    await current._call('GET', '/feed')
                    async for _ in current.save_post({'body': 'Draft with image'}):
                        pass
                    self.assertFalse(current._navigation_reads)
                    self.assertEqual(await current._call('GET', '/feed'), [{'id': 3}])
                    uploads.assert_awaited_once()
                self.assertFalse(current.post_saving)
                if fails:
                    self.assertEqual(current.edit_post_body, 'Draft with image')
                    self.assertTrue(current.post_editor_open)
                    self.assertTrue(image.exists())
                else:
                    self.assertFalse(current.post_editor_open)
                    self.assertFalse(image.exists())
