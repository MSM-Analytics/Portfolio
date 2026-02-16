from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from sqlalchemy.orm import relationship
from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin

class Warehouse(TenantMixin, Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    is_active = Column(Boolean, default=True)