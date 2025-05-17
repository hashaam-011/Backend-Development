from pydantic import BaseModel
from typing import Optional

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None

class Sale(SaleBase):
    id: int
    sale_date: str

    class Config:
        orm_mode = True