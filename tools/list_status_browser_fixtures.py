"""Create minimal disposable browser fixtures, with a separate private journal."""
import argparse
import json
from pathlib import Path

from tools import list_status_live as live


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('setup', 'cleanup'))
    parser.add_argument('--private-dir', required=True, type=Path)
    args = parser.parse_args()
    private = args.private_dir.resolve()
    if not private.is_relative_to((live.ROOT / '.local').resolve()):
        raise ValueError('Private journal must stay under .local')
    private.mkdir(parents=True, exist_ok=True)
    live.PRIVATE = private
    run = live.Run()
    try:
        if args.action == 'cleanup':
            run.cleanup_fixtures()
            return
        if run.journal.get('browser_fixture_ready'):
            raise ValueError('Fixtures already ready; preserve or clean this run')
        a, b = run.fixture_users()
        marker = run.journal['fixture_marker']
        if not run.journal.get('fixture_media_ids'):
            run.journal['fixture_media_ids'] = run.bulk_add('media', [{
                'identity_key': marker, 'external_source': 'test',
                'external_id': marker, 'media_type': 'movie', 'title': marker}])
            run.save()
        mid = run.journal['fixture_media_ids'][0]
        run.api('POST', 'posts', b, False, json={'body': marker}).raise_for_status()
        run.api('PUT', 'interactions', a, False, json={
            'media_id': mid, 'status': 'planned', 'rating': 4.5,
            'review': marker, 'spoiler': False}).raise_for_status()
        run.check('reader_has_no_posts', not any(r['user_id'] == a['id'] for r in run.rows('post')))
        run.check('reader_starts_unfollowed', not any(r['follower_id'] == a['id'] for r in run.rows('user_follow')))
        run.check('reader_starts_without_list_status', run.api(
            'GET', f'media-list-status/{mid}', a, False).json().get('status') is None)
        run.journal['browser_fixture_ready'] = True
        run.save()
        print(json.dumps({'browser_fixture_ready': True, 'users': 2, 'media': 1}))
    finally:
        run.client.close()


if __name__ == '__main__':
    main()
