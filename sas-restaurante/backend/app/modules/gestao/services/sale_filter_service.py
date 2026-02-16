from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.modules.gestao.models.sale import Sale
from app.modules.gestao.enums.shift_type import ShiftType
from app.core.utils.shift_utils import get_shift_time_range


class SaleFilterService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def filter(
        self,
        shift: ShiftType | None = None,
        day: datetime | None = None,
        week: int | None = None,
        month: int | None = None,
        year: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ):
        query = self.db.query(Sale).filter(
            Sale.tenant_id == self.tenant_id
        )

        # 📆 Dia específico
        if day:
            start = datetime.combine(day.date(), datetime.min.time())
            end = datetime.combine(day.date(), datetime.max.time())
            query = query.filter(Sale.created_at.between(start, end))

        # 📆 Semana do ano
        if week:
            query = query.filter(extract("week", Sale.created_at) == week)

        # 📆 Mês
        if month:
            query = query.filter(extract("month", Sale.created_at) == month)

        # 📆 Ano
        if year:
            query = query.filter(extract("year", Sale.created_at) == year)

        # 📆 Intervalo customizado
        if start_date and end_date:
            query = query.filter(
                Sale.created_at.between(start_date, end_date)
            )

        # ⏰ Turno
        if shift:
            start_time, end_time = get_shift_time_range(shift)
            if start_time and end_time:
                query = query.filter(
                    extract("hour", Sale.created_at).between(
                        start_time.hour,
                        end_time.hour
                    )
                )

        return query.all()
