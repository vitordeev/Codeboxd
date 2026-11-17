"""Client for durable Xano reservations. No activation or implicit upload retry."""
from dataclasses import dataclass
import re

from .api import APIError, request


STATES = frozenset(('reserved', 'verified', 'attached', 'reconciliation_required',
                    'cleanup_pending', 'deleted'))


@dataclass(frozen=True)
class ImageReservation:
    id: int
    owner_id: int
    operation_key: str
    operation: str
    post_id: int
    expected_revision: int
    state: str
    cloud: str
    public_id: str

    @classmethod
    def parse(cls, body, *, owner_id, operation_key=None):
        try:
            if (type(owner_id) is not int or owner_id <= 0 or not isinstance(body, dict)
                    or type(body.get('contract_version')) is not int or body['contract_version'] != 1
                    or type(body.get('id')) is not int or body['id'] <= 0
                    or type(body.get('user_id')) is not int or body['user_id'] != owner_id
                    or not isinstance(body.get('operation_key'), str)
                    or not re.fullmatch(r'[a-f0-9]{32}', body['operation_key'])
                    or (operation_key is not None and body['operation_key'] != operation_key)
                    or body.get('operation') not in ('create', 'replace')
                    or body.get('state') not in STATES
                    or type(body.get('expected_image_revision')) is not int
                    or body['expected_image_revision'] < 0
                    or type(body.get('post_id')) is not int or body['post_id'] < 0
                    or (body['operation'] == 'replace' and body['post_id'] == 0)
                    or not isinstance(body.get('cloud'), str)
                    or not re.fullmatch(r'[A-Za-z0-9_-]+', body['cloud'])
                    or not isinstance(body.get('public_id'), str)
                    or not re.fullmatch(rf'codeboxd/posts/u{owner_id}/[a-f0-9]{{32}}', body['public_id'])):
                raise ValueError('Invalid reservation')
            return cls(body['id'], owner_id, body['operation_key'], body['operation'], body['post_id'],
                       body['expected_image_revision'], body['state'], body['cloud'], body['public_id'])
        except (ValueError, TypeError, KeyError):
            raise APIError('O serviço retornou uma reserva de imagem inválida.') from None


def _session(token, owner_id):
    if not isinstance(token, str) or not token.strip() or type(owner_id) is not int or owner_id <= 0:
        raise APIError('Entre na sua conta antes de anexar uma imagem.')


async def reserve_image(*, token, owner_id, operation_key, operation='create', post_id=0,
                        expected_revision=0):
    _session(token, owner_id)
    if (not isinstance(operation_key, str) or not re.fullmatch(r'[a-f0-9]{32}', operation_key)
            or operation not in ('create', 'replace') or type(post_id) is not int or post_id < 0
            or type(expected_revision) is not int or expected_revision < 0
            or (operation == 'create' and (post_id != 0 or expected_revision != 0))
            or (operation == 'replace' and post_id <= 0)):
        raise APIError('A operação de imagem é inválida.')
    body = await request('POST', '/post-image-uploads', token=token, data={
        'operation_key': operation_key, 'operation': operation, 'post_id': post_id,
        'expected_image_revision': expected_revision})
    reservation = ImageReservation.parse(body, owner_id=owner_id, operation_key=operation_key)
    if (reservation.operation != operation or reservation.expected_revision != expected_revision
            or (operation == 'replace' and reservation.post_id != post_id)):
        raise APIError('A reserva pertence a outro contexto de edição.')
    return reservation


async def read_reservation(*, token, owner_id, reservation_id):
    _session(token, owner_id)
    if type(reservation_id) is not int or reservation_id <= 0:
        raise APIError('A reserva de imagem é inválida.')
    body = await request('GET', f'/post-image-uploads/{reservation_id}', token=token)
    result = ImageReservation.parse(body, owner_id=owner_id)
    if result.id != reservation_id:
        raise APIError('A reserva retornada não corresponde à operação.')
    return result
