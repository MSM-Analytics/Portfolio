from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.dependencies import get_db, get_current_user
from app.core.security.role_guard import require_roles
from app.core.roles import UserRole


# SCHEMAS
from app.modules.gestao.schemas.sale import SaleCreate, SaleOut
from app.modules.gestao.schemas.payment import PaymentCreate

# MODELS
from app.modules.gestao.models.sale import Sale

# SERVICES
from app.modules.gestao.services.sale_service import SaleService
from app.modules.gestao.services.payment_service import PaymentService
from app.modules.gestao.services.sale_filter_service import SaleFilterService

# ENUMS
from app.modules.gestao.enums.shift_type import ShiftType
from app.modules.gestao.api.dependencies.permissions import require_permission



router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post(
    "/sales/",
    dependencies=[Depends(require_permission("sale:create"))]
)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = SaleService(db, user["tenant_id"])
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[SaleOut])
def list_sales(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = SaleService(db, tenant_id=user["tenant_id"])
    return service.list()


@router.post(
    "/sales/{sale_id}/cancel",
    dependencies=[Depends(require_permission("sale:cancel"))]
)
def cancel_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = SaleService(db, user["tenant_id"])
    try:
        return service.cancel(sale_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{sale_id}/payments", response_model=SaleOut)
def add_payment(
    sale_id: int,
    data: PaymentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sale = (
        db.query(Sale)
        .filter(
            Sale.id == sale_id,
            Sale.tenant_id == user["tenant_id"],
            Sale.is_active == True,
        )
        .first()
    )

    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    payment_service = PaymentService(db, user["tenant_id"])
    payment_service.register(
        sale=sale,
        payments=[data]
    )

    db.commit()
    db.refresh(sale)
    return sale

@router.get("/filter")
def filter_sales(
    shift: ShiftType | None = Query(None),
    day: datetime | None = Query(None),
    week: int | None = Query(None),
    month: int | None = Query(None),
    year: int | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = SaleFilterService(db, tenant_id=user.tenant_id)

    return service.filter(
        shift=shift,
        day=day,
        week=week,
        month=month,
        year=year,
        start_date=start_date,
        end_date=end_date,
    )
