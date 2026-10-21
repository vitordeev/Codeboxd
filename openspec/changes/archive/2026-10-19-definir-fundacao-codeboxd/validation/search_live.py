"""Read-only provider search smoke; run from the repository root."""
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / 'rxconfig.py').is_file())
sys.path.insert(0, str(ROOT))

from Codeboxd_main.services import catalog


async def main():
    checks = []
    for kind, query, source in (
        ('movie', 'Matrix', 'tmdb'),
        ('series', 'Breaking Bad', 'tmdb'),
        ('anime', 'Cowboy Bebop', 'kitsu'),
        ('book', 'Duna', 'openlibrary'),
    ):
        items, errors = await catalog.search(query, kind)
        passed = bool(items) and not errors and all(
            item.get('media_type') == kind
            and item.get('external_source') == source
            and item.get('external_id')
            and item.get('identity_key')
            for item in items
        )
        checks.append({
            'kind': kind, 'query': query, 'provider': source,
            'result': 'PASS' if passed else 'FAIL', 'count': len(items),
            'errors': errors,
            'examples': [
                {key: item.get(key) for key in ('title', 'media_type', 'external_source', 'external_id', 'identity_key')}
                for item in items[:3]
            ],
        })
    print(json.dumps({'checked_at': datetime.now(timezone.utc).isoformat(), 'checks': checks}, ensure_ascii=True, indent=2))
    return 0 if all(check['result'] == 'PASS' for check in checks) else 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
