from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db, get_current_user
from app.modules.gestao.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductOut,
)
from app.modules.gestao.services.product_service import ProductService
from app.modules.gestao.api.dependencies.permissions import require_permission


router = APIRouter(prefix="/products", tags=["Products"])


def get_service(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> ProductService:
    return ProductService(db, tenant_id=user["tenant_id"])


@router.get("/", response_model=List[ProductOut])
def list_products(
    service: ProductService = Depends(get_service),
):
    return service.list()


@router.post(
    "/products/",
    dependencies=[Depends(require_permission("product:create"))]
)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_service),
):
    return service.create(data)


@router.put(
    "/products/{product_id}",
    dependencies=[Depends(require_permission("product:update"))]
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_service),
):
    try:
        return service.update(product_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")
    
