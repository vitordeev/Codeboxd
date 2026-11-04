"""Journaled, scoped rehearsal and cutover for the default-list change."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import secrets
import time
import threading
import uuid

import httpx
from dotenv import dotenv_values

from tools.default_list_integrity import digest, read_table
from tools.list_status_contracts import candidate, ROOT
from tools.list_status_deployment import expected_operations, fingerprint
from tools.list_status_migration import PRIVATE, migration_plan, verify_preservation
from tools.session_revocation import blocks, identity, metadata_config, export_workspace

PREFIX = '_cb_status_20261103/'
EVIDENCE = ROOT / 'openspec/changes/corrigir-conexoes-feed-listas/validation'


class PacedClient(httpx.Client):
    def __init__(self, *args, **kwargs):
        self._metadata_slot = threading.Lock()
        self._metadata_last = 0.0
        super().__init__(*args, **kwargs)

    def request(self, method, url, **kwargs):
        metadata = '/api:meta/' in str(url)
        for attempt in range(3):
            if metadata:
                with self._metadata_slot:
                    time.sleep(max(0, .95 - (time.monotonic() - self._metadata_last)))
                    self._metadata_last = time.monotonic()
            response = super().request(method, url, **kwargs)
            if method.upper() != 'GET' or response.status_code != 429 or attempt == 2:
                return response
            # Safe read only. A failed write is never replayed automatically.
            delay = response.headers.get('Retry-After', '21')
            time.sleep(max(1, min(30, int(delay))) if delay.isdigit() else 21)


def route(doc):
    m = re.search(r'^query\s+(?:"([^"]+)"|(\w+))\s+verb=(\w+)', doc, re.M)
    return (m[1] or m[2], m[3]) if m else None


def staged_candidate():
    documents = []
    for doc in blocks(candidate()):
        key = route(doc)
        if key:
            label, method = key
            doc = doc.replace('query "' + label + '"', 'query "' + PREFIX + label + '"', 1)
            guid = 'CBTest' + hashlib.sha256((label + method).encode()).hexdigest()[:20]
            doc = re.sub(r'guid\s*=\s*"[^"]+"', 'guid = "' + guid + '"', doc)
            documents.append(doc)
        elif doc.startswith('table user_media_list_status') or doc.startswith('function '):
            documents.append(doc)
    return '\n---\n'.join(documents) + '\n'


class Run:
    def __init__(self):
        self.base, self.headers = metadata_config()
        config = dotenv_values(ROOT / '.env')
        self.social = config['XANO_SOCIAL_URL'].rstrip('/')
        self.auth = config['XANO_AUTH_URL'].rstrip('/')
        self.client = PacedClient(timeout=40, follow_redirects=False)
        self.tables = self.table_ids()
        self.journal_path = PRIVATE / 'live-journal.json'
        self.journal = json.loads(self.journal_path.read_text(encoding='utf-8')) if self.journal_path.exists() else {}
        self.report = {'checks': [], 'passed': False}

    def save(self):
        self.journal_path.write_text(json.dumps(self.journal, indent=2), encoding='utf-8')

    def check(self, name, passed):
        row = {'check': name, 'passed': bool(passed)}
        self.report['checks'].append(row)
        print(json.dumps(row), flush=True)
        (PRIVATE / 'current-checks.json').write_text(json.dumps(self.report, indent=2), encoding='utf-8')
        if not passed:
            raise ValueError(name)

    def request(self, method, url, **kwargs):
        # No automatic retry of writes, including failures with uncertain commit.
        response = self.client.request(method, url, **kwargs)
        if response.status_code >= 400:
            (PRIVATE / 'last-error.json').write_text(json.dumps({
                'method': method, 'status': response.status_code,
                'body': response.text}, indent=2), encoding='utf-8')
        return response

    def table_ids(self):
        response = self.client.get(self.base + '/table', headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return {r['name']: r['id'] for r in (data.get('items', []) if isinstance(data, dict) else data)}

    def rows(self, table):
        return read_table(self.client, self.base, self.headers, self.tables[table])

    def content(self, table, row_id=None):
        return self.base + '/table/' + str(self.tables[table]) + '/content' + (('/' + str(row_id)) if row_id is not None else '')

    def meta(self, method, table, row_id=None, **kwargs):
        response = self.request(method, self.content(table, row_id),
                                headers={**self.headers, 'x-data-source': 'live'}, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else None

    def bulk_add(self, table, rows, allow_ids=False):
        response = self.request('POST', self.content(table) + '/bulk',
            headers={**self.headers, 'x-data-source': 'live'},
            json={'items': rows, 'allow_id_field': allow_ids})
        response.raise_for_status()
        return response.json()

    def bulk_delete(self, table, ids):
        if not ids:
            return
        response = self.request('POST', self.content(table) + '/bulk/delete',
            headers={**self.headers, 'x-data-source': 'live'}, json={'row_ids': [str(i) for i in ids]})
        response.raise_for_status()
        result = response.json()
        if result.get('error') or result.get('success_total') != len(ids):
            raise ValueError('Incomplete restricted cleanup')

    def import_docs(self, text, label, publish=False):
        baseline = export_workspace(self.client, self.base, self.headers)
        response = self.request('POST', self.base + '/multidoc/dry-run',
            headers={**self.headers, 'Content-Type': 'text/x-xanoscript'},
            params={'partial': 'true', 'env': 'false', 'records': 'false', 'delete': 'false'}, content=text.encode())
        response.raise_for_status()
        preview = response.json()
        (PRIVATE / (label + '-preview.json')).write_text(json.dumps(preview), encoding='utf-8')
        expected = expected_operations(text, baseline)
        actual = {(r['type'], r['name'], r['action']) for r in preview.get('operations', [])}
        # Already identical documents may be reported unchanged instead of update.
        normalized = {(a, b, 'update' if c == 'unchanged' else c) for a, b, c in actual}
        missing = expected - normalized
        unchanged_matches = all(
            sum(1 for kind, _, action in missing if kind == category and action == 'update') ==
            preview.get('summary', {}).get(category, {}).get('unchanged', 0)
            for category in ('table', 'function', 'query'))
        if (normalized - expected or any(action != 'update' for _, _, action in missing)
                or not unchanged_matches or preview.get('warnings') or preview.get('has_records') or preview.get('has_env')):
            raise ValueError('Unexpected preview scope: ' + label)
        if not publish:
            return baseline
        if export_workspace(self.client, self.base, self.headers) != baseline:
            raise ValueError('Contract drift between preview and publication')
        response = self.request('POST', self.base + '/multidoc',
            headers={**self.headers, 'Content-Type': 'text/x-xanoscript'},
            params={'partial': 'true', 'env': 'false', 'records': 'false', 'delete': 'false', 'transaction': 'true'}, content=text.encode())
        (PRIVATE / (label + '-publication.json')).write_text(response.text, encoding='utf-8')
        response.raise_for_status()
        after = export_workspace(self.client, self.base, self.headers)
        old, new = ({identity(d): d for d in blocks(s)} for s in (baseline, after))
        touched = {identity(d) for d in blocks(text)}
        if any(new.get(k) != value for k, value in old.items() if k not in touched) or (new.keys() - old.keys()) - touched:
            raise ValueError('Unrelated contract changed')
        return after

    def stage(self):
        if self.journal.get('staged'):
            self.check('stage_already_recorded', True)
            return
        baseline = (PRIVATE / 'baseline.xs').read_text(encoding='utf-8')
        self.check('no_drift_before_staging', export_workspace(self.client, self.base, self.headers) == baseline)
        text = staged_candidate()
        self.journal['stage_intent'] = fingerprint(text)
        self.save()
        after = self.import_docs(text, 'stage', publish=True)
        (PRIVATE / 'staged.xs').write_text(after, encoding='utf-8')
        self.journal.update(staged=True, candidate_sha256=fingerprint(candidate()))
        self.save()
        self.check('only_additive_stage_published', True)

    def api(self, method, path, user=None, prefix=True, **kwargs):
        token = user['token'] if user else None
        headers = {'Authorization': 'Bearer ' + token} if token else {}
        time.sleep(3.1)
        return self.request(method, self.social + '/' + (PREFIX if prefix else '') + path.lstrip('/'), headers=headers, **kwargs)

    def fixture_users(self):
        if self.journal.get('test_users'):
            return self.journal['test_users']
        marker = 'cbst_' + uuid.uuid4().hex[:12]
        self.journal['fixture_marker'] = marker
        self.journal['test_users'] = []
        self.save()
        for suffix in ('a', 'b'):
            username = marker + '_' + suffix
            password = 'CbTest!9' + secrets.token_urlsafe(18)
            response = self.request('POST', self.auth + '/auth/signup', json={
                'name': username, 'username': username, 'email': username + '@example.invalid', 'password': password})
            response.raise_for_status()
            result = response.json()
            user = {'id': result['user_id'], 'token': result['authToken'], 'password': password,
                    'email': username + '@example.invalid', 'username': username}
            self.journal['test_users'].append(user)
            self.save()
            time.sleep(1.2)
        return self.journal['test_users']

    def rehearse(self, final=False):
        self.tables = self.table_ids()
        a, b = self.fixture_users()
        prefix = not final
        marker = self.journal['fixture_marker']
        media = self.journal.get('fixture_media_ids', [])
        if not media:
            media = self.bulk_add('media', [{'identity_key': marker + ':' + str(i), 'external_source': 'test',
                'external_id': marker + ':' + str(i), 'media_type': 'movie', 'title': marker + ' ' + str(i)} for i in range(102)])
            self.journal['fixture_media_ids'] = media
            self.save()
        mid = media[0]
        owned = [r for r in self.rows('user_list') if r['user_id'] == a['id']]
        planned = next(r for r in owned if r.get('default_key') == f"{a['id']}:planned")
        watched = next(r for r in owned if r.get('default_key') == f"{a['id']}:completed")
        self.check('fixture_default_identities', len(owned) == 2)
        # Author has historical posts; reader never creates a post.
        if not any(r['user_id'] == b['id'] for r in self.rows('post')):
            self.bulk_add('post', [{'user_id': b['id'], 'body': marker + ' historical ' + str(i), 'media_id': 0, 'spoiler': False} for i in range(21)])
        for method, expected in (('PUT', True), ('PUT', True), ('DELETE', False), ('DELETE', False), ('PUT', True)):
            r = self.api(method, f"follows/{b['id']}", a, prefix)
            self.check('follow_' + method + '_' + str(expected), r.status_code == 200 and r.json().get('following') is expected)
        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(lambda _: self.api('PUT', f"follows/{b['id']}", a, prefix), range(2)))
        self.check('concurrent_follow_idempotent', all(r.status_code == 200 for r in responses) and len([
            r for r in self.rows('user_follow') if r['follower_id'] == a['id'] and r['followed_id'] == b['id']]) == 1)
        r = self.api('GET', 'feed', a, prefix, params={'page': 1, 'per_page': 20})
        second = self.api('GET', 'feed', a, prefix, params={'page': 2, 'per_page': 20})
        self.check('new_reader_historical_feed_pagination', r.status_code == second.status_code == 200 and
                   len(r.json()) == 20 and len(second.json()) == 1 and not any(x['user_id'] == a['id'] for x in self.rows('post')))
        self.api('DELETE', f"follows/{b['id']}", a, prefix).raise_for_status()
        self.check('unfollow_removes_feed', self.api('GET', 'feed', a, prefix).json() == [])
        self.check('self_follow_rejected', self.api('PUT', f"follows/{a['id']}", a, prefix).status_code in (400, 422))
        self.check('guest_follow_rejected', self.api('PUT', f"follows/{b['id']}", None, prefix).status_code == 401)
        review = self.api('PUT', 'interactions', a, False, json={'media_id': mid, 'status': 'planned',
            'rating': 4.5, 'review': marker + ' preserve review', 'spoiler': True})
        review.raise_for_status()
        interaction_before = next(r for r in self.rows('user_media_interaction') if r['user_id'] == a['id'] and r['media_id'] == mid)
        for status in (None, 'want_to_watch', 'watched', 'watched', None):
            r = self.api('PUT', f'media-list-status/{mid}', a, prefix, json={'status': status})
            self.check('status_confirmed_' + str(status), r.status_code == 200 and r.json().get('status') == status)
            current = self.api('GET', f'media-list-status/{mid}', a, prefix)
            self.check('status_reloaded_' + str(status), current.status_code == 200 and current.json().get('status') == status)
            for li, kind in ((planned, 'want_to_watch'), (watched, 'watched')):
                items = self.api('GET', f"lists/{li['id']}/items", a, prefix).json()
                self.check('projection_' + kind + '_' + str(status), any(row['media_id'] == mid for row in items) == (status == kind))
        interaction_after = next(r for r in self.rows('user_media_interaction') if r['id'] == interaction_before['id'])
        self.check('review_rating_spoiler_preserved', all(interaction_before[k] == interaction_after[k] for k in ('rating', 'review', 'spoiler', 'identity_key')))
        self.check('missing_status_rejected', self.api('PUT', f'media-list-status/{mid}', a, prefix, json={}).status_code in (400, 422))
        self.check('invalid_status_rejected', self.api('PUT', f'media-list-status/{mid}', a, prefix, json={'status': 'invalid'}).status_code in (400, 422))
        for method, path in (('POST', f"lists/{planned['id']}/items"), ('POST', f"lists/{watched['id']}/items")):
            self.api(method, path, a, prefix, json={'media_id': mid}).raise_for_status()
        self.api('DELETE', f"lists/{planned['id']}/items/{mid}", a, prefix).raise_for_status()
        self.check('late_conditional_delete_preserves_other_status', self.api('GET', f'media-list-status/{mid}', a, prefix).json()['status'] == 'watched')
        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(lambda status: self.api('PUT', f'media-list-status/{mid}', a, prefix, json={'status': status}), ('want_to_watch', 'watched')))
        self.check('opposing_writes_unique', all(r.status_code == 200 for r in responses) and len([
            r for r in self.rows('user_media_list_status') if r['user_id'] == a['id'] and r['media_id'] == mid]) == 1)
        self.check('other_account_status_empty', self.api('GET', f'media-list-status/{mid}', b, prefix).json()['status'] is None)
        self.check('other_account_write_denied', self.api('POST', f"lists/{planned['id']}/items", b, prefix, json={'media_id': mid}).status_code == 403)
        custom = self.api('POST', 'lists', a, False, json={'title': 'Já assisti / li', 'description': marker, 'is_public': False})
        custom.raise_for_status()
        cid = custom.json()['id']
        self.api('POST', f'lists/{cid}/items', a, prefix, json={'media_id': mid}).raise_for_status()
        self.api('PUT', f'media-list-status/{mid}', a, prefix, json={'status': None}).raise_for_status()
        self.check('custom_homonym_independent', len(self.api('GET', f'lists/{cid}/items', a, prefix).json()) == 1)
        self.check('private_custom_not_public', self.api('GET', f'lists/public/{cid}/items', None, prefix).status_code == 403)
        rename = self.api('PUT', f"lists/{planned['id']}", a, False, json={'title': marker + ' renamed', 'description': marker, 'is_public': False})
        rename.raise_for_status()
        self.check('private_default_not_public', self.api('GET', f"lists/public/{planned['id']}/items", None, prefix).status_code == 403)
        # Bulk setup is restricted to this run's media/user, then real API pagination.
        self.bulk_add('user_media_list_status', [{'user_id': a['id'], 'media_id': m, 'status': 'want_to_watch'} for m in media])
        first = self.api('GET', f"lists/{planned['id']}/items", a, prefix, params={'per_page': 100, 'page': 1})
        second = self.api('GET', f"lists/{planned['id']}/items", a, prefix, params={'per_page': 100, 'page': 2})
        self.check('more_than_100_items_real_pagination', first.status_code == second.status_code == 200 and len(first.json()) == 100 and len(second.json()) == 2)
        self.api('DELETE', f"lists/{planned['id']}", a, prefix).raise_for_status()
        self.check('delete_default_clears_only_status', not any(r['user_id'] == a['id'] for r in self.rows('user_media_list_status')) and
                   any(r['id'] == interaction_before['id'] for r in self.rows('user_media_interaction')) and len(self.api('GET', f'lists/{cid}/items', a, prefix).json()) == 1)
        # Rehearse exact-ID restoration on a fixture item, never on an existing row.
        item = next(r for r in self.rows('user_list_item') if r['list_id'] == cid)
        self.bulk_delete('user_list_item', [item['id']])
        ids = self.bulk_add('user_list_item', [item], allow_ids=True)
        restored = self.meta('GET', 'user_list_item', item['id'])
        self.check('rollback_fixture_exact_id_and_fields', ids == [item['id']] and restored == item)
        self.report.update(passed=True, final_contracts=final, candidate_sha256=fingerprint(candidate()))
        name = 'real-final' if final else 'rehearsal'
        (EVIDENCE / (name + '-2026-11-03.json')).write_text(json.dumps(self.report, indent=2), encoding='utf-8')
        self.journal[name + '_passed'] = True
        self.save()

    def cleanup_fixtures(self):
        users = {r['id'] for r in self.journal.get('test_users', [])}
        media = set(self.journal.get('fixture_media_ids', []))
        if not users:
            return
        for name, predicate in (
            ('user_media_list_status', lambda r: r['user_id'] in users),
            ('user_media_interaction', lambda r: r['user_id'] in users),
            ('user_follow', lambda r: r['follower_id'] in users or r['followed_id'] in users),
            ('post', lambda r: r['user_id'] in users),
            ('user_list_item', lambda r: r['list_id'] in {li['id'] for li in owned_lists}),
            ('user_list', lambda r: r['user_id'] in users),
            ('profile', lambda r: r['user_id'] in users),
            ('user', lambda r: r['id'] in users),
            ('media', lambda r: r['id'] in media),
        ):
            owned_lists = [r for r in self.rows('user_list') if r['user_id'] in users]
            rows = [r for r in self.rows(name) if predicate(r)]
            self.bulk_delete(name, [r['id'] for r in rows])
        self.journal['test_users'] = []
        self.journal['fixture_media_ids'] = []
        self.save()
        self.check('fixture_cleanup_complete', True)

    def edge_tests(self):
        a, _ = self.journal['test_users']
        mid, other = self.journal['fixture_media_ids'][:2]
        prepared = self.api('POST', 'lists', a, False, json={'default_kind': 'planned',
            'title': 'Quero ver / ler', 'description': '', 'is_public': False})
        prepared.raise_for_status()
        planned = prepared.json()
        self.api('PUT', f'media-list-status/{mid}', a, False, json={'status': 'want_to_watch'}).raise_for_status()
        with ThreadPoolExecutor(max_workers=2) as pool:
            put = pool.submit(self.api, 'PUT', f'media-list-status/{mid}', a, False, json={'status': 'watched'})
            delete = pool.submit(self.api, 'DELETE', f"lists/{planned['id']}/items/{mid}", a, False)
            responses = [put.result(), delete.result()]
        self.check('concurrent_conditional_delete_cannot_erase_other_status', all(r.status_code == 200 for r in responses)
                   and self.api('GET', f'media-list-status/{mid}', a, False).json()['status'] == 'watched')
        # A 1ms timeout against Xano can expire before delivery. Instead delay
        # only the response of a local proxy after the actual backend commits.
        committed = threading.Event()
        run = self
        class DelayedResponse(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_PUT(self):
                self.rfile.read(int(self.headers.get('Content-Length', '0')))
                upstream = run.request('PUT', run.social + f'/media-list-status/{other}',
                    headers={'Authorization': 'Bearer ' + a['token']}, json={'status': 'want_to_watch'})
                if upstream.status_code == 200: committed.set()
                time.sleep(.2)
                self.send_response(upstream.status_code)
                self.end_headers()
                try: self.wfile.write(upstream.content)
                except OSError: pass  # Expected socket close in the timeout probe.
        proxy = ThreadingHTTPServer(('127.0.0.1', 0), DelayedResponse)
        threading.Thread(target=proxy.serve_forever, daemon=True).start()
        timed_out = False
        try:
            with httpx.Client(timeout=httpx.Timeout(.05, connect=3)) as client:
                client.put(f'http://127.0.0.1:{proxy.server_port}/commit', json={})
        except httpx.ReadTimeout:
            timed_out = True
        finally:
            completed = committed.wait(timeout=15)
            proxy.shutdown()
            proxy.server_close()
        reconciled = self.api('GET', f'media-list-status/{other}', a, False)
        self.check('real_commit_delayed_response_timeout_reconciled', timed_out and completed and reconciled.status_code == 200
                   and reconciled.json()['status'] == 'want_to_watch')
        self.api('DELETE', f"lists/{planned['id']}", a, False).raise_for_status()
        remaining = [r for r in self.rows('user_media_list_status') if r['user_id'] == a['id']]
        self.check('delete_default_preserves_opposite_status', len(remaining) == 1 and remaining[0]['media_id'] == mid
                   and remaining[0]['status'] == 'watched')
        self.report['passed'] = True
        (EVIDENCE / 'real-edge-cases-2026-11-03.json').write_text(json.dumps(self.report, indent=2), encoding='utf-8')

    def remove_temporary_routes(self):
        groups = self.request('GET', self.base + '/apigroup', headers=self.headers).json()
        if isinstance(groups, dict):
            groups = groups['items']
        group = next(r for r in groups if r['name'] == 'Codeboxd')
        url = self.base + '/apigroup/' + str(group['id']) + '/api'
        apis = self.request('GET', url, headers=self.headers).json()
        if isinstance(apis, dict):
            apis = apis['items']
        expected = {identity(d) for d in blocks(staged_candidate()) if route(d)}
        for api in apis:
            if not api['name'].startswith(PREFIX):
                continue
            if api.get('guid') not in expected:
                raise ValueError('Unexpected temporary route identity')
            response = self.request('DELETE', url + '/' + str(api['id']), headers=self.headers)
            response.raise_for_status()
        self.check('temporary_routes_removed', True)

    def verify_final(self):
        fixture_sessions = [r['token'] for r in self.journal.get('test_users', [])]
        self.cleanup_fixtures()
        self.remove_temporary_routes()
        original = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
        plan = migration_plan(original)
        after = {name:self.rows(name) for name in original}
        after['user_media_list_status'] = self.rows('user_media_list_status')
        self.check('final_data_preservation_after_fixture_cleanup', verify_preservation(original, after, plan))
        source = export_workspace(self.client, self.base, self.headers)
        before_docs = {identity(d):d for d in blocks((PRIVATE/'baseline.xs').read_text(encoding='utf-8'))}
        current_docs = {identity(d):d for d in blocks(source)}
        scope = {identity(d) for d in blocks(candidate())}
        self.check('final_contract_scope', all(current_docs.get(k)==v for k,v in before_docs.items() if k not in scope)
                   and len(current_docs)==85 and not any((route(d) or ('',))[0].startswith(PREFIX) for d in current_docs.values())
                   and 'Manutenção breve das listas' not in source)
        self.import_docs(candidate(), 'final-no-delta', publish=False)
        preview = json.loads((PRIVATE/'final-no-delta-preview.json').read_text(encoding='utf-8'))
        self.check('published_candidate_has_zero_delta', not preview.get('operations'))
        if fixture_sessions:
            self.check('deleted_fixture_sessions_rejected', all(
                self.request('GET', self.auth+'/auth/me', headers={'Authorization':'Bearer '+token}).status_code==401
                for token in fixture_sessions))
        self.report.update(passed=True, fixture_users_remaining=0, fixture_media_remaining=0,
                           original_statuses=len(plan['statuses']), original_data_preserved=True,
                           candidate_sha256=fingerprint(candidate()), remote_documents=len(current_docs))
        (EVIDENCE/'final-integrity-2026-11-03.json').write_text(json.dumps(self.report,indent=2),encoding='utf-8')

    def cutover(self):
        if self.journal.get('phase') == 'released':
            raise ValueError('Cutover already released; refusing duplicate migration')
        rehearsal = json.loads((EVIDENCE / 'rehearsal-2026-11-03.json').read_text(encoding='utf-8'))
        self.check('matching_real_rehearsal', rehearsal['passed'] and rehearsal['candidate_sha256'] == fingerprint(candidate()))
        self.cleanup_fixtures()
        self.remove_temporary_routes()
        source = export_workspace(self.client, self.base, self.headers)
        (PRIVATE / 'before-cutover.xs').write_text(source, encoding='utf-8')
        original = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
        current = {name: self.rows(name) for name in original}
        self.check('no_original_data_drift', digest(original) == digest(current))
        self.check('new_status_table_empty', self.rows('user_media_list_status') == [])
        # All legacy/default writers and item reads, plus signup preparation.
        freeze = {'follows/{user_id}', 'lists', 'lists/{id}', 'lists/{id}/items',
                  'lists/{id}/items/{media_id}', 'lists/public/{id}/items', 'auth/signup'}
        originals, gated = [], []
        for doc in blocks(source):
            key = route(doc)
            if not key or key[0] not in freeze or (key[0] in ('lists', 'lists/{id}') and key[1] == 'GET'):
                continue
            originals.append(doc)
            gate = '\n    precondition (false) {\n      error_type = "standard"\n      error = "Manutenção breve das listas. Tente novamente em instantes."\n    }\n'
            gated.append(re.sub(r'(\bstack\s*{)', lambda m: m[0] + gate, doc, count=1))
        (PRIVATE / 'release-originals.xs').write_text('\n---\n'.join(originals), encoding='utf-8')
        self.journal['phase'] = 'gate_intent'
        self.save()
        self.import_docs('\n---\n'.join(gated), 'maintenance', publish=True)
        self.journal['phase'] = 'gated'
        self.save()
        after_gate = {name: self.rows(name) for name in original}
        self.check('no_drift_after_gate', digest(original) == digest(after_gate))
        plan = migration_plan(original)
        self.journal['migration_plan'] = plan
        self.save()
        self.journal['new_status_ids'] = self.bulk_add('user_media_list_status', plan['statuses'])
        self.journal['phase'] = 'statuses_copied'
        self.save()
        if plan['follow_delete_ids'] or plan['follow_rewrites']:
            raise ValueError('Unexpected follow cleanup requires reviewed additional journal')
        self.bulk_delete('user_list_item', plan['legacy_item_ids'])
        self.journal['phase'] = 'legacy_items_removed'
        self.save()
        after = {name: self.rows(name) for name in original}
        after['user_media_list_status'] = self.rows('user_media_list_status')
        self.check('migration_preservation_verified', verify_preservation(original, after, plan))
        self.finish_cutover(original, plan, originals)

    def resume_cutover(self):
        if self.journal.get('phase') != 'legacy_items_removed':
            raise ValueError('Unsupported resume phase; inspect journal')
        original = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
        plan = self.journal['migration_plan']
        originals = blocks((PRIVATE / 'release-originals.xs').read_text(encoding='utf-8'))
        before = {identity(d):d for d in blocks((PRIVATE / 'before-cutover.xs').read_text(encoding='utf-8'))}
        # Older Xano exports can leave simple route names unquoted. Include every
        # default-list preparation writer even if an earlier attempt missed it.
        known = {identity(d) for d in originals}
        additions = [d for d in before.values() if route(d) == ('lists', 'POST') and identity(d) not in known]
        if additions:
            gate = '\n    precondition (false) {\n      error_type = "standard"\n      error = "Manutenção breve das listas. Tente novamente em instantes."\n    }\n'
            originals.extend(additions)
            (PRIVATE / 'release-originals.xs').write_text('\n---\n'.join(originals), encoding='utf-8')
            self.import_docs('\n---\n'.join(re.sub(r'(\bstack\s*{)', lambda m:m[0]+gate, d, count=1) for d in additions), 'additional-preparation-gate', publish=True)
        current = {identity(d):d for d in blocks(export_workspace(self.client, self.base, self.headers))}
        gated_ids = {identity(d) for d in originals}
        self.check('resume_gates_and_contract_scope', all(current.get(k)==v for k,v in before.items() if k not in gated_ids)
                   and all('Manutenção breve das listas' in current.get(k,'') for k in gated_ids))
        after = {name:self.rows(name) for name in original}
        after['user_media_list_status'] = self.rows('user_media_list_status')
        self.check('migration_preservation_verified', verify_preservation(original, after, plan))
        self.finish_cutover(original, plan, originals)

    def finish_cutover(self, original, plan, originals):
        rehearsal = json.loads((EVIDENCE / 'rehearsal-2026-11-03.json').read_text(encoding='utf-8'))
        self.check('release_candidate_matches_rehearsal', rehearsal['passed'] and rehearsal['candidate_sha256']==fingerprint(candidate()))
        replacements = {identity(d): d for d in blocks('\n---\n'.join(originals))}
        replacements.update({identity(d): d for d in blocks(candidate())})
        final = '\n---\n'.join(replacements.values()) + '\n'
        self.import_docs(final, 'final-cutover', publish=True)
        self.journal['phase'] = 'released'
        self.save()
        final_source = export_workspace(self.client, self.base, self.headers)
        (PRIVATE / 'published.xs').write_text(final_source, encoding='utf-8')
        before_docs = {identity(d): d for d in blocks((PRIVATE / 'baseline.xs').read_text(encoding='utf-8'))}
        after_docs = {identity(d): d for d in blocks(final_source)}
        scope = {identity(d) for d in blocks(candidate())}
        self.check('no_unrelated_contract_change_at_release', all(after_docs.get(k) == v for k,v in before_docs.items() if k not in scope))
        report = {'passed': True, 'published': True, 'statuses_migrated': len(plan['statuses']),
                  'legacy_items_migrated': len(plan['legacy_item_ids']), 'conflicts_resolved': plan['conflicts_resolved'],
                  'candidate_sha256': fingerprint(candidate()), 'unrelated_data_preserved': True,
                  'unrelated_contracts_preserved': True}
        (EVIDENCE / 'cutover-2026-11-03.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

    def rollback_before_release(self):
        if self.journal.get('phase') == 'released':
            raise ValueError('Refusing rollback after writers released')
        if self.journal.get('phase') not in ('gated', 'statuses_copied', 'legacy_items_removed', 'gate_intent'):
            raise ValueError('No cutover phase to restore')
        original = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
        plan = migration_plan(original)
        current = {r['id']: r for r in self.rows('user_list_item')}
        missing = [r for r in original['user_list_item'] if r['id'] in plan['legacy_item_ids'] and r['id'] not in current]
        if missing:
            self.bulk_add('user_list_item', missing, allow_ids=True)
        statuses = self.rows('user_media_list_status')
        expected = {(r['user_id'], r['media_id'], r['status']) for r in plan['statuses']}
        if any((r['user_id'], r['media_id'], r['status']) not in expected for r in statuses):
            raise ValueError('Unexpected status written while gated')
        self.bulk_delete('user_media_list_status', [r['id'] for r in statuses])
        self.check('rollback_original_data_restored', digest({name:self.rows(name) for name in original}) == digest(original))
        self.import_docs((PRIVATE/'release-originals.xs').read_text(encoding='utf-8'), 'rollback-release', publish=True)
        self.journal['phase'] = 'rolled_back'
        self.save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'rehearse', 'cutover', 'resume-cutover', 'final-test', 'edge-tests', 'cleanup', 'verify-final', 'rollback'))
    args = parser.parse_args()
    if not EVIDENCE.parent.is_dir():
        parser.error('Change is no longer active; create a new change before reusing historical tooling')
    run = Run()
    try:
        if args.action == 'stage': run.stage()
        elif args.action == 'rehearse': run.rehearse()
        elif args.action == 'cutover': run.cutover()
        elif args.action == 'resume-cutover': run.resume_cutover()
        elif args.action == 'final-test': run.rehearse(final=True)
        elif args.action == 'edge-tests': run.edge_tests()
        elif args.action == 'cleanup': run.cleanup_fixtures(); run.remove_temporary_routes()
        elif args.action == 'verify-final': run.verify_final()
        elif args.action == 'rollback': run.rollback_before_release()
    except Exception as exc:
        failure = {'action': args.action, 'passed': False, 'failure_type': type(exc).__name__, 'phase': run.journal.get('phase')}
        if isinstance(exc, httpx.HTTPStatusError):
            failure.update(http_status=exc.response.status_code, endpoint=exc.request.url.path)
            try:
                payload = exc.response.json()
                failure.update(error_code=payload.get('code'), message=payload.get('message'))
            except ValueError: pass
        print(json.dumps(failure), flush=True)
        raise SystemExit(1) from None
    finally:
        run.client.close()


if __name__ == '__main__':
    main()
