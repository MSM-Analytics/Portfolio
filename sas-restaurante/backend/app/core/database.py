from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/sas_restaurante"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # evita conexões mortas
    pool_size=10,
    max_overflow=20,
)

class TenantAwareSession(Session):
    """
    Sessão consciente do tenant.
    O tenant_id fica disponível em session.info
    """

    def set_tenant(self, tenant_id: str | None):
        self.info["tenant_id"] = tenant_id

    @property
    def tenant_id(self) -> str | None:
        return self.info.get("tenant_id")

SessionLocal = sessionmaker(
    bind=engine,
    class_=TenantAwareSession,
    autocommit=False,
    autoflush=False
)

def get_tenant_session(tenant_id: str | None):
    session = SessionLocal()
    session.set_tenant(tenant_id)
    return session

Base = declarative_base()
