from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas

from . import models
from .dependency import get_product_stock, get_product


def create_order_by_cart(db: Session, cart: dict):
    cart_items = cart.get('cart_items')
    for item in cart_items:
        product_id = item.get('product_id')
        product_inventory = get_product_stock(product_id)
        if product_inventory.get('stock_quantity') < item.get('quantity'):
            raise HTTPException(status_code=400, detail=f'Not enough stock for product id:{product_id}')

    order = models.Order(
        user_id=cart.get('user_id'),
        total_price=cart.get('total_price')
    )

    for item in cart.get('cart_items'):
        order_item = models.OrderItem(
            product_id=item.get('product_id'),
            quantity=item.get('quantity'),
            subtotal=item.get('subtotal')
        )
        order.order_items.append(order_item)

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def create_order(db: Session, order: schemas.PlaceOrder, current_user: dict):
    user_id = current_user.get('id')
    for item in order.order_items:
        product_id = item.product_id
        product_inventory = get_product_stock(product_id)
        if product_inventory.get('stock_quantity') < item.quantity:
            raise HTTPException(status_code=400, detail=f'Not enough stock for product id:{product_id}')

    db_order = models.Order(
        user_id=user_id,
        total_price=0
    )

    for item in order.order_items:
        product = get_product(item.product_id)
        order_item = models.OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            subtotal=item.quantity * product.get("price")
        )

        db_order.order_items.append(order_item)
        db_order.total_price += order_item.subtotal

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_user_orders(db: Session, current_user: dict):
    user_id = current_user.get('id')
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    return orders
