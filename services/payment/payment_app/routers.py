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


@router.get("/auto-capture-payment-after-approval/")
async def capture_payment(token: str, PayerID: str, db: Session = Depends(get_db)):
    return crud.auto_capture_payment_after_approval(db=db, token=token, PayerID=PayerID)


@router.get("/capture-payment/{token}")
async def capture_payment(token: str,db: Session = Depends(get_db)):
    return crud.auto_capture_payment_after_approval(db=db, token=token)
