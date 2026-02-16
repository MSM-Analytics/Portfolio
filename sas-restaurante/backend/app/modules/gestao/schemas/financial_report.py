from pydantic import BaseModel
from typing import List


class FinancialSummaryOut(BaseModel):
    income: float
    outcome: float
    balance: float


class PaymentMethodReportOut(BaseModel):
    payment_method: str
    total: float
