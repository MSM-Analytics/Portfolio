from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin

class StockBalance(TenantMixin, Base):
    __tablename__ = "stock_balances"

    id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    quantity = Column(Numeric(10, 2), nullable=False, default=0)
    avg_cost = Column(Numeric(10, 2), nullable=False, default=0)

    product = relationship("Product")
    warehouse = relationship("Warehouse")
