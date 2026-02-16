from typing import List, Tuple

PermissionDef = Tuple[str, str]

PERMISSIONS: List[PermissionDef] = [
    ("product:create", "Create product"),
    ("product:update", "Update product"),

    ("category:create", "Create category"),
    ("category:update", "Update category"),

    ("sale:create", "Create sale"),
    ("sale:cancel", "Cancel sale"),

    ("payment:add", "Add payment"),

    ("cash:close", "Close cash"),
    ("cash:reopen", "Reopen cash"),

    ("report:view", "View reports"),
]

# ⬇️ REEXPORTA O GUARD (chave da solução)
from app.core.security.role_guard import require_roles

__all__ = ["PERMISSIONS", "require_roles"]