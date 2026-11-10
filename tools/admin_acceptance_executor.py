"""Admin acceptance rehearsal with in-memory HTTP only, never a live executor.

No credentials/environment are loaded. MockTransport and a .invalid origin are
mandatory. The transport handler is trusted test code, not an untrusted plugin.
The Metadata/auth paths model the sequencing; real branch routing, authorization,
audit checks and provisioning still need an explicitly approved integration.
"""
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import threading
import time
from urllib.parse import urlsplit

import httpx

from tools.admin_acceptance_guard import Approval, GuardRejected, digest, identity_digest, preview_update


class RehearsalExecutor:
    def __init__(self, *, destination, approval, manifest, table_ids, transport,
                 journal_path, request_limit=12, interval=3.1,
                 clock=time.monotonic, sleep=time.sleep):
        if type(transport) is not httpx.MockTransport:
            raise GuardRejected('mock_transport_required')
        if not isinstance(approval, Approval):
            raise GuardRejected('approval_required')
        host = urlsplit(destination.origin).hostname or ''
        if not host.endswith('.invalid'):
            raise GuardRejected('synthetic_destination_required')
        if (type(request_limit) is not int or request_limit < 4 or request_limit > 500
                or not isinstance(interval, (float, int)) or not 3.1 <= interval < float('inf')):
            raise GuardRejected('invalid_limits')
        if (set(table_ids) != {'user', 'media', 'report'} or
                any(type(value) is not int or value <= 0 for value in table_ids.values()) or
                len(set(table_ids.values())) != 3):
            raise GuardRejected('invalid_table_mapping')
        self.destination = destination
        self.approval = approval
        self.manifest = tuple(manifest)
        self.table_ids = dict(table_ids)
        self.request_limit, self.calls = request_limit, 0
        self.interval, self.clock, self.sleep = interval, clock, sleep
        self.last_call = None
        self.halted = False
        self.attempted = set()
        self.lock = threading.Lock()
        self.journal_path = Path(journal_path)
        # Exclusive creation prevents silent replay after a previous process/run.
        try:
            with self.journal_path.open('x', encoding='utf-8') as journal:
                journal.write(json.dumps({'event': 'simulation_started', 'remote_execution': False,
                    'destination_digest': digest(asdict(destination)),
                    'approval_digest': digest(approval.reference)}) + '\n')
                journal.flush()
                os.fsync(journal.fileno())
        except FileExistsError:
            raise GuardRejected('journal_exists_requires_reconciliation') from None
        except OSError:
            raise GuardRejected('journal_write_failed') from None
        self.client = httpx.Client(transport=transport, follow_redirects=False, timeout=10,
                                   trust_env=False)

    def close(self):
        self.client.close()

    def _append(self, event, **fields):
        try:
            with self.journal_path.open('a', encoding='utf-8') as journal:
                journal.write(json.dumps({'event': event, **fields}) + '\n')
                journal.flush()
                os.fsync(journal.fileno())
        except OSError:
            self.halted = True
            raise GuardRejected('journal_write_failed') from None

    def _request(self, method, path, *, payload=None):
        if self.halted or self.calls >= self.request_limit:
            raise GuardRejected('executor_stopped')
        if self.last_call is not None:
            self.sleep(max(0, self.interval - (self.clock() - self.last_call)))
        self.calls += 1
        self.last_call = self.clock()
        try:
            response = self.client.request(method, self.destination.origin + path,
                headers={'x-data-source': self.destination.data_source}, json=payload)
            self._append('response', method=method, path_digest=digest(path),
                         status=response.status_code)
            if response.status_code != 200:
                raise GuardRejected('unexpected_http_status')
            body = response.json()
            if not isinstance(body, dict):
                raise GuardRejected('invalid_response_contract')
            return body
        except httpx.HTTPError:
            self.halted = True
            raise GuardRejected('transport_error_no_retry') from None
        except (ValueError, GuardRejected):
            self.halted = True
            raise GuardRejected('response_rejected_no_retry') from None

    def update(self, *, path, payload, cached_record, confirmed=False):
        """Exercise one approved synthetic update and independent verification."""
        with self.lock:
            if self.halted:
                raise GuardRejected('executor_stopped')
            # Copy inputs before invoking test handlers so they cannot mutate intent.
            payload = json.loads(json.dumps(payload, allow_nan=False))
            cached_record = json.loads(json.dumps(cached_record, allow_nan=False))
            args = dict(destination=self.destination, approval=self.approval,
                manifest=self.manifest, actor_id=self.approval.admin_id if self.approval else None,
                method='PUT', path=path, payload=payload, confirmed=confirmed)
            preview = preview_update(**args, current_record=cached_record)
            table, row_id = preview['table'], cached_record['id']
            operation = (table, row_id, preview['payload_digest'])
            if operation in self.attempted:
                raise GuardRejected('operation_already_attempted')
            if self.request_limit - self.calls < 4:
                raise GuardRejected('insufficient_request_budget')
            actor = self._request('GET', '/api:auth/auth/me')
            if (type(actor.get('id')) is not int or actor['id'] != self.approval.admin_id
                    or actor.get('role') != 'admin' or actor.get('account_status') != 'active'):
                self.halted = True
                raise GuardRejected('actor_not_authorized')
            record_path = (f'/api:meta/workspace/{self.destination.workspace}/table/'
                           f'{self.table_ids[table]}/content/{row_id}')
            before = self._request('GET', record_path)
            try:
                preview_update(**args, current_record=before)
            except GuardRejected:
                self.halted = True
                self._append('preflight_rejected')
                raise
            self._append('intent', operation_digest=digest(operation),
                         snapshot_digest=digest(before), payload_digest=digest(payload))
            self.attempted.add(operation)
            try:
                self._request('PUT', '/' + self.destination.api_group + path, payload=payload)
                after = self._request('GET', record_path)
                self._verify(table, before, after, payload)
                self._append('verified', operation_digest=digest(operation),
                             snapshot_digest=digest(after), remote_execution=False)
            except Exception:
                self.halted = True
                self._append('requires_reconciliation', operation_digest=digest(operation))
                raise GuardRejected('write_requires_reconciliation') from None
            self.manifest = tuple(replace(row, snapshot_digest=digest(after))
                if row.table == table and row.row_id == row_id else row for row in self.manifest)
            return {'mode': 'simulated_verified', 'remote_execution': False,
                    'table': table, 'snapshot_digest': digest(after), 'calls': self.calls}

    def _verify(self, table, before, after, payload):
        if (type(after.get('id')) is not int or after['id'] != before['id'] or
                identity_digest(table, before) != identity_digest(table, after)):
            raise GuardRejected('persisted_identity_changed')
        persisted = dict(payload)
        if table == 'user':
            persisted.pop('reason', None)  # Reason belongs to audit, not the user row.
        if any(after.get(key) != value for key, value in persisted.items()):
            raise GuardRejected('persistence_mismatch')
        allowed = set(persisted)
        if table == 'report':
            allowed.update({'reviewer_user_id', 'reviewed_at'})
            if after.get('reviewer_user_id') != self.approval.admin_id:
                raise GuardRejected('reviewer_mismatch')
        if any(after.get(key) != value for key, value in before.items() if key not in allowed):
            raise GuardRejected('unrelated_field_changed')
