from pydantic import BaseModel


class AddToCart(BaseModel):
    product_id: int
    quantity: float


class RemoveFromCart(BaseModel):
    product_id: int


class CartItem(BaseModel):
    product_id: int
    quantity: int
    subtotal: float


class GetCart(BaseModel):
    user_id: int
    total_price: float
    cart_items: list[CartItem]

    class Config:
        orm_mode = True
