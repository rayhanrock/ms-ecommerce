from pydantic import BaseModel, field_validator


class Item(BaseModel):
    name: str
    quantity: str
    unit_amount_value: str


class OrderSchemaForPaypal(BaseModel):
    total_price: str
    items: list[Item]


class Payment(BaseModel):
    id: int
    user_id: int
    total_price: float
    order_id: int
    paypal_order_id: str
    approve_url: str

    class Config:
        orm_mode = True
