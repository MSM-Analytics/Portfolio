from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"


class StockMovementCreate(BaseModel):
    stock_id: int
    type: MovementType
    quantity: int
    reason: Optional[str] = None


class StockMovementOut(BaseModel):
    id: int
    stock_id: int
    type: MovementType
    quantity: int
    reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
