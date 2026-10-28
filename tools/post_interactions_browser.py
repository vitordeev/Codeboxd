"""Real Reflex UI with isolated production files and entirely fictional social data."""
import argparse
import asyncio
import json
import os
from pathlib import Path
import time
from urllib.parse import urlsplit

from playwright.async_api import expect
from tools import feed_lists_browser as base

COMMENTS=[]
LIKED=False
FAIL_COMMENT=False


class Fixture(base.Fixture):
    def do_DELETE(self): self.respond()

    def respond(self):
        global LIKED, FAIL_COMMENT
        path=urlsplit(self.path).path
        if path not in ('/likes','/posts/55/discussion','/posts/55/like','/comments') and not path.startswith('/comments/'):
            return super().respond()
        base.CALLS[(self.command,path)]+=1
        payload=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))) or b'{}')
        status=200; data={}
        if path=='/likes': status=404
        elif path.endswith('/discussion'):
            time.sleep(.2)
            data=dict(likes=[dict(user_id=7)] if LIKED else [],comments=COMMENTS)
        elif path.endswith('/like'):
            time.sleep(.4); LIKED=self.command=='PUT'
        elif path=='/comments' and self.command=='POST':
            if FAIL_COMMENT:
                FAIL_COMMENT=False; status=503; data=dict(message='Falha de teste. Tente novamente.')
            else:
                comment=dict(id=300+len(COMMENTS),post_id=55,user_id=7,body=payload['body'])
                COMMENTS.append(comment); data=comment
        elif path.startswith('/comments/'):
            if self.command=='PUT':
                COMMENTS[0]['body']=payload['body']; data=COMMENTS[0]
            elif self.command=='DELETE': COMMENTS.clear()
        body=json.dumps(data).encode()
        self.send_response(status); self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)


async def check(browser,width,case):
    global LIKED, FAIL_COMMENT
    LIKED=False; FAIL_COMMENT=False; COMMENTS.clear(); base.CALLS.clear()
    image='https://images.example.invalid/photo.svg'
    base.MEDIA[0].update(title='Obra de teste'+(' com um título longo para conferir a largura da miniatura' if case==4 else ''),cover_url='' if case==4 else 'https://images.example.invalid/cover.svg')
    base.POSTS[:]=[dict(id=55,user_id=7,body='Uma foto pessoal e uma descoberta.',media_id=0 if case==3 else 1,
        image=image if case in (1,3) else '',spoiler=False,created_at=1,likes_count=0,comments_count=0)]
    context,page,errors=await base.context_for(browser,width)
    async def image_fixture(route):
        cover=route.request.url.endswith('cover.svg')
        body=('<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480">'
              '<rect width="640" height="480" fill="'+('#4b4467' if cover else '#376263')+'"/>'
              '<circle cx="320" cy="190" r="70" fill="#e0ae83"/>'
              '<path d="M160 480 Q160 280 320 280 Q480 280 480 480" fill="#ce936a"/>'
              '<text x="24" y="40" fill="white" font-size="22">'+('Obra' if cover else 'Foto pessoal de teste')+'</text></svg>')
        await route.fulfill(status=200,content_type='image/svg+xml',body=body)
    await context.route('https://images.example.invalid/**',image_fixture)
    try:
        print(json.dumps(dict(phase='browser_case',width=width,case=case)),flush=True)
        await page.goto('http://127.0.0.1:3031/login')
        await page.locator('input[name=email]').fill('reader@example.invalid')
        await page.locator('input[name=password]').fill('fictional-password')
        await page.get_by_role('button',name='Entrar',exact=True).click()
        await expect(page.get_by_role('heading',name='Conta fictícia',exact=True)).to_be_visible(timeout=30000)
        await page.goto('http://127.0.0.1:3031/feed')
        card=page.locator('.post-card').first
        await expect(card).to_be_visible(timeout=30000)
        await expect(card.locator('.post-personal-image')).to_have_count(1 if case in (1,3) else 0)
        await expect(card.locator('.post-work-card')).to_have_count(0 if case==3 else 1)
        if case in (1,2):
            cover=await card.locator('.post-work-thumbnail').bounding_box()
            assert cover and cover['width'] <= 60 and cover['height'] <= 85
            await expect(card.locator('.post-work-card')).to_have_attribute('href','/obra/1')
            if case==1:
                photo=await card.locator('.post-personal-image').bounding_box()
                assert photo and photo['width'] > cover['width']*3
        if case==4: await expect(card.locator('.post-work-placeholder')).to_be_visible()
        heart=card.locator('.post-interactions button').first
        await heart.click()
        await expect(heart).to_have_attribute('aria-pressed','true',timeout=10000)
        await expect(card.locator('.post-like-count')).to_have_text('1 curtida')
        await heart.click()
        await expect(heart).to_have_attribute('aria-pressed','false')
        assert base.CALLS[('PUT','/posts/55/like')]==1 and base.CALLS[('DELETE','/posts/55/like')]==1
        await card.get_by_role('button',name='Abrir comentários',exact=True).click()
        dialog=page.get_by_role('dialog',name='Comentários',exact=True)
        await expect(dialog).to_be_visible()
        await expect(dialog.get_by_text('Ainda não há comentários',exact=True)).to_be_visible()
        composer=dialog.get_by_role('textbox',name='Comentário',exact=True)
        await composer.fill('Primeiro comentário')
        await dialog.get_by_role('button',name='Publicar',exact=True).click()
        await expect(dialog.locator('.comment-text')).to_contain_text('Primeiro comentário')
        await expect(composer).to_have_value('')
        FAIL_COMMENT=True
        await composer.fill('Rascunho preservado')
        await dialog.get_by_role('button',name='Publicar',exact=True).click()
        await expect(dialog.get_by_role('alert')).to_be_visible()
        await expect(composer).to_have_value('Rascunho preservado')
        assert len(COMMENTS)==1
        await dialog.get_by_role('button',name='Publicar',exact=True).click()
        await expect(dialog.locator('.post-comment')).to_have_count(2)
        await expect(page.get_by_text('Serviço indisponível. Tente novamente.',exact=True)).not_to_be_visible()
        await dialog.get_by_role('button',name='Editar',exact=True).first.click()
        await composer.fill('Comentário editado')
        await dialog.get_by_role('button',name='Salvar',exact=True).click()
        await expect(dialog.locator('.comment-text').first).to_contain_text('Comentário editado')
        color=await dialog.locator('.comment-text').first.evaluate('(node) => getComputedStyle(node).color')
        assert color=='rgb(229, 229, 235)', color
        await page.screenshot(path=str(base.OUTPUT/f'comments-{width}-{case}.png'),full_page=True)
        await page.keyboard.press('Escape')
        await expect(dialog).not_to_be_visible()
        await expect(card.locator('.post-comments-link')).to_contain_text('(2)')
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        assert not errors, errors
        await page.screenshot(path=str(base.OUTPUT/f'feed-{width}-{case}.png'),full_page=True)
        return dict(case=case,width=width,passed=True,thumbnail=True,like_toggle=True,
                    comments_create_edit=True,draft_after_error=True,escape_closes=True,javascript_errors=errors)
    except Exception:
        await page.screenshot(path=str(base.OUTPUT/f'failure-{width}-{case}.png'),full_page=True)
        raise
    finally: await context.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--frontend-workdir',type=Path)
    args=parser.parse_args()
    # Client UI validation remains production mode; avoid unrelated route
    # prerender timeouts in the isolated build. The normal app is untouched.
    os.environ['REFLEX_SSR']='false'
    base.Fixture=Fixture; base.check=check
    raise SystemExit(asyncio.run(base.main(args.output,args.frontend_workdir,readiness_path='/')))
