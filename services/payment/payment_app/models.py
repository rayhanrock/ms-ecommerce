from sqlalchemy import Column, Integer, ForeignKey, Float, String
from enum import Enum
from sqlalchemy.types import Enum as SQLAlchemyEnum

from database import Base


class PaymentStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETE = "complete"
    REFUND = "refund"


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    total_price = Column(Float, default=0.0)
    order_id = Column(Integer, index=True)
    paypal_order_id = Column(String(length=100), index=True)
    status = Column(SQLAlchemyEnum(PaymentStatus), default=PaymentStatus.PENDING)
