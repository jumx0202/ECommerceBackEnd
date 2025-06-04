from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    product_name: str
    sku: str
    description: Optional[str] = None
    unit_price: Optional[Decimal] = None
    category_id: int = Field(default=1)
    status: str = Field(default="inactive", pattern="^(active|inactive)$")
    supplier_id: Optional[str] = None

class ProductCreate(ProductBase):
    product_id: int

class ProductUpdate(ProductBase):
    product_name: Optional[str] = None
    sku: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = Field(default=None, pattern="^(active|inactive)$")

class ProductInDBBase(ProductBase):
    product_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Product(ProductInDBBase):
    pass 