import csv
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4
from io import StringIO, BytesIO
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.modules.gestao.models.cash_closure import CashClosure

class CashClosureExportService:

    @staticmethod
    def export_csv(
        db: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> StringIO:

        query = db.query(CashClosure)
        if start_date:
            query = query.filter(CashClosure.created_at >= start_date)
        if end_date:
            query = query.filter(CashClosure.created_at <= end_date)

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "ID",
            "Usuário",
            "Total Vendas",
            "Total Dinheiro",
            "Total Cartão",
            "Data"
        ])

        for c in query.all():
            writer.writerow([
                c.id,
                c.user_id,
                c.total_sales,
                c.total_cash,
                c.total_card,
                c.created_at
            ])

        output.seek(0)
        return output
    
    @staticmethod
    def export_excel(db: Session, start_date=None, end_date=None) -> BytesIO:
        wb = Workbook()
        ws = wb.active
        ws.title = "Fechamentos"

        ws.append([
            "ID",
            "Usuário",
            "Total Vendas",
            "Total Dinheiro",
            "Total Cartão",
            "Data"
        ])

        query = db.query(CashClosure)
        if start_date:
            query = query.filter(CashClosure.created_at >= start_date)
        if end_date:
            query = query.filter(CashClosure.created_at <= end_date)

        for c in query.all():
            ws.append([
                c.id,
                c.user_id,
                float(c.total_sales),
                float(c.total_cash),
                float(c.total_card),
                c.created_at
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output
    
    @staticmethod
    def export_pdf(db: Session, start_date=None, end_date=None) -> BytesIO:
        output = BytesIO()
        pdf = SimpleDocTemplate(output, pagesize=A4)

        data = [[
            "ID", "Usuário", "Total", "Dinheiro", "Cartão", "Data"
        ]]

        query = db.query(CashClosure)
        if start_date:
            query = query.filter(CashClosure.created_at >= start_date)
        if end_date:
            query = query.filter(CashClosure.created_at <= end_date)

        for c in query.all():
            data.append([
                c.id,
                c.user_id,
                str(c.total_sales),
                str(c.total_cash),
                str(c.total_card),
                c.created_at.strftime("%d/%m/%Y")
            ])

        table = Table(data)
        pdf.build([table])

        output.seek(0)
        return output
