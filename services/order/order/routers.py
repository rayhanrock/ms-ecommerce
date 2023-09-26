from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.openapi.models import Response

from database import get_db, Base, engine
from sqlalchemy.orm import Session
from . import schemas, crud
from .dependency import get_user_cart, get_user

Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Order"])


@router.post("/create-order-by-cart", response_model=schemas.Order)
async def create_order_by_cart(db: Session = Depends(get_db), cart=Depends(get_user_cart)):
    return crud.create_order_by_cart(db=db, cart=cart)


@router.post("/create-order", response_model=schemas.Order)
async def create_order(order: schemas.PlaceOrder, db: Session = Depends(get_db), current_user=Depends(get_user)):
    return crud.create_order(db=db, order=order, current_user=current_user)


@router.get("/get-order/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order(db=db, order_id=order_id)


@router.get("/get-user-orders/", response_model=list[schemas.Order])
async def get_order(current_user=Depends(get_user), db: Session = Depends(get_db)):
    return crud.get_user_orders(db=db, current_user=current_user)
