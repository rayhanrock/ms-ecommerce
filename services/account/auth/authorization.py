from users.models import UserRole
from users.schemas import User


def is_admin(user: User):
    return user.role == UserRole.admin


def is_member(user: User):
    return user.role == UserRole.member


def is_object_owner(user: User, object_id: int):
    return user.id == object_id
