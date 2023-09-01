from datetime import datetime
from pydantic import BaseModel
from inventory.schemas import Inventory


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int


class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
