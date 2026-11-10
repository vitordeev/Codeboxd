"""Offline previews for admin acceptance. No transport or remote execution.

Approval objects must represent independently reviewed human authorization;
constructing one does not obtain permission. Never import historical executors
here. A future transport still needs trusted journals, budgets and reconciliation.
"""
from dataclasses import dataclass
import hashlib
import json
import re
from urllib.parse import urlsplit


class GuardRejected(ValueError):
    """A fixed reason code, without record contents or credentials."""


def digest(value):
    """Canonical hash; raw snapshots remain in private storage or memory."""
    try:
        encoded = json.dumps(value, sort_keys=True, ensure_ascii=True,
                             separators=(',', ':'), allow_nan=False).encode()
    except (TypeError, ValueError):
        raise GuardRejected('invalid_json') from None
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class Destination:
    origin: str
    workspace: int
    branch: str
    data_source: str
    api_group: str
    shared: bool


@dataclass(frozen=True)
class Fixture:
    table: str
    row_id: int
    run_id: str
    identity_digest: str
    snapshot_digest: str


@dataclass(frozen=True)
class Approval:
    reference: str
    destination: Destination
    run_id: str
    admin_id: int
    phases: frozenset[str]
    shared_destination_approved: bool
    # Exact (table, row_id, payload digest) intents reviewed by the operator.
    updates: frozenset[tuple[str, int, str]]


_ROUTES = (
    (re.compile(r'/admin/users/([1-9][0-9]*)/status'), 'user'),
    (re.compile(r'/admin/catalog/([1-9][0-9]*)'), 'media'),
    (re.compile(r'/admin/reports/([1-9][0-9]*)'), 'report'),
)
_FIELDS = {
    'user': {'account_status', 'reason'},
    'media': {'title', 'description', 'cover_url', 'year'},
    'report': {'status', 'decision'},
}
_IDENTITY = {
    'user': ('username',),
    'media': ('identity_key', 'external_source', 'external_id', 'media_type'),
    'report': ('reporter_user_id', 'target_type', 'target_id'),
}
_MARKER = {'user': 'username', 'media': 'identity_key', 'report': 'description'}


def identity_digest(table, record):
    """Not ownership proof: the trusted provisioning journal supplies this hash."""
    fields = _IDENTITY.get(table)
    if fields is None or any(record.get(key) in (None, '') for key in fields):
        raise GuardRejected('missing_identity')
    return digest({key: record[key] for key in fields})


def preview_update(*, destination, approval, manifest, actor_id, method, path,
                   payload, current_record, confirmed=False):
    """Validate an exact proposed PUT; return a digest-only local preview.

    Does not issue a request, authorize a real run, or produce a reusable permit.
    Snapshot comparison is deliberately strict: reconcile drift before proceeding.
    """
    if confirmed is not True:
        raise GuardRejected('confirmation_required')
    if not isinstance(approval, Approval) or not approval.reference.strip():
        raise GuardRejected('approval_required')
    if 'A3' not in approval.phases:
        raise GuardRejected('phase_not_approved')
    if not isinstance(destination, Destination) or destination != approval.destination:
        raise GuardRejected('destination_mismatch')
    origin = urlsplit(destination.origin)
    if (origin.scheme != 'https' or not origin.hostname or origin.username or
            origin.password or origin.path or origin.query or origin.fragment or
            origin.netloc != origin.hostname or type(destination.workspace) is not int or
            destination.workspace <= 0 or not destination.branch.strip() or
            not destination.data_source.strip() or type(destination.shared) is not bool or
            not re.fullmatch(r'api:[A-Za-z0-9_-]+', destination.api_group)):
        raise GuardRejected('invalid_destination')
    if ((destination.shared or destination.data_source == 'live' or destination.branch == 'live')
            and approval.shared_destination_approved is not True):
        raise GuardRejected('shared_destination_not_approved')
    if not re.fullmatch(r'cbh9_[0-9a-f]{12}', approval.run_id):
        raise GuardRejected('invalid_run_id')
    if (type(actor_id) is not int or actor_id <= 0 or
            type(approval.admin_id) is not int or actor_id != approval.admin_id):
        raise GuardRejected('actor_mismatch')
    if method != 'PUT':
        raise GuardRejected('method_not_supported')
    route = next(((pattern.fullmatch(path), table) for pattern, table in _ROUTES
                  if pattern.fullmatch(path)), None)
    if route is None:
        raise GuardRejected('route_not_supported')
    match, table = route
    row_id = int(match.group(1))
    if table == 'user' and row_id == actor_id:
        raise GuardRejected('actor_is_target')
    if not manifest or any(not isinstance(row, Fixture) for row in manifest):
        raise GuardRejected('manifest_required')
    if len({(row.table, row.row_id) for row in manifest}) != len(manifest):
        raise GuardRejected('duplicate_manifest_id')
    fixture = next((row for row in manifest if row.table == table and
                    type(row.row_id) is int and row.row_id == row_id), None)
    if fixture is None or fixture.run_id != approval.run_id:
        raise GuardRejected('foreign_target')
    if (not isinstance(current_record, dict) or type(current_record.get('id')) is not int
            or current_record['id'] != row_id):
        raise GuardRejected('record_id_mismatch')
    if table == 'user' and current_record.get('role') != 'member':
        raise GuardRejected('protected_account')
    marker = current_record.get(_MARKER[table])
    if not isinstance(marker, str) or approval.run_id not in marker:
        raise GuardRejected('run_marker_missing')
    if identity_digest(table, current_record) != fixture.identity_digest:
        raise GuardRejected('identity_changed')
    if digest(current_record) != fixture.snapshot_digest:
        raise GuardRejected('snapshot_changed')
    if not isinstance(payload, dict) or not payload or set(payload) - _FIELDS[table]:
        raise GuardRejected('payload_fields_not_allowed')
    if table == 'user':
        if payload.get('account_status') not in ('active', 'disabled'):
            raise GuardRejected('invalid_account_status')
        marker = payload.get('reason')
    elif table == 'report':
        if payload.get('status') not in ('reviewing', 'resolved', 'rejected'):
            raise GuardRejected('invalid_report_status')
        marker = payload.get('decision')
    else:
        marker = payload.get('title')
    if not isinstance(marker, str) or approval.run_id not in marker:
        raise GuardRejected('payload_marker_missing')
    payload_hash = digest(payload)
    if (table, row_id, payload_hash) not in approval.updates:
        raise GuardRejected('update_not_approved')
    return {'mode': 'offline_preview', 'remote_execution': False,
            'table': table, 'payload_digest': payload_hash,
            'snapshot_digest': fixture.snapshot_digest}
