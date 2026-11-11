"""Opt-in isolated Cloudinary transport probe. Never calls Xano or modifies app env."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import time
from urllib.parse import urlsplit
import uuid
import zlib

from dotenv import dotenv_values
import httpx

ROOT = Path(__file__).resolve().parents[1]


def png():
    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', 2, 2, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b'\0\xff\0\0\0\xff\0' * 2)) + chunk(b'IEND', b''))


def signed(params, secret, key):
    value = '&'.join(f'{k}={params[k]}' for k in sorted(params)) + secret
    return {**params, 'api_key': key, 'signature': hashlib.sha256(value.encode()).hexdigest()}


def run(client, config, report, save):
    """Report must be privately saved before any upload; failures remain reconcilable."""
    cloud, key, secret = (config[k].strip() for k in
                         ('CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET'))
    if not re.fullmatch(r'[A-Za-z0-9_-]+', cloud) or not key or not secret:
        raise ValueError('incomplete_configuration')
    public_id = 'codeboxd/acceptance/' + uuid.uuid4().hex
    content = png()
    report.update(public_id=public_id, passed=False, upload='not_started', download='not_started',
                  cleanup='not_started', input_sha256=hashlib.sha256(content).hexdigest())
    save(report)
    base = f'https://api.cloudinary.com/v1_1/{cloud}/image/'
    report['upload'] = 'outcome_uncertain'
    save(report)
    try:
        response = client.post(base + 'upload', data=signed({'public_id': public_id,
            'overwrite': 'false', 'timestamp': str(int(time.time()))}, secret, key),
            files={'file': ('acceptance.png', content, 'image/png')})
        report['upload_http'] = response.status_code
        if response.status_code != 200:
            return report
        body = response.json()
        url = urlsplit(body.get('secure_url', ''))
        if not (body.get('public_id') == public_id and body.get('asset_id')
                and body.get('resource_type') == 'image' and body.get('type') == 'upload'
                and body.get('format') == 'png' and body.get('width') == body.get('height') == 2
                and url.scheme == 'https' and url.netloc == 'res.cloudinary.com'
                and url.path.startswith('/' + cloud + '/image/upload/')
                and url.path.endswith('/' + public_id + '.png') and not url.query and not url.fragment):
            return report
        report['upload'] = 'confirmed_own_asset'
        save(report)
    except (httpx.HTTPError, ValueError, TypeError, AttributeError):
        return report
    try:
        try:
            with client.stream('GET', url.geturl()) as received:
                report['download_http'] = received.status_code
                downloaded = bytearray()
                for block in received.iter_bytes():
                    downloaded.extend(block)
                    if len(downloaded) > 4096:
                        break
                report['download'] = ('verified_bytes' if received.status_code == 200
                    and bytes(downloaded) == content else 'failed_verification')
        except httpx.HTTPError:
            report['download'] = 'request_failed'
    finally:
        # Only the exact unique asset confirmed above can reach this mutation.
        report['cleanup'] = 'outcome_uncertain'
        save(report)
        try:
            removed = client.post(base + 'destroy', data=signed({'public_id': public_id,
                'invalidate': 'true', 'timestamp': str(int(time.time()))}, secret, key))
            report['cleanup_http'] = removed.status_code
            if removed.status_code == 200 and removed.json().get('result') == 'ok':
                report['cleanup'] = 'provider_confirmed_deleted'
        except (httpx.HTTPError, ValueError, AttributeError):
            pass
        report['passed'] = report['download'] == 'verified_bytes' and report['cleanup'] == 'provider_confirmed_deleted'
        save(report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--approval-reference')
    parser.add_argument('--config', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    if not args.execute:
        print(json.dumps({'mode': 'preview_only', 'uploads': 1, 'downloads': 1, 'own_asset_deletions': 1,
                          'xano_calls': 0, 'retries': 0, 'app_configuration_changes': 0}))
        return 0
    if not args.approval_reference or not args.config or not args.output:
        parser.error('execution_requires_approval_config_and_private_output')
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / '.local') or output.exists():
        parser.error('new_private_output_required')
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive reservation prevents accidental reuse of an existing journal.
    with output.open('x', encoding='utf-8') as reserved:
        reserved.write('{}\n')
    report = {'mode': 'isolated_transport_probe', 'xano_calls': 0, 'passed': False}
    def save(value):
        output.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    try:
        with httpx.Client(timeout=20, follow_redirects=False, trust_env=False) as client:
            run(client, dotenv_values(args.config), report, save)
    except Exception:
        report['execution_error'] = 'private_details_suppressed'
    finally:
        save(report)
    print(json.dumps({k:v for k,v in report.items() if k != 'public_id'}))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
