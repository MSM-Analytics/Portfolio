from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.modules.gestao.models.cashflow import Cashflow
from app.modules.gestao.models.payment import Payment
from app.modules.gestao.models.payment_method import PaymentMethod
from app.modules.gestao.enums.cashflow_type import CashflowType


class FinancialReportService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def summary(self, start_date: date, end_date: date):
        base = (
            self.db.query(
                Cashflow.flow_type,
                func.sum(Cashflow.amount).label("total"),
            )
            .filter(
                Cashflow.tenant_id == self.tenant_id,
                Cashflow.created_at >= start_date,
                Cashflow.created_at <= end_date,
            )
            .group_by(Cashflow.flow_type)
            .all()
        )

        income = next(
            (b.total for b in base if b.flow_type == CashflowType.IN),
            0,
        ) or 0

        outcome = next(
            (b.total for b in base if b.flow_type == CashflowType.OUT),
            0,
        ) or 0

        return {
            "income": float(income),
            "outcome": float(outcome),
            "balance": float(income - outcome),
        }

    def by_payment_method(self, start_date: date, end_date: date):
        result = (
            self.db.query(
                PaymentMethod.name,
                func.sum(Cashflow.amount).label("total"),
            )
            .join(Payment, Payment.payment_method_id == PaymentMethod.id)
            .join(
                Cashflow,
                (Cashflow.reference == "PAYMENT")
                & (Cashflow.reference_id == Payment.id),
            )
            .filter(
                Cashflow.flow_type == CashflowType.IN,
                Cashflow.tenant_id == self.tenant_id,
                Cashflow.created_at >= start_date,
                Cashflow.created_at <= end_date,
            )
            .group_by(PaymentMethod.name)
            .all()
        )

        return [
            {"payment_method": r.name, "total": float(r.total)}
            for r in result
        ]
