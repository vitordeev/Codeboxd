import asyncio
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.services import post_image_flow as flow
from Codeboxd_main.services.post_image_reservations import ImageReservation
from Codeboxd_main.state.social import SocialState


def reservation(state='reserved'):
    return ImageReservation(12, 7, 'a'*32, 'create', 0, 0, state, 'fixture',
                            'codeboxd/posts/u7/'+'b'*32)


class FlowTests(unittest.IsolatedAsyncioTestCase):
    async def run_flow(self, *, state='reserved', api=None, current=lambda: True,
                       upload=None, recover=None):
        with patch.object(flow, 'upload_config', return_value=SimpleNamespace(cloud_name='fixture')), \
             patch.object(flow, 'reserve_image', new=AsyncMock(return_value=reservation(state))) as reserve, \
             patch.object(flow, 'request', new=api or AsyncMock(side_effect=[
                 {'contract_version': 1, 'uploads_enabled': True},
                 {'contract_version': 1, 'id': 12, 'upload_granted': True}])) as request, \
             patch.object(flow, 'upload_post_image', new=upload or AsyncMock(return_value='receipt')) as send, \
             patch.object(flow, 'verify_post_image', new=AsyncMock()) as verify, \
             patch.object(flow, 'recover_post_image', new=recover or AsyncMock(return_value='recovered')) as recovery:
            result = await flow.prepare_image(token='session', owner_id=7, operation_key='a'*32,
                post_id=0, expected_revision=0, content=b'png', mime='image/png', current=current)
            return result, request, reserve, send, verify, recovery

    async def test_contract_is_required_before_reserving_or_uploading(self):
        for capabilities in ({}, {'contract_version': 1, 'uploads_enabled': False},
                             {'contract_version': True, 'uploads_enabled': True}):
            send = AsyncMock()
            with self.assertRaises(APIError):
                await self.run_flow(api=AsyncMock(return_value=capabilities), upload=send)
            send.assert_not_awaited()

    async def test_reserve_claim_upload_verify_order_and_exact_identity(self):
        result, api, reserve, send, verify, recover = await self.run_flow()
        self.assertEqual(result[0].id, 12)
        self.assertEqual(api.await_count, 2)
        self.assertEqual(api.await_args_list[1].args, ('POST', '/post-image-uploads/12/begin'))
        self.assertEqual(send.await_args.kwargs['public_id'], reservation().public_id)
        verify.assert_awaited_once()
        recover.assert_not_awaited()

    async def test_started_upload_is_reconciled_instead_of_resent(self):
        result, api, reserve, send, verify, recover = await self.run_flow(state='reconciliation_required')
        self.assertEqual(result[1], 'recovered')
        send.assert_not_awaited()
        recover.assert_awaited_once()
        self.assertEqual(api.await_count, 1)

    async def test_attached_reservation_does_not_upload_again(self):
        result, api, reserve, send, verify, recover = await self.run_flow(state='attached')
        self.assertIsNone(result[1])
        send.assert_not_awaited()
        verify.assert_not_awaited()
        recover.assert_not_awaited()

    async def test_uncertain_claim_prevents_provider_write(self):
        api=AsyncMock(side_effect=[{'contract_version': 1, 'uploads_enabled': True}, APIError('uncertain', 503)])
        send=AsyncMock()
        with self.assertRaises(APIError):
            await self.run_flow(api=api, upload=send)
        send.assert_not_awaited()
        self.assertEqual(api.await_count, 2)

    async def test_changed_editor_stops_before_any_write(self):
        send=AsyncMock()
        count=0
        def current():
            nonlocal count
            count+=1
            return count==1
        with self.assertRaises(APIError):
            await self.run_flow(current=current, upload=send)
        send.assert_not_awaited()

    async def test_upload_failure_is_not_retried(self):
        send=AsyncMock(side_effect=APIError('timeout', 503))
        with self.assertRaises(APIError):
            await self.run_flow(upload=send)
        send.assert_awaited_once()


class SocialImageIntegrationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'fixture.png'
        self.path.write_bytes(b'\x89PNG\r\n\x1a\nfixture')
        self.state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.user_id=7
        self.state.session_token='session'
        self.state.post_editor_token='a'*32
        self.state.post_editor_open=True
        self.state.edit_post_body='Rascunho'
        self.state._post_image_path=str(self.path)
        self.state.post_image_mime='image/png'

    async def save(self, *, enabled=True, prepare=None, call=None, body='Rascunho'):
        with patch.dict(os.environ, {'CLOUDINARY_UPLOADS_ENABLED': str(enabled).lower()}), \
             patch.object(SocialState, '_require_user', new=AsyncMock(return_value=True)), \
             patch.object(SocialState, '_persist_post_media', new=AsyncMock(return_value=0)), \
             patch.object(SocialState, '_refresh_posts', new=AsyncMock()), \
             patch.object(SocialState, '_call', new=call or AsyncMock(return_value={})), \
             patch('Codeboxd_main.state.social.prepare_image',
                   new=prepare or AsyncMock(return_value=(reservation(),SimpleNamespace(version=2)))), \
             patch('Codeboxd_main.state.social.upload_file', new=AsyncMock()) as legacy:
            async for _ in self.state.save_post({'body': body}):
                pass
            return legacy

    async def test_external_image_is_committed_as_json_without_legacy_upload(self):
        api=AsyncMock(return_value={'id': 9})
        legacy=await self.save(call=api)
        legacy.assert_not_awaited()
        payload=api.await_args.args[2]
        self.assertEqual(payload['image_reservation_id'],12)
        self.assertEqual(payload['image_version'],2)
        self.assertFalse(self.state.post_editor_open)
        self.assertFalse(self.path.exists())

    async def test_external_failure_keeps_draft_file_and_does_not_fallback(self):
        self.state._navigation_reads={'old': {'payload': 'stale'}}
        generation=self.state._navigation_generation
        api=AsyncMock()
        legacy=await self.save(prepare=AsyncMock(side_effect=APIError('A operação está pendente.')), call=api)
        legacy.assert_not_awaited()
        api.assert_not_awaited()
        self.assertTrue(self.path.exists())
        self.assertTrue(self.state.post_editor_open)
        self.assertEqual(self.state.edit_post_body,'Rascunho')
        self.assertEqual(self.state._navigation_reads,{})
        self.assertGreaterEqual(self.state._navigation_generation,generation+2)

    async def test_commit_timeout_preserves_draft_without_second_write(self):
        api=AsyncMock(side_effect=APIError('Timeout',503))
        await self.save(call=api)
        api.assert_awaited_once()
        self.assertTrue(self.path.exists())
        self.assertTrue(self.state.post_editor_open)

    async def test_response_for_previous_account_does_not_commit_or_clear_new_editor(self):
        async def changed(**kwargs):
            self.state.session_token='another-session'
            self.state.post_editor_token='c'*32
            self.state.edit_post_body='Outro rascunho'
            return reservation(), SimpleNamespace(version=2)
        api=AsyncMock()
        await self.save(prepare=AsyncMock(side_effect=changed),call=api)
        api.assert_not_awaited()
        self.assertTrue(self.path.exists())
        self.assertEqual(self.state.edit_post_body,'Outro rascunho')

    async def test_flag_off_preserves_legacy_upload_path(self):
        prepare=AsyncMock()
        legacy=await self.save(enabled=False,prepare=prepare)
        legacy.assert_awaited_once()
        prepare.assert_not_awaited()

    async def test_no_attachment_does_not_depend_on_cloudinary(self):
        self.state._post_image_path=''
        prepare=AsyncMock()
        api=AsyncMock(return_value={'id': 9})
        await self.save(prepare=prepare,call=api)
        prepare.assert_not_awaited()
        api.assert_awaited_once()
        self.assertNotIn('image_reservation_id', api.await_args.args[2])

    async def test_empty_body_is_rejected_before_external_upload(self):
        prepare=AsyncMock()
        await self.save(body=' ',prepare=prepare)
        prepare.assert_not_awaited()
        self.assertTrue(self.path.exists())

    async def test_image_removal_is_explicit_revision_checked_and_keeps_text(self):
        self.state._post_image_path=''
        self.state.edit_post_id='25'
        self.state.post_existing_image_provider='cloudinary'
        self.state.post_existing_image_revision=3
        self.state.post_image_remove_requested=True
        api=AsyncMock(side_effect=[{'contract_version': 1}, {'id': 25}])
        prepare=AsyncMock()
        await self.save(call=api,prepare=prepare)
        prepare.assert_not_awaited()
        self.assertEqual(api.await_args.args[:2],('PUT','/posts/25'))
        self.assertEqual(api.await_args.args[2]['image_action'],'remove')
        self.assertEqual(api.await_args.args[2]['expected_image_revision'],3)
        self.assertEqual(api.await_args.args[2]['body'],'Rascunho')

    async def test_removal_is_not_sent_to_an_old_backend(self):
        self.state._post_image_path=''
        self.state.edit_post_id='25'
        self.state.post_image_remove_requested=True
        api=AsyncMock(return_value={})
        await self.save(call=api)
        self.assertEqual(api.await_count,1)
        self.assertTrue(self.state.post_editor_open)
        self.assertTrue(self.state.post_image_remove_requested)

    async def test_replacement_sends_revision_and_reservation_without_legacy_file(self):
        self.state.edit_post_id='25'
        self.state.post_existing_image_provider='cloudinary'
        self.state.post_existing_image_revision=3
        api=AsyncMock(return_value={'id':25})
        await self.save(call=api)
        self.assertEqual(api.await_args.args[:2],('PUT','/posts/25'))
        self.assertEqual(api.await_args.args[2]['image_action'],'replace')
        self.assertEqual(api.await_args.args[2]['expected_image_revision'],3)

    async def test_disabled_upload_does_not_reprocess_existing_cloudinary_image(self):
        self.state.post_existing_image_provider='cloudinary'
        legacy=await self.save(enabled=False)
        legacy.assert_not_awaited()
        self.assertTrue(self.path.exists())
        self.assertTrue(self.state.post_editor_open)

    async def test_existing_external_image_is_read_even_when_upload_flag_is_off(self):
        api=AsyncMock(side_effect=[[
            {'id': 25, 'user_id': 7, 'body': 'Publicação', 'image_provider': 'cloudinary',
             'image_url': 'https://res.cloudinary.com/fixture/image/upload/v1/own.png',
             'image': {'url': 'https://legacy.invalid/old.png'}, 'image_revision': 3}], [], []])
        with patch.object(SocialState,'_call',new=api), \
             patch.object(SocialState,'_person',return_value={'display_name':'Pessoa','avatar_url':''}), \
             patch.dict(os.environ,{'CLOUDINARY_UPLOADS_ENABLED':'false'}):
            await self.state._refresh_posts()
        self.assertEqual(self.state.posts[0]['image_url'],
                         'https://res.cloudinary.com/fixture/image/upload/v1/own.png')
        self.assertEqual(self.state.posts[0]['image_revision'],'3')


if __name__ == '__main__':
    unittest.main()
