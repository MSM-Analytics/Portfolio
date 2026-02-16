from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.gestao.models.stock_balance import StockBalance
from app.modules.gestao.models.stock_movement import StockMovement
from app.modules.gestao.models.product import Product


class StockService:
    def __init__(self, db: Session):
        self.db = db

    # ===============================
    # PUBLIC METHODS
    # ===============================

    def stock_in(
        self,
        product_id: int,
        warehouse_id: int,
        quantity: Decimal,
        cost_price: Decimal,
        reference: str | None = None,
        reference_id: int | None = None,
    ) -> StockBalance:

        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser maior que zero",
            )

        if cost_price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custo deve ser maior que zero",
            )

        product = self._get_product(product_id)
        balance = self._get_or_create_balance(product.id, warehouse_id)

        # 🔢 cálculo de custo médio
        total_value = (
            balance.quantity * balance.avg_cost
        ) + (quantity * cost_price)

        total_quantity = balance.quantity + quantity

        new_avg_cost = total_value / total_quantity

        balance.quantity = total_quantity
        balance.avg_cost = new_avg_cost

        self._create_movement(
            product_id=product.id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            cost_price=cost_price,
            reference=reference,
            reference_id=reference_id,
            movement_type="IN",
        )

        self.db.commit()
        self.db.refresh(balance)

        return balance

    def stock_out(
        self,
        product_id: int,
        warehouse_id: int,
        quantity: Decimal,
        reference: str | None = None,
        reference_id: int | None = None,
    ) -> StockBalance:

        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser maior que zero",
            )

        balance = self._get_balance(product_id, warehouse_id)

        if balance.quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estoque insuficiente",
            )

        balance.quantity -= quantity

        self._create_movement(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=-quantity,
            cost_price=balance.avg_cost,
            reference=reference,
            reference_id=reference_id,
            movement_type="OUT",
        )

        self.db.commit()
        self.db.refresh(balance)

        return balance

    def transfer(
        self,
        product_id: int,
        from_warehouse: int,
        to_warehouse: int,
        quantity: Decimal,
    ):
        # saída origem
        origin_balance = self.stock_out(
            product_id=product_id,
            warehouse_id=from_warehouse,
            quantity=quantity,
            reference="transfer_out",
        )

        # entrada destino com custo médio preservado
        self.stock_in(
            product_id=product_id,
            warehouse_id=to_warehouse,
            quantity=quantity,
            cost_price=origin_balance.avg_cost,
            reference="transfer_in",
        )

    def get_balance(
        self, product_id: int, warehouse_id: int
    ) -> StockBalance:
        return self._get_balance(product_id, warehouse_id)

    # ===============================
    # PRIVATE METHODS
    # ===============================

    def _get_product(self, product_id: int) -> Product:
        product = (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado",
            )

        return product

    def _get_balance(
        self, product_id: int, warehouse_id: int
    ) -> StockBalance:

        balance = (
            self.db.query(StockBalance)
            .filter(
                StockBalance.product_id == product_id,
                StockBalance.warehouse_id == warehouse_id,
            )
            .first()
        )

        if not balance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Saldo não encontrado para este produto neste depósito",
            )

        return balance

    def _get_or_create_balance(
        self, product_id: int, warehouse_id: int
    ) -> StockBalance:

        balance = (
            self.db.query(StockBalance)
            .filter(
                StockBalance.product_id == product_id,
                StockBalance.warehouse_id == warehouse_id,
            )
            .first()
        )

        if not balance:
            balance = StockBalance(
                product_id=product_id,
                warehouse_id=warehouse_id,
                quantity=0,
                avg_cost=0,
            )
            self.db.add(balance)
            self.db.flush()

        return balance

    def _create_movement(
        self,
        product_id: int,
        warehouse_id: int,
        quantity: Decimal,
        cost_price: Decimal,
        movement_type: str,
        reference: str | None,
        reference_id: int | None,
    ):
        movement = StockMovement(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            cost_price=cost_price,
            type=movement_type,
            reference=reference,
            reference_id=reference_id,
        )

        self.db.add(movement)
