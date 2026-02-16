from sqlalchemy.orm import Session
from typing import Optional, Any
from fastapi import APIRouter, Request
import json

from app.modules.gestao.models.audit_log import AuditLog
from app.modules.gestao.services.audit_diff import build_diff

class AuditService:

    @staticmethod
    def log(
        db,
        action: str,
        entity: str,
        user_id: int | None,
        before: dict | None,
        after: dict | None,
        ip_address: str | None,
        user_agent: str | None,
        #diff: dict | None = None,   # ✅ agora opcional
        #extra: dict | None = None,  # ✅ agora opcional
    ):
        audit = AuditLog(
            action=action,
            entity=entity,
            user_id=user_id,
            before=before,
            after=after,
            #diff=diff,
            ip_address=ip_address,
            user_agent=user_agent,
            #extra=json.dumps(extra) if extra else None  # salva como JSON string
        )

        db.add(audit)
        db.commit()
