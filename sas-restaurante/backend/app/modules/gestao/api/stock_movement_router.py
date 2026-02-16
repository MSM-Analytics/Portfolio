from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.stock_movement import (
    StockMovementCreate,
    StockMovementOut,
)
from app.modules.gestao.services.stock_movement_service import StockMovementService


router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


@router.post("/", response_model=StockMovementOut)
def create_movement(
    data: StockMovementCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = StockMovementService(db, tenant_id=user["tenant_id"])
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock/{stock_id}", response_model=List[StockMovementOut])
def list_movements(
    stock_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = StockMovementService(db, tenant_id=user["tenant_id"])
    return service.list_by_stock(stock_id)
