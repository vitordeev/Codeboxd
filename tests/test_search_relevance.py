import os
import unittest
from unittest.mock import AsyncMock, patch
from Codeboxd_main.services import catalog


class RelevanceTests(unittest.IsolatedAsyncioTestCase):
    def test_all_title_terms_required_not_metadata(self):
        matching=catalog.media('tmdb','movie','1','Homem-Aranha: Sem Volta Para Casa')
        unrelated=catalog.media('openlibrary','book','OL1W','Proverbios 11',details={'Autores':'Homem Aranha'})
        partial=catalog.media('openlibrary','book','OL2W','O Homem da Biblia')
        self.assertEqual(catalog.relevant_results('homen aranha',[unrelated,partial,matching]),[matching])

    def test_accents_punctuation_case_and_original_titles(self):
        item=catalog.media('tmdb','movie','1','Homem-Aranha',search_titles=['Spider-Man'])
        self.assertGreater(catalog.title_score('HOMEM ARANHA',item),0)
        self.assertGreater(catalog.title_score('spider man',item),0)
        self.assertGreater(catalog.title_score('acao',{'title':'Ação'}),0)
        self.assertEqual(catalog.title_score('homem de ferro',item),0)

    def test_exact_title_precedes_related_titles_without_removing_books(self):
        related=catalog.media('tmdb','movie','2','Homem-Aranha 2')
        book=catalog.media('openlibrary','book','OL1W','Homem-Aranha')
        self.assertEqual(catalog.relevant_results('homem aranha',[related,book]),[book,related])
        self.assertEqual(catalog.relevant_results('',[related,book]),[related,book])

    async def test_query_typo_corrected_for_every_provider_and_noise_removed(self):
        async def provider(query,kind,page):
            self.assertEqual(query,'homem aranha')
            source={'movie':'tmdb','series':'tmdb','anime':'jikan','book':'openlibrary'}[kind]
            return [catalog.media(source,kind,'1','Homem-Aranha'),catalog.media(source,kind,'2','Proverbios 30')]
        with patch.object(catalog,'search_one',side_effect=provider):
            items,errors=await catalog.search('homen aranha')
        self.assertFalse(errors)
        self.assertEqual(len(items),4)
        self.assertTrue(all(i['title']=='Homem-Aranha' for i in items))

    async def test_books_use_title_search_and_retain_matching_edition(self):
        payload={'docs':[{'key':'/works/OL1W','title':'Dune','editions':{'docs':[{'title':'Duna'}]}}]}
        with patch.object(catalog,'fetch',new=AsyncMock(return_value=payload)) as fetch:
            items=await catalog.search_one('Duna','book')
        params=fetch.call_args.kwargs['params']
        self.assertEqual(params['title'],'Duna')
        self.assertNotIn('q',params)
        self.assertGreater(catalog.title_score('Duna',items[0]),0)


if __name__=='__main__':
    unittest.main()
