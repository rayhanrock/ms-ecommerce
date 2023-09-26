from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .dependency import ProductQueryParams
from .filters import ProductFilter


# crud functions for categories
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_category(db: Session, id: int):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def update_category(db: Session, id: int, category: schemas.CategoryCreate):
    category_db = get_category(db, id)
    category_db.name = category.name
    db.commit()
    db.refresh(category_db)
    return category_db


def delete_category(db: Session, id: int):
    category = get_category(db, id)
    db.delete(category)
    db.commit()


# crud functions for products
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def get_products(db: Session, params: ProductQueryParams):
    # Initialize a query to retrieve products
    queryset = db.query(models.Product)

    # Create a ProductFilter instance with the params
    product_filter = ProductFilter(params)

    # Apply filters and sorting using the ProductFilter instance
    filtered_queryset = product_filter.apply_filters(queryset)
    product_query = product_filter.apply_sort(filtered_queryset)

    # Execute the query with skip and limit
    products = product_query.offset(params.skip).limit(params.limit).all()
    return products


def update_product(db: Session, id: int, product: schemas.ProductUpdate):
    if product.category_id is not None:
        get_category(db, product.category_id)
    existing_product = get_product(db, id)

    # Update the product attributes with the provided data
    for key, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, key, value)

    db.commit()
    db.refresh(existing_product)

    return existing_product


def delete_product(db: Session, id: int):
    product = get_product(db, id)
    db.delete(product)
    db.commit()
