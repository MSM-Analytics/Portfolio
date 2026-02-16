from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.stock import (
    StockCreate,
    StockUpdate,
    StockOut,
)
from app.modules.gestao.services.stock_service import StockService


router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get("/", response_model=List[StockOut])
def list_stocks(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = StockService(db, tenant_id=user["tenant_id"])
    return service.list()


@router.post("/", response_model=StockOut)
def create_stock(
    data: StockCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = StockService(db, tenant_id=user["tenant_id"])
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{stock_id}", response_model=StockOut)
def update_stock(
    stock_id: int,
    data: StockUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = StockService(db, tenant_id=user["tenant_id"])
    try:
        return service.update(stock_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Stock not found")
