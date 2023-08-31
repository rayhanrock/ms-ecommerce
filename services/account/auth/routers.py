from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from . import schemas, dependency
from users.schemas import User
from database import get_db
from .authentication import Token, authenticate_user, verify_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/token")
async def login_for_access_token(loginData: schemas.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, loginData.email, loginData.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = Token(user).create_access_token()
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify-token/")
def get_user_by_token(user: User = Depends(dependency.get_user_by_token)):
    return user
