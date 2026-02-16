from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.modules.gestao.models.cash_closure import CashClosure
from app.modules.gestao.models.sale_item import SaleItem
from app.modules.gestao.models.product import Product
from app.modules.gestao.models.category import Category


class DashboardChartsService:

    # =========================
    # LINHA — VENDAS POR DIA
    # =========================
    @staticmethod
    def sales_by_day(db: Session, year: int, month: int):
        data = (
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

        return {
            "labels": [str(row.day) for row in data],
            "values": [row.total for row in data]
        }

    # =========================
    # PIZZA — FORMAS DE PAGAMENTO
    # =========================
    @staticmethod
    def payment_methods(db: Session):
        cash = (
            db.query(func.coalesce(func.sum(CashClosure.total_cash), 0))
            .scalar()
        )
        card = (
            db.query(func.coalesce(func.sum(CashClosure.total_card), 0))
            .scalar()
        )

        return {
            "labels": ["Dinheiro", "Cartão"],
            "values": [cash, card]
        }

    # =========================
    # BARRA — VENDAS POR CATEGORIA
    # =========================
    @staticmethod
    def sales_by_category(db: Session):
        data = (
            db.query(
                Category.name,
                func.sum(SaleItem.total_price).label("total")
            )
            .join(Product)
            .join(SaleItem)
            .group_by(Category.name)
            .order_by(func.sum(SaleItem.total_price).desc())
            .all()
        )

        return {
            "labels": [row.name for row in data],
            "values": [row.total for row in data]
        }

    # =========================
    # BARRA — TOP PRODUTOS
    # =========================
    @staticmethod
    def top_products(db: Session, limit: int = 10):
        data = (
            db.query(
                Product.name,
                func.sum(SaleItem.quantity).label("qty")
            )
            .join(SaleItem)
            .group_by(Product.name)
            .order_by(func.sum(SaleItem.quantity).desc())
            .limit(limit)
            .all()
        )

        return {
            "labels": [row.name for row in data],
            "values": [row.qty for row in data]
        }
