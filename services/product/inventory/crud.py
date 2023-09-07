from fastapi import HTTPException

from . import schemas, models
from sqlalchemy.orm import Session

from item.crud import get_product


def get_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()


def create_inventory(db: Session, inventory: schemas.InventoryCreate):
    # check if product exists first. get_product raises an exception if product does not exist
    product = get_product(db, inventory.product_id)
    product_in_inventory = db.query(models.Inventory).filter(models.Inventory.product_id == product.id).first()

    if product_in_inventory:
        raise HTTPException(status_code=400, detail="Product already exists in inventory")

    db_inventory = models.Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def check_stock(db: Session, product_id: int):
    product_in_inventory = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
    if not product_in_inventory:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    return product_in_inventory


def add_stock(db: Session, product_id: int, quantity: int):
    product_in_inventory = check_stock(db, product_id)
    product_in_inventory.stock_quantity += quantity
    db.commit()

    return product_in_inventory


def remove_stock(db: Session, product_id: int, quantity: int):
    product_in_inventory = check_stock(db, product_id)

    if product_in_inventory.stock_quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock in inventory")
    product_in_inventory.stock_quantity -= quantity
    db.commit()

    return product_in_inventory
