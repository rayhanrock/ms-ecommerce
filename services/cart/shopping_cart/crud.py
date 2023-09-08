from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas

from .dependency import get_product
from . import models


def add_to_cart(db: Session, cart: schemas.AddToCart, current_user: dict):
    product = get_product(product_id=cart.product_id)
    user_cart = get_cart(db=db, current_user=current_user)
    for cart_item in user_cart.cart_items:
        if cart_item.product_id == cart.product_id:
            raise HTTPException(status_code=400, detail="Product already in cart")

    sub_total = product.get("price") * cart.quantity
    cart_item = models.CartItem(
        product_id=product.get("id"),
        quantity=cart.quantity,
        subtotal=sub_total
    )

    user_cart.cart_items.append(cart_item)

    user_cart.total_price = sum(cart_item.subtotal for cart_item in user_cart.cart_items)
    db.commit()
    db.refresh(user_cart)

    return user_cart


def get_cart(db: Session, current_user: dict):
    user_id = current_user.get("id")
    user_cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not user_cart:
        user_cart = models.Cart(user_id=user_id)
        db.add(user_cart)
        db.commit()
        db.refresh(user_cart)
    return user_cart


def clear_cart(db: Session, current_user: dict):
    user_id = current_user.get("id")
    user_cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if user_cart:
        db.delete(user_cart)
        db.commit()
