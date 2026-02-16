from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin


class Category(TenantMixin, Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(120),
        nullable=False,
        index=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    products = relationship(
        "Product",
        back_populates="category",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
