from pydantic import BaseModel


class RefundCreate(BaseModel):
    payment_id: int
    amount: float
