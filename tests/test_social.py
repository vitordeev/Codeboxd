import asyncio
import unittest
import reflex as rx
from unittest.mock import AsyncMock, patch
from Codeboxd_main.state.social import SocialState
from Codeboxd_main.services.api import APIError


class SocialTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))

    async def test_guest_rating_is_browser_local_and_restores_per_media(self):
        s=self.state
        s.selected={'key':'tmdb:movie:42','title':'Filme'}
        with patch('Codeboxd_main.state.social.request',new=AsyncMock()) as request:
            s.set_selected_rating('5')
        request.assert_not_awaited()
        self.assertIn('tmdb:movie:42',s.guest_ratings)
        s.selected_rating='0'
        s._restore_guest_rating()
        self.assertEqual(s.selected_rating,'5')

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

    async def test_transient_session_failure_does_not_make_user_look_logged_out(self):
        s=self.state
        s.session_token='temporarily-unavailable'; s.user_id=1; s._identity=1; s.user_name='Test'
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(side_effect=APIError('Unavailable',503))):
            self.assertFalse(await s._validate_session())
        self.assertTrue(s.is_authenticated)
        self.assertEqual(s.user_id,1)
        self.assertEqual(s._token(),'temporarily-unavailable')

    async def test_transient_session_failure_does_not_redirect_social_navigation(self):
        s=self.state
        s.session_token='temporarily-unavailable'; s.user_id=1; s._identity=1
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(side_effect=APIError('Unavailable',503))):
            self.assertTrue(await s._require_user())
        self.assertEqual(s.user_id,1)
        self.assertEqual(s._token(),'temporarily-unavailable')

    async def test_logout_clears_private_data_and_redirects_in_same_tab(self):
        s = self.state
        s.auth_token = 'remembered'
        s.session_token = 'tab-session'
        s.user_id = 1
        s._identity = 1
        s.library = [{'review': 'private'}]
        s.edit_post_body = 'private draft'
        result = s.logout_social()
        self.assertEqual(s._token(), '')
        self.assertFalse(s.is_authenticated)
        self.assertEqual(s.library, [])
        self.assertEqual(s.edit_post_body, '')
        self.assertEqual(s._identity, 0)
        payload = {str(key): str(value) for key, value in result.args}
        self.assertEqual(payload['path'], '"/login"')
        self.assertEqual(payload['external'], 'false')
        self.assertEqual(payload['replace'], 'true')

    async def test_missing_identity_never_writes(self):
        with patch('Codeboxd_main.state.social.request',new=AsyncMock()) as request:
            await self.state.save_interaction({'rating':'5','status':'completed'})
        request.assert_not_awaited()

    async def test_guest_cannot_follow_or_publish(self):
        s=self.state
        with patch('Codeboxd_main.state.social.request',new=AsyncMock()) as request:
            self.assertTrue(s.new_post())
            await s.follow('2')
            await s.save_post({'body':'Not public','media_id':'0'})
        request.assert_not_awaited()
        self.assertFalse(s.post_editor_open)

    async def test_in_progress_and_dropped_statuses_and_review_updates_replace_saved_values(self):
        s=self.state
        s.user_id=1; s._identity=1; s.session_token='valid'; s._selected_raw={'id':7}
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value={'id':1,'role':'member'})), \
             patch('Codeboxd_main.state.social.request',new=AsyncMock(return_value={})) as call:
            await s.save_interaction({'status':'in_progress','rating':'3','review':'Em andamento'})
            await s.save_interaction({'status':'dropped','rating':'4.5','review':'Atualizada'})
        first=call.await_args_list[0].kwargs['data']
        second=call.await_args_list[1].kwargs['data']
        self.assertEqual(first['status'],'in_progress')
        self.assertEqual(second['status'],'dropped')
        self.assertEqual(first['rating'],3)
        self.assertEqual(second['rating'],4.5)
        self.assertEqual(first['review'],'Em andamento')
        self.assertEqual(second['review'],'Atualizada')
        self.assertNotIn('user_id',second)

    async def test_search_uses_cached_catalog_when_external_provider_is_unavailable(self):
        s=self.state
        cached={'id':5,'identity_key':'jikan:anime:1','external_source':'jikan','external_id':'1',
            'media_type':'anime','title':'Cowboy Bebop','description':'','cover_url':'','year':1998,'details':{}}
        with patch('Codeboxd_main.state.social.catalog.search',new=AsyncMock(
                return_value=([],['Anime: A fonte de catálogo está indisponível no momento.']))), \
             patch('Codeboxd_main.state.social.request',new=AsyncMock(return_value=[cached])) as request:
            events=[event async for event in s.search({'query':'Cowboy Bebop','kind':'anime'})]
        request.assert_awaited_once()
        self.assertTrue(events)
        self.assertEqual(s.search_results[0]['title'],'Cowboy Bebop')
        self.assertIn('Anime:',s.notice)

    async def test_invalid_rating_does_not_persist_media(self):
        s=self.state
        s.user_id=1; s._identity=1; s.session_token='valid'
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(return_value={'id':1})),patch('Codeboxd_main.state.social.request',new=AsyncMock()) as request:
            for rating in ('nan','inf','5.5','1.2','-1'):
                await s.save_interaction({'rating':rating})
        request.assert_not_awaited()

    async def test_search_link_carries_external_identity(self):
        s=self.state
        s._results={'tmdb:movie:42':{'id':'0','identity_key':'tmdb:movie:42','external_source':'tmdb','media_type':'movie','external_id':'42'}}
        result=await s.open_result('tmdb:movie:42')
        self.assertIn('external_id',str(result))
        self.assertIn('42',str(result))

    async def test_pagination_keeps_all_records(self):
        first=[{'id':i} for i in range(100)]
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=[first,[{'id':100}]])) as request:
            result=await self.state._call('GET','/media')
        self.assertEqual(len(result),101)
        self.assertEqual(request.call_args.kwargs['params'],{'page':2,'per_page':100})

    async def test_call_can_read_only_one_bounded_page(self):
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(return_value=[{'id':i} for i in range(100)])) as request:
            result=await self.state._call('GET','/media',params={'per_page':50},paginate=False)
        self.assertEqual(len(result),100)
        request.assert_awaited_once()

    async def test_feed_legacy_like_fallback_skips_per_post_requests(self):
        s=self.state; s.user_id=1
        posts=[{'id':i,'user_id':2,'body':'Story','created_at':i} for i in range(1,31)]
        async def api(method,path,**kwargs):
            if path=='/feed': return posts
            if path=='/posts': return []
            if path=='/likes': raise APIError('Missing route',404)
            raise AssertionError(path)
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=api)) as request:
            await s._refresh_posts()
        self.assertEqual(s.liked_posts,[])
        self.assertEqual(len(s.posts),30)
        self.assertEqual(request.await_count,3)

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

    async def test_feed_loads_without_n_plus_one_when_legacy_workspace_has_no_likes_route(self):
        s=self.state
        s.user_id=1
        post={'id':7,'user_id':2,'body':'A story','created_at':0}
        async def api(method,path,**kwargs):
            if path=='/feed': return [post]
            if path=='/posts': return []
            if path=='/likes': raise APIError('Missing route',404)
            raise AssertionError(path)
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=api)) as request:
            await s._refresh_posts()
        self.assertEqual(s.liked_posts,[])
        self.assertEqual(s.posts[0]['body'],'A story')
        self.assertEqual(request.await_count,3)

    async def test_like_uses_discussion_to_toggle_state_when_likes_route_is_missing(self):
        s=self.state; s.user_id=1; s.session_token='valid'; s._identity=1
        liked=True; methods=[]
        async def session_api(method,path,**kwargs): return {'id':1,'role':'member'}
        async def social_api(method,path,**kwargs):
            nonlocal liked
            if path=='/posts/7/discussion':
                return {'likes':[{'user_id':1}] if liked else [],'comments':[]}
            if path=='/posts/7/like':
                methods.append(method); liked=method=='PUT'; return {}
            raise AssertionError(path)
        with patch('Codeboxd_main.state.session.request',new=AsyncMock(side_effect=session_api)), \
             patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=social_api)):
            await s.like('7')
            self.assertNotIn('7',s.liked_posts)
            await s.like('7')
        self.assertEqual(methods,['DELETE','PUT'])
        self.assertIn('7',s.liked_posts)

    async def test_feed_does_not_hide_likes_authorization_errors(self):
        async def api(method,path,**kwargs):
            if path=='/likes': raise APIError('Expired',401)
            return []
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=api)):
            with self.assertRaises(APIError):
                await self.state._refresh_posts()


if __name__=='__main__': unittest.main()
