from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    DateTime,
    ForeignKey,
    Enum as SqlEnum,
    literal,
    and_,
)
from sqlalchemy.orm import relationship, foreign

from app.core.database import Base
from app.core.enums import SaleStatus
from app.modules.gestao.models.tenant_mixin import TenantMixin
from app.modules.gestao.models.cashflow import Cashflow


class Sale(TenantMixin, Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    total_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    status = Column(
        SqlEnum(SaleStatus, name="sale_status_enum"),
        nullable=False,
        default=SaleStatus.OPEN,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    cash_closure_id = Column(
        Integer,
        ForeignKey("cash_closures.id"),
        nullable=True,
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan",
    )

    payments = relationship(
        "Payment",
        back_populates="sale",
        cascade="all, delete-orphan",
    )

    # 🔗 Cashflows relacionados à venda (somente leitura)
    cashflows = relationship(
        "Cashflow",
        primaryjoin=lambda: and_(
            foreign(Cashflow.reference_id) == Sale.id,
            Cashflow.reference == "SALE",
        ),
        viewonly=True,
    )

