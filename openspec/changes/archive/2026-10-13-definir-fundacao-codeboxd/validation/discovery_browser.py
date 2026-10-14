"""Browser checks against the current production test instance on port 3013."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

expect.set_options(timeout=60000)
results=[]
output=Path('openspec/changes/definir-fundacao-codeboxd/validation')
def record(label):
    results.append(label)
    (output/'discovery-browser-results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
    print('PASS '+label,flush=True)

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page()
    page.set_default_timeout(60000)
    errors=[]
    page.on('pageerror',lambda error: (errors.append(str(error)), print('BROWSER ERROR '+str(error.stack),flush=True)))
    page.goto('http://localhost:3013/',wait_until='domcontentloaded')
    expect(page.locator('.media-shelf').first).to_be_visible()
    expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled()
    assert page.locator('.media-shelf').first.locator('.media-card').count()==20
    assert page.locator('.media-shelf').nth(1).locator('.media-card').count()==20
    record('Home shows 20 movies and 20 series')
    image=page.locator('.media-shelf .media-cover').first
    image.scroll_into_view_if_needed()
    page.wait_for_function("document.querySelector('.media-shelf .media-cover').naturalWidth > 0")
    frame=page.locator('.media-shelf .cover-frame').first
    before=frame.bounding_box()
    page.route('**/__missing_cover__.jpg',lambda route: route.fulfill(status=404,body=''))
    image.evaluate("img => { img.src = '/__missing_cover__.jpg'; }")
    expect(frame.locator('img')).to_have_count(0)
    after=frame.bounding_box()
    assert abs(before['height']-after['height'])<1
    record('Cover loads and image error reveals fallback without layout shift')
    page.screenshot(path='.local/discovery-fixed-desktop.png',full_page=True)
    page.get_by_role('button',name='Filmes',exact=True).click()
    page.wait_for_function("document.querySelectorAll('.catalog-grid .media-card').length >= 20")
    expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled()
    initial_count=page.locator('.catalog-grid .media-card').count()
    record('Movie category opens full catalog page')
    page.get_by_role('button',name='Carregar mais resultados',exact=True).click()
    page.wait_for_function("count => document.querySelectorAll('.catalog-grid .media-card').length > count",arg=initial_count)
    expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled()
    record('Movie catalog loads additional page')
    page.locator('input[name=query]').fill('Batman')
    page.get_by_role('button',name='Buscar',exact=True).click()
    expect(page.get_by_role('heading',name='Resultados da busca',exact=True)).to_be_visible()
    expect(page.get_by_role('button',name='Buscar',exact=True)).to_be_enabled(timeout=90000)
    cards=page.locator('.catalog-grid .media-card')
    assert cards.count()>0
    kinds=cards.locator('p').all_text_contents()
    assert any(t.startswith('Filme') for t in kinds)
    assert any(not t.startswith('Filme') for t in kinds), kinds
    assert page.get_by_role('heading',name='Na comunidade',exact=True).count()==0
    record('Search after Movies selection returns multiple media types without unrelated community cards')
    for width in (1440,390):
        page.set_viewport_size({'width':width,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.screenshot(path='.local/discovery-fixed-mobile.png',full_page=True)
    record('Desktop and mobile have no horizontal page overflow')
    assert not errors,errors
    record('No browser JavaScript errors')
    browser.close()
