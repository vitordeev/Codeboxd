"""Build a contracts-only administrative bundle locally. Never publishes or creates resources."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TABLES = ('user', 'profile', 'media', 'post', 'comment', 'post_like', 'report', 'event_log',
          'user_follow', 'user_list', 'user_list_item', 'user_media_interaction', 'user_media_list_status')
FUNCTIONS = ('security/require_current_session', 'Lists/ensure_default_list', 'quick_start/log_event')
ADMIN = ('admin_catalog_GET', 'admin_catalog_POST', 'admin_catalog_id_PUT',
         'admin_dashboard_GET', 'admin_users_GET', 'admin_users_id_status_PUT',
         'admin_reports_GET', 'admin_reports_id_PUT')
FILES = tuple([*(f'xano/table/{name}.xs' for name in TABLES),
               *(f'xano/function/{name}.xs' for name in FUNCTIONS),
               'xano/api/authentication/authentication.xs', 'xano/api/codeboxd/codeboxd.xs',
               *(f'xano/api/authentication/auth/{name}_POST.xs' for name in ('signup', 'login')),
               'xano/api/authentication/auth/me_GET.xs',
               *(f'xano/api/codeboxd/{name}.xs' for name in ADMIN),
               *(f'xano/api/codeboxd/{name}.xs' for name in ('posts_POST', 'reports_POST', 'interactions_GET'))])


class PreparationRejected(ValueError):
    pass


def sha(value):
    return hashlib.sha256(value).hexdigest()


def origin(value):
    try:
        parts = urlsplit(value)
        if (parts.scheme != 'https' or not parts.hostname or not parts.hostname.endswith('.xano.io')
                or parts.username or parts.password or parts.query or parts.fragment
                or parts.path not in ('', '/') or parts.port not in (None, 443)):
            raise ValueError()
        return 'https://' + parts.hostname.lower()
    except (ValueError, TypeError, AttributeError):
        raise PreparationRejected('invalid_xano_origin') from None


def validate_destination(*, protected_origin, protected_workspace_id, target_origin,
                         target_workspace_id=None, kind='workspace'):
    source, target = origin(protected_origin), origin(target_origin)
    if type(protected_workspace_id) is not int or protected_workspace_id <= 0:
        raise PreparationRejected('invalid_protected_workspace')
    if kind not in ('workspace', 'sandbox'):
        raise PreparationRejected('invalid_destination_kind')
    if kind == 'workspace' and (type(target_workspace_id) is not int or target_workspace_id <= 0):
        raise PreparationRejected('invalid_target_workspace')
    if source == target and (kind == 'sandbox' or protected_workspace_id == target_workspace_id):
        raise PreparationRejected('protected_destination')
    return {'kind': kind, 'origin': target, 'workspace_id': target_workspace_id,
            'identity_only_not_isolation_proof': True}


def sanitize_contract(text):
    meaningful = re.sub(r'/\*.*?\*/', '', text.lstrip('\ufeff'), flags=re.S)
    meaningful = re.sub(r'(?m)^\s*//.*$', '', meaningful).strip()
    headers = re.findall(r'(?m)^(table|function|api_group|query)\b', meaningful)
    if len(headers) != 1 or not re.match(r'^(table|function|api_group|query)\b', meaningful):
        raise PreparationRejected('single_allowed_document_required')
    if re.search(r'(?m)^\s*(env|workspace|task|trigger|addon|ai_agent|ai_tool)\b', meaningful):
        raise PreparationRejected('forbidden_document')
    if headers[0] == 'table' and re.search(r'\b(?:items|records)\s*=', meaningful):
        raise PreparationRejected('records_not_allowed')
    if any(value in meaningful for value in ('api.request', 'util.send_email', '$env.')):
        raise PreparationRejected('external_transport_or_env_not_allowed')
    secrets = (r'AKIA[A-Z0-9]{16}', r'SG\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
               r'sk-[A-Za-z0-9_-]{20,}',
               r'''(?i)\b(?:api_key|api_secret|password)\s*[:=]\s*["'][^"']{8,}["']''')
    if any(re.search(pattern, meaningful) for pattern in secrets):
        raise PreparationRejected('literal_secret_pattern')
    sanitized = re.sub(r'(?m)^\s*(?:guid|canonical)\s*=\s*"[^"\r\n]+"\s*$', '', meaningful)
    return headers[0], sanitized.strip() + '\n'


def build_bundle(root, destination):
    root, destination = Path(root).resolve(), Path(destination).resolve()
    if not destination.is_relative_to(root / '.local'):
        raise PreparationRejected('private_output_required')
    if destination.exists():
        raise PreparationRejected('preserve_existing_preparation')
    documents, manifest = [], []
    for name in FILES:
        path = (root / name).resolve()
        if not path.is_relative_to(root):
            raise PreparationRejected('source_outside_project')
        raw = path.read_bytes()
        kind, code = sanitize_contract(raw.decode('utf-8-sig'))
        documents.append((name, code))
        manifest.append({'source': name, 'type': kind, 'source_sha256': sha(raw),
                         'prepared_sha256': sha(code.encode())})
    # Validate all inputs before creating output; no partial package after rejection.
    destination.mkdir(parents=True, exist_ok=False)
    for name, code in documents:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(code, encoding='utf-8')
    combined = '\n---\n'.join(code.strip() for _, code in documents) + '\n'
    (destination / 'contracts.xs').write_text(combined, encoding='utf-8')
    report = {'mode': 'local_contract_preparation', 'published': False, 'records_included': False,
              'environment_included': False, 'mail_routes_included': False,
              'document_count': len(manifest), 'counts': dict(Counter(row['type'] for row in manifest)),
              'bundle_sha256': sha(combined.encode()), 'documents': manifest}
    (destination / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    report = build_bundle(ROOT, args.output)
    print(json.dumps({key: value for key, value in report.items() if key != 'documents'}, indent=2))


if __name__ == '__main__':
    main()
