from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from app.modules.gestao.schemas.category import CategoryOut
from app.modules.gestao.schemas.stock import StockOut




class ProductBase(BaseModel):
    name: str
    sku: str
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category_id: int



class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    is_active: bool
    category: Optional["CategoryOut"] = None
    stock: Optional["StockOut"] = None

    class Config:
        from_attributes = True

