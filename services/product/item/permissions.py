from fastapi import Depends, HTTPException
from .dependency import get_user_by_token


def is_admin(user: dict = Depends(get_user_by_token)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="you don't have enough permissions")
