from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from mixins import CreatedAtMixin
from database import Base


class Inventory(CreatedAtMixin, Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    stock_quantity = Column(Integer)
    product = relationship("Product", back_populates="inventory")
