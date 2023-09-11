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


def remove_from_cart(db: Session, product: schemas.RemoveFromCart, current_user: dict):
    user_cart = get_cart(db=db, current_user=current_user)

    exitsing_cart_item = None
    for cart_item in user_cart.cart_items:
        if cart_item.product_id == product.product_id:
            exitsing_cart_item = cart_item
            break

    if exitsing_cart_item is None:
        raise HTTPException(status_code=400, detail="Product not in cart")

    user_cart.cart_items.remove(exitsing_cart_item)

    user_cart.total_price -= exitsing_cart_item.subtotal
    db.commit()
    db.refresh(user_cart)

    return user_cart


def update_cart(db: Session, update_cart: schemas.UpdateCart, current_user: dict):
    user_cart = get_cart(db=db, current_user=current_user)
    product = get_product(product_id=update_cart.product_id)

    existing_cart_item = None
    for cart_item in user_cart.cart_items:
        if cart_item.product_id == update_cart.product_id:
            existing_cart_item = cart_item
            break

    if existing_cart_item is None:
        raise HTTPException(status_code=400, detail="Product not in cart")

    if update_cart.operation == schemas.OperationEnum.increase:
        existing_cart_item.quantity += update_cart.quantity
    elif update_cart.operation == schemas.OperationEnum.decrease:
        existing_cart_item.quantity -= update_cart.quantity
        if existing_cart_item.quantity < 0:
            existing_cart_item.quantity = 0  # Ensure quantity doesn't go negative

    # Calculate the subtotal for the updated cart item
    existing_cart_item.subtotal = existing_cart_item.quantity * product.get("price")

    # Recalculate the total price for the cart
    user_cart.total_price = sum(cart_item.subtotal for cart_item in user_cart.cart_items)

    db.commit()
    db.refresh(user_cart)

    # Now, you can return the updated user_cart as a GetCart instance
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
