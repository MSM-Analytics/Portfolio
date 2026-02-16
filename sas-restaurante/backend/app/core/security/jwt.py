from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException

from app.core.settings import settings
from app.core.audit.security_audit import log_access_denied

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 dia


def create_access_token(
    *,
    user_id: int,
    role: str,
    tenant_id: str | None,
    expires_delta: timedelta | None = None,
) -> str:

    payload = {
        "sub": str(user_id),
        "role": role,
        "tenant_id": tenant_id,
    }

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

    except JWTError as exc:
        log_access_denied(
            reason="TOKEN_INVALID",
            extra={"error": str(exc)},
        )

        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado",
        )
