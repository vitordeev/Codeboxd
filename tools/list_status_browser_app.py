"""Real app with a longer transport timeout for the paced validation proxy."""
import httpx
from Codeboxd_main.services import api

_original_client = api._new_api_client


def _paced_client():
    client = _original_client()
    client.timeout = httpx.Timeout(60, connect=3)
    return client


api._new_api_client = _paced_client
from Codeboxd_main.Codeboxd_main import app  # noqa: E402,F401
