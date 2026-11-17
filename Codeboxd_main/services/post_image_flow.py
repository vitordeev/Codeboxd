"""Opt-in external image workflow. Durable ownership stays in Xano."""
from .api import APIError, request
from .cloudinary_uploads import upload_config, upload_post_image, verify_post_image, recover_post_image
from .post_image_reservations import reserve_image


def _current(check):
    if not check():
        raise APIError('A sessão ou o editor mudou. Reabra a publicação.')


async def prepare_image(*, token, owner_id, operation_key, post_id, expected_revision,
                        content, mime, current, receipt=None):
    """Reserve, claim once, upload and verify. Never commits or deletes a post.

    Caller may retain the signed receipt privately to retry an uncertain commit.
    Without a receipt, a started upload must be reconciled, never blindly resent.
    """
    config = upload_config()
    _current(current)
    capabilities = await request('GET', '/post-image-capabilities')
    _current(current)
    if (not isinstance(capabilities, dict) or type(capabilities.get('contract_version')) is not int
            or capabilities['contract_version'] != 1 or capabilities.get('uploads_enabled') is not True):
        raise APIError('O contrato de imagens ainda não está disponível. O rascunho foi preservado.')
    reservation = await reserve_image(token=token, owner_id=owner_id, operation_key=operation_key,
        operation='replace' if post_id else 'create', post_id=post_id,
        expected_revision=expected_revision)
    _current(current)
    if reservation.cloud != config.cloud_name:
        raise APIError('A reserva pertence a outro serviço de imagens.')
    if reservation.state == 'attached':
        return reservation, None
    if receipt is None:
        if reservation.state == 'reconciliation_required':
            receipt = await recover_post_image(owner_id=owner_id, public_id=reservation.public_id)
            _current(current)
            return reservation, receipt
        if reservation.state != 'reserved':
            raise APIError('O envio anterior precisa ser conciliado. O rascunho foi preservado.')
        granted = await request('POST', f'/post-image-uploads/{reservation.id}/begin', token=token)
        _current(current)
        if (not isinstance(granted, dict) or type(granted.get('id')) is not int
                or granted['id'] != reservation.id or granted.get('upload_granted') is not True
                or type(granted.get('contract_version')) is not int or granted['contract_version'] != 1):
            raise APIError('O início do envio não foi confirmado. Consulte a operação antes de tentar novamente.')
        receipt = await upload_post_image(owner_id=owner_id, content=content, mime=mime,
                                          public_id=reservation.public_id)
        _current(current)
    await verify_post_image(receipt, owner_id=owner_id, public_id=reservation.public_id)
    _current(current)
    return reservation, receipt
