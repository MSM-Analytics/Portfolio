from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Numeric,
    ForeignKey,
    String,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class CashClosure(Base):
    __tablename__ = "cash_closures"

    id = Column(Integer, primary_key=True, index=True)

    # 👤 Quem FEZ o fechamento
    closed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    shift = Column(String(10), nullable=False)  # MANHA | TARDE | NOITE

    total_sales = Column(Numeric(10, 2), default=0)
    total_cash = Column(Numeric(10, 2), default=0)
    total_card = Column(Numeric(10, 2), default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔁 Reabertura
    is_reopened = Column(Boolean, default=False)
    reopen_reason = Column(Text, nullable=True)
    reopened_at = Column(DateTime, nullable=True)
    reopened_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # 🔗 Relationships EXPLÍCITOS
    closed_by = relationship(
        "User",
        foreign_keys=[closed_by_id],
        backref="cash_closures_closed",
    )

    reopened_by = relationship(
        "User",
        foreign_keys=[reopened_by_id],
        backref="cash_closures_reopened",
    )

    sales = relationship(
        "Sale",
        backref="cash_closure",
    )
