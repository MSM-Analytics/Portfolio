# app/modules/gestao/api/audit_router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.models.audit_log import AuditLog
from app.modules.gestao.schemas.audit_log import AuditLogOut

router = APIRouter(
    prefix="/audit",
    tags=["Auditoria"]
)

@router.get("/", response_model=list[AuditLogOut])
def list_audit_logs(
    entity: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(AuditLog)

    if entity:
        query = query.filter(AuditLog.entity == entity)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    return query.order_by(AuditLog.created_at.desc()).limit(100).all()
