from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
import calendar

from app.modules.gestao.models.cash_closure import CashClosure


class DashboardGoalsService:

    @staticmethod
    def monthly_goal(db: Session, goal_value: Decimal):
        today = date.today()
        year = today.year
        month = today.month

        # =========================
        # FATURAMENTO ATUAL DO MÊS
        # =========================
        current_value = (
            db.query(func.coalesce(func.sum(CashClosure.total_sales), 0))
            .filter(
                func.extract("year", CashClosure.created_at) == year,
                func.extract("month", CashClosure.created_at) == month
            )
            .scalar()
        )

        # =========================
        # PROGRESSO
        # =========================
        achieved_percentage = (
            float((current_value / goal_value) * 100)
            if goal_value > 0
            else 0.0
        )

        # =========================
        # PROJEÇÃO (RUN RATE)
        # =========================
        days_passed = today.day
        total_days = calendar.monthrange(year, month)[1]

        projected_value = (
            (current_value / days_passed) * total_days
            if days_passed > 0
            else Decimal("0.00")
        )

        # =========================
        # STATUS DA META
        # =========================
        projected_percentage = (
            float((projected_value / goal_value) * 100)
            if goal_value > 0
            else 0.0
        )

        if projected_percentage >= 100:
            status = "on_track"
        elif projected_percentage >= 80:
            status = "attention"
        else:
            status = "risk"

        return {
            "month": month,
            "year": year,
            "goal_value": goal_value,
            "current_value": current_value,
            "achieved_percentage": round(achieved_percentage, 2),
            "projected_value": projected_value,
            "status": status
        }
