"""Optional server-side description translation; credentials never leave headers."""
import asyncio
import hashlib
import logging
import os
from pathlib import Path
import sqlite3
import time
from contextlib import closing
from weakref import WeakKeyDictionary

import httpx

logger = logging.getLogger(__name__)
CACHE_PATH = Path(__file__).resolve().parents[2] / '.local' / 'description-translations.sqlite3'
_locks = WeakKeyDictionary()
_blocked_until = 0.0


def _cache(key: str, text: str | None = None) -> str | None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(CACHE_PATH, timeout=1)) as connection:
        with connection:
            connection.execute('CREATE TABLE IF NOT EXISTS translations (cache_key TEXT PRIMARY KEY, text TEXT NOT NULL)')
            if text is not None:
                connection.execute('INSERT OR REPLACE INTO translations VALUES (?, ?)', (key, text))
                connection.execute('DELETE FROM translations WHERE rowid NOT IN (SELECT rowid FROM translations ORDER BY rowid DESC LIMIT 10000)')
                return text
            row = connection.execute('SELECT text FROM translations WHERE cache_key = ?', (key,)).fetchone()
            return row[0] if row else None


async def translate_description(text: str) -> str:
    """Translate on demand, reusing durable results and retaining originals on errors."""
    global _blocked_until
    api_key = os.getenv('DEEPL_API_KEY', '').strip()
    if not api_key or not text.strip() or len(text) > 20000:
        return text
    cache_key = hashlib.sha256(('v1:PT-BR:' + text).encode('utf-8')).hexdigest()
    loop = asyncio.get_running_loop()
    lock = _locks.setdefault(loop, asyncio.Lock())
    async with lock:
        try:
            cached = await asyncio.to_thread(_cache, cache_key)
        except (OSError, sqlite3.Error):
            logger.warning('translation_unavailable reason=cache')
            return text
        if cached is not None:
            return cached
        if time.monotonic() < _blocked_until:
            return text
        endpoint = 'https://api-free.deepl.com/v2/translate' if api_key.endswith(':fx') else 'https://api.deepl.com/v2/translate'
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(8, connect=3)) as client:
                response = await client.post(endpoint,
                    headers={'Authorization': 'DeepL-Auth-Key ' + api_key},
                    json={'text': [text], 'target_lang': 'PT-BR'})
                response.raise_for_status()
                payload = response.json()
                result = payload['translations'][0]
                translated = result['text']
                if not isinstance(translated, str) or not translated.strip():
                    raise ValueError('Empty translation')
                if str(result.get('detected_source_language', '')).upper() == 'PT':
                    translated = text
        except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError):
            status = response.status_code if 'response' in locals() else 0
            _blocked_until = time.monotonic() + (900 if status in (403, 456) else 60)
            logger.warning('translation_unavailable status=%s', status or 'network')
            return text
        try:
            await asyncio.to_thread(_cache, cache_key, translated)
        except (OSError, sqlite3.Error):
            logger.warning('translation_unavailable reason=cache_write')
            return text
        return translated
