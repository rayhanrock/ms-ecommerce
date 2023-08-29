from sqlalchemy import Boolean, Column, Integer, String, Enum
from enum import Enum as PyEnum
from database import Base


class UserRole(str, PyEnum):
    admin = "admin"
    member = "member"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=255), unique=True, index=True)
    hashed_password = Column(String(length=255))
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.member)
