from fastapi import Depends
from .dependency import get_user_by_token


def is_admin(user: dict = Depends(get_user_by_token)):
    print(user)
