from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.services.report_service import ReportService
from app.modules.gestao.exports.csv_export import export_csv
from app.modules.gestao.exports.excel_export import export_excel

router = APIRouter(
    prefix="/exports",
    tags=["Exportações"]
)

# CSV
@router.get("/daily/csv")
def export_daily_csv(
    report_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.daily_report(db, report_date)

    headers = [
        "closure_id",
        "shift",
        "total_sales",
        "total_cash",
        "total_card"
    ]

    rows = report["closures"]

    return export_csv(
        filename=f"relatorio_diario_{report_date}.csv",
        headers=headers,
        rows=rows
    )

@router.get("/period/csv")
def export_period_csv(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.period_report(db, start_date, end_date)

    headers = [
        "date",
        "total_sales",
        "total_cash",
        "total_card"
    ]

    rows = report["daily_summary"]

    return export_csv(
        filename=f"relatorio_periodo_{start_date}_{end_date}.csv",
        headers=headers,
        rows=rows
    )

@router.get("/monthly/csv")
def export_monthly_csv(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.monthly_report(db, year, month)

    headers = [
        "date",
        "total_sales",
        "total_cash",
        "total_card"
    ]

    rows = report["daily_summary"]

    return export_csv(
        filename=f"relatorio_mensal_{year}_{month}.csv",
        headers=headers,
        rows=rows
    )

@router.get("/sales/by-product/csv")
def export_sales_by_product_csv(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    rows = ReportService.sales_by_product(db)

    headers = [
        "product_id",
        "product_name",
        "quantity_sold",
        "total_sales",
        "average_price"
    ]

    return export_csv(
        filename="vendas_por_produto.csv",
        headers=headers,
        rows=rows
    )

@router.get("/sales/by-category/csv")
def export_sales_by_category_csv(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    rows = ReportService.sales_by_category(db)

    headers = [
        "category_id",
        "category_name",
        "quantity_sold",
        "total_sales"
    ]

    return export_csv(
        filename="vendas_por_categoria.csv",
        headers=headers,
        rows=rows
    )

# EXCEL

@router.get("/daily/excel")
def export_daily_excel(
    report_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.daily_report(db, report_date)

    sheets = {
        "Resumo": {
            "headers": [
                "total_sales",
                "total_cash",
                "total_card",
                "sales_count",
                "average_ticket"
            ],
            "rows": [report]
        },
        "Fechamentos": {
            "headers": [
                "closure_id",
                "shift",
                "total_sales",
                "total_cash",
                "total_card"
            ],
            "rows": report["closures"]
        }
    }

    return export_excel(
        filename=f"relatorio_diario_{report_date}.xlsx",
        sheets=sheets
    )

@router.get("/period/excel")
def export_period_excel(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.period_report(db, start_date, end_date)

    sheets = {
        "Resumo": {
            "headers": [
                "total_sales",
                "total_cash",
                "total_card",
                "days_count",
                "sales_count",
                "average_ticket"
            ],
            "rows": [report]
        },
        "Resumo Diário": {
            "headers": [
                "date",
                "total_sales",
                "total_cash",
                "total_card"
            ],
            "rows": report["daily_summary"]
        }
    }

    return export_excel(
        filename=f"relatorio_periodo_{start_date}_{end_date}.xlsx",
        sheets=sheets
    )

@router.get("/monthly/excel")
def export_monthly_excel(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.monthly_report(db, year, month)

    sheets = {
        "Resumo": {
            "headers": [
                "total_sales",
                "total_cash",
                "total_card",
                "days_count",
                "sales_count",
                "average_ticket"
            ],
            "rows": [report]
        },
        "Resumo Diário": {
            "headers": [
                "date",
                "total_sales",
                "total_cash",
                "total_card"
            ],
            "rows": report["daily_summary"]
        }
    }

    return export_excel(
        filename=f"relatorio_mensal_{year}_{month}.xlsx",
        sheets=sheets
    )

@router.get("/sales/by-product/excel")
def export_sales_by_product_excel(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    rows = ReportService.sales_by_product(db)

    sheets = {
        "Vendas por Produto": {
            "headers": [
                "product_id",
                "product_name",
                "quantity_sold",
                "total_sales",
                "average_price"
            ],
            "rows": rows
        }
    }

    return export_excel(
        filename="vendas_por_produto.xlsx",
        sheets=sheets
    )

@router.get("/sales/by-category/excel")
def export_sales_by_category_excel(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    rows = ReportService.sales_by_category(db)

    sheets = {
        "Vendas por Categoria": {
            "headers": [
                "category_id",
                "category_name",
                "quantity_sold",
                "total_sales"
            ],
            "rows": rows
        }
    }

    return export_excel(
        filename="vendas_por_categoria.xlsx",
        sheets=sheets
    )

# PDF
from app.modules.gestao.exports.pdf_export import export_pdf

@router.get("/daily/pdf")
def export_daily_pdf(
    report_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.daily_report(db, report_date)

    summary = {
        "Data": report_date,
        "Total Geral": report["total_sales"],
        "Dinheiro": report["total_cash"],
        "Cartão": report["total_card"],
        "Vendas": report["sales_count"],
        "Ticket Médio": report["average_ticket"]
    }

    headers = [
        "closure_id",
        "shift",
        "total_sales",
        "total_cash",
        "total_card"
    ]

    return export_pdf(
        filename=f"relatorio_diario_{report_date}.pdf",
        title="Relatório Diário de Caixa",
        headers=headers,
        rows=report["closures"],
        summary=summary
    )

@router.get("/period/pdf")
def export_period_pdf(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.period_report(db, start_date, end_date)

    summary = {
        "Período": f"{start_date} até {end_date}",
        "Total Geral": report["total_sales"],
        "Dinheiro": report["total_cash"],
        "Cartão": report["total_card"],
        "Vendas": report["sales_count"],
        "Ticket Médio": report["average_ticket"]
    }

    headers = [
        "date",
        "total_sales",
        "total_cash",
        "total_card"
    ]

    return export_pdf(
        filename=f"relatorio_periodo_{start_date}_{end_date}.pdf",
        title="Relatório por Período",
        headers=headers,
        rows=report["daily_summary"],
        summary=summary
    )

@router.get("/monthly/pdf")
def export_monthly_pdf(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    report = ReportService.monthly_report(db, year, month)

    summary = {
        "Mês/Ano": f"{month}/{year}",
        "Total Geral": report["total_sales"],
        "Dinheiro": report["total_cash"],
        "Cartão": report["total_card"],
        "Vendas": report["sales_count"],
        "Ticket Médio": report["average_ticket"]
    }

    headers = [
        "date",
        "total_sales",
        "total_cash",
        "total_card"
    ]

    return export_pdf(
        filename=f"relatorio_mensal_{year}_{month}.pdf",
        title="Relatório Mensal",
        headers=headers,
        rows=report["daily_summary"],
        summary=summary
    )

@router.get("/sales/by-product/pdf")
def export_sales_by_product_pdf(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    rows = ReportService.sales_by_product(db)

    headers = [
        "product_name",
        "quantity_sold",
        "total_sales",
        "average_price"
    ]

    return export_pdf(
        filename="vendas_por_produto.pdf",
        title="Vendas por Produto",
        headers=headers,
        rows=rows
    )

@router.get("/sales/by-category/pdf")
def export_sales_by_category_pdf(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    rows = ReportService.sales_by_category(db)

    headers = [
        "category_name",
        "quantity_sold",
        "total_sales"
    ]

    return export_pdf(
        filename="vendas_por_categoria.pdf",
        title="Vendas por Categoria",
        headers=headers,
        rows=rows
    )
