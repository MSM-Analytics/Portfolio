from sqlalchemy.orm import Session
from app.modules.gestao.models.payment_method import PaymentMethod
from app.modules.gestao.schemas.payment_method import (
    PaymentMethodCreate,
    PaymentMethodUpdate,
)


class PaymentMethodService:
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def list(self):
        return (
            self.db.query(PaymentMethod)
            .filter(
                PaymentMethod.tenant_id == self.tenant_id,
                PaymentMethod.is_active == True,
            )
            .all()
        )

    def create(self, data: PaymentMethodCreate):
        method = PaymentMethod(
            name=data.name,
            tenant_id=self.tenant_id,
        )
        self.db.add(method)
        self.db.commit()
        self.db.refresh(method)
        return method

    def update(self, method_id: int, data: PaymentMethodUpdate):
        method = (
            self.db.query(PaymentMethod)
            .filter(
                PaymentMethod.id == method_id,
                PaymentMethod.tenant_id == self.tenant_id,
            )
            .first()
        )

        if not method:
            raise ValueError("Payment method not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(method, field, value)

        self.db.commit()
        self.db.refresh(method)
        return method
