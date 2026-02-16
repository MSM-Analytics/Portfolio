from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.core.dependencies import get_current_user
from app.modules.gestao.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryOut,
)
from app.modules.gestao.services.category_service import CategoryService
from app.modules.gestao.api.dependencies.permissions import require_permission


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = CategoryService(db, tenant_id=user["tenant_id"])
    return service.list()


@router.post(
    "/categories/",
    dependencies=[Depends(require_permission("category:create"))]
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = CategoryService(db, tenant_id=user["tenant_id"])
    return service.create(data)


@router.put(
    "/categories/{category_id}",
    dependencies=[Depends(require_permission("category:update"))]
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service = CategoryService(db, tenant_id=user["tenant_id"])
    try:
        return service.update(category_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")
