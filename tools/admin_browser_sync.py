"""Wait for an operation response AND its semantic UI result before capturing."""
import asyncio
import time

from playwright.async_api import expect


async def response_since(responses, cursor, endpoint, method='GET', timeout=90):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        matching = [row for row in list(responses)[cursor:]
                    if row['endpoint'] == endpoint and row.get('method', 'GET') == method]
        if matching:
            return matching[-1]
        await asyncio.sleep(.05)
    raise TimeoutError(f'No completed {method} response for {endpoint}')


async def section_ready(page, responses, cursor, endpoint, *, result, loading,
                        control, method='GET', status=200):
    """result must identify the current operation's data/empty/error, not a heading.

    A heading, HTTP 200, or initial absence of loading alone cannot establish
    readiness. Callers assert an expected row/count/value or error for this action.
    Record responses only when the response body has been sent.
    """
    row = await response_since(responses, cursor, endpoint, method)
    if row['status'] != status:
        raise AssertionError(f'{endpoint}: expected {status}, received {row["status"]}')
    await result()
    await expect(page.get_by_text(loading, exact=True)).not_to_be_visible()
    await expect(control).to_be_enabled()
    return row


async def capture_ready(page, path):
    # Fails closed if any administrative loading or saving UI is still present.
    await expect(page.locator('.admin-loading-message')).to_have_count(0)
    await expect(page.get_by_role('button', name='Salvando…', exact=True)).to_have_count(0)
    if await page.evaluate('document.documentElement.scrollWidth > innerWidth'):
        raise AssertionError('Horizontal page overflow')
    await page.screenshot(path=str(path), full_page=True)
