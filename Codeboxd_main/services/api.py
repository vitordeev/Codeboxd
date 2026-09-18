"""Async Xano transport. No network calls or mandatory secrets at import time."""
import os
import asyncio
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


class APIError(Exception):
    def __init__(self, message: str, status: int = 0):
        super().__init__(message)
        self.status = status


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
        async with httpx.AsyncClient(timeout=httpx.Timeout(20, connect=8)) as client:
            for attempt in range(3):
                response = await client.request(method, base_url(group) + path,
                                                headers=headers, json=data, params=params)
                if response.status_code != 429 or attempt == 2:
                    break
                try:
                    delay = min(30, max(1, int(response.headers.get('Retry-After', '21'))))
                except ValueError:
                    delay = 21
                await asyncio.sleep(delay)
    except httpx.RequestError as exc:
        raise APIError('Não foi possível conectar. Tente novamente em instantes.') from exc
    if response.is_error:
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
