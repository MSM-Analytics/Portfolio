from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.services.financial_report_service import FinancialReportService
from app.modules.gestao.schemas.financial_report import (
    FinancialSummaryOut,
    PaymentMethodReportOut,
)
from app.modules.gestao.api.dependencies.permissions import require_permission


router = APIRouter(
    prefix="/reports/financial",
    tags=["Financial Reports"],
)


@router.get(
    "/reports/financial/summary",
    dependencies=[Depends(require_permission("report:view"))]
)
def financial_summary(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = FinancialReportService(db, user["tenant_id"])
    return service.summary(start_date, end_date)


@router.get("/by-payment-method", response_model=list[PaymentMethodReportOut])
def financial_by_payment_method(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = FinancialReportService(db, user["tenant_id"])
    return service.by_payment_method(start_date, end_date)
