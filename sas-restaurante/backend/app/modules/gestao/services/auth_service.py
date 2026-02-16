from datetime import datetime, timedelta
from jose import jwt

from app.core.settings import settings


def create_access_token(
    *,
    user_id: int,
    tenant_id: str | None,
    expires_delta: timedelta | None = None
) -> str:

    print("🔐 [JWT] Gerando token...")
    print("    user_id :", user_id)
    print("    tenant_id :", tenant_id)
    print("    expires_delta :", expires_delta)

    payload = {
        "sub": str(user_id),
        "tenant_id": tenant_id,
        "iat": datetime.utcnow()
    }

    if expires_delta:
        payload["exp"] = datetime.utcnow() + expires_delta
    else:
        payload["exp"] = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    print("📦 [JWT] Payload final:", payload)

    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    print("✅ [JWT] Token gerado com sucesso")

    return token
