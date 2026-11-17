"""Isolated browser acceptance for URL-driven unified search."""
import argparse
import asyncio
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


def read_calls(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


async def wait_for_call(path, predicate):
    for _ in range(200):
        calls = read_calls(path)
        if any(predicate(call) for call in calls):
            return calls
        await asyncio.sleep(.05)
    raise AssertionError('expected_fixture_call_not_recorded')


async def run(url, output, log_path):
    parsed = urlsplit(url)
    if parsed.scheme != 'http' or parsed.hostname not in ('localhost', '127.0.0.1'):
        raise ValueError('local_fixture_only')
    output = output.resolve()
    log_path = log_path.resolve()
    if not output.is_relative_to(ROOT / '.local') or output.exists():
        raise ValueError('new_private_output_required')
    if not log_path.is_relative_to(ROOT / '.local'):
        raise ValueError('fixture_log_must_stay_local')
    output.mkdir(parents=True)
    errors = []
    report = {'phase': 'unified-search', 'passed': False, 'cases': [], 'javascript_errors': errors}

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel='msedge', headless=True)
        context = await browser.new_context(viewport={'width': 390, 'height': 900})

        async def route_request(route):
            target = urlsplit(route.request.url)
            if target.hostname in ('127.0.0.1', 'localhost'):
                await route.continue_()
            else:
                await route.abort()

        await context.route('**/*', route_request)
        page = await context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_default_timeout(15000)
        try:
            await page.goto(url.rstrip('/') + '/buscar?tipo=pessoas&page=1', wait_until='networkidle')
            await expect(page.get_by_role('navigation', name='Escopo da busca')).to_be_visible()
            initial_calls = len(read_calls(log_path))
            query = page.locator('#unified-search-query')
            await query.fill('Joana')
            await page.wait_for_timeout(300)
            assert len(read_calls(log_path)) == initial_calls, 'typing_triggered_domain_query'
            assert parse_qs(urlsplit(page.url).query).get('q') is None, 'draft_changed_submitted_url'
            report['cases'].append({'scope': 'pessoas', 'typing_queries': 0})

            await page.get_by_role('button', name='Buscar', exact=True).click()
            await expect(page.locator('.search-result-card h2').first).to_have_text('Joana Fixture')
            await page.wait_for_url(lambda value: '/buscar?' in value and 'q=Joana' in value)
            people_calls = await wait_for_call(log_path, lambda row:
                row.get('kind') == 'api' and row.get('path') == '/profiles')
            people_query_calls = [row for row in people_calls if row.get('kind') == 'api'
                                  and row.get('path') in ('/profiles', '/lists/public')]
            assert [row['path'] for row in people_query_calls] == ['/profiles']
            report['cases'].append({'scope': 'pessoas', 'api_calls': people_query_calls})

            await page.get_by_role('button', name='Listas públicas').click()
            await page.wait_for_url(lambda value: 'tipo=listas' in value and 'q=Joana' in value)
            await expect(page.locator('.search-result-card h2').first).to_have_text('Lista pública de Joana')
            list_call = await wait_for_call(log_path, lambda row:
                row.get('kind') == 'api' and row.get('path') == '/lists/public')
            list_query_calls = [row for row in list_call if row.get('kind') == 'api'
                                and row.get('path') in ('/profiles', '/lists/public')]
            assert [row['path'] for row in list_query_calls] == ['/profiles', '/lists/public']
            assert await page.locator('.search-result-card').count() == 1
            report['cases'].append({'scope': 'listas', 'api_calls': list_query_calls})

            await page.locator('#search-creator-id').fill('41')
            await page.locator('#search-list-field').select_option('title_description')
            await page.get_by_role('button', name='Buscar', exact=True).click()
            await page.wait_for_url(lambda value:
                'creator_id=41' in value and 'search_in=title_description' in value)
            await expect(page.locator('.search-result-card h2').first).to_have_text('Lista pública de Joana')
            query_parameters = parse_qs(urlsplit(page.url).query)
            assert query_parameters['tipo'] == ['listas']
            assert query_parameters['q'] == ['Joana']
            assert query_parameters['page'] == ['1']
            assert query_parameters['creator_id'] == ['41']
            assert query_parameters['search_in'] == ['title_description']
            filtered_call = (await wait_for_call(log_path, lambda row:
                row.get('kind') == 'api' and row.get('path') == '/lists/public'
                and row.get('params', {}).get('creator_id') == 41))[-1]
            assert filtered_call['params']['search_in'] == 'title_description'
            report['cases'].append({'scope': 'listas', 'filters_round_trip': query_parameters})

            await page.get_by_role('button', name='Pessoas', exact=True).click()
            await page.wait_for_url(lambda value:
                'tipo=pessoas' in value and 'q=Joana' in value and 'creator_id' not in value)
            await expect(page.locator('.search-result-card h2').first).to_have_text('Joana Fixture')
            await page.go_back()
            await page.wait_for_url(lambda value:
                'tipo=listas' in value and 'creator_id=41' in value
                and 'search_in=title_description' in value)
            await page.reload(wait_until='networkidle')
            await expect(page.locator('.search-result-card h2').first).to_have_text('Lista pública de Joana')
            report['cases'].append({'history_and_reload': True})

            await page.get_by_role('button', name='Próxima página').click()
            await page.wait_for_url(lambda value: 'page=2' in value)
            await expect(page.locator('.search-result-card h2').first).to_have_text(
                'Outra lista pública de Joana')
            await wait_for_call(log_path, lambda row:
                row.get('kind') == 'api' and row.get('path') == '/lists/public'
                and row.get('params', {}).get('page') == 2)
            report['cases'].append({'pagination_page': 2})

            await page.goto(url.rstrip('/') + '/lista?id=51&page=1', wait_until='networkidle')
            await expect(page.get_by_role('heading', name='Lista pública de Joana')).to_be_visible()
            await expect(page.get_by_role('link', name='Joana Fixture')).to_have_attribute(
                'href', '/perfil/41')
            share_url = page.locator('#list-share-url')
            await expect(share_url).to_have_value('/lista?id=51')
            await page.get_by_role('button', name='Copiar link').click()
            await expect(page.locator('[role="status"]').filter(
                has_text='Link copiado.')).to_be_visible()
            await page.evaluate("""() => Object.defineProperty(navigator, 'clipboard', {
                configurable: true,
                value: {writeText: () => Promise.reject(new Error('fixture_clipboard_denied'))}
            })""")
            await page.get_by_role('button', name='Copiar link').click()
            await expect(page.locator('[role="status"]').filter(
                has_text='Não foi possível copiar')).to_be_visible()
            await expect(share_url).to_have_value('/lista?id=51')
            await page.get_by_role('button', name='Próxima página').click()
            await page.wait_for_url(lambda value: '/lista?' in value and 'id=51' in value
                                    and 'page=2' in value)
            await expect(page.get_by_role('heading', name='Obra de lista 21')).to_be_visible()
            await expect(page.locator('.catalog-grid a').first).to_have_attribute(
                'href', '/obra/21')
            await page.goto(url.rstrip('/') + '/lista?id=53&page=1', wait_until='networkidle')
            await expect(page.get_by_role('heading', name='Lista vazia')).to_be_visible()
            await expect(page.get_by_text('Esta página da lista não tem obras.')).to_be_visible()
            report['cases'].append({'addressable_list': True, 'pagination_page': 2,
                                    'zero_items': True, 'share_copy': True,
                                    'clipboard_failure_fallback': True})

            await page.goto(url.rstrip('/') + '/buscar?tipo=pessoas&q=LongName&page=1',
                            wait_until='networkidle')
            long_name = page.locator('.search-result-card h2').first
            await expect(long_name).to_contain_text('Nome público')
            long_profile_layout = await long_name.evaluate('''element => ({
                overflow_wrap: getComputedStyle(element).overflowWrap,
                document_width: document.documentElement.scrollWidth,
                viewport_width: innerWidth
            })''')
            assert len(await long_name.inner_text()) > 100, 'long_profile_name_fixture_too_short'
            assert long_profile_layout['overflow_wrap'] == 'anywhere', 'long_profile_name_does_not_wrap'
            assert long_profile_layout['document_width'] <= long_profile_layout['viewport_width'] + 1
            await page.get_by_role('button', name='Listas públicas').click()
            await page.wait_for_url(lambda value: 'tipo=listas' in value and 'LongName' in value)
            await expect(page.locator('.search-result-card h2').first).to_contain_text('Lista')
            long_list_layout = await page.locator('.search-result-card h2').first.evaluate('''element => ({
                overflow_wrap: getComputedStyle(element).overflowWrap,
                document_width: document.documentElement.scrollWidth,
                viewport_width: innerWidth
            })''')
            assert long_list_layout['overflow_wrap'] == 'anywhere', 'long_list_title_does_not_wrap'
            assert long_list_layout['document_width'] <= long_list_layout['viewport_width'] + 1
            long_creator = page.locator('.search-result-owner').first
            assert len(await long_creator.inner_text()) > 100, 'long_creator_fixture_too_short'
            creator_layout = await long_creator.evaluate('''element => ({
                overflow_wrap: getComputedStyle(element).overflowWrap,
                document_width: document.documentElement.scrollWidth,
                viewport_width: innerWidth
            })''')
            assert creator_layout['document_width'] <= creator_layout['viewport_width'] + 1
            long_name_calls = [row for row in read_calls(log_path)
                               if row.get('kind') == 'api'
                               and row.get('params', {}).get('q') == 'LongName']
            assert [row['path'] for row in long_name_calls] == ['/profiles', '/lists/public']
            report['cases'].append({'long_profile_and_list_names': True,
                                    'creator_embedded_no_n_plus_one': True,
                                    'layout': {'profile': long_profile_layout,
                                               'list': long_list_layout,
                                               'creator': creator_layout}})

            await page.get_by_role('button', name='Listas públicas').click()
            await page.wait_for_url(lambda value: 'tipo=listas' in value)
            await page.locator('#unified-search-query').fill('Partial')
            await page.get_by_role('button', name='Buscar', exact=True).click()
            await page.wait_for_url(lambda value:
                                    'tipo=listas' in value and 'q=Partial' in value)
            await expect(page.get_by_role('alert')).to_contain_text('indisponível')
            assert await page.locator('.search-result-card').count() == 0
            await page.get_by_role('button', name='Pessoas').click()
            await page.wait_for_function("""() => {
                const params = new URLSearchParams(location.search);
                return params.get('tipo') === 'pessoas' && params.get('q') === 'Partial';
            }""")
            await expect(page.locator('.search-result-card h2').first).to_have_text(
                'Pessoa disponível')
            partial_calls = [row for row in read_calls(log_path)
                             if row.get('kind') == 'api'
                             and row.get('params', {}).get('q') == 'Partial']
            assert [row['path'] for row in partial_calls] == ['/lists/public', '/profiles']
            report['cases'].append({'failed_scope_recovers_without_stale_results': True,
                                    'scope_calls': [row['path'] for row in partial_calls]})

            for scope in ('pessoas', 'listas'):
                current_scope = parse_qs(urlsplit(page.url).query).get('tipo', [''])[0]
                if current_scope != scope:
                    await page.get_by_role(
                        'button', name='Pessoas' if scope == 'pessoas' else 'Listas públicas').click()
                    await page.wait_for_function("""expected => {
                        const params = new URLSearchParams(location.search);
                        return params.get('tipo') === expected;
                    }""", arg=scope)
                    if scope == 'listas':
                        await expect(page.get_by_role('alert')).to_contain_text(
                            'Muitas solicitações')
                await page.locator('#unified-search-query').fill('RateLimited')
                await page.get_by_role('button', name='Buscar', exact=True).click()
                await page.wait_for_function("""expected => {
                    const params = new URLSearchParams(location.search);
                    return params.get('q') === 'RateLimited' && params.get('tipo') === expected;
                }""", arg=scope)
                await expect(page.get_by_role('alert')).to_contain_text('30 segundos')
                assert await page.locator('.search-result-card').count() == 0
                path = '/profiles' if scope == 'pessoas' else '/lists/public'
                limited_calls = [row for row in read_calls(log_path)
                                 if row.get('kind') == 'api' and row.get('path') == path
                                 and row.get('params', {}).get('q') == 'RateLimited']
                await page.reload(wait_until='networkidle')
                await expect(page.get_by_role('alert')).to_contain_text('segundos')
                await page.wait_for_timeout(200)
                retry_calls = [row for row in read_calls(log_path)
                               if row.get('kind') == 'api' and row.get('path') == path
                               and row.get('params', {}).get('q') == 'RateLimited']
                assert len(retry_calls) == len(limited_calls), '429_retry_ignored_cooldown'
                report['cases'].append({'scope': scope, 'rate_limit_distinct_from_empty': True,
                                        'reload_respects_retry_after': True})

            assert not errors, 'javascript_errors'
            report['passed'] = True
        except Exception as exc:
            report['failure'] = {'type': type(exc).__name__, 'message': str(exc)[:2000]}
            raise
        finally:
            await context.close()
            await browser.close()
            (output / 'result.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n',
                                                encoding='utf-8')
    print(json.dumps({'phase': report['phase'], 'passed': report['passed'],
                      'cases': len(report['cases']), 'javascript_errors': len(errors)}))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:3036')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--log', type=Path, required=True)
    options = parser.parse_args()
    raise SystemExit(asyncio.run(run(options.url, options.output, options.log)))
