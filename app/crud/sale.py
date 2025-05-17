from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models import Sale, Product, Category
from app.schemas import sale as sale_schema

def get_sale(db: Session, sale_id: int):
    return db.query(Sale).filter(Sale.id == sale_id).first()

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sale).offset(skip).limit(limit).all()

def create_sale(db: Session, sale: sale_schema.SaleCreate):
    db_sale = Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def update_sale(db: Session, sale_id: int, sale: sale_schema.SaleUpdate):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if db_sale:
        for key, value in sale.dict(exclude_unset=True).items():
            setattr(db_sale, key, value)
        db.commit()
        db.refresh(db_sale)
    return db_sale

def delete_sale(db: Session, sale_id: int):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if db_sale:
        db.delete(db_sale)
        db.commit()
    return db_sale

def get_revenue_by_period(db: Session, start_date: datetime, end_date: datetime):
    return db.query(
        func.sum(Sale.total_price).label('total_revenue'),
        func.count(Sale.id).label('total_sales')
    ).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    ).first()

def filter_sales(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    product_id: int = None,
    category_id: int = None
):
    query = db.query(Sale).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    )

    if product_id:
        query = query.filter(Sale.product_id == product_id)

    if category_id:
        query = query.join(Product).filter(Product.category_id == category_id)

    return query.all()