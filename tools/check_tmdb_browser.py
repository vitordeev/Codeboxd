"""Read public TMDB shelves from the running normal app; never logs credentials."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


def check():
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(channel='msedge',headless=True)
        try:
            page=browser.new_page(viewport={'width':1440,'height':900})
            page.goto('http://127.0.0.1:3030/',wait_until='domcontentloaded')
            results={}
            for title in ('Agora nos cinemas','Filmes muito bem avaliados','No radar: próximos filmes'):
                shelf=page.locator('.catalog-shelf').filter(has=page.get_by_role('heading',name=title,exact=True))
                shelf.locator('.shelf-card').first.wait_for(timeout=90000)
                results[title]=shelf.locator('.shelf-card').count()
            assert all(count==20 for count in results.values()), 'Incomplete TMDB shelves'
            return dict(layer='browser-real-public-tmdb',shelves=results,passed=True)
        finally: browser.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists(): raise SystemExit('Choose a new output; existing evidence is preserved.')
    result=check()
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True))
