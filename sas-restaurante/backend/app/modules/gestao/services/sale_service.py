from sqlalchemy.orm import Session, selectinload
from decimal import Decimal

from app.modules.gestao.models.sale import Sale
from app.modules.gestao.models.sale_item import SaleItem
from app.modules.gestao.models.product import Product
from app.modules.gestao.schemas.sale import SaleCreate
from app.modules.gestao.services.stock_service import StockService
from app.modules.gestao.services.cashflow_service import CashflowService
from app.modules.gestao.services.payment_service import PaymentService
from app.core.enums import SaleStatus


class SaleService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def create(self, data: SaleCreate) -> Sale:
        try:
            with self.db.begin():

                sale = Sale(
                    tenant_id=self.tenant_id,
                    total_amount=Decimal("0.00"),
                    status=SaleStatus.OPEN,
                )

                self.db.add(sale)
                self.db.flush()

                total = Decimal("0.00")
                stock_service = StockService(self.db, self.tenant_id)

                for item in data.items:
                    product = (
                        self.db.query(Product)
                        .filter(
                            Product.id == item.product_id,
                            Product.tenant_id == self.tenant_id,
                            Product.is_active.is_(True),
                        )
                        .first()
                    )

                    if not product:
                        raise ValueError("Product not found")

                    stock_service.check_availability(
                        product_id=product.id,
                        quantity=item.quantity,
                    )

                    subtotal = Decimal(product.price) * item.quantity
                    total += subtotal

                    sale_item = SaleItem(
                        sale_id=sale.id,
                        product_id=product.id,
                        quantity=item.quantity,
                        unit_price=product.price,
                        subtotal=subtotal,
                    )

                    self.db.add(sale_item)

                    stock_service.register_out(
                        product_id=product.id,
                        quantity=item.quantity,
                        reference="SALE",
                        reference_id=sale.id,
                    )

                sale.total_amount = total

                # 💰 CAIXA
                cashflow_service = CashflowService(self.db, self.tenant_id)
                cashflow_service.register_in(
                    amount=sale.total_amount,
                    reference="SALE",
                    reference_id=sale.id,
                    description=f"Sale #{sale.id}",
                )

                # 💳 PAGAMENTOS
                paid_total = sum(
                    Decimal(p.amount) for p in data.payments
                )

                if paid_total != sale.total_amount:
                    raise ValueError("Payment total does not match sale total")

                payment_service = PaymentService(self.db, self.tenant_id)
                payment_service.register(
                    sale_id=sale.id,
                    payments=data.payments,
                )

                sale.status = SaleStatus.PAID

                return sale

        except Exception:
            raise

    def list(self):
        return (
            self.db.query(Sale)
            .options(
                selectinload(Sale.items),
                selectinload(Sale.payments),
            )
            .filter(
                Sale.tenant_id == self.tenant_id,
                Sale.status != SaleStatus.CANCELED,
            )
            .all()
        )

    def cancel(self, sale_id: int) -> Sale:
        try:
            with self.db.begin():

                sale = (
                    self.db.query(Sale)
                    .options(
                        selectinload(Sale.items),
                        selectinload(Sale.payments),
                    )
                    .filter(
                        Sale.id == sale_id,
                        Sale.tenant_id == self.tenant_id,
                        Sale.status == SaleStatus.PAID,
                    )
                    .first()
                )

                if not sale:
                    raise ValueError("Sale not found or cannot be canceled")

                cashflow_service = CashflowService(self.db, self.tenant_id)
                stock_service = StockService(self.db, self.tenant_id)
                payment_service = PaymentService(self.db, self.tenant_id)

                payment_service.refund_sale(sale_id=sale.id)

                cashflow_service.register_out(
                    amount=sale.total_amount,
                    reference="SALE_CANCEL",
                    reference_id=sale.id,
                    description=f"Cancel Sale #{sale.id}",
                )

                for item in sale.items:
                    stock_service.register_in(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        reference="SALE_CANCEL",
                        reference_id=sale.id,
                    )

                sale.status = SaleStatus.CANCELED

                return sale

        except Exception:
            raise
