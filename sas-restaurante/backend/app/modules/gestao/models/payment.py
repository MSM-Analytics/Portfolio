from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    ForeignKey,
    DateTime,
    Enum as SqlEnum,
    and_,
)
from sqlalchemy.orm import relationship, foreign
from datetime import datetime

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin
from app.modules.gestao.enums.payment_status import PaymentStatus
from app.modules.gestao.models.cashflow import Cashflow

class Payment(TenantMixin, Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    sale_id = Column(
        Integer,
        ForeignKey("sales.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    payment_method_id = Column(
        Integer,
        ForeignKey("payment_methods.id"),
        nullable=True,
        index=True,
    )

    amount = Column(Numeric(10, 2), nullable=False)

    status = Column(
        SqlEnum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.CONFIRMED,
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 🔗 Relacionamentos
    sale = relationship("Sale", back_populates="payments")
    payment_method = relationship("PaymentMethod")

    # ✅ CASHFLOW POLIMÓRFICO (AGORA CORRETO)
    cashflows = relationship(
        "Cashflow",
        primaryjoin=and_(
            foreign(Cashflow.reference_id) == id,
            Cashflow.reference == "PAYMENT",
        ),
        viewonly=True,
    )
