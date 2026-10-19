"""Two short public samples; never emits credentials or provider error bodies."""
import asyncio
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from dotenv import load_dotenv
load_dotenv(ROOT / '.env')
from Codeboxd_main.services import translation


async def main():
    original = 'A young explorer discovers a hidden library and begins an unexpected adventure.'
    translated = await translation.translate_description(original)
    with patch.object(translation.httpx, 'AsyncClient', side_effect=AssertionError('Cache miss')):
        cached = await translation.translate_description(original)
    portuguese = 'Uma jovem descobre uma biblioteca e começa uma aventura.'
    preserved = await translation.translate_description(portuguese)
    report = {'layer': 'remote_deepl_and_local_persistent_cache',
              'translation_changed': translated != original,
              'translated_sample': translated,
              'cache_reused_without_network': cached == translated and translated != original,
              'portuguese_preserved': preserved == portuguese,
              'browser_executed': False}
    Path(__file__).with_name('deepl-smoke-2026-10-19.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return 0 if all(report[key] for key in ('translation_changed', 'cache_reused_without_network', 'portuguese_preserved')) else 1


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
