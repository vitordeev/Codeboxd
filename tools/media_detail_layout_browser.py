"""Measure actual detail CSS against long fixture content; no remote services."""
import argparse
import asyncio
from html import escape
import json
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


async def run(output, screenshots):
    if output.exists():
        raise FileExistsError('Preserve previous evidence')
    if not screenshots.resolve().is_relative_to((ROOT / '.local').resolve()):
        raise ValueError('Screenshots must stay private under .local')
    screenshots.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    css = (ROOT / 'assets/codeboxd.css').read_text(encoding='utf-8')
    report = {'layer': 'browser_actual_css_fictional_markup', 'remote_requests': 0, 'cases': [], 'passed': False}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='msedge', headless=True)
        try:
            page = await browser.new_page()
            await page.route('**/*', lambda route: route.abort())
            for width in (320, 390, 640, 1440):
                await page.set_viewport_size({'width': width, 'height': 900})
                for kind in ('book', 'movie', 'series', 'anime', 'missing-cover'):
                    cover = ('<div class="media-detail-poster cover-empty" style="background:#b99548">Sem capa</div>'
                             if kind == 'missing-cover' else
                             '<img class="media-detail-poster" alt="Capa fictícia" '
                             'src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' '
                             'width=\'200\' height=\'300\'%3E%3Crect width=\'200\' height=\'300\' '
                             'fill=\'%23b99548\'/%3E%3C/svg%3E">')
                    title = escape('Uma longa história sobre memórias, encontros e descobertas — ' + kind)
                    description = escape('Uma sinopse longa permanece integralmente legível, com todos os detalhes da história. ' * 8)
                    await page.set_content('<!doctype html><html lang="pt-BR"><head><style>' + css +
                        '</style></head><body><main class="site-main"><section class="media-detail-hero">' +
                        cover + '<div class="media-detail-copy"><h2 class="media-detail-title">' + title +
                        '</h2><p class="media-detail-description">' + description + '</p></div></section></main></body></html>')
                    await page.evaluate('document.fonts.ready')
                    geometry = await page.evaluate('''() => {
                        const box = selector => {
                            const r = document.querySelector(selector).getBoundingClientRect();
                            return {x:r.x, y:r.y, right:r.right, bottom:r.bottom, width:r.width, height:r.height};
                        };
                        const cover=box('.media-detail-poster'), title=box('.media-detail-title'), description=box('.media-detail-description');
                        const overlaps = (a,b) => Math.min(a.right,b.right)>Math.max(a.x,b.x)
                            && Math.min(a.bottom,b.bottom)>Math.max(a.y,b.y);
                        return {cover, title, description, overlap:overlaps(cover,title)||overlaps(cover,description),
                            overflow:document.documentElement.scrollWidth>innerWidth};
                    }''')
                    passed = not geometry['overlap'] and not geometry['overflow'] and geometry['cover']['width'] > 0
                    report['cases'].append({'width': width, 'kind': kind, 'passed': passed, **geometry})
                    if kind == 'book':
                        await page.screenshot(path=str(screenshots / f'book-{width}.png'), full_page=True)
        finally:
            await browser.close()
    report['passed'] = all(row['passed'] for row in report['cases'])
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': report['passed'], 'cases': len(report['cases']),
                      'failed': sum(not row['passed'] for row in report['cases'])}))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--screenshots', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args.output, args.screenshots)))
