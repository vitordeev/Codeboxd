"""Regression: an HTTP response and initially idle DOM must not end readiness."""
import time
import unittest

from playwright.async_api import async_playwright, expect
from tools.admin_browser_sync import section_ready, response_since


class BrowserReadinessTests(unittest.IsolatedAsyncioTestCase):
    async def test_response_before_render_waits_for_semantic_result(self):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(channel='msedge', headless=True)
            try:
                page = await browser.new_page()
                await page.set_content('''<button>Filtrar</button><main></main>
                    <script>
                    setTimeout(() => {
                        document.querySelector('main').innerHTML = '<p>Carregando reports…</p>';
                        document.querySelector('button').disabled = true;
                    }, 75);
                    setTimeout(() => {
                        document.querySelector('main').innerHTML = '<p>Report #301</p>';
                        document.querySelector('button').disabled = false;
                    }, 500);
                    </script>''')
                responses = [dict(endpoint='/admin/reports', status=200)]
                async def rendered():
                    await expect(page.get_by_text('Report #301', exact=True)).to_be_visible()
                start = time.monotonic()
                await section_ready(page, responses, 0, '/admin/reports', result=rendered,
                    loading='Carregando reports…', control=page.get_by_role('button', name='Filtrar'))
                self.assertGreater(time.monotonic() - start, .25)
                await expect(page.get_by_text('Carregando reports…')).to_have_count(0)
            finally:
                await browser.close()

    async def test_previous_response_cannot_satisfy_new_operation(self):
        responses = [dict(endpoint='/admin/reports', status=200)]
        with self.assertRaises(TimeoutError):
            await response_since(responses, 1, '/admin/reports', timeout=.1)

    async def test_wrong_method_cannot_satisfy_operation(self):
        responses = [dict(endpoint='/admin/reports', method='GET', status=200)]
        with self.assertRaises(TimeoutError):
            await response_since(responses, 0, '/admin/reports', method='PUT', timeout=.1)
