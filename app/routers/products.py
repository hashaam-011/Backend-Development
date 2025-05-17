from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import product as product_crud
from app.schemas import product as product_schema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/products/", response_model=product_schema.Product)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create_product(db=db, product=product)

@router.get("/products/", response_model=list[product_schema.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = product_crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/products/{product_id}", response_model=product_schema.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=product_schema.Product)
def update_product(product_id: int, product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    db_product = product_crud.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", response_model=product_schema.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
