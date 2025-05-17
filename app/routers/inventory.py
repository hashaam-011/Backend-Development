from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import inventory as inventory_crud
from app.schemas import inventory as inventory_schema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/inventory/", response_model=inventory_schema.Inventory)
def create_inventory(inventory: inventory_schema.InventoryCreate, db: Session = Depends(get_db)):
    return inventory_crud.create_inventory(db=db, inventory=inventory)

@router.get("/inventory/", response_model=list[inventory_schema.Inventory])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventory = inventory_crud.get_inventory(db, skip=skip, limit=limit)
    return inventory

@router.get("/inventory/{inventory_id}", response_model=inventory_schema.Inventory)
def read_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = inventory_crud.get_inventory_item(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory

@router.put("/inventory/{inventory_id}", response_model=inventory_schema.Inventory)
def update_inventory(inventory_id: int, inventory: inventory_schema.InventoryUpdate, db: Session = Depends(get_db)):
    db_inventory = inventory_crud.update_inventory(db, inventory_id=inventory_id, inventory=inventory)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory

@router.delete("/inventory/{inventory_id}", response_model=inventory_schema.Inventory)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = inventory_crud.delete_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory

@router.get("/inventory/low-stock")
def get_low_stock_items(threshold: int = 10, db: Session = Depends(get_db)):
    return inventory_crud.get_low_stock_items(db, threshold)
