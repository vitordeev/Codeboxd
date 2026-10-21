"""Async Xano transport. No network calls or mandatory secrets at import time."""
import os
import asyncio
import math
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


class APIError(Exception):
    def __init__(self, message: str, status: int = 0, retry_after: int = 0):
        super().__init__(message)
        self.status = status
        self.retry_after = retry_after


def retry_after_seconds(value: str) -> int:
    try:
        seconds = float(value)
        return max(1, math.ceil(seconds)) if math.isfinite(seconds) else 30
    except (ValueError, TypeError):
        try:
            deadline = parsedate_to_datetime(value)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
            return max(1, math.ceil((deadline - datetime.now(timezone.utc)).total_seconds()))
        except (ValueError, TypeError, OverflowError):
            return 30


def base_url(group: str) -> str:
    key = {'auth': 'XANO_AUTH_URL', 'social': 'XANO_SOCIAL_URL', 'legacy': 'XANO_BASE_URL'}[group]
    url = os.getenv(key, '').strip().rstrip('/')
    if not url:
        raise APIError('Este serviço ainda não está disponível. Tente novamente mais tarde.')
    if not url.startswith(('https://', 'http://localhost', 'http://127.0.0.1')):
        raise APIError('Configuração de serviço inválida.')
    return url


async def request(method: str, path: str, *, group: str = 'social', token: str = '',
                  data: dict | None = None, params: dict | None = None) -> Any:
    if not path.startswith('/') or '://' in path or '..' in path:
        raise ValueError('Invalid API path')
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10, connect=3)) as client:
            for attempt in range(3):
                response = await client.request(method, base_url(group) + path,
                                                headers=headers, json=data, params=params)
                # This legacy GET sends email and is not a safe read.
                safe_read = (method.upper() in ('GET', 'HEAD')
                             and not (group == 'auth' and path == '/reset/request-reset-link'))
                if response.status_code != 429 or not safe_read or attempt == 2:
                    break
                delay = retry_after_seconds(response.headers.get('Retry-After', ''))
                if delay > 3:
                    break
                await asyncio.sleep(delay)
    except httpx.RequestError as exc:
        raise APIError('Não foi possível conectar. Tente novamente em instantes.') from exc
    if response.is_error:
        if response.status_code == 429:
            wait = retry_after_seconds(response.headers.get('Retry-After', ''))
            raise APIError(f'Muitas solicitações. Tente novamente em {wait} segundos.', 429, wait)
        messages = {
            400: 'Confira os dados informados.', 401: 'Sua sessão expirou. Entre novamente.',
            403: 'Você não tem permissão para esta ação.', 404: 'Conteúdo não encontrado.',
            409: 'Este registro já existe.', 422: 'Confira os dados informados.',
            429: 'Muitas solicitações. Aguarde alguns instantes.',
        }
        raise APIError(messages.get(response.status_code, 'Serviço indisponível. Tente novamente.'), response.status_code)
    if response.status_code == 204 or not response.content:
        return None
    try:
        return response.json()
    except ValueError as exc:
        raise APIError('O serviço retornou uma resposta inválida.') from exc


def rows(value: Any) -> list[dict]:
    """Accept list and Xano paginated response without silently ignoring bad data."""
    if isinstance(value, dict):
        value = value.get('items')
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise APIError('O serviço retornou dados em formato inesperado.')
    return value
