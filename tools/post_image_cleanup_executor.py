"""Supervised, hash-bound Cloudinary cleanup executor. Never retries writes."""
import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path

from Codeboxd_main.services.api import APIError, request
from Codeboxd_main.services.cloudinary_uploads import destroy_cleanup_candidate
from tools.post_image_cleanup_preflight import fetch_xano_snapshot, validate_execution_approval

ROOT = Path(__file__).resolve().parents[1]


def _private_new_path(path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT / '.local') or resolved.exists():
        raise ValueError('new_private_output_required')
    return resolved


async def execute_cleanup(*, preview: dict, approval_reference: str, expected_cloud: str,
                          token: str) -> dict:
    """Run one approved batch, with one claim/destroy/result attempt per item."""
    fresh = await fetch_xano_snapshot(token=token)
    approved = validate_execution_approval(
        preview, approval_reference=approval_reference,
        fresh_snapshot=fresh, expected_cloud=expected_cloud)
    receipt = {
        'contract_version': 1,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'approval_reference': approved['approval_reference'],
        'candidate_count': approved['candidate_count'],
        'physical_cleanup_executed': False,
        'results': [],
    }
    for candidate in approved['candidates']:
        digest = approval_reference.removeprefix('sha256:')
        claim = {
            'user_id': candidate['owner_id'],
            'post_id': candidate['post_id'],
            'cloud': candidate['cloud'],
            'public_id': candidate['public_id'],
            'asset_id': candidate['asset_id'],
            'version': candidate['version'],
            'approval_sha256': digest,
        }
        claim_path = f"/admin/post-image-cleanup/{candidate['record_id']}/claim"
        try:
            claimed = await request('POST', claim_path, token=token, data=claim)
            if (not isinstance(claimed, dict) or claimed.get('contract_version') != 1
                    or claimed.get('state') != 'reconciliation_required'
                    or claimed.get('approval_sha256') != digest
                    or any(claimed.get(key) != value for key, value in {
                        'id': candidate['record_id'], 'user_id': candidate['owner_id'],
                        'post_id': candidate['post_id'], 'cloud': candidate['cloud'],
                        'public_id': candidate['public_id'], 'asset_id': candidate['asset_id'],
                        'version': candidate['version'], 'format': candidate['format'],
                        'bytes': candidate['bytes'], 'width': candidate['width'],
                        'height': candidate['height'],
                    }.items())):
                raise ValueError('cleanup_claim_contract_invalid')
        except Exception:
            # Claim may have reached Xano; never destroy after an ambiguous claim.
            receipt['results'].append({'record_id': candidate['record_id'], 'outcome': 'claim_uncertain'})
            continue

        try:
            outcome = await destroy_cleanup_candidate(candidate)
        except Exception:
            outcome = 'uncertain'
        try:
            result = await request(
                'POST', f"/admin/post-image-cleanup/{candidate['record_id']}/result",
                token=token, data={'approval_sha256': digest, 'result': outcome})
            state = result.get('state') if isinstance(result, dict) else None
            if (not isinstance(result, dict) or result.get('contract_version') != 1
                    or result.get('id') != candidate['record_id']
                    or state != ('deleted' if outcome == 'deleted' else 'reconciliation_required')):
                state = 'result_uncertain'
        except Exception:
            state = 'result_uncertain'
        receipt['results'].append({'record_id': candidate['record_id'],
                                   'outcome': outcome, 'journal_state': state})
        if outcome == 'deleted' and state == 'deleted':
            receipt['physical_cleanup_executed'] = True
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', required=True, type=Path)
    parser.add_argument('--approval-reference', required=True)
    parser.add_argument('--expected-cloud', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    token = os.getenv('CLOUDINARY_CLEANUP_ADMIN_TOKEN', '')
    if not token.strip():
        parser.error('admin_session_required_in_CLOUDINARY_CLEANUP_ADMIN_TOKEN')
    try:
        output = _private_new_path(args.output)
        preview = json.loads(args.preview.read_text(encoding='utf-8'))
        receipt = asyncio.run(execute_cleanup(
            preview=preview, approval_reference=args.approval_reference,
            expected_cloud=args.expected_cloud, token=token))
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, indent=2)
            stream.write('\n')
    except (APIError, OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc) if isinstance(exc, ValueError) else 'cleanup_execution_failed')
    print(json.dumps({key: value for key, value in receipt.items() if key != 'results'} |
                     {'result_count': len(receipt['results'])}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
