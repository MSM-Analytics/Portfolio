from pydantic import BaseModel
from typing import List

class PaymentCreate(BaseModel):
    payment_method_id: int
    amount: float

class PaymentItem(BaseModel):
    payment_method_id: int
    amount: float

class PaymentOut(BaseModel):
    id: int
    amount: float
    payment_method_id: int

    class Config:
        from_attributes = True
