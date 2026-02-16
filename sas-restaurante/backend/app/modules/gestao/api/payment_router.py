from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.modules.gestao.schemas.payment import PaymentCreate
from app.modules.gestao.services.payment_service import PaymentService
from app.modules.gestao.services.sale_service import SaleService
from app.core.roles import UserRole
from app.modules.gestao.api.dependencies.permissions import require_permission

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/sales/{sale_id}/payments",
    dependencies=[Depends(require_permission("payment:add"))]
)
def add_payment(
    sale_id: int,
    data: PaymentCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(UserRole.ADMIN_TENANT, UserRole.OPERATOR)),
):
    sale_service = SaleService(db, user["tenant_id"])
    sale = sale_service.get_by_id(sale_id)

    payment_service = PaymentService(db, user["tenant_id"])
    payment_service.register(
        sale=sale,
        payments=data.payments
    )

    return {"message": "Payment registered successfully"}
