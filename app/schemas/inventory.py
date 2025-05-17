from pydantic import BaseModel
from typing import Optional

class InventoryBase(BaseModel):
    product_id: int
    stock_level: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    product_id: Optional[int] = None
    stock_level: Optional[int] = None

class Inventory(InventoryBase):
    id: int
    updated_at: str

    class Config:
        orm_mode = True