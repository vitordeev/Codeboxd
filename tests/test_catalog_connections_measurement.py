import unittest
from unittest.mock import AsyncMock, patch

from Codeboxd_main.services.api import APIError
from tools import catalog_connections_measurement as measurement


class ConnectionMeasurementTests(unittest.IsolatedAsyncioTestCase):
    async def test_comparison_runs_five_pairs_with_matching_content_and_no_network(self):
        with patch.object(measurement.catalog, 'home_collection',
                          new=AsyncMock(return_value=[{'identity_key': 'fixture:1'}])) as read:
            result = await measurement.measure()
        self.assertTrue(result['complete'])
        self.assertEqual(read.await_count, 30)
        self.assertEqual(len(result['samples']), 10)
        self.assertEqual([row['pooled'] for row in result['samples'][:4]], [False, True, True, False])
        self.assertTrue(all(row['elapsed_ms'] >= 0 for row in result['samples']))
        self.assertTrue(all(row['total_requests'] == 0 for row in result['samples']))

    async def test_failure_stops_without_fake_summary_or_sensitive_error(self):
        with patch.object(measurement.catalog, 'home_collection',
                          new=AsyncMock(side_effect=APIError('PRIVATE_DIAGNOSTIC', 429))) as read:
            result = await measurement.measure()
        self.assertFalse(result['complete'])
        read.assert_awaited_once()
        self.assertNotIn('summary', result)
        self.assertNotIn('PRIVATE_DIAGNOSTIC', str(result))

    async def test_sample_budget_is_bounded(self):
        with self.assertRaises(ValueError):
            await measurement.measure(6)
