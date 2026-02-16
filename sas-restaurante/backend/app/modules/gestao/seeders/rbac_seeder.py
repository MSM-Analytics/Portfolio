from sqlalchemy.orm import Session

from app.modules.gestao.models.role import Role
from app.modules.gestao.models.permission import Permission
from app.modules.gestao.models.role_permission import RolePermission

from app.core.permissions import PERMISSIONS, Permissions
from app.core.roles import UserRole
from app.modules.gestao.models.role_permission import RolePermission


def seed_rbac(db: Session):
    permissions_map = {}

    # =========================
    # CRIAR PERMISSÕES
    # =========================
    for code, description in PERMISSIONS:
        permission = (
            db.query(Permission)
            .filter_by(code=code)
            .first()
        )

        if not permission:
            permission = Permission(
                code=code,
                description=description
            )
            db.add(permission)
            db.commit()
            db.refresh(permission)

        permissions_map[code] = permission

    # =========================
    # CRIAR ROLES E VÍNCULOS
    # =========================
    for role_enum, permission_enums in RolePermission.items():
        role_name = role_enum.value

        role = (
            db.query(Role)
            .filter_by(name=role_name)
            .first()
        )

        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.commit()
            db.refresh(role)

        for perm_enum in permission_enums:
            permission = permissions_map.get(perm_enum.value)

            if not permission:
                continue

            exists = (
                db.query(RolePermission)
                .filter_by(
                    role_id=role.id,
                    permission_id=permission.id
                )
                .first()
            )

            if not exists:
                db.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id
                    )
                )

    db.commit()
