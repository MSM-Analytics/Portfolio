from enum import Enum
from typing import List, Dict


class UserRole(str, Enum):
    ADMIN_MASTER = "admin_master"   # acesso global (bootstrap)
    ADMIN_TENANT = "admin_tenant"   # admin da empresa
    OPERATOR = "operator"           # caixa / usuário comum


# 🎯 Mapeamento: ROLE → PERMISSÕES
ROLE_PERMISSIONS: Dict[str, List[str]] = {
    UserRole.ADMIN_MASTER.value: ["*"],  # acesso total

    UserRole.ADMIN_TENANT.value: [
        "product:create",
        "product:update",

        "category:create",
        "category:update",

        "sale:create",
        "sale:cancel",

        "payment:add",

        "cash:close",
        "cash:reopen",

        "report:view",
    ],

    UserRole.OPERATOR.value: [
        "sale:create",
        "payment:add",
        "report:view",
    ],
}


def get_permissions_by_role(role: str) -> List[str]:
    """
    Retorna a lista de permissões associadas a um role.
    """
    return ROLE_PERMISSIONS.get(role, [])
