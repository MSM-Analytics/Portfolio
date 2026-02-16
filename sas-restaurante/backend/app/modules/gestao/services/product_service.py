from typing import List
from sqlalchemy.orm import Session

from app.modules.gestao.models.product import Product
from app.modules.gestao.schemas.product import ProductCreate, ProductUpdate
from app.modules.gestao.models.stock import Stock


class ProductNotFoundError(Exception):
    pass


class ProductService:
    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    def list(self) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(
                Product.tenant_id == self.tenant_id,
                Product.is_active
            )
            .all()
        )

    def create(data: ProductCreate, db: Session, tenant_id: str):
        product = Product(**data.model_dump(), tenant_id=tenant_id)

        db.add(product)
        db.commit()
        db.refresh(product)

        stock = Stock(
            product_id=product.id,
            quantity=0,
            min_quantity=0,
            tenant_id=tenant_id,
        )

        db.add(stock)
        db.commit()

        return product


    def update(self, product_id: int, data: ProductUpdate) -> Product:
        product = (
            self.db.query(Product)
            .filter(
                Product.id == product_id,
                Product.tenant_id == self.tenant_id
            )
            .first()
        )

        if not product:
            raise ProductNotFoundError()

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product
