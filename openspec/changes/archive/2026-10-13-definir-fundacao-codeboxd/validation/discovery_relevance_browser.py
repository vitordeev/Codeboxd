"""Live UI regression for vertical catalogs and Spider-Man search relevance."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

expect.set_options(timeout=90000)
output=Path('openspec/changes/definir-fundacao-codeboxd/validation/vertical-relevance-browser-results.json')
results=[]
def record(label, **data):
    results.append(dict(test=label,result='PASS',**data))
    output.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print('PASS '+label,flush=True)

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.set_default_timeout(90000)
    errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto('http://localhost:3013/',wait_until='domcontentloaded')
    grids=page.locator('.popular-grid')
    expect(grids).to_have_count(2)
    expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled()
    for index in (0,1):
        grid=grids.nth(index)
        assert grid.locator('.media-card').count()==20
        bounds=grid.locator('.media-card').evaluate_all('(cards) => cards.map(e => ({x:e.offsetLeft,y:e.offsetTop}))')
        assert len({b['y'] for b in bounds})>=4
        assert grid.evaluate('e => e.scrollWidth <= e.clientWidth')
    record('Movies and series use multiple vertical rows without horizontal scrolling')
    page.get_by_role('button',name='Carregar mais filmes',exact=True).click()
    page.wait_for_function("document.querySelector('.popular-grid').querySelectorAll('.media-card').length > 20")
    expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled()
    assert grids.nth(1).locator('.media-card').count()==20
    record('More movies append in the home section',movie_count=grids.first.locator('.media-card').count())
    page.screenshot(path='.local/vertical-home-desktop.png',full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    bounds=grids.first.locator('.media-card').evaluate_all('(cards) => cards.slice(0,3).map(e => e.getBoundingClientRect().top)')
    assert bounds[0]==bounds[1] and bounds[2]>bounds[1]
    page.screenshot(path='.local/vertical-home-mobile.png')
    record('Mobile uses two columns with content continuing below')
    page.set_viewport_size({'width':1440,'height':1000})
    page.get_by_role('button',name='Filmes',exact=True).click()
    expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled()
    for query in ('homen aranha','homem aranha'):
        page.locator('input[name=query]').fill(query)
        page.get_by_role('button',name='Buscar',exact=True).click()
        expect(page.get_by_role('heading',name='Resultados da busca',exact=True)).to_be_visible()
        expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled()
        cards=page.locator('.catalog-grid .media-card')
        titles=cards.locator('h3').all_text_contents()
        kinds=cards.locator('p').all_text_contents()
        assert titles,query
        assert all('aranh' in title.lower() for title in titles),titles
        assert not any('prov' in title.lower() or 'biblia' in title.lower() for title in titles),titles
        assert any(kind.startswith('Filme') for kind in kinds)
        assert any(not kind.startswith('Filme') for kind in kinds)
        record('Relevant global results for '+query,titles=titles,provider_notices=page.locator('[role=status]').all_text_contents())
    page.screenshot(path='.local/spiderman-search-desktop.png',full_page=True)
    assert not errors,errors
    record('No JavaScript exceptions')
    browser.close()
