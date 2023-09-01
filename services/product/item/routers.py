from fastapi import APIRouter, Depends
from database import get_db, Base, engine
from sqlalchemy.orm import Session
from . import crud, schemas
from .permissions import is_admin

Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Products"])


# route for categories
@router.post("/categories/", response_model=schemas.CategoryCreate, dependencies=[Depends(is_admin)])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)


@router.get("/categories/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)


@router.get("/categories/{id}")
def read_category(id: int, db: Session = Depends(get_db)):
    return crud.get_category(db, id)


@router.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    crud.delete_category(db, id)
    return {"message": "Category deleted"}


@router.patch("/categories/{id}")
def update_category(id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.update_category(db, id, category)


# route for products
@router.post("/products/", response_model=schemas.ProductCreate)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    crud.get_category(db, id=product.category_id)
    return crud.create_product(db=db, product=product)


@router.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, category_id: int = None, db: Session = Depends(get_db)):
    if category_id is not None:
        # Filter products by category
        products = crud.filter_products_by_category(db, category_id, skip, limit)
    else:
        # Retrieve all products when no category_id is provided
        products = crud.get_all_products(db, skip, limit)

    return products


@router.get("/products/{id}", response_model=schemas.Product)
def read_product(id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, id)


@router.patch("/products/{id}")
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, id, product)


@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, id)
    return {"message": "Product deleted"}
