from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.crud import sale as sale_crud
from app.schemas import sale as sale_schema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sales/", response_model=sale_schema.Sale)
def create_sale(sale: sale_schema.SaleCreate, db: Session = Depends(get_db)):
    return sale_crud.create_sale(db=db, sale=sale)

@router.get("/sales/", response_model=list[sale_schema.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = sale_crud.get_sales(db, skip=skip, limit=limit)
    return sales

@router.get("/sales/{sale_id}", response_model=sale_schema.Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = sale_crud.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.put("/sales/{sale_id}", response_model=sale_schema.Sale)
def update_sale(sale_id: int, sale: sale_schema.SaleUpdate, db: Session = Depends(get_db)):
    db_sale = sale_crud.update_sale(db, sale_id=sale_id, sale=sale)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.delete("/sales/{sale_id}", response_model=sale_schema.Sale)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = sale_crud.delete_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.get("/sales/revenue/daily")
def get_daily_revenue(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    return sale_crud.get_revenue_by_period(db, today, today)

@router.get("/sales/revenue/weekly")
def get_weekly_revenue(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    return sale_crud.get_revenue_by_period(db, week_start, week_end)

@router.get("/sales/revenue/monthly")
def get_monthly_revenue(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    if today.month == 12:
        month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    return sale_crud.get_revenue_by_period(db, month_start, month_end)

@router.get("/sales/revenue/annual")
def get_annual_revenue(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    year_start = today.replace(month=1, day=1)
    year_end = today.replace(month=12, day=31)
    return sale_crud.get_revenue_by_period(db, year_start, year_end)

@router.get("/sales/filter")
def filter_sales(
    start_date: datetime,
    end_date: datetime,
    product_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    return sale_crud.filter_sales(db, start_date, end_date, product_id, category_id)
