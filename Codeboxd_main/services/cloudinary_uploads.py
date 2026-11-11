"""Prepared server-only Cloudinary transport; not yet wired into post persistence."""
from dataclasses import dataclass, field
import hashlib
import os
import re
import time
from urllib.parse import urlsplit
import uuid

import httpx

from .api import APIError

MAX_BYTES = 5 * 1024 * 1024
MIMES = {'image/png': ('png', (b'\x89PNG\r\n\x1a\n',)),
         'image/jpeg': ('jpg', (b'\xff\xd8\xff',)),
         'image/gif': ('gif', (b'GIF87a', b'GIF89a')),
         'image/webp': ('webp', (b'RIFF',))}


@dataclass(frozen=True)
class CloudinaryConfig:
    cloud_name: str
    api_key: str = field(repr=False)
    api_secret: str = field(repr=False)


@dataclass(frozen=True)
class CloudinaryImage:
    secure_url: str
    public_id: str
    asset_id: str
    width: int
    height: int
    bytes: int
    format: str


def upload_config() -> CloudinaryConfig:
    if os.getenv('CLOUDINARY_UPLOADS_ENABLED', 'false').strip().lower() != 'true':
        raise APIError('A hospedagem externa de imagens ainda não está ativada.')
    cloud, key, secret = (os.getenv(name, '').strip() for name in
                          ('CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET'))
    if not cloud or not key or not secret or not re.fullmatch(r'[A-Za-z0-9_-]+', cloud):
        raise APIError('A configuração da hospedagem de imagens está incompleta.')
    return CloudinaryConfig(cloud, key, secret)


def _read_image(body, config, public_id):
    if not isinstance(body, dict):
        raise ValueError('Invalid response')
    url = body.get('secure_url', '')
    if not isinstance(url, str):
        raise ValueError('Invalid URL')
    parts = urlsplit(url)
    if (parts.scheme != 'https' or parts.netloc != 'res.cloudinary.com'
            or parts.path.split('/')[1:2] != [config.cloud_name] or parts.query or parts.fragment):
        raise ValueError('Invalid URL')
    if (body.get('public_id') != public_id or not isinstance(body.get('asset_id'), str)
            or not body['asset_id'] or body.get('resource_type') != 'image' or body.get('type') != 'upload'
            or body.get('format') not in ('png', 'jpg', 'jpeg', 'gif', 'webp')):
        raise ValueError('Invalid metadata')
    if any(type(body.get(k)) is not int or body[k] <= 0 for k in ('width', 'height', 'bytes')) or body['bytes'] > MAX_BYTES:
        raise ValueError('Invalid dimensions/size')
    return CloudinaryImage(url, public_id, body['asset_id'], body['width'], body['height'], body['bytes'], body['format'])


async def upload_post_image(*, owner_id: int, content: bytes, mime: str) -> CloudinaryImage:
    """Caller must authorize the owner; this adapter only signs/uploads validated bytes."""
    config = upload_config()
    if type(owner_id) is not int or owner_id <= 0:
        raise APIError('Entre na sua conta antes de anexar uma imagem.')
    if not isinstance(content, bytes) or not 0 < len(content) <= MAX_BYTES:
        raise APIError('A imagem deve ter no máximo 5 MB.')
    kind = MIMES.get(mime)
    if not kind or not any(content.startswith(s) for s in kind[1]) or (mime == 'image/webp' and content[8:12] != b'WEBP'):
        raise APIError('Envie uma imagem PNG, JPG, WEBP ou GIF válida.')
    public_id = f'codeboxd/posts/u{owner_id}/{uuid.uuid4().hex}'
    params = {'overwrite': 'false', 'public_id': public_id, 'timestamp': str(int(time.time()))}
    canonical = '&'.join(f'{key}={params[key]}' for key in sorted(params))
    signature = hashlib.sha256((canonical + config.api_secret).encode()).hexdigest()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(45, connect=5), follow_redirects=False) as client:
            response = await client.post(f'https://api.cloudinary.com/v1_1/{config.cloud_name}/image/upload',
                data={**params, 'api_key': config.api_key, 'signature': signature},
                files={'file': ('image.' + kind[0], content, mime)})
    except httpx.RequestError:
        raise APIError('Não foi possível enviar a imagem. Tente novamente.') from None
    if not response.is_success:
        raise APIError('O serviço de imagens não aceitou o envio. Tente novamente mais tarde.')
    try:
        return _read_image(response.json(), config, public_id)
    except (ValueError, TypeError, KeyError):
        raise APIError('O serviço de imagens retornou uma resposta inválida.') from None
