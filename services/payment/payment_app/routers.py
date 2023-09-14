from fastapi import APIRouter, Depends

from database import get_db, Base, engine
from sqlalchemy.orm import Session
from . import schemas, crud
from .dependency import get_user

Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Payment"])


@router.post("/make-payment/{order_id}")
async def make_payment(order_id: int, db: Session = Depends(get_db), user=Depends(get_user)):
    return crud.make_payment(db=db, user=user, order_id=order_id)
