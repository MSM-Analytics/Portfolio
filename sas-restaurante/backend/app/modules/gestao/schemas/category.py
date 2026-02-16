from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class CategoryOut(CategoryBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
