from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.roles import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default=UserRole.OPERATOR.value)
    tenant_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    # relacionamento com AuditLog
    audit_logs = relationship("AuditLog", back_populates="user")  # string evita circular import
