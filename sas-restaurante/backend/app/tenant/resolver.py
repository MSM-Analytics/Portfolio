from typing import Generator
from fastapi import Header, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL_TEMPLATE = "postgresql://postgres:postgres@localhost:5432/{}"

def get_tenant_db(
    x_tenant_id: str = Header(...)
) -> Generator[Session, None, None]:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Tenant não informado")

    engine = create_engine(DATABASE_URL_TEMPLATE.format(x_tenant_id))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
