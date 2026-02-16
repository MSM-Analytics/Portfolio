from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.refund import RefundCreate
from app.modules.gestao.services.refund_service import RefundService
from app.core.permissions import require_roles
from app.core.roles import UserRole


router = APIRouter(prefix="/refunds", tags=["Refunds"])


@router.post("/")
def refund_payment(
    data: RefundCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(UserRole.ADMIN_TENANT)),
):
    service = RefundService(db, user["tenant_id"])
    try:
        service.create(data.payment_id, data.amount)
        db.commit()
        return {"message": "Refund processed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
