from pydantic import BaseModel
from enum import Enum


class AddToCart(BaseModel):
    product_id: int
    quantity: float


class RemoveFromCart(BaseModel):
    product_id: int


class OperationEnum(str, Enum):
    increase = "increase"
    decrease = "decrease"


class UpdateCart(BaseModel):
    product_id: int
    operation: OperationEnum
    quantity: int


class CartItem(BaseModel):
    product_id: int
    product_price: float
    product_name: str
    quantity: int
    subtotal: float


class GetCart(BaseModel):
    user_id: int
    total_price: float
    cart_items: list[CartItem]

    class Config:
        orm_mode = True
