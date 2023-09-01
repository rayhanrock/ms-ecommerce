from pydantic import BaseModel


class InventoryBase(BaseModel):
    stock_quantity: int


class InventoryCreate(InventoryBase):
    pass


class Inventory(InventoryBase):
    id: int
    product_id: int
    product: "Product"  # Relationship field

    class Config:
        orm_mode = True
