"""Read-only public browser checks against the running app and real catalog APIs."""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode

import httpx
from playwright.async_api import async_playwright, expect

from Codeboxd_main.services.translation import _cache


async def main(base, output):
    if output.exists(): raise FileExistsError('Preserve existing evidence; use a new directory')
    output.mkdir(parents=True)
    cases=[]; failure=''; stage='public-references'
    try:
        async with httpx.AsyncClient(timeout=25,follow_redirects=True) as client:
            anime=await client.get('https://kitsu.app/api/edge/anime/1')
            anime.raise_for_status()
            attributes=anime.json()['data']['attributes']
            book=await client.get('https://openlibrary.org/works/OL82563W.json')
            book.raise_for_status()
            book_description=book.json().get('description','')
            if isinstance(book_description,dict): book_description=book_description.get('value','')
        records=[('kitsu','anime','1',attributes.get('synopsis') or attributes.get('description','')),
                 ('openlibrary','book','OL82563W',book_description)]
        if not all(isinstance(item[3],str) and item[3].strip() for item in records):
            raise ValueError('Public reference must have an original description')
        async with async_playwright() as playwright:
            browser=await playwright.chromium.launch(channel='msedge',headless=True)
            try:
                for width in (1440,390):
                    for source,kind,identifier,original in records:
                        context=await browser.new_context(viewport={'width':width,'height':900})
                        try:
                            page=await context.new_page()
                            errors=[]
                            page.on('pageerror',lambda exc:errors.append(type(exc).__name__))
                            query=urlencode(dict(external_source=source,external_id=identifier,media_type=kind))
                            stage=f'{kind}-{width}:navigation'
                            await page.goto(base+'/obra?'+query,wait_until='domcontentloaded',timeout=90000)
                            description=page.locator('.media-detail-description')
                            stage=f'{kind}-{width}:description-visible'
                            await expect(description).to_be_visible(timeout=90000)
                            key=hashlib.sha256(('v1:PT-BR:'+original).encode()).hexdigest()
                            translated=None
                            stage=f'{kind}-{width}:translated-cache-match'
                            for _ in range(80):
                                translated=await asyncio.to_thread(_cache,key)
                                if translated and ' '.join((await description.inner_text()).split())==' '.join(translated.split()): break
                                await asyncio.sleep(.5)
                            if not translated or translated.strip()==original.strip():
                                await page.screenshot(path=str(output/f'failure-{kind}-{width}.png'),full_page=True)
                                raise AssertionError('No translated cache entry for the public reference')
                            await expect(description).to_have_text(translated,timeout=10000)
                            title=(await page.locator('.media-detail-title').inner_text()).strip()
                            if not title or title=='Sem título': raise AssertionError('Missing media identity')
                            await page.reload(wait_until='domcontentloaded')
                            await expect(description).to_have_text(translated,timeout=60000)
                            assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
                            assert not errors,errors
                            await page.screenshot(path=str(output/f'{kind}-{width}.png'),full_page=True)
                            result=dict(source=source,kind=kind,external_id=identifier,width=width,
                                translated_cache_matches_dom=True,different_from_original=True,
                                reload_preserves_translation=True,identity_present=True,
                                original_sha256=hashlib.sha256(original.encode()).hexdigest(),
                                translated_sha256=hashlib.sha256(translated.encode()).hexdigest(),
                                javascript_errors=errors,passed=True)
                            cases.append(result)
                            print(json.dumps(result),flush=True)
                        finally: await context.close()
            finally: await browser.close()
    except Exception as exc:
        failure=stage+':'+type(exc).__name__
        print('VALIDATION_FAILURE: '+failure,flush=True)
    finally:
        (output/'result.json').write_text(json.dumps(dict(layer='browser-real-public-catalog',
            base=base,expected=4,completed=cases,failure=failure,
            cache_reuse_mechanism_previously_tested=True,
            provider_request_count_in_running_server_measured=False),indent=2),encoding='utf-8')
    if failure or len(cases)!=4: raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',default='http://127.0.0.1:3000')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    asyncio.run(main(args.base.rstrip('/'),args.output.resolve()))
