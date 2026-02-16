from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from datetime import date
import calendar

# MODELS
from app.modules.gestao.models.cash_closure import CashClosure
from app.modules.gestao.models.sale import Sale
from app.modules.gestao.models.sale_item import SaleItem
from app.modules.gestao.models.product import Product
from app.modules.gestao.models.category import Category


class ReportService:

    @staticmethod
    def daily_report(db: Session, report_date: date):
        closures = (
            db.query(CashClosure)
            .filter(func.date(CashClosure.created_at) == report_date)
            .all()
        )

        total_sales = Decimal("0.00")
        total_cash = Decimal("0.00")
        total_card = Decimal("0.00")
        sales_count = 0

        closures_data = []

        for closure in closures:
            total_sales += closure.total_sales
            total_cash += closure.total_cash
            total_card += closure.total_card

            count_sales = (
                db.query(func.count(Sale.id))
                .filter(Sale.cash_closure_id == closure.id)
                .scalar()
            )

            sales_count += count_sales

            closures_data.append({
                "closure_id": closure.id,
                "shift": closure.shift,
                "total_sales": closure.total_sales,
                "total_cash": closure.total_cash,
                "total_card": closure.total_card,
            })

        average_ticket = (
            total_sales / sales_count
            if sales_count > 0
            else Decimal("0.00")
        )

        return {
            "date": report_date,
            "total_sales": total_sales,
            "total_cash": total_cash,
            "total_card": total_card,
            "closures_count": len(closures),
            "sales_count": sales_count,
            "average_ticket": average_ticket,
            "closures": closures_data
        }

    @staticmethod
    def period_report(
        db: Session,
        start_date: date,
        end_date: date
    ):
        closures = (
            db.query(CashClosure)
            .filter(
                func.date(CashClosure.created_at) >= start_date,
                func.date(CashClosure.created_at) <= end_date
            )
            .all()
        )

        total_sales = Decimal("0.00")
        total_cash = Decimal("0.00")
        total_card = Decimal("0.00")
        sales_count = 0

        closures_count = len(closures)
        days_set = set()
        daily_map = {}

        for closure in closures:
            closure_date = closure.created_at.date()
            days_set.add(closure_date)

            total_sales += closure.total_sales
            total_cash += closure.total_cash
            total_card += closure.total_card

            count_sales = (
                db.query(func.count(Sale.id))
                .filter(Sale.cash_closure_id == closure.id)
                .scalar()
            )

            sales_count += count_sales

            if closure_date not in daily_map:
                daily_map[closure_date] = {
                    "total_sales": Decimal("0.00"),
                    "total_cash": Decimal("0.00"),
                    "total_card": Decimal("0.00"),
                }

            daily_map[closure_date]["total_sales"] += closure.total_sales
            daily_map[closure_date]["total_cash"] += closure.total_cash
            daily_map[closure_date]["total_card"] += closure.total_card

        average_ticket = (
            total_sales / sales_count
            if sales_count > 0
            else Decimal("0.00")
        )

        daily_summary = [
            {
                "date": day,
                "total_sales": values["total_sales"],
                "total_cash": values["total_cash"],
                "total_card": values["total_card"],
            }
            for day, values in sorted(daily_map.items())
        ]

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_sales": total_sales,
            "total_cash": total_cash,
            "total_card": total_card,
            "days_count": len(days_set),
            "closures_count": closures_count,
            "sales_count": sales_count,
            "average_ticket": average_ticket,
            "daily_summary": daily_summary,
        }
    
    @staticmethod
    def monthly_report(db: Session, year: int, month: int):
        last_day = calendar.monthrange(year, month)[1]

        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)

        closures = (
            db.query(CashClosure)
            .filter(
                func.date(CashClosure.created_at) >= start_date,
                func.date(CashClosure.created_at) <= end_date
            )
            .all()
        )

        total_sales = Decimal("0.00")
        total_cash = Decimal("0.00")
        total_card = Decimal("0.00")
        sales_count = 0

        closures_count = len(closures)
        days_set = set()
        daily_map = {}

        for closure in closures:
            closure_date = closure.created_at.date()
            days_set.add(closure_date)

            total_sales += closure.total_sales
            total_cash += closure.total_cash
            total_card += closure.total_card

            count_sales = (
                db.query(func.count(Sale.id))
                .filter(Sale.cash_closure_id == closure.id)
                .scalar()
            )

            sales_count += count_sales

            if closure_date not in daily_map:
                daily_map[closure_date] = {
                    "total_sales": Decimal("0.00"),
                    "total_cash": Decimal("0.00"),
                    "total_card": Decimal("0.00"),
                }

            daily_map[closure_date]["total_sales"] += closure.total_sales
            daily_map[closure_date]["total_cash"] += closure.total_cash
            daily_map[closure_date]["total_card"] += closure.total_card

        average_ticket = (
            total_sales / sales_count
            if sales_count > 0
            else Decimal("0.00")
        )

        daily_summary = [
            {
                "date": day,
                "total_sales": values["total_sales"],
                "total_cash": values["total_cash"],
                "total_card": values["total_card"],
            }
            for day, values in sorted(daily_map.items())
        ]

        return {
            "year": year,
            "month": month,
            "total_sales": total_sales,
            "total_cash": total_cash,
            "total_card": total_card,
            "days_count": len(days_set),
            "closures_count": closures_count,
            "sales_count": sales_count,
            "average_ticket": average_ticket,
            "daily_summary": daily_summary,
        }

    @staticmethod
    def sales_by_product(db: Session):
        rows = (
            db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(SaleItem.quantity).label("quantity_sold"),
                func.sum(SaleItem.total_price).label("total_sales"),
            )
            .join(SaleItem.product)
            .join(SaleItem.sale)
            .filter(Sale.cash_closure_id.isnot(None))
            .group_by(Product.id, Product.name)
            .order_by(func.sum(SaleItem.total_price).desc())
            .all()
        )

        return [
            {
                "product_id": r.product_id,
                "product_name": r.product_name,
                "quantity_sold": int(r.quantity_sold),
                "total_sales": r.total_sales,
                "average_price": (
                    r.total_sales / r.quantity_sold
                    if r.quantity_sold > 0
                    else Decimal("0.00")
                )
            }
            for r in rows
        ]
    
    @staticmethod
    def sales_by_category(db: Session):
        rows = (
            db.query(
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                func.sum(SaleItem.quantity).label("quantity_sold"),
                func.sum(SaleItem.total_price).label("total_sales"),
            )
            .join(Product, Product.category_id == Category.id)
            .join(SaleItem, SaleItem.product_id == Product.id)
            .join(Sale, Sale.id == SaleItem.sale_id)
            .filter(Sale.cash_closure_id.isnot(None))
            .group_by(Category.id, Category.name)
            .order_by(func.sum(SaleItem.total_price).desc())
            .all()
        )

        return [
            {
                "category_id": r.category_id,
                "category_name": r.category_name,
                "quantity_sold": int(r.quantity_sold),
                "total_sales": r.total_sales,
            }
            for r in rows
        ]
