import asyncio, json, os, time
from datetime import datetime, timezone
from pathlib import Path
import httpx
from dotenv import load_dotenv
load_dotenv()

async def main():
    checks=[
      ('Kitsu search','https://kitsu.io/api/edge/anime',{'filter[text]':'Cowboy Bebop','page[limit]':2},{}),
      ('Kitsu ranking','https://kitsu.app/api/edge/anime',{'sort':'-averageRating','filter[nsfw]':'false','page[limit]':20,'include':'mappings'},{}),
      ('Kitsu detail','https://kitsu.app/api/edge/anime/1',{'include':'categories,mappings'},{}),
      ('Kitsu legacy mapping','https://kitsu.app/api/edge/mappings',{'filter[externalSite]':'myanimelist/anime','filter[externalId]':'1','include':'item'},{}),
      ('Kitsu relations','https://kitsu.app/api/edge/anime/1/media-relationships',{'include':'destination','page[limit]':8},{}),
      ('Kitsu reviews','https://kitsu.app/api/edge/reviews',{'filter[mediaType]':'Anime','filter[mediaId]':'1','include':'user','page[limit]':3},{}),
      ('Jikan ranking','https://api.jikan.moe/v4/top/anime',{'limit':20,'sfw':'true'},{}),
      ('Open Library','https://openlibrary.org/search.json',{'title':'Duna','limit':2,'fields':'key,title'},{}),
    ]
    token=os.getenv('TMDB_READ_TOKEN','').strip()
    if token: checks.append(('TMDB','https://api.themoviedb.org/3/movie/popular',{'language':'pt-BR'},{'Authorization':'Bearer '+token}))
    reports=[]
    async with httpx.AsyncClient(timeout=20,follow_redirects=True,headers={'User-Agent':'Codeboxd/1.0','Accept':'application/vnd.api+json'}) as client:
        for name,url,params,headers in checks:
            start=time.monotonic()
            try:
                r=await client.get(url,params=params,headers=headers)
                try: body=r.json()
                except ValueError: body={}
                report={'name':name,'http':r.status_code,'host':r.url.host,'seconds':round(time.monotonic()-start,2)}
                if r.is_error: report['error']=body.get('message') or body.get('errors') or body.get('status_message') or r.reason_phrase
                else:
                    data=body.get('data',body.get('docs',body.get('results')))
                    report['items']=len(data) if isinstance(data,list) else 1
                    if name.startswith('Kitsu'):
                        report['sample']=data[:1] if isinstance(data,list) else data
                        report['included']=body.get('included',[])[:4]
                reports.append(report)
                print(json.dumps({k:v for k,v in report.items() if k not in ('sample','included')},ensure_ascii=True),flush=True)
            except httpx.HTTPError as exc:
                reports.append({'name':name,'error':type(exc).__name__,'seconds':round(time.monotonic()-start,2)})
                print(json.dumps(reports[-1]),flush=True)
    Path('.local/kitsu-diagnostic.json').write_text(json.dumps({'checked_at':datetime.now(timezone.utc).isoformat(),'checks':reports},ensure_ascii=False,indent=2),encoding='utf8')
asyncio.run(main())
