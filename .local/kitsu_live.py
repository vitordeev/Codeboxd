import asyncio, json, sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from Codeboxd_main.services import catalog

async def main():
    ranking=await catalog.home_collection('anime_rated')
    results,errors=await catalog.search('Cowboy Bebop','anime')
    detail=await catalog.detail(results[0])
    legacy=await catalog.detail(catalog.media('jikan','anime','20','Naruto'))
    related,trailers,reviews=await asyncio.gather(catalog.recommendations(detail),catalog.trailers(detail),catalog.reviews(detail))
    checks={'ranking_items':len(ranking),'search_items':len(results),'search_errors':errors,
        'detail_title':detail['title'],'source':detail['external_source'], 'cover':bool(detail['cover_url']),
        'mal_id':detail['details'].get('MyAnimeList ID'), 'related':len(related),'trailers':len(trailers),
        'reviews':len(reviews),'legacy_title':legacy['title'],'legacy_identity':legacy['identity_key'],
        'legacy_kitsu_id':legacy['details'].get('Kitsu ID')}
    print(json.dumps(checks,ensure_ascii=True),flush=True)
    assert ranking and results and not errors and detail['external_source']=='kitsu'
    assert legacy['external_id']=='20' and legacy['details']['Kitsu ID']!='20'
    Path('.local/kitsu-live-result.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
asyncio.run(main())
