from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.charts import LineChart, PieChart, BarChart
from app.modules.gestao.dashboards.chart_service import DashboardChartsService

router = APIRouter(
    prefix="/dashboard/charts",
    tags=["Dashboard"]
)

@router.get("/sales-by-day", response_model=LineChart)
def sales_by_day(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardChartsService.sales_by_day(db, year, month)


@router.get("/payment-methods", response_model=PieChart)
def payment_methods(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardChartsService.payment_methods(db)


@router.get("/sales-by-category", response_model=BarChart)
def sales_by_category(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardChartsService.sales_by_category(db)


@router.get("/top-products", response_model=BarChart)
def top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardChartsService.top_products(db, limit)
