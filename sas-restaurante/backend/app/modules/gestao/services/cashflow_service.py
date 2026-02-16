from decimal import Decimal
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func

from app.modules.gestao.models.cashflow import Cashflow
from app.modules.gestao.enums.cashflow_type import CashflowType
from app.modules.gestao.enums.cashflow_category import CashflowCategory


class CashflowService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def register_in(
        self,
        amount: Decimal,
        reference: str,
        reference_id: int,
        description: str | None = None,
        category: CashflowCategory = CashflowCategory.SALE,
    ) -> Cashflow:
        cashflow = Cashflow(
            tenant_id=self.tenant_id,
            amount=amount,
            flow_type=CashflowType.IN,
            category=category,
            reference=reference,
            reference_id=reference_id,
            description=description,
        )
        self.db.add(cashflow)
        self.db.flush()
        return cashflow

    def register_out(
        self,
        amount: Decimal,
        reference: str,
        reference_id: int,
        description: str | None = None,
        category: CashflowCategory = CashflowCategory.REFUND,
    ) -> Cashflow:
        cashflow = Cashflow(
            tenant_id=self.tenant_id,
            amount=amount,
            flow_type=CashflowType.OUT,
            category=category,
            reference=reference,
            reference_id=reference_id,
            description=description,
        )
        self.db.add(cashflow)
        self.db.flush()
        return cashflow

    def get_balance(self) -> Decimal:
        income = (
            self.db.query(func.coalesce(func.sum(Cashflow.amount), 0))
            .filter(
                Cashflow.tenant_id == self.tenant_id,
                Cashflow.flow_type == CashflowType.IN,
            )
            .scalar()
        )

        outcome = (
            self.db.query(func.coalesce(func.sum(Cashflow.amount), 0))
            .filter(
                Cashflow.tenant_id == self.tenant_id,
                Cashflow.flow_type == CashflowType.OUT,
            )
            .scalar()
        )

        return Decimal(income) - Decimal(outcome)

    # 🔍 AUDITORIA / RELATÓRIOS
    def list_all(self):
        return (
            self.db.query(Cashflow)
            .options(
                selectinload(Cashflow.sale),
                selectinload(Cashflow.payment),
            )
            .filter(Cashflow.tenant_id == self.tenant_id)
            .order_by(Cashflow.created_at.desc())
            .all()
        )
