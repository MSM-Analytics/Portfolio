from sqlalchemy.orm import Session
from app.modules.gestao.models.refund import Refund
from app.modules.gestao.models.payment import Payment
from app.modules.gestao.services.cashflow_service import CashflowService


class RefundService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def create(self, payment_id: int, amount: float):
        payment = (
            self.db.query(Payment)
            .filter(
                Payment.id == payment_id,
                Payment.tenant_id == self.tenant_id,
            )
            .first()
        )

        if not payment:
            raise ValueError("Payment not found")

        refunded_amount = (
            self.db.query(Refund)
            .filter(Refund.payment_id == payment_id)
            .with_entities(Refund.amount)
            .all()
        )

        total_refunded = sum(r[0] for r in refunded_amount)

        if total_refunded + amount > payment.amount:
            raise ValueError("Refund exceeds payment amount")

        refund = Refund(
            tenant_id=self.tenant_id,
            payment_id=payment_id,
            amount=amount,
        )
        self.db.add(refund)

        cashflow_service = CashflowService(self.db, self.tenant_id)
        cashflow_service.register_out(
            amount=amount,
            reference="REFUND",
            reference_id=payment_id,
            description=f"Refund payment #{payment_id}"
        )
