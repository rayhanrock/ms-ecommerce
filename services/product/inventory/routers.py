from typing import Annotated

from fastapi import APIRouter, Depends, Body
from database import get_db, Base, engine
from sqlalchemy.orm import Session
from . import schemas, crud

Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Inventory"])


@router.get("/inventory/", response_model=list[schemas.Inventory])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_inventory(db, skip=skip, limit=limit)


@router.post("/inventory/", response_model=schemas.Inventory)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return crud.create_inventory(db=db, inventory=inventory)


@router.get("/check-stock/{product_id}", response_model=schemas.Inventory)
def check_stock(product_id: int, db: Session = Depends(get_db)):
    return crud.check_stock(db, product_id)


@router.post("/add-stock/{product_id}", response_model=schemas.Inventory)
def add_stock(product_id: int, quantity: Annotated[int, Body(gt=0, embed=True)], db: Session = Depends(get_db)):
    return crud.add_stock(db, product_id, quantity)


@router.post("/remove-stock/{product_id}", response_model=schemas.Inventory)
def remove_stock(product_id: int, quantity: Annotated[int, Body(gt=0, embed=True)], db: Session = Depends(get_db)):
    return crud.remove_stock(db, product_id, quantity)
