"""Offline library/lists measurements using real handlers and MockTransport.

No real account, server, credentials or network. Synthetic mutations, including
default-list preparation, affect only in-memory fixture data.
Run: python -B -m tools.library_lists_performance_scenario
"""
import argparse
import asyncio
import json
import statistics
import time
from unittest.mock import patch

import httpx
import reflex as rx

from Codeboxd_main.services import api
from Codeboxd_main.state.social import DEFAULT_MEDIA_LISTS, SocialState
from tools.performance_probe import HttpProbe


CASES=('ready','slow-people','people-429','media-429','missing-defaults','legacy-defaults')


async def run_sample(section='library',case='ready',size=5,delay_ms=50,visits=1):
    if (section not in ('library','lists') or case not in CASES or not 0<=size<=1000
            or not 0<=delay_ms<=1000 or not 1<=visits<=5):
        raise ValueError('Invalid synthetic scenario')
    root=rx.State(_reflex_internal_init=True)
    root.router.url.path='/biblioteca' if section=='library' else '/listas'
    state=root.get_substate(SocialState.get_full_name().split('.'))
    state.session_token='synthetic-library-token'
    media=[{'id':i,'title':f'Synthetic {i}','media_type':'book'} for i in range(1,size+1)]
    profiles=[{'user_id':i,'username':f'synthetic-{i}','display_name':'Synthetic'}
              for i in range(1,size+1)]
    interactions=[{'media_id':i,'status':'completed','rating':1.5} for i in range(1,size+1)]
    own=[{'id':i+10,'title':f'Own {i}','user_id':7,'is_public':False}
         for i in range(1,size+1)]
    if case!='missing-defaults':
        own.extend({'id':i,'title':title,'description':description,'user_id':7,'is_public':True}
                   for i,(title,description) in enumerate(DEFAULT_MEDIA_LISTS,1))
    if case=='legacy-defaults':
        own[ -1 ]['title']='jã¡ assisti / li'
        own.append({'id':9999,'title':'gostei','user_id':7,'is_public':True})
    public=[{'id':i+20000,'title':f'Public {i}','user_id':8,'is_public':True}
            for i in range(1,size+1)]

    def page_of(items,request):
        page=int(request.url.params.get('page','1'))
        per_page=int(request.url.params.get('per_page','100'))
        return items[(page-1)*per_page:page*per_page]

    async def respond(request):
        path=request.url.path
        if case=='slow-people' and path=='/profiles':
            await asyncio.sleep(delay_ms/1000)
        if ((case=='people-429' and path=='/profiles') or
                (case=='media-429' and path=='/media')):
            return httpx.Response(429,headers={'Retry-After':'20'},json={})
        payloads={'/media':media,'/profiles':profiles,'/interactions':interactions,
                  '/lists':own,'/lists/public':public}
        if path=='/auth/me':
            result={'id':7,'role':'member','account_status':'active'}
        elif request.method=='GET' and path in payloads:
            result=page_of(payloads[path],request)
        elif request.method=='POST' and path=='/lists':
            result=dict(json.loads(request.content),id=30000+len(own),user_id=7)
            own.append(result)
        elif request.method=='PUT' and path.startswith('/lists/'):
            result=next(item for item in own if item['id']==int(path.rsplit('/',1)[1]))
            result.update(json.loads(request.content))
        elif request.method=='GET' and path=='/lists/9999/items':
            result=[]
        elif request.method=='DELETE' and path=='/lists/9999':
            own[:]=[item for item in own if item['id']!=9999]
            result={}
        else:
            raise AssertionError('Unexpected synthetic operation')
        return httpx.Response(200,json=result)

    original_client=httpx.AsyncClient
    def local_client(*args,**kwargs):
        kwargs['transport']=httpx.MockTransport(respond)
        return original_client(*args,**kwargs)

    probe=HttpProbe()
    timings=[]
    with probe.capture(),patch.object(api,'base_url',return_value='https://scenario.xano.io'), \
            patch.object(api.httpx,'AsyncClient',side_effect=local_client):
        for index in range(visits):
            count_before=probe.total
            started=time.perf_counter()
            first_content_ms=None
            async for _ in state.visit(section):
                if first_content_ms is None and (state.library if section=='library' else state.lists):
                    first_content_ms=round((time.perf_counter()-started)*1000,3)
            # Permit already-scheduled gather siblings to finish within this capture.
            await asyncio.sleep(0)
            timings.append(dict(visit=index+1,requests=probe.total-count_before,
                first_content_ms=first_content_ms,total_ms=round((time.perf_counter()-started)*1000,3)))
        loaded=state.library if section=='library' else state.lists
        visible_before=len(state.visible_library if section=='library' else state.visible_lists)
        before_more=probe.total
        state.show_more()
        visible_after=len(state.visible_library if section=='library' else state.visible_lists)
        more_requests=probe.total-before_more

    return dict(layer='simulated-handlers',section=section,case=case,size=size,
        injected_people_delay_ms=delay_ms if case=='slow-people' else 0,visits=timings,
        loaded_count=len(loaded),unique_loaded_count=len({item['id'] for item in loaded}),
        catalog_count=len(state.catalog_items),
        library_titles_resolved=sum(item['title']!='Sem título' for item in state.library),
        private_lists_count=sum(item.get('is_public')=='False' for item in state.lists),
        public_lists_count=sum(item.get('is_public')=='True' for item in state.lists),
        visible_before=visible_before,visible_after_more=visible_after,
        show_more_requests=more_requests,error_present=bool(state.notice),busy_after=state.busy,
        default_lists_ready=all(any(item['title']==title for item in own) for title,_ in DEFAULT_MEDIA_LISTS),
        simulated_writes=sum(event['method'] not in ('GET','HEAD') for event in probe.events),
        browser_measured=False,remote_measured=False,**probe.report())


async def run_suite(samples=5):
    if not 1<=samples<=10: raise ValueError('Invalid sample count')
    scenarios=[(section,case,size,visits) for section in ('library','lists')
        for case,size,visits in [('ready',0,1),('ready',5,1),('ready',100,1),
            ('ready',250,1),('ready',5,2),('slow-people',5,1),('people-429',5,1),('media-429',5,1)]]
    scenarios.extend([('lists','missing-defaults',5,1),('lists','legacy-defaults',5,1)])
    results=[]
    for section,case,size,visits in scenarios:
        rows=[await run_sample(section,case,size,visits=visits) for _ in range(samples)]
        times=[row['visits'][0]['total_ms'] for row in rows]
        results.append(dict(section=section,case=case,size=size,visits_per_sample=visits,
                            median_ms=statistics.median(times),worst_ms=max(times),samples=rows))
    return dict(layer='simulated-handlers',scenarios=results)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples',type=int,choices=range(1,11),default=5)
    args=parser.parse_args()
    print(json.dumps(asyncio.run(run_suite(args.samples)),indent=2))
