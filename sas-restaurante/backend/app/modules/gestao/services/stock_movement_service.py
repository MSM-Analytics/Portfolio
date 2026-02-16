from sqlalchemy.orm import Session

from app.modules.gestao.models.stock import Stock
from app.modules.gestao.models.stock_movement import StockMovement, MovementType
from app.modules.gestao.schemas.stock_movement import StockMovementCreate


class StockMovementService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def create(self, data: StockMovementCreate) -> StockMovement:
        stock = (
            self.db.query(Stock)
            .filter(
                Stock.id == data.stock_id,
                Stock.tenant_id == self.tenant_id,
                Stock.is_active == True
            )
            .first()
        )

        if not stock:
            raise ValueError("Stock not found")

        if data.type == MovementType.OUT and stock.quantity < data.quantity:
            raise ValueError("Insufficient stock")

        # Apply movement
        if data.type == MovementType.IN:
            stock.quantity += data.quantity
        elif data.type == MovementType.OUT:
            stock.quantity -= data.quantity
        elif data.type == MovementType.ADJUST:
            stock.quantity = data.quantity

        movement = StockMovement(
            stock_id=stock.id,
            tenant_id=self.tenant_id,
            type=data.type,
            quantity=data.quantity,
            reason=data.reason,
        )

        self.db.add(movement)
        self.db.commit()
        self.db.refresh(movement)

        return movement

    def list_by_stock(self, stock_id: int):
        return (
            self.db.query(StockMovement)
            .filter(
                StockMovement.stock_id == stock_id,
                StockMovement.tenant_id == self.tenant_id
            )
            .order_by(StockMovement.created_at.desc())
            .all()
        )
