"""Reviewable migration plans; no network or writes at import time."""
from collections import defaultdict
from copy import deepcopy
import json
from pathlib import Path

from tools.default_list_integrity import digest

PRIVATE = Path(__file__).resolve().parents[1] / '.local/conexoes-feed-listas/deployment-2026-11-03'


def default_status(row):
    key = row.get('default_key')
    if key is None:
        return None
    mapping = {f"{row['user_id']}:planned": 'want_to_watch',
               f"{row['user_id']}:completed": 'watched'}
    if key not in mapping:
        raise ValueError('Invalid default list identity; review before migration')
    return mapping[key]


def migration_plan(snapshot):
    """Preserve custom/orphan rows; only keyed default items enter the plan."""
    lists = {row['id']: row for row in snapshot['user_list']}
    users = {row['id'] for row in snapshot['user']}
    media = {row['id'] for row in snapshot['media']}
    if len(lists) != len(snapshot['user_list']):
        raise ValueError('Duplicate list IDs')
    seen_keys = set()
    for row in lists.values():
        kind = default_status(row)
        if kind:
            if row['default_key'] in seen_keys:
                raise ValueError('Duplicate default list identity')
            seen_keys.add(row['default_key'])

    statuses, legacy_items, conflicts = {}, [], set()
    for row in snapshot.get('user_media_list_status', []):
        pair = (row['user_id'], row['media_id'])
        if (row['status'] not in ('watched', 'want_to_watch') or pair in statuses
                or pair[0] not in users or pair[1] not in media):
            raise ValueError('Invalid or duplicate existing status')
        statuses[pair] = row['status']
    for row in snapshot['user_list_item']:
        owner_list = lists.get(row['list_id'])
        kind = default_status(owner_list) if owner_list else None
        if not kind:
            continue
        pair = (owner_list['user_id'], row['media_id'])
        if pair[0] not in users or pair[1] not in media:
            raise ValueError('Default item has invalid owner/media; preserve and review')
        previous = statuses.get(pair)
        if previous and previous != kind:
            conflicts.add(pair)
        statuses[pair] = 'watched' if 'watched' in (kind, previous) else kind
        legacy_items.append(row['id'])

    follows = defaultdict(list)
    for row in snapshot['user_follow']:
        follows[(row['follower_id'], row['followed_id'])].append(row)
    deletions, rewrites = [], []
    for pair, rows in sorted(follows.items()):
        rows = sorted(rows, key=lambda row: row['id'])
        canonical = f'{pair[0]}:{pair[1]}'
        valid = pair[0] in users and pair[1] in users and pair[0] != pair[1]
        if not valid and len(rows) > 1:
            raise ValueError('Duplicate orphan/self follow requires manual review')
        if not valid:
            continue
        deletions.extend(row['id'] for row in rows[1:])
        if rows[0].get('identity_key') != canonical:
            if any(row.get('identity_key') == canonical and
                   (row['follower_id'], row['followed_id']) != pair
                   for row in snapshot['user_follow']):
                raise ValueError('Follow identity points to a different pair')
            rewrites.append({'id': rows[0]['id'], 'identity_key': canonical})
    return {
        'snapshot_sha256': digest(snapshot),
        'statuses': [{'user_id': pair[0], 'media_id': pair[1], 'status': kind}
                     for pair, kind in sorted(statuses.items())],
        'legacy_item_ids': sorted(legacy_items),
        'conflicts_resolved': len(conflicts),
        'follow_delete_ids': sorted(deletions), 'follow_rewrites': rewrites,
    }


def verify_preservation(before, after, plan):
    """Compare complete rows, including ratings/reviews and custom metadata."""
    if digest(before) != plan['snapshot_sha256']:
        raise ValueError('Plan does not match backup')
    for name, rows in before.items():
        if name in ('user_media_list_status', 'user_list_item', 'user_follow'):
            continue
        if sorted(rows, key=lambda r: r['id']) != sorted(after[name], key=lambda r: r['id']):
            raise ValueError('Unrelated data changed: ' + name)
    expected_items = [r for r in before['user_list_item'] if r['id'] not in plan['legacy_item_ids']]
    if sorted(expected_items, key=lambda r: r['id']) != sorted(after['user_list_item'], key=lambda r: r['id']):
        raise ValueError('Unexpected custom/legacy item mutation')
    expected_follows = [deepcopy(r) for r in before['user_follow'] if r['id'] not in plan['follow_delete_ids']]
    rewrites = {r['id']: r['identity_key'] for r in plan['follow_rewrites']}
    for row in expected_follows:
        if row['id'] in rewrites:
            row['identity_key'] = rewrites[row['id']]
    if sorted(expected_follows, key=lambda r: r['id']) != sorted(after['user_follow'], key=lambda r: r['id']):
        raise ValueError('Unexpected follow mutation')
    actual_statuses = [{key: row[key] for key in ('user_id', 'media_id', 'status')}
                       for row in after['user_media_list_status']]
    order = lambda r: (r['user_id'], r['media_id'])
    if sorted(actual_statuses, key=order) != plan['statuses']:
        raise ValueError('Migration status mismatch')
    return True


if __name__ == '__main__':
    snapshot = json.loads((PRIVATE / 'backup.json').read_text(encoding='utf-8'))
    plan = migration_plan(snapshot)
    target = PRIVATE / 'migration-plan.json'
    if target.exists() and json.loads(target.read_text(encoding='utf-8')) != plan:
        raise SystemExit('Preserve existing plan; review changed backup')
    target.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    print(json.dumps({'statuses': len(plan['statuses']), 'legacy_items': len(plan['legacy_item_ids']),
                      'conflicts': plan['conflicts_resolved'], 'follow_deletes': len(plan['follow_delete_ids']),
                      'follow_rewrites': len(plan['follow_rewrites']), 'remote_writes': 0}))
