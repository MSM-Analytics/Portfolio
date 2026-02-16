from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    product_id: int
    quantity: int = 0
    minimum_quantity: int = 0


class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    quantity: Optional[int] = None
    minimum_quantity: Optional[int] = None
    is_active: Optional[bool] = None


class StockOut(StockBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
