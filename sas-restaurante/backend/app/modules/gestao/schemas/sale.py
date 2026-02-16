from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime
from app.modules.gestao.schemas.payment import PaymentItem


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    items: List[SaleItemCreate]
    payments: List[PaymentItem]


class SaleItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class SaleOut(BaseModel):
    id: int
    total_amount: Decimal
    created_at: datetime
    items: List[SaleItemOut]

    class Config:
        from_attributes = True
