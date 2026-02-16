from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.dashboard import DashboardKPIs
from app.modules.gestao.dashboards.kpi_service import DashboardKPIService
from app.modules.gestao.dashboards.chart_service import DashboardChartsService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/kpis", response_model=DashboardKPIs)
def dashboard_kpis(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardKPIService.get_kpis(db)

@router.get("/charts/sales-by-day")
def sales_by_day(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardChartsService.sales_by_day(db, year, month)


@router.get("/charts/sales-by-category")
def sales_by_category(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardChartsService.sales_by_category(db)

