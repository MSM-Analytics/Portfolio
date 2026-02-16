from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.modules.gestao.models.tenant_mixin import TenantMixin


class Refund(TenantMixin, Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)

    payment_id = Column(
        Integer,
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    amount = Column(Numeric(10, 2), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # 🔗 Relacionamentos
    payment = relationship(
        "Payment",  # manter como string evita ImportError circular
        backref="refunds",
    )
