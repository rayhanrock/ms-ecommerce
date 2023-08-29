from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session

from . import schemas
from database import get_db
from .authentication import Token, authenticate_user, verify_access_token

router = APIRouter( tags=["Authentication"] )


@router.post("/token")
async def login_for_access_token(loginData: schemas.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, loginData.email, loginData.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = Token(user).create_access_token()
    return {"access_token": token, "token_type": "bearer"}


@router.post("/verify-token/")
def get_user_by_token(authorization: Annotated[str | None, Header(...)] = None, db: Session = Depends(get_db)):
    print(authorization)
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split("Bearer ")[1]

    user = verify_access_token(token, db)

    return user
