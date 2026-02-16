from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.forecast import ForecastResponse
from app.modules.gestao.dashboards.forecast_service import DashboardForecastService

router = APIRouter(
    prefix="/dashboard/forecast",
    tags=["Dashboard"]
)

@router.get("/monthly", response_model=ForecastResponse)
def monthly_forecast(
    window: int = Query(7, ge=3, le=14, description="Janela da média móvel"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardForecastService.monthly_forecast(db, window)
