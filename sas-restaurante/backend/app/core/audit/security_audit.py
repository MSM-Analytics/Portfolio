from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger("security_audit")


def log_access_denied(
    *,
    reason: str,
    path: Optional[str] = None,
    method: Optional[str] = None,
    user_id: Optional[int] = None,
    tenant_id: Optional[str] = None,
    role: Optional[str] = None,
    extra: Optional[dict] = None,
):
    """
    Auditoria de segurança para acessos negados.
    Compliance: rastreável, estruturado, centralizado.
    """

    event = {
        "event": "ACCESS_DENIED",
        "reason": reason,
        "user_id": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "path": path,
        "method": method,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if extra:
        event["extra"] = extra

    logger.warning(event)
