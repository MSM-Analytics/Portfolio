from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    String,
    DateTime,
    Enum,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin


class StockMovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"


class StockOrigin(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    INVENTORY = "inventory"
    LOSS = "loss"
    TRANSFER = "transfer"
    MANUAL = "manual"


class StockMovement(TenantMixin, Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    quantity = Column(Numeric(10, 2), nullable=False)

    type = Column(Enum(StockMovementType), nullable=False)
    origin = Column(Enum(StockOrigin), nullable=False)

    cost_price = Column(Numeric(10, 2), nullable=True)

    reference = Column(String(120), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product")
    warehouse = relationship("Warehouse")

