from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.services.permission_service import PermissionService


def require_permission(permission_code: str):

    def dependency(
        db: Session = Depends(get_db),
        user = Depends(get_current_user)
    ):
        if not user.role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned"
            )

        allowed = PermissionService.role_has_permission(
            db=db,
            role_id=user.role_id,
            permission_code=permission_code
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return True

    return dependency
