from fastapi import Request, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Generator

from app.modules.gestao.models.user import User
from app.core.database import SessionLocal
from app.core.security.jwt import decode_token
from app.core.pagination import MAX_LIMIT, DEFAULT_LIMIT
from app.core.audit.security_audit import log_access_denied


def get_token_from_header(request: Request) -> str:
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        log_access_denied(
            reason="AUTH_HEADER_MISSING",
            request=request,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente ou inválido",
        )

    return auth.replace("Bearer ", "")


def get_current_user(
    request: Request,
    token: str = Depends(get_token_from_header),
) -> dict:
    payload = decode_token(token)

    if not payload or "sub" not in payload or "tenant_id" not in payload:
        log_access_denied(
            reason="TOKEN_PAYLOAD_INVALID",
            request=request,
            extra={"payload": payload},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    tenant_id = payload["tenant_id"]

    user = {
        "sub": int(payload["sub"]),
        "user_id": int(payload["sub"]),
        "tenant_id": tenant_id,
        "role": payload.get("role"),
    }

    # 🔍 valida se o usuário ainda existe e está ativo
    db = SessionLocal()
    try:
        exists = (
            db.query(User)
            .filter(
                User.id == user["user_id"],
                User.is_active.is_(True),
            )
            .first()
        )

        if not exists:
            log_access_denied(
                reason="USER_INACTIVE_OR_NOT_FOUND",
                request=request,
                user=user,
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário inválido",
            )
    finally:
        db.close()

    # 🔥 CONTEXTO OFICIAL DA REQUEST
    request.state.user = user
    request.state.tenant_id = tenant_id

    return user


def pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=1),
):
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT

    return {"skip": skip, "limit": limit}


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
