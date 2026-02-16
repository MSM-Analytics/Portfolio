from pydantic import BaseModel
from datetime import datetime


# =========================
# Base compartilhada
# =========================

class UserBase(BaseModel):
    email: str

    model_config = {
        "from_attributes": True
    }


# =========================
# Para LISTAGENS
# =========================

class UserListItem(UserBase):
    id: int


class UserList(BaseModel):
    items: list[UserListItem]
    total: int


# =========================
# Para DETALHES / /me
# =========================

class UserOut(UserBase):
    id: int
    is_admin: bool
    tenant_id: int
    created_at: datetime
