"""Isolated browser entry point: fixture accounts and no catalog network calls."""
from Codeboxd_main.services import catalog

async def no_fetch(*args, **kwargs):
    return {}

async def no_items(*args, **kwargs):
    return []

catalog.fetch = no_fetch
catalog.home_collection = no_items
catalog.series_highlights = no_items
from tools.feed_lists_fixture_app import app  # noqa: E402,F401
