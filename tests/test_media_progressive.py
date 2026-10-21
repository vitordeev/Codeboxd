import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import reflex as rx

from Codeboxd_main.services.api import APIError
from Codeboxd_main.state.social import SocialState


class MediaProgressiveTests(unittest.IsolatedAsyncioTestCase):
    async def test_external_primary_keeps_source_identity_in_all_four_types(self):
        for kind,source in (('movie','tmdb'),('series','tmdb'),('anime','jikan'),('book','openlibrary')):
            with self.subTest(kind=kind):
                self.state.router.url.path='/obra'
                self.state.router.url.query_parameters={'external_source':source,'media_type':kind,'external_id':'42'}
                record={'id':0,'identity_key':f'{source}:{kind}:42','external_source':source,
                        'external_id':'42','media_type':kind,'title':'External','description':'Descrição traduzida'}
                with patch.object(SocialState,'_validate_navigation_session',new=AsyncMock(return_value=False)), \
                     patch('Codeboxd_main.services.catalog.detail',new=AsyncMock(return_value=record)), \
                     patch('Codeboxd_main.services.catalog.trailers',new=AsyncMock(return_value=[])), \
                     patch('Codeboxd_main.services.catalog.availability',new=AsyncMock(return_value=[])), \
                     patch('Codeboxd_main.services.catalog.recommendations',new=AsyncMock(return_value=[])), \
                     patch('Codeboxd_main.services.catalog.reviews',new=AsyncMock(return_value=[])):
                    await self.state.load_external_media()
                self.assertEqual(self.state.selected['key'],record['identity_key'])
                self.assertEqual(self.state.selected['description'],'Descrição traduzida')

    async def test_late_saved_review_cannot_close_or_replace_new_work_draft(self):
        self.state._selected_raw={'id':1}
        self.state.user_id=7
        started,release=asyncio.Event(),asyncio.Event()
        async def write(*args,**kwargs):
            started.set(); await release.wait()
            return {}
        with patch.object(SocialState,'_require_user',new=AsyncMock(return_value=True)), \
             patch.object(SocialState,'_call',side_effect=write) as call:
            task=asyncio.create_task(self.state.save_interaction({'rating':'4,5','review':'Old'}))
            await started.wait()
            self.state._selected_raw={'id':2}
            self.state.selected_review='New draft'; self.state.review_editor_open=True
            release.set(); await task
        self.assertEqual(self.state.selected_review,'New draft')
        self.assertTrue(self.state.review_editor_open)
        self.assertFalse(self.state.interaction_saved)
        self.assertEqual(call.await_args.args[2]['media_id'],1)

    async def test_account_change_during_auth_does_not_send_review(self):
        self.state._selected_raw={'id':1}
        async def auth():
            self.state.session_token='new-account'
            return True
        with patch.object(SocialState,'_require_user',side_effect=auth), \
             patch.object(SocialState,'_call',new=AsyncMock()) as call:
            await self.state.save_interaction({'rating':'4,5','review':'Old'})
        call.assert_not_awaited()

    def setUp(self):
        root=rx.State(_reflex_internal_init=True)
        root.router.url.path='/obra/1'
        self.state=root.get_substate(SocialState.get_full_name().split('.'))

    async def test_primary_content_is_published_before_slow_complement_for_all_types(self):
        for kind in ('movie','series','anime','book'):
            with self.subTest(kind=kind):
                started,release=asyncio.Event(),asyncio.Event()
                async def slow(item):
                    started.set(); await release.wait()
                    return [{'title':'Trailer','embed_url':'https://example.invalid'}]
                record={'id':1,'title':'Primary','media_type':kind,'external_source':''}
                with patch.object(SocialState,'_validate_navigation_session',new=AsyncMock(return_value=False)), \
                     patch.object(SocialState,'_call',new=AsyncMock(return_value=record)), \
                     patch('Codeboxd_main.services.catalog.trailers',side_effect=slow), \
                     patch('Codeboxd_main.services.catalog.availability',new=AsyncMock(return_value=[])), \
                     patch('Codeboxd_main.services.catalog.reviews',new=AsyncMock(return_value=[])):
                    updates=self.state._media_updates(False)
                    await anext(updates)
                    self.assertEqual(self.state.selected['title'],'Primary')
                    self.assertTrue(self.state.media_details_loading)
                    async def finish():
                        async for _ in updates: pass
                    pending=asyncio.create_task(finish())
                    await started.wait()
                    self.assertEqual(self.state.trailers,[])
                    release.set(); await pending
                    self.assertFalse(self.state.media_details_loading)
                    self.assertEqual(len(self.state.trailers),1)

    async def test_late_primary_does_not_replace_new_work(self):
        started,release=asyncio.Event(),asyncio.Event()
        async def old(*args,**kwargs):
            started.set(); await release.wait()
            return {'id':1,'title':'Old','media_type':'movie'}
        with patch.object(SocialState,'_validate_navigation_session',new=AsyncMock(return_value=False)), \
             patch.object(SocialState,'_call',side_effect=old):
            task=asyncio.create_task(self.state.load_media())
            await started.wait()
            self.state.router.url.path='/obra/2'
            self.state.selected={'title':'New'}
            release.set(); await task
        self.assertEqual(self.state.selected['title'],'New')

    async def test_late_optional_results_and_errors_do_not_replace_new_work(self):
        for helper,provider in (('_load_trailers','trailers'),('_load_availability','availability'),
                                ('_load_recommendations','recommendations'),('_load_community_reviews','reviews')):
            for error in (False,True):
                with self.subTest(helper=helper,error=error):
                    self.state._selected_raw={'id':1,'identity_key':'tmdb:movie:1','external_source':'tmdb'}
                    self.state.media_details_error=''
                    started,release=asyncio.Event(),asyncio.Event()
                    async def slow(item):
                        started.set(); await release.wait()
                        if error: raise APIError('Old error',503)
                        return [{'id':9,'title':'Old','media_type':'movie'}]
                    with patch('Codeboxd_main.services.catalog.'+provider,side_effect=slow):
                        pending=asyncio.create_task(getattr(self.state,helper)())
                        await started.wait()
                        self.state._selected_raw={'id':2,'identity_key':'tmdb:movie:2'}
                        self.state.trailers=[]; self.state.availability=[]
                        self.state.recommendations=[]; self.state.community_reviews=[]
                        release.set(); await pending
                    self.assertEqual(self.state.media_details_error,'')
                    self.assertEqual(self.state.trailers+self.state.availability+
                                     self.state.recommendations+self.state.community_reviews,[])

    async def test_late_review_does_not_overwrite_current_draft(self):
        self.state._selected_raw={'id':1}
        self.state.user_id=7
        started,release=asyncio.Event(),asyncio.Event()
        async def call(*args,**kwargs):
            started.set(); await release.wait()
            return [{'media_id':1,'status':'completed','review':'Old review','rating':5}]
        with patch.object(SocialState,'_call',side_effect=call):
            pending=asyncio.create_task(self.state._load_personal_interaction('1',True))
            await started.wait()
            self.state._selected_raw={'id':2}
            self.state.selected_review='New draft'
            release.set(); await pending
        self.assertEqual(self.state.selected_review,'New draft')

    async def test_partial_failure_keeps_primary_and_reports_error(self):
        with patch.object(SocialState,'_validate_navigation_session',new=AsyncMock(return_value=False)), \
             patch.object(SocialState,'_call',new=AsyncMock(return_value={'id':1,'title':'Primary'})), \
             patch('Codeboxd_main.services.catalog.trailers',new=AsyncMock(side_effect=APIError('Unavailable',503))), \
             patch('Codeboxd_main.services.catalog.availability',new=AsyncMock(return_value=[])), \
             patch('Codeboxd_main.services.catalog.reviews',new=AsyncMock(return_value=[])):
            await self.state.load_media()
        self.assertEqual(self.state.selected['title'],'Primary')
        self.assertEqual(self.state.media_details_error,'Unavailable')
        self.assertFalse(self.state.media_details_loading)
