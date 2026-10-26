import unittest
from unittest.mock import patch

from tools.library_lists_performance_scenario import run_sample


class LibraryListsScenarioTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        legacy = patch.dict('os.environ', {'DEFAULT_LIST_IDENTITY_ENABLED':'false'})
        legacy.start(); self.addCleanup(legacy.stop)

    async def test_small_library_initial_request_count(self):
        result=await run_sample('library')
        self.assertEqual(result['total_requests'],3)
        self.assertEqual(result['loaded_count'],5)
        self.assertEqual(result['library_titles_resolved'],5)
        self.assertEqual(result['catalog_count'],5)
        self.assertEqual(result['simulated_writes'],0)

    async def test_small_personal_lists_with_defaults_use_three_requests(self):
        result=await run_sample('lists')
        self.assertEqual(result['total_requests'],3)
        self.assertEqual(result['loaded_count'],7)
        self.assertEqual(result['catalog_count'],5)
        self.assertEqual(result['private_lists_count'],5)
        self.assertEqual(result['public_lists_count'],2)
        self.assertEqual(result['simulated_writes'],0)

    async def test_large_library_downloads_all_pages_before_show_more(self):
        result=await run_sample('library',size=250)
        self.assertEqual(result['total_requests'],7)
        self.assertEqual(result['loaded_count'],250)
        self.assertEqual(result['unique_loaded_count'],250)
        self.assertEqual(result['visible_before'],20)
        self.assertEqual(result['visible_after_more'],40)
        self.assertEqual(result['show_more_requests'],0)

    async def test_large_lists_download_all_references_and_directories(self):
        result=await run_sample('lists',size=250)
        self.assertEqual(result['total_requests'],7)
        self.assertEqual(result['loaded_count'],252)
        self.assertEqual(result['unique_loaded_count'],252)

    async def test_full_hundred_requires_extra_empty_pages(self):
        result=await run_sample('library',size=100)
        self.assertEqual(result['total_requests'],5)
        self.assertEqual(result['loaded_count'],100)

    async def test_neither_screen_queries_slow_people(self):
        for section in ('library','lists'):
            result=await run_sample(section,'slow-people',delay_ms=30)
            self.assertFalse(any(event['endpoint']=='/profiles' for event in result['events']))
            self.assertGreater(result['loaded_count'],0)

    async def test_people_failure_does_not_block_either_screen(self):
        for section in ('library','lists'):
            result=await run_sample(section,'people-429')
            self.assertEqual(result['total_requests'],3)
            self.assertGreater(result['loaded_count'],0)
            self.assertEqual(result['rate_limited'],0)
            self.assertFalse(result['error_present'])
            self.assertFalse(result['busy_after'])

    async def test_default_list_creation_is_only_simulated(self):
        result=await run_sample('lists','missing-defaults')
        self.assertEqual(result['total_requests'],6)
        self.assertEqual(result['simulated_writes'],2)
        self.assertTrue(result['default_lists_ready'])

    async def test_legacy_default_is_repaired_without_deleting_custom_list(self):
        result=await run_sample('lists','legacy-defaults')
        self.assertEqual(result['total_requests'],5)
        self.assertEqual(result['simulated_writes'],1)
        self.assertTrue(result['default_lists_ready'])

    async def test_personal_revisit_does_not_request_public_directory(self):
        library=await run_sample('library',visits=2)
        lists=await run_sample('lists',visits=2)
        self.assertEqual(library['visits'][1]['requests'],0)
        self.assertEqual(lists['visits'][1]['requests'],0)

    async def test_required_media_failure_remains_visible(self):
        for section in ('library','lists'):
            result=await run_sample(section,'media-429')
            self.assertEqual(result['total_requests'],2)
            self.assertEqual(result['loaded_count'],0)
            self.assertEqual(result['rate_limited'],1)
            self.assertTrue(result['error_present'])
            self.assertFalse(result['busy_after'])
