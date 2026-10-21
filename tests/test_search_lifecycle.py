import asyncio
import os
import unittest
from unittest.mock import AsyncMock, patch

import httpx
import reflex as rx

from Codeboxd_main.services import catalog
from Codeboxd_main.state.social import SocialState


class SearchLifecycleTests(unittest.IsolatedAsyncioTestCase):
    async def test_repeated_public_search_uses_cache_but_query_and_page_stay_separate(self):
        for kind in ('movie','series','book'):
            with self.subTest(kind=kind):
                catalog._public_cache.clear()
                self.addCleanup(catalog._public_cache.clear)
                client=AsyncMock()
                client.get.return_value=httpx.Response(200,json={'results':[],'docs':[]},
                    request=httpx.Request('GET','https://example.invalid/search'))
                context=AsyncMock(); context.__aenter__.return_value=client
                with patch.dict(os.environ,{'TMDB_READ_TOKEN':'fictional'}), \
                     patch.object(catalog.httpx,'AsyncClient',return_value=context):
                    await catalog.search_one('Dune',kind,1)
                    await catalog.search_one('Dune',kind,1)
                    self.assertEqual(client.get.await_count,1)
                    await catalog.search_one('Dune',kind,2)
                    await catalog.search_one('Batman',kind,1)
                    self.assertEqual(client.get.await_count,3)

    async def test_search_and_continuation_ignore_results_after_leaving_route(self):
        for more in (False,True):
            with self.subTest(more=more):
                root=rx.State(_reflex_internal_init=True)
                root.router.url.path='/'
                state=root.get_substate(SocialState.get_full_name().split('.'))
                state.submitted_query='Batman'; state.search_type='all'
                state.search_active=True
                started,release=asyncio.Event(),asyncio.Event()
                async def search(*args,**kwargs):
                    started.set(); await release.wait()
                    return [catalog.media('tmdb','movie','1','Batman')],[]
                async def drain():
                    events=state.more_results() if more else state.search({'query':'Batman'})
                    async for _ in events: pass
                with patch.object(catalog,'search',side_effect=search):
                    pending=asyncio.create_task(drain())
                    await started.wait()
                    root.router.url.path='/obra/2'
                    state.search_results=[{'title':'Current'}]
                    release.set(); await pending
                self.assertEqual(state.search_results,[{'title':'Current'}])
