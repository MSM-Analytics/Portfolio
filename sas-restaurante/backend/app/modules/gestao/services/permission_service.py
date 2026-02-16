from sqlalchemy.orm import Session
from app.modules.gestao.models.role_permission import RolePermission
from app.modules.gestao.models.permission import Permission


class PermissionService:

    @staticmethod
    def role_has_permission(
        db: Session,
        role_id: int,
        permission_code: str
    ) -> bool:
        return (
            db.query(RolePermission)
            .join(Permission)
            .filter(
                RolePermission.role_id == role_id,
                Permission.code == permission_code
            )
            .first()
            is not None
        )
