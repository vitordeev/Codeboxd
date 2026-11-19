"""Offline preview for supervised Cloudinary cleanup."""
from dataclasses import dataclass
from datetime import datetime, timezone
import re

from .api import APIError


@dataclass(frozen=True)
class CleanupCandidate:
    asset_id: int
    owner_id: int
    cloud: str
    public_id: str
    state: str
    retain_until: datetime
    reference_count: int
    provider_asset_id: str


@dataclass(frozen=True)
class CleanupPreview:
    approval_reference: str
    candidates: tuple[CleanupCandidate, ...]


def prepare_cleanup_preview(*, owner_id: int, cloud: str, approval_reference: str,
                            candidates, now=None, limit=10):
    if (type(owner_id) is not int or owner_id <= 0
            or not isinstance(cloud, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', cloud)
            or not isinstance(approval_reference, str)
            or not re.fullmatch(r'[A-Za-z0-9_.:-]{8,128}', approval_reference)
            or type(limit) is not int or limit != 10):
        raise APIError('A prévia de limpeza é inválida.')
    now = now or datetime.now(timezone.utc)
    if not isinstance(candidates, (list, tuple)):
        raise APIError('Os candidatos de limpeza são inválidos.')
    if len(candidates) > limit:
        raise APIError('A prévia excede o limite supervisionado de dez candidatos.')
    accepted = []
    seen = set()
    for item in candidates:
        if not isinstance(item, CleanupCandidate):
            raise APIError('A prévia contém um candidato inválido.')
        if (type(item.asset_id) is not int or item.asset_id <= 0 or item.asset_id in seen
                or type(item.owner_id) is not int or item.owner_id != owner_id or item.cloud != cloud
                or item.state != 'cleanup_pending' or item.reference_count != 0
                or type(item.reference_count) is not int
                or not isinstance(item.provider_asset_id, str) or not item.provider_asset_id
                or not re.fullmatch(rf'codeboxd/posts/u{owner_id}/[a-f0-9]{{32}}', item.public_id)):
            raise APIError('A prévia contém um arquivo que não pertence ao lote aprovado.')
        retain_until = item.retain_until
        if not isinstance(retain_until, datetime):
            raise APIError('A retenção do candidato não foi confirmada.')
        if retain_until.tzinfo is None:
            retain_until = retain_until.replace(tzinfo=timezone.utc)
        if retain_until > now:
            raise APIError('A prévia contém um arquivo ainda dentro da retenção.')
        seen.add(item.asset_id)
        accepted.append(item)
    return CleanupPreview(approval_reference, tuple(accepted))
