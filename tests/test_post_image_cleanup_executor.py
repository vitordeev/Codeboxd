"""Supervised cleanup orchestration contracts; all service calls are mocked."""
from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import AsyncMock, patch

from tools.post_image_cleanup_executor import execute_cleanup
from tools.post_image_cleanup_preflight import build_preview


class CleanupExecutorTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)
        record = {'id': 9, 'user_id': 7, 'post_id': 12, 'state': 'cleanup_pending',
            'cloud': 'fixture', 'public_id': 'codeboxd/posts/u7/' + 'a'*32,
            'asset_id': 'asset-9', 'version': 3, 'format': 'png', 'bytes': 128,
            'width': 32, 'height': 32, 'retain_until': (self.now - timedelta(hours=1)).isoformat(),
            'reference_count': 0}
        self.preview = build_preview({'contract_version': 1, 'fetched_at': self.now.isoformat(),
            'records': [record]}, expected_cloud='fixture', now=self.now)

    async def test_approved_item_claims_verifies_destroys_once_and_records_result(self):
        async def request(method, path, **kwargs):
            if method == 'GET':
                return {'contract_version': 1, 'fetched_at': self.now.isoformat(),
                        'records': [self.preview['candidates'][0] | {'id': 9, 'user_id': 7,
                            'state': 'cleanup_pending', 'retain_until': self.preview['candidates'][0]['retain_until']} ]}
            if path.endswith('/claim'):
                candidate = self.preview['candidates'][0]
                return {'contract_version': 1, 'id': 9, 'user_id': 7, 'post_id': 12,
                    'state': 'reconciliation_required', 'cloud': 'fixture',
                    'public_id': candidate['public_id'], 'asset_id': 'asset-9', 'version': 3,
                    'format': 'png', 'bytes': 128, 'width': 32, 'height': 32,
                    'approval_sha256': self.preview['batch_sha256']}
            return {'contract_version': 1, 'id': 9, 'state': 'deleted'}
        with patch('tools.post_image_cleanup_executor.fetch_xano_snapshot', new=AsyncMock(
                return_value={'contract_version': 1, 'fetched_at': self.now.isoformat(),
                    'records': [{'id': 9, 'user_id': 7, 'post_id': 12, 'state': 'cleanup_pending',
                        'cloud': 'fixture', 'public_id': self.preview['candidates'][0]['public_id'],
                        'asset_id': 'asset-9', 'version': 3, 'format': 'png', 'bytes': 128,
                        'width': 32, 'height': 32,
                        'retain_until': self.preview['candidates'][0]['retain_until'], 'reference_count': 0}]})), \
             patch('tools.post_image_cleanup_executor.request', new=AsyncMock(side_effect=request)) as api, \
             patch('tools.post_image_cleanup_executor.destroy_cleanup_candidate', new=AsyncMock(
                 return_value='deleted')) as destroy:
            receipt = await execute_cleanup(preview=self.preview,
                approval_reference=self.preview['approval_reference'], expected_cloud='fixture', token='secret')
        destroy.assert_awaited_once()
        self.assertEqual(api.await_count, 2)
        self.assertTrue(receipt['physical_cleanup_executed'])
        self.assertEqual(receipt['results'], [{'record_id': 9, 'outcome': 'deleted', 'journal_state': 'deleted'}])
        self.assertNotIn('secret', repr(receipt))

    async def test_claim_failure_never_calls_provider_or_retries_write(self):
        fresh = {'contract_version': 1, 'fetched_at': self.now.isoformat(),
            'records': [{'id': 9, 'user_id': 7, 'post_id': 12, 'state': 'cleanup_pending',
                'cloud': 'fixture', 'public_id': self.preview['candidates'][0]['public_id'],
                'asset_id': 'asset-9', 'version': 3, 'format': 'png', 'bytes': 128,
                'width': 32, 'height': 32, 'retain_until': self.preview['candidates'][0]['retain_until'],
                'reference_count': 0}]}
        with patch('tools.post_image_cleanup_executor.fetch_xano_snapshot', new=AsyncMock(return_value=fresh)), \
             patch('tools.post_image_cleanup_executor.request', new=AsyncMock(side_effect=TimeoutError)) as api, \
             patch('tools.post_image_cleanup_executor.destroy_cleanup_candidate', new=AsyncMock()) as destroy:
            receipt = await execute_cleanup(preview=self.preview,
                approval_reference=self.preview['approval_reference'], expected_cloud='fixture', token='secret')
        self.assertEqual(api.await_count, 1)
        destroy.assert_not_awaited()
        self.assertEqual(receipt['results'][0]['outcome'], 'claim_uncertain')

    async def test_uncertain_provider_outcome_is_recorded_without_retry(self):
        fresh = {'contract_version': 1, 'fetched_at': self.now.isoformat(),
            'records': [{'id': 9, 'user_id': 7, 'post_id': 12, 'state': 'cleanup_pending',
                'cloud': 'fixture', 'public_id': self.preview['candidates'][0]['public_id'],
                'asset_id': 'asset-9', 'version': 3, 'format': 'png', 'bytes': 128,
                'width': 32, 'height': 32, 'retain_until': self.preview['candidates'][0]['retain_until'],
                'reference_count': 0}]}
        async def request(method, path, **kwargs):
            if path.endswith('/claim'):
                candidate = self.preview['candidates'][0]
                return {'contract_version': 1, 'id': 9, 'user_id': 7, 'post_id': 12,
                    'state': 'reconciliation_required', 'cloud': 'fixture',
                    'public_id': candidate['public_id'], 'asset_id': 'asset-9', 'version': 3,
                    'format': 'png', 'bytes': 128, 'width': 32, 'height': 32,
                    'approval_sha256': self.preview['batch_sha256']}
            return {'contract_version': 1, 'id': 9, 'state': 'reconciliation_required'}
        with patch('tools.post_image_cleanup_executor.fetch_xano_snapshot', new=AsyncMock(return_value=fresh)), \
             patch('tools.post_image_cleanup_executor.request', new=AsyncMock(side_effect=request)) as api, \
             patch('tools.post_image_cleanup_executor.destroy_cleanup_candidate', new=AsyncMock(
                 side_effect=TimeoutError)) as destroy:
            receipt = await execute_cleanup(preview=self.preview,
                approval_reference=self.preview['approval_reference'], expected_cloud='fixture', token='secret')
        destroy.assert_awaited_once()
        self.assertEqual(api.await_count, 2)
        self.assertFalse(receipt['physical_cleanup_executed'])
        self.assertEqual(receipt['results'][0], {
            'record_id': 9, 'outcome': 'uncertain', 'journal_state': 'reconciliation_required'})

    async def test_empty_candidate_snapshot_is_rejected_before_writes(self):
        fresh = {'contract_version': 1, 'fetched_at': self.now.isoformat(), 'records': []}
        with patch('tools.post_image_cleanup_executor.fetch_xano_snapshot', new=AsyncMock(return_value=fresh)), \
             patch('tools.post_image_cleanup_executor.request', new=AsyncMock()) as api, \
             patch('tools.post_image_cleanup_executor.destroy_cleanup_candidate', new=AsyncMock()) as destroy:
            with self.assertRaisesRegex(ValueError, 'fresh_server_state_mismatch'):
                await execute_cleanup(preview=self.preview,
                    approval_reference=self.preview['approval_reference'], expected_cloud='fixture', token='secret')
        api.assert_not_awaited()
        destroy.assert_not_awaited()


if __name__ == '__main__':
    unittest.main()
