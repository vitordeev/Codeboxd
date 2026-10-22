"""Test-only app entry point: real pages/state with a fictional catalog search."""
from copy import deepcopy
from Codeboxd_main.services import catalog
from tools.feed_lists_browser import MEDIA


async def fixture_search(query, kind='all', page=1):
    return [deepcopy(item) for item in MEDIA
            if catalog.title_score(query,item)>0 and (kind=='all' or item['media_type']==kind)], []


catalog.search=fixture_search

from Codeboxd_main.Codeboxd_main import app  # noqa: E402,F401
