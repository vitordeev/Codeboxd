import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.state.social import SocialState


class RequiredSubmissionContentTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        self.state.user_id=7; self.state._identity=7
        self.state.session_token='fictional-member'
        self.state._selected_raw={'id':9}

    async def test_review_missing_empty_null_or_whitespace_never_authenticates_or_writes(self):
        for value in (None,'',' ','\n\t','\u00a0'):
            for rating in ('0','4,5'):
                with self.subTest(value=value,rating=rating):
                    with patch.object(SocialState,'_require_user',new=AsyncMock()) as auth, \
                         patch.object(SocialState,'_call',new=AsyncMock()) as call:
                        await self.state.save_interaction({'rating':rating,'review':value})
                    auth.assert_not_awaited(); call.assert_not_awaited()
                    self.assertIn('Escreva sua avaliação',self.state.notice)
                    self.assertTrue(self.state.review_editor_open)
                    self.assertFalse(self.state.interaction_saving)

    async def test_review_absent_is_rejected_and_valid_review_is_trimmed(self):
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={})) as call:
            await self.state.save_interaction({'rating':'3'})
            call.assert_not_awaited()
            await self.state.save_interaction({'rating':'3','review':'  Gostei da história. \n'})
        self.assertEqual(call.await_args.args[2]['review'],'Gostei da história.')
        self.assertTrue(self.state.interaction_saved)

    async def test_report_blank_is_rejected_for_every_reason_without_closing_modal(self):
        for reason in ('spam','harassment','inappropriate','other'):
            for value in (None,'',' ','\n\t','\u00a0'):
                with self.subTest(reason=reason,value=value):
                    self.state.open_report('post','15')
                    with patch.object(SocialState,'_call',new=AsyncMock()) as call:
                        async for _ in self.state.submit_report({'reason':reason,'description':value}): pass
                    call.assert_not_awaited()
                    self.assertTrue(self.state.report_dialog_open)
                    self.assertFalse(self.state.report_sending)
                    self.assertIn('Escreva os detalhes',self.state.report_error)

    async def test_report_absent_is_rejected_and_valid_description_is_trimmed(self):
        self.state.open_report('profile','8')
        with patch.object(SocialState,'_call',new=AsyncMock(return_value={})) as call:
            async for _ in self.state.submit_report({'reason':'other'}): pass
            call.assert_not_awaited()
            async for _ in self.state.submit_report({'reason':'other','description':'  Descrição do problema. \n'}): pass
        self.assertEqual(call.await_args.kwargs['data']['description'],'Descrição do problema.')
        self.assertFalse(self.state.report_dialog_open)

    async def test_positive_rating_shortcut_cannot_bypass_written_review(self):
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await self.state.quick_add('completed',4.5,'Já assisti / li')
        call.assert_not_awaited()
        self.assertIn('Escreva sua avaliação',self.state.notice)

    async def test_organizing_without_rating_does_not_require_a_review(self):
        self.state.quick_lists=[{'id':'1','title':'Quero ver / ler'}]
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_ensure_default_lists',new=AsyncMock()), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={})) as call:
            await self.state.quick_add('planned',0,'Quero ver / ler')
        self.assertEqual(call.await_count,2)
        self.assertEqual(call.await_args_list[0].args[2]['rating'],0)
