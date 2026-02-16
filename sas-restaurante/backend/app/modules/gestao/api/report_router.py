from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

# CORE
from app.core.dependencies import get_db, get_current_user

# SCHEMAS
from app.modules.gestao.schemas.report import CategorySalesReport, DailyReportResponse, MonthlyReportResponse, ProductSalesReport
from app.modules.gestao.schemas.report import PeriodReportResponse

# SERVICES
from app.modules.gestao.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Relatórios"]
)

@router.get("/daily", response_model=DailyReportResponse)
def daily_report(
    report_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return ReportService.daily_report(db, report_date)

@router.get("/period", response_model=PeriodReportResponse)
def period_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return ReportService.period_report(
        db=db,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/monthly", response_model=MonthlyReportResponse)
def monthly_report(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return ReportService.monthly_report(
        db=db,
        year=year,
        month=month
    )

@router.get("/sales/by-product", response_model=list[ProductSalesReport])
def sales_by_product(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return ReportService.sales_by_product(db)

@router.get("/sales/by-category", response_model=list[CategorySalesReport])
def sales_by_category(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return ReportService.sales_by_category(db)
