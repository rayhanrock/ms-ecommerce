from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.openapi.models import Response

from database import get_db, Base, engine
from sqlalchemy.orm import Session
from . import schemas, crud
from .dependency import get_user_by_token

Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Cart"])


@router.post("/add-to-cart", response_model=schemas.GetCart)
async def add_to_cart(cart: schemas.AddToCart, db: Session = Depends(get_db),
                      current_user: dict = Depends(get_user_by_token)):
    return crud.add_to_cart(db=db, cart=cart, current_user=current_user)


@router.post("/remove-from-cart", response_model=schemas.GetCart)
async def remove_product_from_cart(product: schemas.RemoveFromCart, db: Session = Depends(get_db),
                                   current_user: dict = Depends(get_user_by_token)):
    return crud.remove_from_cart(db=db, product=product, current_user=current_user)


@router.post("/update-cart", response_model=schemas.GetCart)
async def update_product_quantity_in_cart(update_cart: schemas.UpdateCart, db: Session = Depends(get_db),
                                          current_user: dict = Depends(get_user_by_token)):
    return crud.update_cart(db=db, update_cart=update_cart, current_user=current_user)


@router.get("/get-cart/", response_model=schemas.GetCart)
async def get_cart(current_user: dict = Depends(get_user_by_token), db: Session = Depends(get_db)):
    return crud.get_cart(db=db, current_user=current_user)


@router.delete("/clear-cart/")
async def clear_cart(current_user: dict = Depends(get_user_by_token), db: Session = Depends(get_db)):
    crud.clear_cart(db=db, current_user=current_user)
    return {"message": "Cart cleared"}
