from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin


class Product(TenantMixin, Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("tenant_id", "sku", name="uq_product_tenant_sku"),
        Index("ix_product_tenant_name", "tenant_id", "name"),
    )

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(120), nullable=False)

    sku = Column(String(60), nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    category = relationship(
        "Category",
        back_populates="products",
        lazy="selectin",
    )

    stock = relationship(
        "Stock",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
