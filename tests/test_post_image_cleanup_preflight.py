"""Fail-closed, read-only cleanup preview tests with synthetic Xano exports."""
from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import AsyncMock, patch

from tools.post_image_cleanup_preflight import (
    build_preview, fetch_xano_snapshot, validate_execution_approval)


NOW = datetime(2026, 11, 19, 12, tzinfo=timezone.utc)
PUBLIC_ID = 'codeboxd/posts/u7/' + 'a' * 32


def candidate(**changes):
    row = {
        'id': 11, 'user_id': 7, 'post_id': 21, 'state': 'cleanup_pending',
        'cloud': 'fixture', 'public_id': PUBLIC_ID, 'asset_id': 'asset-11',
        'version': 3, 'format': 'png', 'bytes': 128, 'width': 2, 'height': 2,
        'retain_until': (NOW - timedelta(hours=1)).isoformat(), 'reference_count': 0,
    }
    row.update(changes)
    return row


def snapshot(*rows, fetched_at=None):
    fetched = NOW - timedelta(minutes=1) if fetched_at is None else fetched_at
    if isinstance(fetched, datetime):
        fetched = fetched.isoformat()
    return {'contract_version': 1,
            'fetched_at': fetched,
            'records': list(rows)}


class CleanupPreviewTests(unittest.TestCase):
    def preview(self, data):
        return build_preview(data, expected_cloud='fixture', now=NOW)

    def test_valid_candidate_creates_hash_bound_non_executable_preview(self):
        result = self.preview(snapshot(candidate()))
        self.assertEqual(result['mode'], 'read_only_preview')
        self.assertEqual(result['candidate_count'], 1)
        self.assertEqual(result['approval_reference'], 'sha256:' + result['batch_sha256'])
        self.assertTrue(result['requires_fresh_server_reread'])
        self.assertFalse(result['physical_cleanup_executed'])

    def test_empty_server_batch_returns_non_executable_no_candidates_result(self):
        fetched_ms = int((NOW - timedelta(seconds=1)).timestamp() * 1000)
        result = self.preview(snapshot(fetched_at=fetched_ms))
        self.assertEqual(result['mode'], 'no_candidates')
        self.assertEqual(result['candidate_count'], 0)
        self.assertIsNone(result['approval_reference'])
        self.assertEqual(result['candidates'], [])
        self.assertFalse(result['physical_cleanup_executed'])

    def test_rejects_owner_namespace_and_cloud_mismatch(self):
        for row in (candidate(user_id=8), candidate(public_id='https://host/image.png'),
                    candidate(cloud='other')):
            with self.subTest(row=row):
                with self.assertRaises(ValueError):
                    self.preview(snapshot(row))

    def test_rejects_active_references_and_retention(self):
        for row in (candidate(reference_count=1),
                    candidate(retain_until=(NOW + timedelta(seconds=1)).isoformat())):
            with self.subTest(row=row):
                with self.assertRaises(ValueError):
                    self.preview(snapshot(row))

    def test_rejects_legacy_or_uncertain_records_and_arbitrary_urls(self):
        for row in (candidate(state='attached'), candidate(state='reconciliation_required'),
                    candidate(image_url='https://host/legacy.png')):
            with self.subTest(row=row):
                with self.assertRaises(ValueError):
                    self.preview(snapshot(row))

    def test_rejects_stale_or_future_snapshot(self):
        for fetched in (NOW - timedelta(minutes=16), NOW + timedelta(minutes=2)):
            with self.subTest(fetched=fetched):
                with self.assertRaisesRegex(ValueError, 'snapshot_stale'):
                    self.preview(snapshot(candidate(), fetched_at=fetched))

    def test_accepts_xano_unix_millisecond_timestamps(self):
        fetched_ms = int((NOW - timedelta(minutes=1)).timestamp() * 1000)
        retention_ms = int((NOW - timedelta(hours=1)).timestamp() * 1000)
        data = snapshot(candidate(retain_until=retention_ms), fetched_at=fetched_ms)
        result = self.preview(data)
        self.assertEqual(result['candidate_count'], 1)
        self.assertEqual(result['candidates'][0]['retain_until'],
                         (NOW - timedelta(hours=1)).isoformat())

    def test_rejects_numeric_timestamps_that_are_not_milliseconds(self):
        for value in (True, 1_795_094_613, 0):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.preview(snapshot(candidate(), fetched_at=value))

    def test_rejects_provider_version_and_duplicate_assets(self):
        with self.assertRaises(ValueError):
            self.preview(snapshot(candidate(version=0)))
        with self.assertRaisesRegex(ValueError, 'duplicate_asset'):
            self.preview(snapshot(candidate(), candidate(id=12)))

    def test_batch_is_capped_at_ten(self):
        rows = [candidate(id=n, public_id=f'codeboxd/posts/u7/{n:032x}') for n in range(1, 12)]
        with self.assertRaisesRegex(ValueError, 'batch_limit_exceeded'):
            self.preview(snapshot(*rows))

    def test_execution_gate_requires_approval_and_exact_fresh_server_state(self):
        preview = self.preview(snapshot(candidate()))
        approval = preview['approval_reference']
        fresh = snapshot(candidate(), fetched_at=NOW)
        result = validate_execution_approval(
            preview, approval_reference=approval, fresh_snapshot=fresh,
            expected_cloud='fixture', now=NOW)
        self.assertEqual(result['mode'], 'execution_approval_validated')
        self.assertFalse(result['physical_cleanup_executed'])
        with self.assertRaisesRegex(ValueError, 'approval_reference_mismatch'):
            validate_execution_approval(preview, approval_reference='sha256:wrong',
                fresh_snapshot=fresh, expected_cloud='fixture', now=NOW)
        with self.assertRaisesRegex(ValueError, 'fresh_server_state_mismatch'):
            validate_execution_approval(preview, approval_reference=approval,
                fresh_snapshot=snapshot(candidate(reference_count=1), fetched_at=NOW),
                expected_cloud='fixture', now=NOW)

    def test_execution_gate_rejects_stale_preview(self):
        preview = self.preview(snapshot(candidate()))
        with self.assertRaisesRegex(ValueError, 'preview_stale'):
            validate_execution_approval(preview, approval_reference=preview['approval_reference'],
                fresh_snapshot=snapshot(candidate(), fetched_at=NOW),
                expected_cloud='fixture', now=NOW + timedelta(minutes=16))


class LiveCleanupSnapshotTests(unittest.IsolatedAsyncioTestCase):
    async def test_fetches_admin_snapshot_without_exposing_token(self):
        body = {'contract_version': 1, 'fetched_at': 1795094613610, 'records': []}
        with patch('tools.post_image_cleanup_preflight.request',
                   new=AsyncMock(return_value=body)) as api:
            result = await fetch_xano_snapshot(token='private-session-token')
        self.assertEqual(result, body)
        api.assert_awaited_once_with('GET', '/admin/post-image-cleanup-candidates',
                                     token='private-session-token', params={'per_page': 10})

    async def test_rejects_missing_session_bad_limit_and_malformed_contract(self):
        for token, per_page in (('', 10), ('session', 11), ('session', 0)):
            with self.subTest(token=bool(token), per_page=per_page):
                with self.assertRaises(ValueError):
                    await fetch_xano_snapshot(token=token, per_page=per_page)
        with patch('tools.post_image_cleanup_preflight.request',
                   new=AsyncMock(return_value={'records': []})):
            with self.assertRaisesRegex(ValueError, 'cleanup_endpoint_contract_invalid'):
                await fetch_xano_snapshot(token='private-session-token')


if __name__ == '__main__':
    unittest.main()
