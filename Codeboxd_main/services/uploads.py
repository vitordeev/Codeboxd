"""Multipart file uploads to Xano file-resource inputs."""
import httpx

from .api import APIError, base_url


async def upload_file(path: str, *, method: str = 'POST', token: str, data: dict, field: str,
                      filename: str, content: bytes, mime: str):
    if not path.startswith('/') or '://' in path or '..' in path:
        raise ValueError('Invalid API path')
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(45, connect=5)) as client:
            response = await client.request(method, base_url('social') + path, headers=headers,
                data=data, files={field: (filename, content, mime)})
    except httpx.RequestError as exc:
        raise APIError('N\\u00e3o foi poss\\u00edvel enviar a imagem. Tente novamente.') from exc
    if response.is_error:
        messages = {
            400: 'A imagem ou os dados do post foram rejeitados.',
            401: 'Sua sess\\u00e3o expirou. Entre novamente.',
            403: 'Voc\\u00ea n\\u00e3o tem permiss\\u00e3o para esta a\\u00e7\\u00e3o.',
            404: 'Publica\\u00e7\\u00e3o n\\u00e3o encontrada.',
            413: 'A imagem excede o tamanho permitido.',
            422: 'Confira os dados da publica\\u00e7\\u00e3o.',
            429: 'Muitas solicita\\u00e7\\u00f5es. Aguarde e tente novamente.',
        }
        raise APIError(messages.get(response.status_code,
            'N\\u00e3o foi poss\\u00edvel salvar a imagem. Tente novamente.'), response.status_code)
    if response.status_code == 204 or not response.content:
        return None
    try:
        return response.json()
    except ValueError as exc:
        raise APIError('O servi\\u00e7o retornou uma resposta inv\\u00e1lida.') from exc
