from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List

class CashClosureCreate(BaseModel):
    user_id: int

class SaleRead(BaseModel):
    id: int
    total: Decimal
    payment_method: str
    created_at: datetime

    class Config:
        from_attributes = True

class CashClosureRead(BaseModel):
    id: int
    user_id: int
    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

class CashClosureReopen(BaseModel):
    reason: str

class CashClosureSummary(BaseModel):
    id: int
    shift: str
    created_at: datetime

    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal

    sales_count: int
    average_ticket: Decimal

    is_reopened: bool

    class Config:
        from_attributes = True

