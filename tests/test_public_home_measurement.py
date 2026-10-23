import unittest
from unittest.mock import AsyncMock, patch

from Codeboxd_main.services import catalog
from Codeboxd_main.state.social import SocialState
from tools import public_home_measurement as measurement


class PublicHomeMeasurementTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_probe_uses_real_handler_without_xano(self):
        item = catalog.media('tmdb', 'movie', '1', 'Fixture')
        with patch.object(SocialState, '_call', side_effect=AssertionError('No Xano')), \
                patch.object(catalog, 'search', new=AsyncMock(return_value=([item], []))), \
                patch.object(catalog, 'series_highlights', new=AsyncMock(return_value=[])), \
                patch.object(catalog, 'home_collection', new=AsyncMock(return_value=[item])):
            result = await measurement.sample()
        self.assertTrue(result['complete'])
        self.assertIsNotNone(result['primary_ms'])
        self.assertEqual(len(result['shelves']), len(catalog.HOME_COLLECTIONS))
        self.assertEqual(result['total_requests'], 0)

    async def test_rate_limit_stops_subsequent_samples(self):
        row = dict(complete=False, rate_limited=1)
        with patch.object(measurement, 'sample', new=AsyncMock(return_value=row)) as sample:
            result = await measurement.run()
        sample.assert_awaited_once()
        self.assertFalse(result['complete'])
        self.assertEqual(result['failure_type'], 'rate_limit')

    async def test_timeout_remains_failure_without_fabricated_summary(self):
        with patch.object(measurement, 'sample', new=AsyncMock(side_effect=TimeoutError)):
            result = await measurement.run()
        self.assertFalse(result['complete'])
        self.assertNotIn('summary', result)
        self.assertEqual(result['failure_type'], 'TimeoutError')
