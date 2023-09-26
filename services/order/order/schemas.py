from pydantic import BaseModel, field_validator
from .models import OrderStatus


class Item(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")
        return value


class PlaceOrder(BaseModel):
    order_items: list[Item]


class OrderItem(BaseModel):
    product_id: int
    product_price: float
    product_name: str
    quantity: int
    subtotal: float


class Order(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatus
    order_items: list[OrderItem]

    class Config:
        orm_mode = True
