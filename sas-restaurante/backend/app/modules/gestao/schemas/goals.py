from pydantic import BaseModel
from decimal import Decimal


class MonthlyGoalResponse(BaseModel):
    month: int
    year: int
    goal_value: Decimal
    current_value: Decimal
    achieved_percentage: float
    projected_value: Decimal
    status: str  # on_track | attention | risk
