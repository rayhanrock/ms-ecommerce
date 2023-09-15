from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas
from .dependency import get_order
from . import models

from .paypal_api import create_paypal_order, capture_payment


def make_payment(db: Session, user: dict, order_id: int):
    user_id = user.get('id')
    order = get_order(order_id)
    order_id = order.get('user_id')

    if order_id != user_id:
        raise HTTPException(status_code=401, detail="Invalid user")

    paypal_order_schema = schemas.OrderSchemaForPaypal(
        total_price=str(order.get('total_price')),
        items=[{"name": item.get('product_name'), "quantity": str(item.get('quantity')),
                "unit_amount_value": str(item.get('product_price'))} for item in order.get('order_items')]
    )

    payload = create_paypal_order(paypal_order_schema)

    db_payment = models.Payment(
        user_id=user_id,
        total_price=order.get('total_price'),
        order_id=order_id,
        paypal_order_id=payload.get('id')

    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    payment_info = schemas.Payment(
        id=db_payment.id,
        user_id=db_payment.user_id,
        total_price=db_payment.total_price,
        order_id=db_payment.order_id,
        status=db_payment.status,
        paypal_order_id=db_payment.paypal_order_id,
        approve_url=payload.get('links')[1].get('href')

    )

    return payment_info


def auto_capture_payment_after_approval(db: Session, token: str, PayerID: str = None):
    payload = capture_payment(token)
    print(payload)
    if payload.get('status') == 'COMPLETED':
        get_db_payment = db.query(models.Payment).filter(models.Payment.paypal_order_id == payload.get('id')).first()
        get_db_payment.status = models.PaymentStatus.COMPLETE

        db.commit()
        db.refresh(get_db_payment)

        order = get_order(get_db_payment.order_id)

        # payment completed!!
        # do shipping (shipping service is not build yet)
        # update the stock of the product in the inventory for the order items

        return {"details": get_db_payment}

    return {"message": "something went wrong"}
