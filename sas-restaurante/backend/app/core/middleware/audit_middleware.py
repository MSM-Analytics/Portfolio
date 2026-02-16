import json
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.database import SessionLocal
from app.modules.gestao.services.audit_service import AuditService
from app.modules.gestao.services.audit_entity_map import ENTITY_MAP
from app.modules.gestao.services.audit_diff import build_diff

def extract_id_from_path(path: str) -> int | None:
    for part in path.split("/"):
        if part.isdigit():
            return int(part)
    return None

class AuditMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        if request.method == "OPTIONS":
            return await call_next(request)

        start_time = time.time()

        if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
            response = await call_next(request)
            response.headers["X-Process-Time"] = str(round(time.time() - start_time, 4))
            return response

        body = None
        try:
            body_bytes = await request.body()
            request._body = body_bytes
            body = json.loads(body_bytes.decode()) if body_bytes else None
        except Exception:
            body = None

        db = SessionLocal()

        try:
            model = None
            entity_id = extract_id_from_path(request.url.path)

            for base_path, mapped_model in ENTITY_MAP.items():
                if request.url.path.startswith(base_path):
                    model = mapped_model
                    break

            # BEFORE
            before = None
            if model and entity_id:
                obj = db.get(model, entity_id)
                if obj:
                    before = obj.__dict__.copy()
                    before.pop("_sa_instance_state", None)

            # EXECUTA REQUEST
            response = await call_next(request)

            # AFTER
            after = None
            if model and entity_id:
                obj = db.get(model, entity_id)
                if obj:
                    after = obj.__dict__.copy()
                    after.pop("_sa_instance_state", None)
            else:
                after = body

            #diff = build_diff(before, after)

            user = getattr(request.state, "user", None)

            AuditService.log(
                db=db,
                action=request.method,
                entity=model.__name__ if model else request.url.path,
                user_id=user["user_id"] if user else None,
                before=before,
                after=after,
                #diff=diff,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                #extra={"entity_id": entity_id}  # agora compatível
            )

        finally:
            db.close()

        response.headers["X-Process-Time"] = str(round(time.time() - start_time, 4))
        return response
