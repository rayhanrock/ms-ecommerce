from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db

from .authentication import verify_access_token


def get_user_by_token(authorization: Annotated[str | None, Header(...)] = None, db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split("Bearer ")[1]

    user = verify_access_token(token, db)

    return user
