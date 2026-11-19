"""Browser regression of real shared controls, with fictional data only."""
import asyncio
import json
from pathlib import Path
from urllib.parse import urlsplit
from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


async def run():
    report = {'passed': False, 'layer': 'real_components_fictional_backend', 'cases': []}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='msedge', headless=True)
        try:
            for width in (320, 390, 768, 1024, 1440):
                context = await browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
                async def route_request(route):
                    if urlsplit(route.request.url).hostname in ('localhost', '127.0.0.1'):
                        await route.continue_()
                    else:
                        await route.abort()
                await context.route('**/*', route_request)
                page = await context.new_page()
                await context.grant_permissions(['clipboard-read', 'clipboard-write'], origin='http://127.0.0.1:3036')
                errors = []
                page.on('pageerror', lambda exc: errors.append(str(exc)))
                await page.goto('http://127.0.0.1:3036/ui-controls-fixture')
                name = page.get_by_label('Nome de exibição')
                await expect(name).to_have_value('Pessoa de teste')
                await name.fill('Nome alterado de teste')
                await page.evaluate('navigator.clipboard.writeText("Nome colado de teste")')
                await name.focus()
                await page.keyboard.press('Control+a')
                await page.keyboard.press('Control+v')
                await expect(name).to_have_value('Nome colado de teste')
                review = page.get_by_label('Sua crítica')
                await review.fill('Rascunho longo de teste, preservado após uma falha.')
                await page.get_by_role('button', name='Salvar teste', exact=True).click()
                await expect(page.get_by_role('alert')).to_contain_text('Seu texto foi preservado')
                await expect(review).to_have_value('Rascunho longo de teste, preservado após uma falha.')
                await expect(name).to_have_value('Nome colado de teste')
                await page.get_by_role('button', name='Simular carregamento', exact=True).click()
                await expect(page.get_by_role('button', name='Salvando…', exact=True)).to_be_disabled()
                await expect(page.get_by_role('button', name='Simular carregamento', exact=True)).to_be_enabled()
                await expect(page.locator('.ui-empty-state')).to_contain_text('Nenhuma obra adicionada')
                await expect(page.get_by_role('status').filter(has_text='Parte das informações')).to_be_visible()
                await expect(page.get_by_role('status').filter(has_text='Alteração confirmada')).to_be_visible()
                trigger = page.get_by_role('button', name='Abrir edição', exact=True)
                await trigger.click()
                dialog = page.get_by_role('dialog')
                await expect(dialog).to_be_visible()
                await dialog.get_by_label('Descrição').fill('Rascunho no diálogo')
                await page.keyboard.press('Tab')
                await page.keyboard.press('Tab')
                assert await dialog.evaluate('e=>e.contains(document.activeElement)')
                await page.keyboard.press('Escape')
                await expect(dialog).to_have_count(0)
                await expect(trigger).to_be_focused()
                delete = page.get_by_role('button', name='Excluir rascunho de teste', exact=True)
                await delete.click()
                await expect(page.get_by_role('alertdialog')).to_be_visible()
                await page.get_by_role('button', name='Cancelar', exact=True).click()
                await expect(delete).to_be_focused()
                await name.focus()
                assert await name.evaluate('e=>getComputedStyle(e).outlineStyle!=="none"')
                assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                assert (await trigger.bounding_box())['height'] >= 44
                contrast = await name.evaluate('''e=>{
                  const rgb=s=>s.match(/[\\d.]+/g).slice(0,3).map(Number);
                  const lum=c=>c.map(x=>x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
                  const ratio=(a,b)=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);
                  const s=getComputedStyle(e),bg=rgb(s.backgroundColor);
                  return {text:ratio(rgb(s.color),bg),border:ratio(rgb(s.borderTopColor),bg)};
                }''')
                assert contrast['text']>=4.5 and contrast['border']>=3
                assert not errors
                await page.screenshot(path=str(ROOT/f'.local/controls-{width}.png'), full_page=True)
                report['cases'].append({'width': width, 'draft_preserved_on_error': True,
                    'disabled_state': True, 'editor_escape_and_focus_return': True,
                    'confirmation_cancel_and_focus_return': True, 'focus_visible': True,
                    'secondary_target_44px': True, 'document_overflow': False, 'javascript_errors': errors})
                report['cases'][-1].update({'clipboard_paste': True, 'dialog_tab_contained': True, 'contrast': contrast})
                await context.close()
            report['passed'] = True
        finally:
            await browser.close()
            (ROOT/'.local/controls-result.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    asyncio.run(run())
