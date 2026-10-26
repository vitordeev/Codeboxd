import asyncio
import tempfile
import unittest
from pathlib import Path
import reflex as rx
from unittest.mock import AsyncMock, patch
from Codeboxd_main.state.social import SocialState, normalize_rating
from Codeboxd_main.services.api import APIError


class SocialTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))

    async def test_navigation_reads_reuse_copies_and_expire(self):
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(return_value=[{'id':1}])) as request, \
             patch('Codeboxd_main.state.social.time.monotonic',return_value=100) as clock:
            first=await self.state._call('GET','/lists')
            first[0]['id']=999
            self.assertEqual(await self.state._call('GET','/lists'),[{'id':1}])
            request.assert_awaited_once()
            clock.return_value=116
            await self.state._call('GET','/lists')
            self.assertEqual(request.await_count,2)

    async def test_navigation_reads_separate_tokens_params_and_sessions(self):
        other=rx.State(_reflex_internal_init=True).get_substate(SocialState.get_full_name().split('.'))
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(return_value=[])) as request:
            await self.state._call('GET','/media',params={'identity_key':'a'})
            await self.state._call('GET','/media',params={'identity_key':'b'})
            self.state.session_token='another-token'
            await self.state._call('GET','/media',params={'identity_key':'b'})
            await other._call('GET','/media',params={'identity_key':'b'})
            self.assertEqual(request.await_count,4)

    async def test_navigation_write_and_identity_reset_invalidate_reads(self):
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(return_value=[])) as request:
            await self.state._call('GET','/lists')
            await self.state._call('POST','/lists',data={'title':'new'})
            await self.state._call('GET','/lists')
            self.state._reset_personal()
            await self.state._call('GET','/lists')
            self.assertEqual(request.await_count,4)

    async def test_navigation_errors_are_not_cached(self):
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(side_effect=[APIError('Limit',429),[]])) as request:
            with self.assertRaises(APIError):
                await self.state._call('GET','/interactions')
            self.assertEqual(await self.state._call('GET','/interactions'),[])
            self.assertEqual(request.await_count,2)

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

    def test_rating_normalizes_comma_dot_and_all_half_steps(self):
        for step in range(11):
            number = step / 2
            for value in (str(number), str(number).replace('.', ',')):
                self.assertEqual(float(normalize_rating(value)), number)
        self.assertEqual(normalize_rating('4.0'), '4')
        self.assertEqual(normalize_rating('-0'), '0')
        for invalid in ('nan', 'inf', '-inf', '1.2', '1,7', '-0.5', '5.5', 'abc'):
            with self.assertRaises(ValueError): normalize_rating(invalid)

    async def test_guest_half_ratings_and_clear_restore_without_network(self):
        s = self.state
        s.selected = {'key': 'tmdb:movie:42', 'title': 'Filme'}
        with patch('Codeboxd_main.state.social.request', new=AsyncMock()) as request:
            for value, canonical in (('0,5', '0.5'), ('1,5', '1.5'), ('4.5', '4.5'), ('0', '0')):
                s.set_selected_rating(value)
                self.assertEqual(s.selected_rating, canonical)
                s.selected_rating = '5'
                s._restore_guest_rating()
                self.assertEqual(s.selected_rating, canonical)
                self.assertEqual(s.selected_rating_value, float(canonical))
        request.assert_not_awaited()

    def test_invalid_guest_rating_does_not_overwrite_previous_value(self):
        s = self.state
        s.selected = {'key': 'tmdb:movie:42'}
        s.set_selected_rating('1.5')
        saved = s.guest_ratings
        for invalid in ('1.2', 'nan', '6', ''):
            s.set_selected_rating(invalid)
            self.assertEqual(s.selected_rating, '1.5')
            self.assertEqual(s.guest_ratings, saved)

    async def test_comma_rating_is_saved_as_decimal_without_rounding(self):
        s = self.state
        s.user_id = 1; s._identity = 1; s.session_token = 'valid'; s._selected_raw = {'id': 7}
        with patch('Codeboxd_main.state.session.request', new=AsyncMock(return_value={'id': 1})), \
             patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value={})) as request:
            await s.save_interaction({'rating': '1,5', 'status': 'completed', 'review': 'Review'})
        self.assertEqual(request.await_args.kwargs['data']['rating'], 1.5)
        self.assertEqual(request.await_args.kwargs['data']['review'], 'Review')

    async def test_saved_decimal_rating_restores_canonical_selection(self):
        s = self.state
        for number, canonical in ((0.5, '0.5'), (1.5, '1.5'), (4.0, '4')):
            # Each rating represents an independent server/session scenario.
            s._navigation_reads={}
            with patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value=[{
                'media_id': 7, 'status': 'completed', 'rating': number}])):
                await s._load_personal_interaction('7', True)
            self.assertEqual(s.selected_rating, canonical)

    def test_closing_post_editor_discards_only_its_staged_image(self):
        s = self.state
        s.user_id = 1
        s.post_editor_open = True
        s.edit_post_body = 'Canceled draft'
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / 'staged.png'
            image.write_bytes(b'staged fixture')
            original = Path(directory) / 'existing.png'
            original.write_bytes(b'existing image')
            s._post_image_path = str(image)
            s.post_image_filename = 'staged.png'
            s.set_post_editor_open(False)
            self.assertFalse(image.exists())
            self.assertEqual(original.read_bytes(), b'existing image')
        self.assertFalse(s.post_editor_open)
        self.assertEqual(s.edit_post_body, '')
        self.assertEqual(s._post_image_path, '')

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

    async def test_rate_limited_session_validation_preserves_current_post_draft(self):
        s = self.state
        s.session_token = 'current-session'; s.user_id = 1; s._identity = 1
        s.post_editor_open = True
        s.edit_post_body = 'An unsaved draft'
        s.posts = [{'body': 'Previously loaded post'}]
        with patch('Codeboxd_main.state.session.request',
                   new=AsyncMock(side_effect=APIError('Rate limited', 429))):
            self.assertTrue(await s._require_user())
        self.assertTrue(s.post_editor_open)
        self.assertEqual(s.edit_post_body, 'An unsaved draft')
        self.assertEqual(s.posts, [{'body': 'Previously loaded post'}])

    async def test_rejected_session_validation_still_clears_post_draft(self):
        s = self.state
        s.session_token = 'revoked'; s.user_id = 1; s._identity = 1
        s.post_editor_open = True
        s.edit_post_body = 'Private draft'
        with patch('Codeboxd_main.state.session.request',
                   new=AsyncMock(side_effect=APIError('Revoked', 401))):
            self.assertFalse(await s._require_user())
        self.assertFalse(s.post_editor_open)
        self.assertEqual(s.edit_post_body, '')
        self.assertEqual(s._token(), '')

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
            async for _ in s.save_post({'body':'Not public','media_id':'0'}):
                pass
        request.assert_not_awaited()
        self.assertFalse(s.post_editor_open)

    async def test_guest_cannot_open_report_form(self):
        result = self.state.open_report('post', '15')
        self.assertFalse(self.state.report_dialog_open)
        payload = {str(key): str(value) for key, value in result.args}
        self.assertEqual(payload['path'], '"/login"')

    async def test_report_submission_uses_authenticated_target_without_client_snapshot(self):
        s = self.state
        s.session_token = 'member-token'; s.user_id = 4; s._identity = 4
        s.open_report('post', '15')
        with patch('Codeboxd_main.state.session.request',
                   new=AsyncMock(return_value={'id': 4, 'role': 'member'})), \
             patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value={'id': 8, 'status': 'pending'})) as request:
            async for _ in s.submit_report({'reason': 'harassment', 'description': 'Repeated unwanted contact'}):
                pass

        request.assert_awaited_once_with('POST', '/reports', token='member-token', params=None, data={
            'target_type': 'post', 'target_id': '15', 'reason': 'harassment',
            'description': 'Repeated unwanted contact',
        })
        self.assertFalse(s.report_dialog_open)
        self.assertEqual(s.notice, 'Report enviado para análise. O conteúdo não foi alterado.')

    async def test_report_rate_limit_preserves_draft_and_blocks_early_retry(self):
        s = self.state
        s.session_token = 'member-token'; s.user_id = 4; s._identity = 4
        s.open_report('media', '9')
        with patch('Codeboxd_main.state.social.request',
                   new=AsyncMock(side_effect=APIError('Limit', 429, 90))) as request:
            async for _ in s.submit_report({'reason': 'other', 'description': 'Wrong description'}):
                pass
            self.assertTrue(s.report_dialog_open)
            self.assertFalse(s.report_sending)
            self.assertEqual(s.report_description, 'Wrong description')
            self.assertEqual(s.report_reason, 'other')
            self.assertIn('90 segundos', s.report_error)
            async for _ in s.submit_report({'reason': 'other', 'description': 'Wrong description'}):
                pass
            request.assert_awaited_once()
        with patch('Codeboxd_main.state.social.time.monotonic', return_value=s._report_retry_at + 1), \
             patch('Codeboxd_main.state.social.request', new=AsyncMock(return_value={'id': 5, 'status': 'pending'})) as request:
            async for _ in s.submit_report({}):
                pass
        request.assert_awaited_once()
        self.assertFalse(s.report_dialog_open)
        self.assertEqual(s.report_error, '')

    async def test_external_media_report_persists_once_and_uses_real_id(self):
        s = self.state
        s.session_token = 'member-token'; s.user_id = 4; s._identity = 4
        s._selected_raw = {'id': 0, 'external_source': 'tmdb', 'external_id': '42',
                           'media_type': 'movie', 'title': 'Title', 'description': '',
                           'cover_url': '', 'year': 2020, 'details': {}}
        s.open_report('media', '')
        self.assertTrue(s.report_dialog_open)
        saved = {**s._selected_raw, 'id': 17}
        with patch('Codeboxd_main.state.session.request', new=AsyncMock()) as auth, \
             patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=[saved, {'id': 8, 'status': 'pending'}])) as request:
            async for _ in s.submit_report({'reason': 'spam', 'description': 'Conteúdo repetido e indesejado'}):
                pass
        auth.assert_not_awaited()
        self.assertEqual(request.await_count, 2)
        self.assertEqual(request.await_args_list[0].args[:2], ('POST', '/media'))
        self.assertEqual(request.await_args_list[1].kwargs['data']['target_id'], '17')
        self.assertEqual(s.selected['id'], '17')
        self.assertFalse(s.report_dialog_open)

    async def test_report_does_not_duplicate_in_flight_and_shows_other_failures(self):
        s = self.state
        s.session_token = 'member-token'; s.user_id = 4
        s.open_report('post', '15')
        with patch('Codeboxd_main.state.social.request', new=AsyncMock(side_effect=APIError('Conteúdo não encontrado.', 404))) as request:
            sending = s.submit_report({'reason': 'spam', 'description': 'Keep draft'})
            await anext(sending)
            async for _ in s.submit_report({'reason': 'spam'}):
                pass
            request.assert_not_awaited()
            async for _ in sending:
                pass
        request.assert_awaited_once()
        self.assertEqual(s.report_error, 'Conteúdo não encontrado.')
        self.assertEqual(s.report_description, 'Keep draft')
        self.assertTrue(s.report_dialog_open)

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

    async def test_repairs_mojibake_default_list_for_existing_user(self):
        legacy = patch.dict('os.environ', {'DEFAULT_LIST_IDENTITY_ENABLED':'false'})
        legacy.start(); self.addCleanup(legacy.stop)
        s=self.state
        broken={'id':22,'title':'JÃ¡ assisti / li','description':'Obras que vocÃª jÃ¡ terminou.',
                'is_public':True}
        repaired={'id':22,'title':'Já assisti / li','description':'Obras que você já terminou.',
                  'is_public':True}
        created={'id':23,'title':'Quero ver / ler','description':'Obras para descobrir depois.',
                 'is_public':True}
        with patch('Codeboxd_main.state.social.request',new=AsyncMock(
                side_effect=[[broken],repaired,created])) as request:
            await s._ensure_default_lists()

        self.assertEqual(request.await_args_list[1].args[:2],('PUT','/lists/22'))
        self.assertEqual(request.await_args_list[1].kwargs['data'],{
            'title':'Já assisti / li','description':'Obras que você já terminou.','is_public':True})
        self.assertEqual({item['title'] for item in s.quick_lists},{'Quero ver / ler','Já assisti / li'})

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
