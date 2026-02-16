from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin


class PaymentMethod(TenantMixin, Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(50),
        nullable=False,
        index=True,  # 🔎 consultas frequentes
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    payments = relationship(
        "Payment",
        back_populates="payment_method",
    )
