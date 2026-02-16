from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.payment_method import (
    PaymentMethodCreate,
    PaymentMethodUpdate,
    PaymentMethodOut,
)
from app.modules.gestao.services.payment_method_service import PaymentMethodService


router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment Methods"],
)


@router.get("/", response_model=List[PaymentMethodOut])
def list_payment_methods(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = PaymentMethodService(db, user["tenant_id"])
    return service.list()


@router.post("/", response_model=PaymentMethodOut)
def create_payment_method(
    data: PaymentMethodCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = PaymentMethodService(db, user["tenant_id"])
    return service.create(data)


@router.put("/{method_id}", response_model=PaymentMethodOut)
def update_payment_method(
    method_id: int,
    data: PaymentMethodUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = PaymentMethodService(db, user["tenant_id"])
    try:
        return service.update(method_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
