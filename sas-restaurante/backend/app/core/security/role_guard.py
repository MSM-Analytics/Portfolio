from fastapi import Depends, HTTPException, status, Request

from app.core.roles import UserRole
from app.core.dependencies import get_current_user
from app.core.audit.security_audit import log_access_denied


def require_roles(*roles: UserRole):
    def checker(
        request: Request,
        user: dict = Depends(get_current_user),
    ):
        user_role = user.get("role")

        if not user_role:
            log_access_denied(
                reason="ROLE_MISSING",
                request=request,
                user=user,
                extra={
                    "required_roles": [r.value for r in roles],
                },
            )

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not defined",
            )

        allowed_roles = [r.value for r in roles]

        if user_role not in allowed_roles:
            log_access_denied(
                reason="ROLE_NOT_ALLOWED",
                request=request,
                user=user,
                extra={
                    "user_role": user_role,
                    "required_roles": allowed_roles,
                },
            )

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return user

    return checker
