from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SupplierBase(BaseModel):
    supplier_name: str
    contact_info: Optional[str] = None
    cooperation_status: str
    address: Optional[str] = None
    email: Optional[str] = None

class SupplierCreate(SupplierBase):
    supplier_id: str
    created_at: datetime

class SupplierUpdate(SupplierBase):
    supplier_name: Optional[str] = None
    cooperation_status: Optional[str] = None

class SupplierInDBBase(SupplierBase):
    supplier_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Supplier(SupplierInDBBase):
    pass 