from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.modules.gestao.models.cash_closure import CashClosure


class DashboardAlertsService:

    @staticmethod
    def get_alerts(db: Session):
        alerts = []
        today = date.today()
        year = today.year
        month = today.month

        # =========================
        # 1️⃣ CAIXA NÃO FECHADO HOJE
        # =========================
        closed_today = (
            db.query(CashClosure.id)
            .filter(func.date(CashClosure.created_at) == today)
            .first()
        )

        if not closed_today:
            alerts.append({
                "code": "CASH_NOT_CLOSED",
                "level": "warning",
                "message": "Caixa de hoje ainda não foi fechado"
            })

        # =========================
        # 2️⃣ DIA SEM VENDAS
        # =========================
        today_sales = (
            db.query(func.coalesce(func.sum(CashClosure.total_sales), 0))
            .filter(func.date(CashClosure.created_at) == today)
            .scalar()
        )

        if today_sales == 0:
            alerts.append({
                "code": "NO_SALES_TODAY",
                "level": "danger",
                "message": "Nenhuma venda registrada hoje"
            })

        # =========================
        # 3️⃣ QUEDA DE FATURAMENTO MENSAL
        # =========================
        current_month_sales = (
            db.query(func.coalesce(func.sum(CashClosure.total_sales), 0))
            .filter(
                func.extract("year", CashClosure.created_at) == year,
                func.extract("month", CashClosure.created_at) == month
            )
            .scalar()
        )

        prev_month = month - 1 or 12
        prev_year = year if month > 1 else year - 1

        prev_month_sales = (
            db.query(func.coalesce(func.sum(CashClosure.total_sales), 0))
            .filter(
                func.extract("year", CashClosure.created_at) == prev_year,
                func.extract("month", CashClosure.created_at) == prev_month
            )
            .scalar()
        )

        if prev_month_sales > 0 and current_month_sales < prev_month_sales:
            alerts.append({
                "code": "MONTHLY_DROP",
                "level": "warning",
                "message": "Faturamento mensal abaixo do mês anterior"
            })

        return {"alerts": alerts}
