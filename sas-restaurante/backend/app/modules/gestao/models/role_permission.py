from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)
    permission = Column(String, index=True)
