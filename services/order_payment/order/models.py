from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.types import Enum as SQLAlchemyEnum

from database import Base


class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    REFUND = "refund"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    total_price = Column(Float, default=0.0)
    status = Column(SQLAlchemyEnum(OrderStatus, name="order_status"), default=OrderStatus.PENDING)

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer)
    quantity = Column(Integer)
    subtotal = Column(Float, default=0.0)

    order = relationship("Order", back_populates="order_items")
