from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.goals import MonthlyGoalResponse
from app.modules.gestao.dashboards.goals_service import DashboardGoalsService

router = APIRouter(
    prefix="/dashboard/goals",
    tags=["Dashboard"]
)

@router.get("/monthly", response_model=MonthlyGoalResponse)
def monthly_goal(
    goal_value: Decimal = Query(..., description="Valor da meta mensal"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardGoalsService.monthly_goal(db, goal_value)
