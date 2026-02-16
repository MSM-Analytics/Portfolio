from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
