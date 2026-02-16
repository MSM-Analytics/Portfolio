from sqlalchemy.orm import Session, selectinload
from decimal import Decimal
from sqlalchemy import func

from app.modules.gestao.models.payment import Payment
from app.modules.gestao.models.refund import Refund
from app.modules.gestao.models.sale import Sale
from app.modules.gestao.services.cashflow_service import CashflowService
from app.core.enums import SaleStatus


class PaymentService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    # 🔁 MÉTODO CENTRAL — recalcula status da venda
    def _recalculate_sale_status(self, sale: Sale):
        total_paid = sum(
            Decimal(p.amount) for p in sale.payments
        )

        total_refunded = (
            self.db.query(func.coalesce(func.sum(Refund.amount), 0))
            .join(Payment)
            .filter(Payment.sale_id == sale.id)
            .scalar()
        )

        effective_paid = total_paid - Decimal(total_refunded)

        if effective_paid <= 0:
            sale.status = SaleStatus.OPEN
        elif effective_paid < sale.total_amount:
            sale.status = SaleStatus.PARTIALLY_PAID
        else:
            sale.status = SaleStatus.PAID

    # 💰 REGISTRAR PAGAMENTOS
    def register(
        self,
        sale_id: int,
        payments: list,
    ):
        sale = (
            self.db.query(Sale)
            .options(selectinload(Sale.payments))
            .filter(
                Sale.id == sale_id,
                Sale.tenant_id == self.tenant_id,
                Sale.status != SaleStatus.CANCELED,
            )
            .first()
        )

        if not sale:
            raise ValueError("Sale not found or canceled")

        cashflow_service = CashflowService(self.db, self.tenant_id)

        for item in payments:
            payment = Payment(
                tenant_id=self.tenant_id,
                sale_id=sale.id,
                payment_method_id=item.payment_method_id,
                amount=item.amount,
            )

            self.db.add(payment)
            self.db.flush()  # garante payment.id

            cashflow_service.register_in(
                amount=Decimal(item.amount),
                reference="PAYMENT",
                reference_id=payment.id,  # ✅ CORRETO
                description=f"Payment for sale #{sale.id}",
            )

        self._recalculate_sale_status(sale)

    # 🔄 ESTORNO (REFUND)
    def refund(
        self,
        payment: Payment,
        amount: Decimal,
        description: str | None = None,
    ):
        if amount <= 0:
            raise ValueError("Refund amount must be greater than zero")

        if amount > payment.amount:
            raise ValueError("Refund amount exceeds payment amount")

        if payment.tenant_id != self.tenant_id:
            raise ValueError("Invalid tenant")

        cashflow_service = CashflowService(self.db, self.tenant_id)

        refund = Refund(
            tenant_id=self.tenant_id,
            payment_id=payment.id,
            amount=amount,
            description=description,
        )

        self.db.add(refund)

        cashflow_service.register_out(
            amount=amount,
            reference="REFUND",
            reference_id=payment.id,  # alinhado com PAYMENT
            description=description or f"Refund payment #{payment.id}",
        )

        self._recalculate_sale_status(payment.sale)
