from pydantic import BaseModel
from typing import List
from decimal import Decimal


class ForecastResponse(BaseModel):
    labels: List[str]
    daily_values: List[Decimal]
    moving_average: List[Decimal]
    trend: str            # up | down | stable
    projected_month_total: Decimal
