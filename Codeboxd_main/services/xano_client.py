"""Cliente HTTP para conversar com a API do Xano.

O Xano tem dois API Groups com URLs base diferentes:
- XANO_BASE_URL  -> grupo "Titulos" (CRUD de conteúdo)
- XANO_AUTH_URL  -> grupo "Authentication" (login/signup/reset)

Uso básico:
    from Codeboxd_main.services.xano_client import xano_get, xano_post, auth_post

    titulos = await xano_get("/titulos")
    login_resp = await auth_post("/auth/login", {"email": e, "password": p})
"""

import os

import httpx
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env na raiz do projeto.
load_dotenv()

XANO_BASE_URL = os.getenv("XANO_BASE_URL")
XANO_AUTH_URL = os.getenv("XANO_AUTH_URL")

if not XANO_BASE_URL:
    raise RuntimeError(
        "XANO_BASE_URL não encontrada. Confirme que o arquivo .env está na raiz "
        "do projeto e contém a linha XANO_BASE_URL=..."
    )

if not XANO_AUTH_URL:
    raise RuntimeError(
        "XANO_AUTH_URL não encontrada. Confirme que o arquivo .env está na raiz "
        "do projeto e contém a linha XANO_AUTH_URL=..."
    )


def _headers(token: str | None = None) -> dict:
    """Monta os headers da requisição, incluindo o token de auth quando houver."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def _get(base_url: str, path: str, token: str | None = None) -> dict | list:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}{path}", headers=_headers(token))
        response.raise_for_status()
        return response.json()


async def _post(base_url: str, path: str, data: dict, token: str | None = None) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}{path}", json=data, headers=_headers(token)
        )
        response.raise_for_status()
        return response.json()


async def _patch(base_url: str, path: str, data: dict, token: str | None = None) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{base_url}{path}", json=data, headers=_headers(token)
        )
        response.raise_for_status()
        return response.json()


async def _delete(base_url: str, path: str, token: str | None = None) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{base_url}{path}", headers=_headers(token))
        response.raise_for_status()


# ---------- Grupo "Titulos" (conteúdo) ----------

async def xano_get(path: str, token: str | None = None):
    """GET em {XANO_BASE_URL}{path}. Ex: xano_get('/titulos')."""
    return await _get(XANO_BASE_URL, path, token)


async def xano_post(path: str, data: dict, token: str | None = None):
    """POST em {XANO_BASE_URL}{path}. Ex: criar um título."""
    return await _post(XANO_BASE_URL, path, data, token)


async def xano_patch(path: str, data: dict, token: str | None = None):
    """PATCH em {XANO_BASE_URL}{path}. Ex: editar um título existente."""
    return await _patch(XANO_BASE_URL, path, data, token)


async def xano_delete(path: str, token: str | None = None):
    """DELETE em {XANO_BASE_URL}{path}. Ex: remover um título."""
    return await _delete(XANO_BASE_URL, path, token)


# ---------- Grupo "Authentication" (login/signup/reset) ----------

async def auth_get(path: str, token: str | None = None):
    """GET em {XANO_AUTH_URL}{path}. Ex: buscar dados do usuário logado."""
    return await _get(XANO_AUTH_URL, path, token)


async def auth_post(path: str, data: dict, token: str | None = None):
    """POST em {XANO_AUTH_URL}{path}. Ex: auth_post('/auth/login', {...})."""
    return await _post(XANO_AUTH_URL, path, data, token)