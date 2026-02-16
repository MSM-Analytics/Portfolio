from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from decimal import Decimal

from app.modules.gestao.models.cash_closure import CashClosure
from app.modules.gestao.models.sale import Sale
from app.modules.gestao.services.cash_shift_service import get_shift_by_time


class CashClosureService:

    # 🔒 Fechamento de caixa com bloqueio por turno
    @staticmethod
    def close_cash(db: Session, user_id: int) -> CashClosure:
        try:
            now = datetime.utcnow()
            today = date.today()
            shift = get_shift_by_time(now)

            # 1️⃣ Bloqueio de fechamento duplicado no mesmo turno
            already_closed = (
                db.query(CashClosure)
                .filter(
                    CashClosure.shift == shift,
                    CashClosure.created_at >= today
                )
                .first()
            )

            if already_closed:
                raise ValueError(
                    f"Já existe fechamento de caixa para o turno {shift}."
                )

            # 2️⃣ Buscar vendas abertas DO DIA
            sales = (
                db.query(Sale)
                .filter(
                    Sale.cash_closure_id.is_(None),
                    Sale.created_at >= today
                )
                .all()
            )

            # 3️⃣ Filtrar vendas por turno
            sales = [
                sale for sale in sales
                if get_shift_by_time(sale.created_at) == shift
            ]

            if not sales:
                raise ValueError(
                    f"Não existem vendas abertas para o turno {shift}."
                )

            # 4️⃣ Calcular totais
            total_sales = sum((sale.total for sale in sales), Decimal("0.00"))

            total_cash = sum(
                (sale.total for sale in sales if sale.payment_method == "cash"),
                Decimal("0.00")
            )

            total_card = sum(
                (sale.total for sale in sales if sale.payment_method == "card"),
                Decimal("0.00")
            )

            # 5️⃣ Validação matemática
            if total_sales != (total_cash + total_card):
                raise ValueError(
                    "Inconsistência nos totais do fechamento de caixa."
                )

            # 6️⃣ Criar fechamento
            closure = CashClosure(
                user_id=user_id,
                shift=shift,
                total_sales=total_sales,
                total_cash=total_cash,
                total_card=total_card,
                created_at=datetime.utcnow()
            )

            db.add(closure)
            db.flush()  # garante closure.id

            # 7️⃣ Associar vendas ao fechamento
            for sale in sales:
                sale.cash_closure_id = closure.id
                db.add(sale)

            # 8️⃣ Commit único (atomicidade)
            db.commit()
            db.refresh(closure)

            return closure

        except (ValueError, SQLAlchemyError) as e:
            db.rollback()
            raise e

    # 📜 Histórico de fechamentos (mantido 100%)
    @staticmethod
    def get_cash_closure_history(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[CashClosure]:

        query = db.query(CashClosure)

        if start_date:
            query = query.filter(CashClosure.created_at >= start_date)

        if end_date:
            query = query.filter(CashClosure.created_at <= end_date)

        return (
            query
            .order_by(CashClosure.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def reopen_cash_closure(
        db: Session,
        closure_id: int,
        user_id: int,
        reason: str
    ) -> CashClosure:
        try:
            closure = (
                db.query(CashClosure)
                .filter(CashClosure.id == closure_id)
                .first()
            )

            if not closure:
                raise ValueError("Fechamento não encontrado.")

            if closure.is_reopened:
                raise ValueError("Este fechamento já foi reaberto.")

            # 1️⃣ Desassociar vendas
            sales = (
                db.query(Sale)
                .filter(Sale.cash_closure_id == closure.id)
                .all()
            )

            for sale in sales:
                sale.cash_closure_id = None
                db.add(sale)

            # 2️⃣ Marcar fechamento como reaberto (auditoria)
            closure.is_reopened = True
            closure.reopen_reason = reason
            closure.reopened_at = datetime.utcnow()
            closure.reopened_by = user_id

            db.add(closure)
            db.commit()
            db.refresh(closure)

            return closure

        except (ValueError, SQLAlchemyError) as e:
            db.rollback()
            raise e
        
    @staticmethod
    def get_summary(db: Session, closure_id: int):
        closure = (
            db.query(CashClosure)
            .filter(CashClosure.id == closure_id)
            .first()
        )

        if not closure:
            raise ValueError("Fechamento não encontrado.")

        sales = (
            db.query(Sale)
            .filter(Sale.cash_closure_id == closure.id)
            .all()
        )

        sales_count = len(sales)

        average_ticket = (
            closure.total_sales / sales_count
            if sales_count > 0
            else Decimal("0.00")
        )

        return {
            "id": closure.id,
            "shift": closure.shift,
            "created_at": closure.created_at,
            "total_sales": closure.total_sales,
            "total_cash": closure.total_cash,
            "total_card": closure.total_card,
            "sales_count": sales_count,
            "average_ticket": average_ticket,
            "is_reopened": closure.is_reopened,
        }