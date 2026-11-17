"""Local contract regressions; these do not execute a Xano database."""
import json
from pathlib import Path
import re
import unittest

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1] / 'xano'


class PublicSearchContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel='msedge', headless=True)
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def source(self, name):
        return (ROOT / name).read_text(encoding='utf-8')

    def lambdas(self, source):
        return [json.loads(match) for match in re.findall(r'code = ("(?:[^"\\]|\\.)*")', source)]

    def evaluate(self, code, inputs=None, variables=None):
        return self.page.evaluate(
            '(arg) => new Function("$input", "$var", arg.code)(arg.inputs, arg.variables)',
            {'code': code, 'inputs': inputs or {}, 'variables': variables or {}})

    def test_literal_search_escapes_sql_wildcards_without_changing_normal_text(self):
        for endpoint in ('profiles_GET.xs', 'lists_public_GET.xs'):
            code = self.lambdas(self.source('api/codeboxd/' + endpoint))[0]
            for query, expected in [('joana', 'joana'), ('50%_\\', '50\\%\\_\\\\'),
                                    ('ficção', 'ficção'), ("a'b", "a'b")]:
                self.assertEqual(self.evaluate(code, {'q': query}), expected)

    def test_search_page_limit_is_bounded_independently_of_legacy_limit(self):
        for endpoint in ('profiles_GET.xs', 'lists_public_GET.xs'):
            source = self.source('api/codeboxd/' + endpoint)
            code = self.lambdas(source)[1]
            self.assertEqual(self.evaluate(code, {'per_page': 100}), 50)
            self.assertEqual(self.evaluate(code, {'per_page': 20}), 20)
            self.assertIn('metadata: false', source)
            self.assertIn('if ($input.q == null', source)
            self.assertIn('var.update $result { value = $rows }', source)

    def test_public_list_filter_is_applied_in_query_before_pagination_and_totals(self):
        source = self.source('api/codeboxd/lists_public_GET.xs')
        query = source.split('} as $limit', 1)[1].split('} as $found', 1)[0]
        self.assertIn('where = $db.user_list.is_public == true &&', query)
        self.assertIn('$db.user_list.user_id == $input.creator_id', query)
        self.assertIn('$input.search_in == "title_description" &&', query)
        self.assertLess(query.index('where ='), query.index('paging:'))
        self.assertIn('totals: true', query)
        self.assertNotIn('foreach', source)

    def test_search_projection_excludes_private_and_internal_fields(self):
        source = self.source('api/codeboxd/lists_public_GET.xs')
        code = self.lambdas(source)[-1]
        row = {'id': 5, 'user_id': 9, 'title': 'Coleção', 'description': '',
               'default_key': None, 'custom_count': 3, 'default_count': 42,
               'creator': None, 'email': 'must-not-leak', 'internal': 'secret'}
        result = self.evaluate(code, variables={'found': {
            'items': [row], 'itemsTotal': 1, 'curPage': 1, 'nextPage': None}, 'limit': 20})
        self.assertEqual(result['items'][0]['items_count'], 3)
        self.assertEqual(result['items'][0]['creator']['user_id'], 9)
        self.assertNotIn('email', result['items'][0])
        self.assertNotIn('default_key', result['items'][0])
        self.assertNotIn('internal', result['items'][0])

    def test_default_counts_use_status_rows_only_for_the_correct_owner(self):
        code = self.lambdas(self.source('api/codeboxd/lists_public_GET.xs'))[-1]
        for key, expected in [('9:planned', 7), ('9:completed', 7), ('8:planned', 2), (None, 2)]:
            row = {'id': 1, 'user_id': 9, 'title': 'Lista', 'default_key': key,
                   'custom_count': 2, 'default_count': 7, 'creator': None}
            result = self.evaluate(code, variables={'found': {
                'items': [row], 'itemsTotal': 21, 'curPage': 2, 'nextPage': 3}, 'limit': 20})
            self.assertEqual(result['items'][0]['items_count'], expected)
            self.assertEqual(result['page'], 2)
            self.assertEqual(result['next_page'], 3)
            self.assertEqual(result['total'], 21)

    def test_addons_return_counts_and_only_public_creator_fields(self):
        creator = self.source('addon/search_list_creator.xs')
        self.assertIn('output = ["user_id", "username", "display_name", "avatar_url"]', creator)
        self.assertNotRegex(creator, r'email|password|role|account_status')
        for name in ('custom', 'default'):
            self.assertIn('return = {type: "count"}',
                          self.source(f'addon/search_list_{name}_count.xs'))
        default = self.source('addon/search_list_default_count.xs')
        self.assertIn('$db.user_media_list_status.user_id == $input.user_id &&', default)


if __name__ == '__main__':
    unittest.main()
