from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from decimal import Decimal
import calendar

from app.modules.gestao.models.cash_closure import CashClosure


class DashboardForecastService:

    @staticmethod
    def monthly_forecast(db: Session, window: int = 7):
        today = date.today()
        year = today.year
        month = today.month

        # =========================
        # SÉRIE DIÁRIA DO MÊS
        # =========================
        rows = (
            db.query(
                func.date(CashClosure.created_at).label("day"),
                func.sum(CashClosure.total_sales).label("total")
            )
            .filter(
                func.extract("year", CashClosure.created_at) == year,
                func.extract("month", CashClosure.created_at) == month
            )
            .group_by("day")
            .order_by("day")
            .all()
        )

        labels = [str(r.day) for r in rows]
        daily = [r.total for r in rows]

        # =========================
        # MÉDIA MÓVEL
        # =========================
        ma = []
        for i in range(len(daily)):
            start = max(0, i - window + 1)
            slice_vals = daily[start:i + 1]
            ma.append(sum(slice_vals) / len(slice_vals))

        # =========================
        # TENDÊNCIA (janela atual vs anterior)
        # =========================
        if len(ma) >= window * 2:
            prev_avg = sum(ma[-window*2:-window]) / window
            curr_avg = sum(ma[-window:]) / window
            if curr_avg > prev_avg:
                trend = "up"
            elif curr_avg < prev_avg:
                trend = "down"
            else:
                trend = "stable"
        else:
            trend = "stable"

        # =========================
        # PROJEÇÃO DE FECHAMENTO
        # =========================
        current_total = sum(daily) if daily else Decimal("0.00")
        days_passed = today.day
        total_days = calendar.monthrange(year, month)[1]

        projected = (
            (current_total / days_passed) * total_days
            if days_passed > 0
            else Decimal("0.00")
        )

        return {
            "labels": labels,
            "daily_values": daily,
            "moving_average": ma,
            "trend": trend,
            "projected_month_total": projected
        }
