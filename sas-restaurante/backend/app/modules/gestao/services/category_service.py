from sqlalchemy.orm import Session

from app.modules.gestao.models.category import Category
from app.modules.gestao.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    def list(self):
        return (
            self.db.query(Category)
            .filter(
                Category.tenant_id == self.tenant_id,
                Category.is_active == True
            )
            .all()
        )

    def create(self, data: CategoryCreate) -> Category:
        category = Category(
            name=data.name,
            tenant_id=self.tenant_id
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = (
            self.db.query(Category)
            .filter(
                Category.id == category_id,
                Category.tenant_id == self.tenant_id
            )
            .first()
        )

        if not category:
            raise ValueError("Category not found")

        ALLOWED_FIELDS = {"name", "is_active"}

        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ALLOWED_FIELDS:
                setattr(category, field, value)


        self.db.commit()
        self.db.refresh(category)
        return category
