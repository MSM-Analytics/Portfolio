from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin


class Stock(TenantMixin, Base):
    __tablename__ = "stocks"
    __table_args__ = (
        Index("ix_stock_tenant_product", "tenant_id", "product_id"),
    )

    id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    quantity = Column(Integer, default=0, nullable=False)

    min_quantity = Column(Integer, default=0, nullable=False)

    product = relationship(
        "Product",
        back_populates="stock",
        lazy="selectin",
    )
