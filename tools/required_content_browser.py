"""Browser rejection/success checks with fictional local records only."""
import asyncio
import json
from pathlib import Path

from playwright.async_api import expect

from tools import performance_continuation_browser as runner


WRITES={'review':[],'report':[]}


class ContentFixture(runner.Fixture):
    def reply(self,kind):
        payload=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))) or b'{}')
        WRITES[kind].append(payload)
        body=json.dumps({'id':99,'status':'pending'} if kind=='report' else {}).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def do_PUT(self):
        if self.path=='/interactions': self.reply('review')
        else: self.send_error(404)

    def do_POST(self):
        if self.path=='/reports': self.reply('report')
        else: super().do_POST()


async def check(browser,width,identifier):
    runner.MODE['case']='ready'
    WRITES['review'].clear(); WRITES['report'].clear()
    context,page,errors=await runner.context_for(browser,width)
    try:
        await page.goto('http://127.0.0.1:3031/login')
        await page.locator('input[name=email]').fill('reader@example.invalid')
        await page.locator('input[name=password]').fill('fictional-password1')
        await page.get_by_role('button',name='Entrar',exact=True).click()
        await expect(page.get_by_role('heading',name='Conta fictícia',exact=True)).to_be_visible(timeout=30000)
        # This suite tests form validation after login has finished; rapid
        # navigation during profile hydration belongs to navigation regressions.
        await expect(page.get_by_text('Carregando…',exact=True)).not_to_be_visible(timeout=30000)
        await page.goto(f'http://127.0.0.1:3031/obra/{identifier}')
        submit=page.get_by_role('button',name='Salvar avaliação',exact=True)
        await expect(submit).to_be_visible(timeout=30000)
        review=page.locator('textarea[name=review]')
        assert await review.evaluate('(el)=>el.required')
        await submit.click()
        assert await review.evaluate('(el)=>el.validity.valueMissing')
        assert not WRITES['review']
        await review.fill(' \n\t ')
        await submit.click()
        await expect(page.get_by_text('Escreva sua avaliação antes de enviar.',exact=True)).to_be_visible()
        assert not WRITES['review']
        # The form intentionally throttles submits for one second. A corrected
        # input must be submitted after that window rather than being dropped.
        await page.wait_for_timeout(1100)
        await review.fill('  Gostei da história.  ')
        await page.locator('select[name=rating]').select_option('4.5')
        await submit.click()
        await expect(page.get_by_text('Avaliação salva',exact=True)).to_be_visible()
        assert len(WRITES['review'])==1 and WRITES['review'][0]['review']=='Gostei da história.'
        await page.get_by_role('button',name='Denunciar obra',exact=True).click()
        details=page.locator('#report-description')
        send=page.get_by_role('button',name='Enviar report',exact=True)
        assert await details.evaluate('(el)=>el.required')
        await send.click()
        assert await details.evaluate('(el)=>el.validity.valueMissing')
        assert not WRITES['report']
        await details.fill(' \n\t ')
        await send.click()
        await expect(page.get_by_role('alert')).to_contain_text('Escreva os detalhes')
        assert not WRITES['report']
        await details.fill('  Descrição do problema.  ')
        await send.click()
        await expect(page.get_by_role('dialog')).not_to_be_visible()
        assert len(WRITES['report'])==1 and WRITES['report'][0]['description']=='Descrição do problema.'
        assert not errors
        return dict(case='required-content',width=width,identifier=identifier,
                    empty_rejected=True,whitespace_rejected=True,valid_text_sent_once=True,passed=True)
    finally: await context.close()


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'openspec/changes/exigir-texto-denuncias-avaliacoes/validation/browser-2026-10-20')
    parser.add_argument('--normal-base',default='http://127.0.0.1:3030')
    parser.add_argument('--frontend-workdir',type=Path)
    args=parser.parse_args()
    runner.Fixture=ContentFixture
    runner.media_case=check
    runner.OUTPUT=args.output.resolve()
    asyncio.run(runner.main(normal_base=args.normal_base,frontend_workdir=args.frontend_workdir))
