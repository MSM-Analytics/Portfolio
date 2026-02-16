from pydantic import BaseModel
from typing import Optional


class PaymentMethodBase(BaseModel):
    name: str


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class PaymentMethodOut(PaymentMethodBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
