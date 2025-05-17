from sqlalchemy.orm import Session
from app.models import Inventory, Product
from app.schemas import inventory as inventory_schema

def get_inventory_item(db: Session, inventory_id: int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()

def get_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Inventory).offset(skip).limit(limit).all()

def create_inventory(db: Session, inventory: inventory_schema.InventoryCreate):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory(db: Session, inventory_id: int, inventory: inventory_schema.InventoryUpdate):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory:
        for key, value in inventory.dict(exclude_unset=True).items():
            setattr(db_inventory, key, value)
        db.commit()
        db.refresh(db_inventory)
    return db_inventory

def delete_inventory(db: Session, inventory_id: int):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory:
        db.delete(db_inventory)
        db.commit()
    return db_inventory

def get_low_stock_items(db: Session, threshold: int):
    return db.query(Inventory).join(Product).filter(
        Inventory.stock_level <= threshold
    ).all()