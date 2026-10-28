import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx
from Codeboxd_main.state.social import SocialState
from Codeboxd_main.services.api import APIError


async def finish(event):
    async for _ in event: pass


class PostInteractionsTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.s=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.s.user_id=7; self.s.session_token='fixture-token'
        self.s.posts=[dict(id='55',likes_count='0',comments_count='0'),dict(id='56',likes_count='0',comments_count='0')]
        self.s.selected_post='55'; self.s.comment_editor_token='draft-token'
        self.form=dict(post_id='55',comment_token='draft-token',body='Meu comentário')

    async def test_late_discussion_cannot_replace_another_post(self):
        started=asyncio.Event(); release=asyncio.Event()
        async def call(method,path):
            if path=='/posts/55/discussion':
                started.set(); await release.wait()
                return dict(likes=[],comments=[dict(id=1,user_id=7,body='Antigo')])
            return dict(likes=[],comments=[dict(id=2,user_id=7,body='Atual')])
        with patch.object(SocialState,'_call',new=AsyncMock(side_effect=call)):
            old=asyncio.create_task(finish(self.s.discussion('55')))
            await started.wait(); await finish(self.s.discussion('56'))
            release.set(); await old
        self.assertEqual(self.s.selected_post,'56')
        self.assertEqual(self.s.comments[0]['body'],'Atual')
        self.assertFalse(self.s.discussion_loading)

    async def test_close_discussion_discards_pending_response(self):
        async def call(*args):
            self.s.close_discussion()
            return dict(likes=[],comments=[dict(id=1,user_id=7,body='Antigo')])
        with patch.object(SocialState,'_call',new=AsyncMock(side_effect=call)):
            await finish(self.s.discussion('55'))
        self.assertEqual(self.s.comments,[]); self.assertEqual(self.s.selected_post,'')

    async def test_account_switch_does_not_apply_old_discussion(self):
        async def call(*args):
            self.s.session_token='another-account'
            return dict(likes=[],comments=[dict(id=1,user_id=7,body='Privado')])
        with patch.object(SocialState,'_call',new=AsyncMock(side_effect=call)):
            await finish(self.s.discussion('55'))
        self.assertEqual(self.s.comments,[])

    async def test_like_pending_blocks_duplicate_mutation_and_failure_recovers(self):
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value=dict(likes=[],comments=[]))) as call:
            event=self.s.like('55'); await anext(event)
            self.assertIn('55',self.s.liking_posts)
            await finish(self.s.like('55')); await finish(event)
        self.assertEqual([c.args[0] for c in call.await_args_list],['GET','PUT'])
        self.assertIn('55',self.s.liked_posts)
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=APIError('Falha',503))):
            await finish(self.s.like('55'))
        self.assertEqual(self.s.liking_posts,[])
        self.assertIn('55',self.s.liked_posts)
        self.assertEqual(self.s.post_interaction_errors['55'],'Falha')

    async def test_comment_pending_and_completed_replay_send_only_once(self):
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value=dict(likes=[],comments=[]))) as call:
            event=self.s.save_comment(self.form); await anext(event)
            await finish(self.s.save_comment(self.form)); await finish(event)
            await finish(self.s.save_comment(self.form))
        self.assertEqual([c.args[0] for c in call.await_args_list],['POST','GET'])
        self.assertFalse(self.s.comment_saving); self.assertEqual(self.s.edit_comment_body,'')

    async def test_failed_comment_preserves_draft_without_retry(self):
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=APIError('Indisponível',503))) as call:
            await finish(self.s.save_comment(self.form))
        self.assertEqual(call.await_count,1)
        self.assertEqual(self.s.edit_comment_body,self.form['body'])
        self.assertEqual(self.s.comment_editor_token,'draft-token')
        self.assertEqual(self.s.discussion_error,'Indisponível')
        self.assertEqual(self.s.notice,'')

    async def test_saved_comment_with_failed_refresh_does_not_repost(self):
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(side_effect=[{},APIError('Refresh',503)])) as call:
            await finish(self.s.save_comment(self.form)); await finish(self.s.save_comment(self.form))
        self.assertEqual(call.await_count,2)
        self.assertIn('Comentário salvo',self.s.discussion_error)
        self.assertEqual(self.s.edit_comment_body,'')

    async def test_context_changed_during_auth_does_not_send_to_another_post(self):
        async def auth():
            self.s.selected_post='56'
            return True
        with patch.object(SocialState,'_require_user',new=AsyncMock(side_effect=auth)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.save_comment(self.form))
        call.assert_not_awaited()

    async def test_missing_form_context_and_foreign_comment_cannot_mutate(self):
        self.s.comments=[dict(id='9',user_id='8',body='Outra conta')]
        with patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await finish(self.s.save_comment({'body':'Sem contexto'}))
            await finish(self.s.remove_comment('9'))
        call.assert_not_awaited()

    async def test_delete_own_comment_clears_edit_context_and_blocks_duplicate(self):
        self.s.comments=[dict(id='9',user_id='7',body='Meu texto')]
        self.s.edit_comment('9')
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value=dict(likes=[],comments=[]))) as call:
            event=self.s.remove_comment('9'); await anext(event)
            await finish(self.s.remove_comment('9')); await finish(event)
        self.assertEqual([c.args[0] for c in call.await_args_list],['DELETE','GET'])
        self.assertEqual(self.s.edit_comment_id,''); self.assertEqual(self.s.comments,[])

    async def test_invalid_like_payload_never_sends_a_mutation(self):
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={'comments':[]})) as call:
            await finish(self.s.like('55'))
        self.assertEqual(call.await_count,1)
        self.assertEqual(self.s.liking_posts,[])
        self.assertIn('55',self.s.post_interaction_errors)
