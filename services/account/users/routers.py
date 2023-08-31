from fastapi import APIRouter, Depends, HTTPException
from . import schemas, crud
from sqlalchemy.orm import Session
from auth.dependency import get_user_by_token
from auth.authorization import is_object_owner

from database import get_db, Base, engine

Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Users"])


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_user_by_token)):
    db_user = crud.get_user(db, user_id=user_id)

    if not is_object_owner(current_user, db_user.id):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted"}
