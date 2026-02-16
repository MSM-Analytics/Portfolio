from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    entity: str
    entity_id: Optional[int]
    before: Optional[Any]
    after: Optional[Any]
    created_at: datetime

    class Config:
        from_attributes = True
