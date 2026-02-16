from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

#CORE
from app.core.dependencies import get_db, get_current_user

# MODELS
from app.modules.gestao.services.cash_closure_service import CashClosureService
from app.modules.gestao.schemas.cash_closure import CashClosureReopen, CashClosureRead
from app.modules.gestao.services.cash_closure_export_service import CashClosureExportService
from app.modules.gestao.schemas.cash_closure import CashClosureSummary
from app.modules.gestao.api.dependencies.permissions import require_permission

router = APIRouter(
    prefix="/cash-closure",
    tags=["Fechamento de Caixa"]
)

# Endpoint existente para fechar caixa
@router.post(
    "/cash-closure/",
    dependencies=[Depends(require_permission("cash:close"))]
)
def close_cash(db: Session = Depends(get_db), user=Depends(get_current_user)):
    closure = CashClosureService.close_cash(db, user.id)
    return closure

# Novo endpoint: histórico
def cash_closure_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return CashClosureService.get_cash_closure_history(
        db=db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/export/csv")
def export_csv(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    file = CashClosureExportService.export_csv(db, start_date, end_date)
    return StreamingResponse(
        file,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fechamento_caixa.csv"}
    )


@router.get("/export/excel")
def export_excel(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    file = CashClosureExportService.export_excel(db, start_date, end_date)
    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=fechamento_caixa.xlsx"}
    )


@router.get("/export/pdf")
def export_pdf(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    file = CashClosureExportService.export_pdf(db, start_date, end_date)
    return StreamingResponse(
        file,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=fechamento_caixa.pdf"}
    )

@router.post(
    "/cash-closure/{closure_id}/reopen",
    dependencies=[Depends(require_permission("cash:reopen"))]
)
def reopen_cash_closure(
    closure_id: int,
    payload: CashClosureReopen,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return CashClosureService.reopen_cash_closure(
        db=db,
        closure_id=closure_id,
        user_id=user.id,
        reason=payload.reason
    )

@router.get("/{closure_id}/summary", response_model=CashClosureSummary)
def cash_closure_summary(
    closure_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return CashClosureService.get_summary(db, closure_id)
