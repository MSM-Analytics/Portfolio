from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.modules.gestao.models.cash_closure import CashClosure
from app.modules.gestao.models.sale_item import SaleItem
from app.modules.gestao.models.product import Product
from app.modules.gestao.models.category import Category


class DashboardKPIService:

    @staticmethod
    def get_kpis(db: Session):
        today = date.today()
        year = today.year
        month = today.month

        # ======================
        # TOTAL HOJE
        # ======================
        today_sales = (
            db.query(func.coalesce(func.sum(CashClosure.total_sales), 0))
            .filter(func.date(CashClosure.created_at) == today)
            .scalar()
        )

        # ======================
        # TOTAL MÊS ATUAL
        # ======================
        month_sales = (
            db.query(func.coalesce(func.sum(CashClosure.total_sales), 0))
            .filter(
                func.extract("year", CashClosure.created_at) == year,
                func.extract("month", CashClosure.created_at) == month
            )
            .scalar()
        )

        # ======================
        # MÊS ANTERIOR (CRESCIMENTO)
        # ======================
        prev_month = 12 if month == 1 else month - 1
        prev_year = year - 1 if month == 1 else year

        prev_month_sales = (
            db.query(func.coalesce(func.sum(CashClosure.total_sales), 0))
            .filter(
                func.extract("year", CashClosure.created_at) == prev_year,
                func.extract("month", CashClosure.created_at) == prev_month
            )
            .scalar()
        )

        month_growth = (
            float(((month_sales - prev_month_sales) / prev_month_sales) * 100)
            if prev_month_sales > 0
            else 0.0
        )

        # ======================
        # TICKET MÉDIO
        # (por fechamento de caixa)
        # ======================
        total_closures = (
            db.query(func.count(CashClosure.id))
            .filter(
                func.extract("year", CashClosure.created_at) == year,
                func.extract("month", CashClosure.created_at) == month
            )
            .scalar()
        )

        average_ticket = (
            month_sales / total_closures
            if total_closures > 0
            else Decimal("0.00")
        )

        # ======================
        # DINHEIRO vs CARTÃO
        # ======================
        cash = (
            db.query(func.coalesce(func.sum(CashClosure.total_cash), 0))
            .scalar()
        )

        card = (
            db.query(func.coalesce(func.sum(CashClosure.total_card), 0))
            .scalar()
        )

        total_payment = cash + card or Decimal("1.00")

        # ======================
        # PRODUTO MAIS VENDIDO
        # ======================
        top_product = (
            db.query(Product.name)
            .join(SaleItem)
            .group_by(Product.name)
            .order_by(func.sum(SaleItem.quantity).desc())
            .first()
        )

        # ======================
        # CATEGORIA LÍDER
        # ======================
        top_category = (
            db.query(Category.name)
            .join(Product)
            .join(SaleItem)
            .group_by(Category.name)
            .order_by(func.sum(SaleItem.quantity).desc())
            .first()
        )

        return {
            "today_sales": today_sales,
            "month_sales": month_sales,
            "average_ticket": average_ticket,
            "cash_percentage": round((cash / total_payment) * 100, 2),
            "card_percentage": round((card / total_payment) * 100, 2),
            "top_product": top_product[0] if top_product else "-",
            "top_category": top_category[0] if top_category else "-",
            "month_growth": round(month_growth, 2),
        }
