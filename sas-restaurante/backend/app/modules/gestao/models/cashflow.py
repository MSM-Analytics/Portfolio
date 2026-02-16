from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    DateTime,
    Enum as SqlEnum,
    and_,
)
from sqlalchemy.orm import relationship, foreign
from datetime import datetime

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin

from app.modules.gestao.enums.cashflow_type import CashflowType
from app.modules.gestao.enums.cashflow_category import CashflowCategory


class Cashflow(TenantMixin, Base):
    __tablename__ = "cashflows"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Numeric(10, 2), nullable=False)

    flow_type = Column(
        SqlEnum(CashflowType, name="cashflow_type_enum"),
        nullable=False,
    )

    category = Column(
        SqlEnum(CashflowCategory, name="cashflow_category_enum"),
        nullable=False,
    )

    reference = Column(String(30), nullable=False)  # SALE | PAYMENT | REFUND
    reference_id = Column(Integer, nullable=False)

    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)