from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.alerts import AlertsResponse
from app.modules.gestao.dashboards.alerts_service import DashboardAlertsService

router = APIRouter(
    prefix="/dashboard/alerts",
    tags=["Dashboard"]
)

@router.get("/", response_model=AlertsResponse)
def get_alerts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return DashboardAlertsService.get_alerts(db)
