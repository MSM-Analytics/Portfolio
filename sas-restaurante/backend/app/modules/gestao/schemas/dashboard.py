from pydantic import BaseModel
from decimal import Decimal


class DashboardKPIs(BaseModel):
    today_sales: Decimal
    month_sales: Decimal
    average_ticket: Decimal
    cash_percentage: float
    card_percentage: float
    top_product: str
    top_category: str
    month_growth: float
