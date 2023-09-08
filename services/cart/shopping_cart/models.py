from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    total_price = Column(Float, default=0.0)

    # Define a one-to-many relationship with CartItem
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer)
    quantity = Column(Integer)
    subtotal = Column(Float, default=0.0)

    # Define a many-to-one relationship with Cart
    cart = relationship("Cart", back_populates="cart_items")
