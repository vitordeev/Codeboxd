"""Build a read-only, hash-bound cleanup preview from Xano candidate data.

Optionally reads candidates from the authenticated admin endpoint. It never
calls Cloudinary or mutates Xano; physical cleanup requires a separate executor
and approval for the exact preview.
"""
import argparse
import asyncio
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re

from Codeboxd_main.services.api import APIError, request

ROOT = Path(__file__).resolve().parents[1]
MAX_BATCH = 10
MAX_SNAPSHOT_AGE = timedelta(minutes=15)
MAX_CLOCK_SKEW = timedelta(seconds=60)
MAX_IMAGE_BYTES = 5 * 1024 * 1024
FORMATS = frozenset(('png', 'jpg', 'jpeg', 'webp', 'gif'))
URL_FIELDS = frozenset(('url', 'secure_url', 'image_url', 'file_url'))


def _date(value, name):
    if type(value) is int:
        # Xano serializes timestamps as Unix milliseconds in JSON responses.
        if not 1_000_000_000_000 <= value < 100_000_000_000_000:
            raise ValueError(f'{name}_invalid')
        try:
            return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            raise ValueError(f'{name}_invalid') from None
    if not isinstance(value, str):
        raise ValueError(f'{name}_invalid')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(f'{name}_invalid') from None
    if parsed.tzinfo is None:
        raise ValueError(f'{name}_timezone_required')
    return parsed.astimezone(timezone.utc)


def _positive_int(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(f'{name}_invalid')
    return value


def build_preview(snapshot, *, expected_cloud, now=None):
    """Validate every supplied candidate and return a non-executable preview."""
    if not isinstance(snapshot, dict) or snapshot.get('contract_version') != 1:
        raise ValueError('snapshot_contract_invalid')
    if not isinstance(expected_cloud, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', expected_cloud):
        raise ValueError('expected_cloud_invalid')
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    fetched = _date(snapshot.get('fetched_at'), 'snapshot_time')
    if fetched > now + MAX_CLOCK_SKEW or now - fetched > MAX_SNAPSHOT_AGE:
        raise ValueError('snapshot_stale')
    records = snapshot.get('records')
    if not isinstance(records, list):
        raise ValueError('candidate_list_invalid')
    if len(records) > MAX_BATCH:
        raise ValueError('batch_limit_exceeded')

    if not records:
        canonical = b'[]'
        digest = hashlib.sha256(canonical).hexdigest()
        return {
            'mode': 'no_candidates',
            'contract_version': 1,
            'generated_at': now.isoformat(),
            'expected_cloud': expected_cloud,
            'candidate_count': 0,
            'batch_sha256': digest,
            'approval_reference': None,
            'requires_fresh_server_reread': False,
            'physical_cleanup_executed': False,
            'candidates': [],
        }

    accepted = []
    seen_ids, seen_assets = set(), set()
    for row in records:
        if not isinstance(row, dict) or URL_FIELDS.intersection(row):
            raise ValueError('candidate_shape_or_url_invalid')
        record_id = _positive_int(row.get('id'), 'record_id')
        owner_id = _positive_int(row.get('user_id'), 'owner_id')
        post_id = _positive_int(row.get('post_id'), 'post_id')
        if record_id in seen_ids:
            raise ValueError('duplicate_record')
        seen_ids.add(record_id)
        if row.get('state') != 'cleanup_pending':
            raise ValueError('candidate_state_not_cleanable')
        if row.get('cloud') != expected_cloud:
            raise ValueError('candidate_cloud_mismatch')
        public_id = row.get('public_id')
        if not isinstance(public_id, str) or not re.fullmatch(
                rf'codeboxd/posts/u{owner_id}/[a-f0-9]{{32}}', public_id):
            raise ValueError('candidate_identity_invalid')
        if public_id in seen_assets:
            raise ValueError('duplicate_asset')
        seen_assets.add(public_id)
        asset_id = row.get('asset_id')
        if not isinstance(asset_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,200}', asset_id):
            raise ValueError('candidate_asset_id_invalid')
        version = _positive_int(row.get('version'), 'version')
        if type(row.get('reference_count')) is not int or row['reference_count'] != 0:
            raise ValueError('candidate_still_referenced')
        retained_until = _date(row.get('retain_until'), 'retention')
        if retained_until > now:
            raise ValueError('candidate_retention_active')
        image_format = row.get('format')
        if image_format not in FORMATS:
            raise ValueError('candidate_format_invalid')
        size = row.get('bytes')
        if type(size) is not int or not 0 < size <= MAX_IMAGE_BYTES:
            raise ValueError('candidate_size_invalid')
        width = _positive_int(row.get('width'), 'width')
        height = _positive_int(row.get('height'), 'height')
        accepted.append({
            'record_id': record_id,
            'owner_id': owner_id,
            'post_id': post_id,
            'cloud': expected_cloud,
            'public_id': public_id,
            'asset_id': asset_id,
            'version': version,
            'format': image_format,
            'bytes': size,
            'width': width,
            'height': height,
            'retain_until': retained_until.isoformat(),
            'reference_count': 0,
        })

    canonical = json.dumps(accepted, sort_keys=True, separators=(',', ':')).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        'mode': 'read_only_preview',
        'contract_version': 1,
        'generated_at': now.isoformat(),
        'expected_cloud': expected_cloud,
        'candidate_count': len(accepted),
        'batch_sha256': digest,
        'approval_reference': f'sha256:{digest}',
        'requires_fresh_server_reread': True,
        'physical_cleanup_executed': False,
        'candidates': accepted,
    }


def validate_execution_approval(preview, *, approval_reference, fresh_snapshot,
                                expected_cloud, now=None):
    """Revalidate a preview against a fresh authenticated server snapshot.

    This is a decision gate only; it deliberately does not call Cloudinary or
    perform any state transition. The caller must obtain ``fresh_snapshot``
    from an authenticated, authoritative Xano read immediately before a
    separately approved executor acts.
    """
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if not isinstance(preview, dict) or preview.get('mode') != 'read_only_preview':
        raise ValueError('preview_invalid')
    generated = _date(preview.get('generated_at'), 'preview_time')
    if generated > now + MAX_CLOCK_SKEW or now - generated > MAX_SNAPSHOT_AGE:
        raise ValueError('preview_stale')
    digest = preview.get('batch_sha256')
    expected_approval = f'sha256:{digest}' if isinstance(digest, str) else ''
    if (not re.fullmatch(r'[a-f0-9]{64}', digest or '')
            or approval_reference != expected_approval
            or preview.get('approval_reference') != expected_approval):
        raise ValueError('approval_reference_mismatch')
    try:
        fresh = build_preview(fresh_snapshot, expected_cloud=expected_cloud, now=now)
    except (TypeError, ValueError):
        raise ValueError('fresh_server_state_mismatch') from None
    if (fresh['batch_sha256'] != digest
            or fresh['candidate_count'] != preview.get('candidate_count')
            or fresh.get('candidates') != preview.get('candidates')):
        raise ValueError('fresh_server_state_mismatch')
    return {
        'mode': 'execution_approval_validated',
        'approval_reference': expected_approval,
        'candidate_count': fresh['candidate_count'],
        'candidates': fresh['candidates'],
        'physical_cleanup_executed': False,
    }


async def fetch_xano_snapshot(*, token, per_page=10):
    """Read the current admin cleanup candidates without logging session data."""
    if not isinstance(token, str) or not token.strip():
        raise ValueError('admin_session_required')
    if type(per_page) is not int or not 1 <= per_page <= MAX_BATCH:
        raise ValueError('batch_limit_exceeded')
    response = await request('GET', '/admin/post-image-cleanup-candidates',
                             token=token, params={'per_page': per_page})
    if (not isinstance(response, dict) or response.get('contract_version') != 1
            or not isinstance(response.get('records'), list)
            or 'fetched_at' not in response):
        raise ValueError('cleanup_endpoint_contract_invalid')
    return {
        'contract_version': 1,
        'fetched_at': response['fetched_at'],
        'records': response['records'],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--input', type=Path)
    source.add_argument('--from-xano', action='store_true',
                        help='read current candidates from the authenticated Xano admin route')
    parser.add_argument('--expected-cloud', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.execute:
        parser.error('execution_unavailable_requires_authenticated_server_reread_and_approved_executor')
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / '.local') or output.exists():
        parser.error('new_private_output_required')
    try:
        if args.from_xano:
            token = os.getenv('CLOUDINARY_CLEANUP_ADMIN_TOKEN', '')
            snapshot = asyncio.run(fetch_xano_snapshot(token=token))
        else:
            snapshot = json.loads(args.input.read_text(encoding='utf-8'))
        preview = build_preview(snapshot, expected_cloud=args.expected_cloud)
    except (APIError, OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc) if isinstance(exc, ValueError) else 'snapshot_unreadable')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(preview, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in preview.items() if key != 'candidates'}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
