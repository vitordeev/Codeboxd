"""Browser baseline/acceptance against an already running isolated UI fixture."""
import argparse
import asyncio
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (320, 390, 768, 1024, 1440)


async def run(url, output, phase, widths=WIDTHS):
    origin = urlsplit(url)
    if origin.scheme != 'http' or origin.hostname not in ('localhost', '127.0.0.1'):
        raise ValueError('local_fixture_only')
    output = output.resolve()
    if not output.is_relative_to(ROOT / '.local') or output.exists():
        raise ValueError('new_private_output_required')
    output.mkdir(parents=True)
    report = {'layer': 'real_reflex_ui_fictional_backend', 'phase': phase,
              'cases': [], 'passed': False, 'blocked_external': 0,
              'css_sha256': hashlib.sha256((ROOT/'assets/codeboxd.css').read_bytes()).hexdigest()}
    errors = []
    completed = False
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='msedge', headless=True)
        try:
            for width in widths:
                context = await browser.new_context(viewport={'width': width, 'height': 900})
                async def route_request(route):
                    target = urlsplit(route.request.url)
                    if target.hostname == 'ui-fixture.invalid':
                        await route.fulfill(content_type='image/png', body=(ROOT/'assets/default-movie-cover.png').read_bytes())
                    elif target.hostname in ('127.0.0.1', 'localhost'):
                        await route.continue_()
                    else:
                        report['blocked_external'] += 1
                        await route.abort()
                await context.route('**/*', route_request)
                page = await context.new_page()
                page.set_default_timeout(15000)
                page._ui_frames = []
                def socket_opened(socket, frames=page._ui_frames):
                    socket.on('framesent', lambda data: frames.append(1)
                        if isinstance(data, str) and data.startswith('42') else None)
                page.on('websocket', socket_opened)
                page.on('pageerror', lambda exc: errors.append(str(exc)))
                try:
                    for path, name in (('/', 'home'), ('/login', 'login'),
                            ('/obra?external_source=tmdb&media_type=movie&external_id=1', 'media')):
                        await page.goto(url.rstrip('/') + path)
                        await page.wait_for_load_state('networkidle')
                        if name == 'home':
                            await expect(page.locator('.shelf-card').first).to_be_visible(timeout=30000)
                        elif name == 'login':
                            await expect(page.get_by_role('button', name='Entrar', exact=True)).to_be_visible()
                        else:
                            await expect(page.locator('.media-shelf .media-card').first).to_be_visible(timeout=30000)
                        await page.evaluate('document.fonts.ready')
                        await page.screenshot(path=str(output/f'{name}-{width}.png'), full_page=True)
                        row = await page.evaluate('''() => ({
                          overflow: document.documentElement.scrollWidth > innerWidth + 1,
                          title: document.querySelector('h1')?.textContent,
                          rail_count: document.querySelectorAll('.catalog-rail').length,
                          rail_cards: document.querySelectorAll('.shelf-card').length,
                          links: [...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))
                        })''')
                        report['cases'].append({'width': width, 'page': name, **row})
                        print(f'{width}px {name}: captured', flush=True)
                        if phase == 'acceptance' and name == 'login':
                            report['cases'][-1]['accessibility'] = await check_login(page)
                    if phase == 'acceptance':
                        await page.goto(url.rstrip('/') + '/')
                        await expect(page.locator('[data-codeboxd-rail]').first).to_be_visible(timeout=30000)
                        report['cases'].append(await check_rail(page, width))
                finally:
                    await context.close()
            completed = True
        except Exception as exc:
            report['failure'] = {'type': type(exc).__name__, 'message': str(exc)[:2000]}
            raise
        finally:
            await browser.close()
            report['javascript_errors'] = errors
            report['passed'] = completed and not errors and all(not row.get('overflow', False) and row.get('passed', True)
                                                  for row in report['cases'])
            (output/'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'phase': phase, 'passed': report['passed'], 'cases': len(report['cases']),
                      'javascript_errors': len(errors)}))
    return 0 if report['passed'] else 1


async def check_rail(page, width):
    print(f'{width}px rail: initial', flush=True)
    await page.emulate_media(reduced_motion='reduce')
    await page.wait_for_function('window.CodeboxdRails !== undefined')
    rail = page.locator('[data-codeboxd-rail]').first
    await rail.scroll_into_view_if_needed()
    rail_id = await rail.get_attribute('id')
    arrows = page.locator(f'button[aria-controls="{rail_id}"]')
    previous, following = arrows.nth(0), arrows.nth(1)
    await page.wait_for_timeout(300)
    requests = []
    initial_frames = len(page._ui_frames)
    page.on('request', lambda request: requests.append(request.url))
    await rail.evaluate('r => {r.scrollLeft=0; window.__railClicks=0; r.addEventListener("click", e=>{if(e.target.closest("[data-rail-item]")) window.__railClicks++});}')
    await expect(previous).to_be_disabled()
    await expect(following).to_be_enabled()
    box = await rail.bounding_box()
    x, y = box['x'] + min(box['width'] * .7, 300), box['y'] + 50
    # Trusted mouse input: no page-script synthetic click is used for dragging.
    await page.mouse.move(x, y)
    await page.mouse.down()
    await page.mouse.move(x - min(box['width'] * .5, 200), y, steps=12)
    await page.mouse.up()
    await page.wait_for_function('(id) => document.getElementById(id).scrollLeft > 5', arg=rail_id)
    assert await page.evaluate('window.__railClicks') == 0, 'drag_opened_card'
    assert await rail.get_attribute('data-dragging') is None
    print(f'{width}px rail: mouse', flush=True)
    # Controls and keyboard must be independent of the pointer path.
    await rail.focus()
    await page.keyboard.press('End')
    await expect(following).to_be_disabled()
    await page.keyboard.press('Home')
    await expect(previous).to_be_disabled()
    await following.click()
    await page.wait_for_function('(id) => document.getElementById(id).scrollLeft > 5', arg=rail_id)
    await rail.focus()
    await page.keyboard.press('Home')
    await page.keyboard.press('ArrowRight')
    await page.wait_for_function('(id) => document.getElementById(id).scrollLeft > 5', arg=rail_id)
    # Re-loading the asset must not duplicate document listeners.
    await page.add_script_tag(path=str(ROOT/'assets/horizontal-collections.js'))
    await rail.focus()
    await page.keyboard.press('Home')
    await rail.evaluate('r=>{window.__scrollCommands=0; const native=r.scrollTo; r.scrollTo=function(...args){window.__scrollCommands++;return native.apply(this,args);};}')
    await page.keyboard.press('ArrowRight')
    distance = await rail.evaluate('r => r.scrollLeft')
    viewport = await rail.evaluate('r => r.clientWidth')
    assert distance <= viewport * 1.2, 'duplicate_key_handler'
    assert await page.evaluate('window.__scrollCommands') == 1, 'duplicate_scroll_command'
    await rail.evaluate('r=>delete r.scrollTo')
    print(f'{width}px rail: keyboard', flush=True)
    # Cancel an active mouse drag without leaving selection/capture locked.
    box = await rail.bounding_box()
    await page.mouse.move(box['x']+100, box['y']+45)
    await page.mouse.down()
    await page.mouse.move(box['x']+60, box['y']+45, steps=5)
    await rail.dispatch_event('pointercancel', {'pointerId': 1, 'pointerType': 'mouse'})
    # A browser cancellation never emits click. DOM dispatch alone does not tell
    # the input engine that the physical mouse was cancelled, so mirror that here.
    await page.evaluate('document.addEventListener("click",e=>{e.preventDefault();e.stopImmediatePropagation();},{capture:true,once:true})')
    await page.mouse.up()
    assert await rail.get_attribute('data-dragging') is None, 'cancel_left_drag_state'
    # Focusing an offscreen item reveals it horizontally.
    last = rail.locator('[data-rail-item]').last
    await last.focus()
    assert await last.evaluate('e => { const a=e.getBoundingClientRect(), b=e.closest("[data-codeboxd-rail]").getBoundingClientRect(); return a.left>=b.left-2 && a.right<=b.right+2; }'), json.dumps(await last.evaluate('e=>({item:e.getBoundingClientRect().toJSON(),rail:e.closest("[data-codeboxd-rail]").getBoundingClientRect().toJSON(),left:e.closest("[data-codeboxd-rail]").scrollLeft})'))
    # Horizontal trackpad/wheel input remains native; vertical wheel can scroll the page.
    await rail.evaluate('r => r.scrollLeft = 0')
    await rail.hover()
    await page.mouse.wheel(130, 0)
    await page.wait_for_function('(id) => document.getElementById(id).scrollLeft > 5', arg=rail_id)
    touch = await check_touch(page, rail)
    print(f'{width}px rail: touch', flush=True)
    # Lazy fixture images are allowed; no HTTP application call or WS event is.
    unexpected = [url for url in requests if 'horizontal-collections.js' not in url
                  and '/cover.png' not in url]
    assert not unexpected, 'gesture_generated_requests'
    assert len(page._ui_frames) == initial_frames, 'gesture_generated_reflex_event'
    box = await following.bounding_box()
    assert box['width'] >= 44 and box['height'] >= 44
    lifecycle = await check_lifecycle(page) if width == 390 else None
    print(f'{width}px rail: lifecycle', flush=True)
    # A fresh normal click still reaches the real Reflex action after dragging.
    await rail.scroll_into_view_if_needed()
    await rail.focus()
    await page.keyboard.press('Home')
    await rail.locator('[data-rail-item]').first.click()
    await expect(page).to_have_url(re.compile('/obra\\?'))
    await page.wait_for_load_state('networkidle')
    await expect(page.locator('.media-shelf .media-card').first).to_be_visible(timeout=30000)
    activation_frames = len(page._ui_frames) - initial_frames
    assert activation_frames > 0, 'event_counter_missed_real_card_activation'
    recommendation = page.locator('#media-recommendations')
    print('recommendations: ready', json.dumps(await recommendation.evaluate('r=>({connected:r.isConnected,items:r.children.length,url:location.pathname+location.search})')), flush=True)
    await recommendation.evaluate('r=>r.scrollIntoView({block:"center",behavior:"instant"})')
    await expect(recommendation).to_be_visible()
    recommendation_frames = len(page._ui_frames)
    recommendation_requests = len(requests)
    await recommendation.focus()
    await page.keyboard.press('End')
    await expect(page.locator('button[aria-controls="media-recommendations"]').nth(1)).to_be_disabled()
    await page.keyboard.press('Home')
    box = await recommendation.bounding_box()
    await page.mouse.move(box['x']+box['width']*.8, box['y']+50)
    await page.mouse.down()
    await page.mouse.move(box['x']+box['width']*.3, box['y']+50, steps=10)
    await page.mouse.up()
    assert await recommendation.evaluate('r => r.scrollLeft > 5'), 'recommendation_drag'
    await page.wait_for_timeout(100)
    assert len(page._ui_frames) == recommendation_frames, 'recommendation_gesture_reflex_event'
    assert all('/cover.png' in url for url in requests[recommendation_requests:]), 'recommendation_gesture_http'
    # Enter is a native card activation; the drag handler must not swallow it.
    await recommendation.focus()
    await page.keyboard.press('Home')
    await recommendation.locator('[data-rail-item]').nth(1).focus()
    await page.keyboard.press('Enter')
    await expect(page).to_have_url(re.compile('external_id=2'))
    return {'page': 'rail-interactions', 'width': width, 'passed': True,
            'drag_opened_card': False, 'cancel_restored': True, 'keyboard_and_arrows': True,
            'duplicate_script_safe': True, 'focus_revealed_item': True,
            'unexpected_gesture_requests': len(unexpected), 'reflex_gesture_events': 0,
            'normal_click_navigates': True, 'enter_opens_recommendation': True,
            'activation_frames_positive_control': activation_frames,
            'recommendation_drag': True, 'native_horizontal_wheel': True,
            'recommendation_gesture_requests': 0, 'recommendation_gesture_events': 0,
            'lifecycle': lifecycle, **touch}


async def check_lifecycle(page):
    """DOM lifecycle probes use fictional native elements, not backend writes."""
    await page.evaluate('''() => {
      const host=document.createElement('section'); host.id='fixture-lifecycle'; host.style='padding:20px';
      host.innerHTML='<button type="button" data-rail-direction="-1" aria-controls="fixture-rail">Anterior</button><button type="button" data-rail-direction="1" aria-controls="fixture-rail">Próximo</button>';
      const rail=document.createElement('div'); rail.id='fixture-rail';
      rail.dataset.codeboxdRail='true'; rail.tabIndex=0;
      rail.style='display:flex;overflow-x:auto;width:240px;height:80px';
      for(let i=0;i<6;i++) {const card=document.createElement('button');
        card.type='button'; card.dataset.railItem='true'; card.textContent='Teste '+i;
        card.style='flex:0 0 110px'; rail.append(card);}
      rail.addEventListener('click',()=>window.__fixtureClicks=(window.__fixtureClicks||0)+1);
      host.append(rail); document.body.append(host);
    }''')
    rail = page.locator('#fixture-rail')
    await rail.scroll_into_view_if_needed()
    previous = page.locator('[aria-controls="fixture-rail"]').nth(0)
    following = page.locator('[aria-controls="fixture-rail"]').nth(1)
    await expect(previous).to_be_disabled()
    await expect(following).to_be_enabled()
    box = await rail.bounding_box()
    x, y = box['x']+100, box['y']+35
    await page.mouse.move(x, y)
    await page.mouse.down()
    await page.mouse.move(x-4, y, steps=2)
    await page.mouse.up()
    assert await page.evaluate('window.__fixtureClicks') == 1, 'subthreshold_click_suppressed'
    # Vertical mouse intention cancels the horizontal gesture.
    await page.mouse.move(x, y)
    await page.mouse.down()
    await page.mouse.move(x-2, y+30, steps=5)
    assert await rail.get_attribute('data-dragging') is None
    await page.mouse.up()
    assert await rail.evaluate('r=>r.scrollLeft') == 0
    # Capture continues outside the rail; selection is cleared only after intent.
    await page.mouse.move(x, y)
    await page.mouse.down()
    await rail.evaluate('r=>{const range=document.createRange();range.selectNodeContents(r.firstChild);const s=getSelection();s.removeAllRanges();s.addRange(range);}')
    await page.mouse.move(max(1, box['x']-20), y, steps=8)
    assert await rail.get_attribute('data-dragging') == 'true'
    assert await page.evaluate('getSelection().toString()') == '', 'drag_selected_text'
    await page.mouse.up()
    assert await rail.get_attribute('data-dragging') is None
    # A rerender/unmount during capture must restore the removed node and replacement.
    await rail.evaluate('r=>r.scrollLeft=0')
    await page.mouse.move(x, y)
    await page.mouse.down()
    await page.mouse.move(x-35, y, steps=5)
    old = await rail.element_handle()
    await rail.evaluate('r=>{const replacement=r.cloneNode(true); delete replacement.dataset.dragging; r.replaceWith(replacement);}')
    await page.mouse.up()
    await page.wait_for_function('document.querySelector("#fixture-rail").dataset.dragging === undefined')
    assert await old.get_attribute('data-dragging') is None
    await rail.evaluate('r=>{r.replaceChildren(r.firstChild); r.scrollLeft=0;}')
    await expect(previous).to_be_disabled()
    await expect(following).to_be_disabled()
    await rail.evaluate('r=>{for(let i=0;i<5;i++) r.append(r.firstChild.cloneNode(true));}')
    await expect(following).to_be_enabled()
    await following.click()
    assert await rail.evaluate('r=>r.scrollLeft > 5'), 'rerender_lost_controls'
    await rail.focus()
    await page.keyboard.press('Tab')
    assert await page.evaluate('document.activeElement.matches("#fixture-rail [data-rail-item]")')
    await page.locator('#fixture-lifecycle').evaluate('e=>e.remove()')
    return {'subthreshold_click': True, 'vertical_intention': True,
            'pointer_capture_outside': True, 'selection_cleared_after_intent': True,
            'unmount_cleanup': True, 'nonoverflow_controls_disabled': True,
            'tab_reaches_card': True, 'replacement_controls_work': True}


async def check_touch(page, rail):
    """Trusted browser touch emulation, not validation on physical hardware."""
    await rail.scroll_into_view_if_needed()
    await rail.evaluate('r => r.scrollLeft = 0')
    session = await page.context.new_cdp_session(page)
    await session.send('Emulation.setTouchEmulationEnabled', {'enabled': True, 'maxTouchPoints': 5})
    async def swipe(x, y, dx, dy):
        print('touch: begin', flush=True)
        await session.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
        for step in range(1, 11):
            await session.send('Input.dispatchTouchEvent', {'type': 'touchMove',
                'touchPoints': [{'x': x+dx*step/10, 'y': y+dy*step/10}]})
            await page.wait_for_timeout(16)
        await session.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        await page.wait_for_timeout(200)
    try:
        box = await rail.bounding_box()
        await swipe(box['x'] + box['width']*.8, box['y'] + 65, -box['width']*.5, 0)
        print('touch: horizontal completed', flush=True)
        assert await rail.evaluate('r => r.scrollLeft > 5'), 'native_touch_did_not_scroll_rail'
        before = await page.evaluate('scrollY')
        box = await rail.bounding_box()
        await swipe(box['x'] + box['width']*.5, box['y'] + 100, 0, -160)
        print('touch: vertical completed', flush=True)
        assert await page.evaluate('scrollY') > before + 10, 'touch_vertical_scroll_blocked'
        await session.send('Emulation.setPageScaleFactor', {'pageScaleFactor': 1.5})
        assert await page.evaluate('visualViewport.scale') > 1, 'page_zoom_blocked'
        await session.send('Emulation.setPageScaleFactor', {'pageScaleFactor': 1})
    finally:
        await session.send('Emulation.setTouchEmulationEnabled', {'enabled': False})
        await session.detach()
    return {'touch_emulated': True, 'horizontal_swipe': True, 'vertical_scroll': True, 'zoom_allowed': True}


async def check_login(page):
    values = await page.evaluate('''() => {
      const rgb = s => s.match(/[\\d.]+/g).map(Number);
      const lum = c => c.slice(0,3).map(x=>x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4)
          .reduce((sum,x,i)=>sum+x*[.2126,.7152,.0722][i],0);
      const contrast = (a,b) => (Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);
      const background = e => {
        while(e) { const c=rgb(getComputedStyle(e).backgroundColor); if(c.length===3 || c[3]===1) return c; e=e.parentElement; }
        return [0,0,0];
      };
      const nodes = [...document.querySelectorAll('.ui-login-copy,.ui-login-note,.ui-login-link,.ui-login form label,.ui-login header p,.ui-login-primary')];
      const ratios = nodes.map(e=>contrast(rgb(getComputedStyle(e).color),background(e)));
      const input=document.querySelector('#email'), style=getComputedStyle(input);
      return {minimum_text_contrast:Math.min(...ratios),
        input_border_contrast:contrast(rgb(style.borderTopColor),background(input)),
        font_family:getComputedStyle(document.querySelector('.ui-login')).fontFamily,
        all_actions: [...document.querySelectorAll('.ui-login a')].map(e=>({href:e.getAttribute('href'),height:e.getBoundingClientRect().height}))};
    }''')
    assert values['minimum_text_contrast'] >= 4.5, 'login_text_contrast'
    assert values['input_border_contrast'] >= 3, 'login_control_contrast'
    assert 'Inter' in values['font_family'] and 'system-ui' in values['font_family']
    assert all(row['height'] >= 44 for row in values['all_actions'])
    await page.locator('#email').focus()
    assert await page.locator('#email').evaluate('e=>getComputedStyle(e).outlineStyle !== "none"')
    return values


async def check_existing_font(url, output, widths=WIDTHS):
    """Optional check of the Inter dependency already declared by the app.

    Only its existing Google Fonts hosts and the loopback fixture are allowed.
    The main acceptance matrix intentionally blocks these hosts to test fallback.
    """
    if urlsplit(url).hostname not in ('localhost', '127.0.0.1') or urlsplit(url).scheme != 'http':
        raise ValueError('local_fixture_only')
    output = output.resolve()
    if not output.is_relative_to(ROOT/'.local') or output.exists():
        raise ValueError('new_private_output_required')
    output.mkdir(parents=True)
    report = {'phase': 'existing-font', 'passed': False, 'cases': []}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='msedge', headless=True)
        async def route_request(route):
            host = urlsplit(route.request.url).hostname
            if host in ('localhost', '127.0.0.1', 'fonts.googleapis.com', 'fonts.gstatic.com') and route.request.method == 'GET':
                await route.continue_()
            else:
                await route.abort()
        try:
            for width in widths:
                context = await browser.new_context(viewport={'width': width, 'height': 900})
                await context.route('**/*', route_request)
                page = await context.new_page()
                await page.goto(url.rstrip('/')+'/login', wait_until='networkidle')
                await page.evaluate('document.fonts.ready')
                faces = await page.evaluate('Array.from(document.fonts).filter(f=>f.family.includes("Inter")&&f.status==="loaded").map(f=>({family:f.family,weight:f.weight}))')
                assert faces, 'existing_inter_not_loaded'
                report['cases'].append({'width': width, 'loaded_inter': faces,
                                        'accessibility': await check_login(page)})
                await context.close()
            report['passed'] = True
        except Exception as exc:
            report['failure'] = {'type': type(exc).__name__, 'message': str(exc)[:1000]}
            raise
        finally:
            await browser.close()
            (output/'result.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'phase': 'existing-font', 'passed': report['passed'], 'cases': len(report['cases'])}))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:3036')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--phase', choices=('baseline', 'acceptance', 'existing-font'), default='baseline')
    parser.add_argument('--widths', type=int, nargs='+', choices=WIDTHS, default=WIDTHS)
    args = parser.parse_args()
    action = check_existing_font(args.url, args.output, args.widths) if args.phase == 'existing-font' else run(args.url, args.output, args.phase, args.widths)
    raise SystemExit(asyncio.run(action))
