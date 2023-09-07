from pydantic import BaseModel
from datetime import datetime


class InventoryBase(BaseModel):
    stock_quantity: int


class InventoryCreate(InventoryBase):
    product_id: int


class Inventory(InventoryBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
