import unittest
import reflex as rx
from unittest.mock import AsyncMock, patch
from Codeboxd_main.state.social import SocialState
from Codeboxd_main.services.api import APIError


class SocialTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))

    async def test_identity_switch_clears_private_data(self):
        s=self.state
        s.session_token='second-user'; s.user_id=1; s._identity=1
        s.library=[{'review':'private'}]; s.selected_list={'id':'2','user_id':'1'}
        s.edit_post_id='3'; s.edit_post_body='old draft'; s.liked_posts=['4']
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value={'id':2,'role':'member'})):
            self.assertTrue(await s._validate_session())
        self.assertEqual(s.user_id,2)
        self.assertEqual(s.library,[])
        self.assertEqual(s.selected_list['id'],'')
        self.assertEqual(s.edit_post_body,'')
        self.assertEqual(s.liked_posts,[])

    async def test_expiration_clears_social_data(self):
        s=self.state
        s.session_token='expired'; s.user_id=1; s._identity=1
        s.comments=[{'body':'old'}]; s.selected_review='old review'
        s._failure(APIError('Expired',401))
        self.assertEqual(s.comments,[])
        self.assertEqual(s.selected_review,'')
        self.assertEqual(s._token(),'')

    async def test_missing_identity_never_writes(self):
        with patch('Codeboxd_main.state.social.request',new=AsyncMock()) as request:
            await self.state.save_interaction({'rating':'5','status':'completed'})
        request.assert_not_awaited()

    async def test_invalid_rating_does_not_persist_media(self):
        s=self.state
        s.user_id=1; s._identity=1; s.session_token='valid'
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value={'id':1})),patch('Codeboxd_main.state.social.request',new=AsyncMock()) as request:
            for rating in ('nan','inf','5.5','1.2','-1'):
                await s.save_interaction({'rating':rating})
        request.assert_not_awaited()

    async def test_search_link_carries_external_identity(self):
        s=self.state
        s._results={'tmdb:movie:42':{'id':0,'external_source':'tmdb','media_type':'movie','external_id':'42'}}
        result=await s.open_result('tmdb:movie:42')
        self.assertIn('external_id',str(result))
        self.assertIn('42',str(result))

    async def test_pagination_keeps_all_records(self):
        first=[{'id':i} for i in range(100)]
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=[first,[{'id':100}]])) as request:
            result=await self.state._call('GET','/media')
        self.assertEqual(len(result),101)
        self.assertEqual(request.call_args.kwargs['params'],{'page':2,'per_page':100})

    async def test_nested_profile_pagination_does_not_truncate_statistics(self):
        first={'profile':{'user_id':1},'followers':[{'id':i} for i in range(100)],'following':[],'interactions':[]}
        second={'profile':{'user_id':1},'followers':[{'id':100}],'following':[],'interactions':[]}
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=[first,second])):
            result=await self.state._call('GET','/profiles/1')
        self.assertEqual(len(result['followers']),101)

    async def test_loading_flag_is_cleared_on_redirect(self):
        events=[event async for event in self.state.visit('library')]
        self.assertFalse(self.state.busy)
        self.assertEqual(self.state.visible_count,20)
        self.assertTrue(events)


if __name__=='__main__': unittest.main()
