from pydantic import BaseModel
from decimal import Decimal
from datetime import date
from typing import List

# RELATÓRIO DIÁRIO AUTOMÁTICO
class DailyCashClosureSummary(BaseModel):
    closure_id: int
    shift: str
    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal


class DailyReportResponse(BaseModel):
    date: date

    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal

    closures_count: int
    sales_count: int
    average_ticket: Decimal

    closures: List[DailyCashClosureSummary]

# RELATÓRIO INTERVALO DE DATAS
class PeriodDailySummary(BaseModel):
    date: date
    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal


class PeriodReportResponse(BaseModel):
    start_date: date
    end_date: date

    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal

    days_count: int
    closures_count: int
    sales_count: int
    average_ticket: Decimal

    daily_summary: List[PeriodDailySummary]

# RELATÓRIO MENSAL AUTOMÁTICO
class MonthlyDailySummary(BaseModel):
    date: date
    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal


class MonthlyReportResponse(BaseModel):
    year: int
    month: int

    total_sales: Decimal
    total_cash: Decimal
    total_card: Decimal

    days_count: int
    closures_count: int
    sales_count: int
    average_ticket: Decimal

    daily_summary: List[MonthlyDailySummary]


class ProductSalesReport(BaseModel):
    product_id: int
    product_name: str
    quantity_sold: int
    total_sales: Decimal
    average_price: Decimal

class CategorySalesReport(BaseModel):
    category_id: int
    category_name: str
    quantity_sold: int
    total_sales: Decimal
