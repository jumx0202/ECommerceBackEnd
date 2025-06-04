from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 库存
class InventoryBase(BaseModel):
    product_id: int
    current_stock_quantity: int
    alert_threshold: int

class InventoryCreate(InventoryBase):
    inventory_id: int
    last_updated_at: datetime

class InventoryUpdate(BaseModel):
    current_stock_quantity: Optional[int] = None
    alert_threshold: Optional[int] = None

class InventoryInDBBase(InventoryBase):
    inventory_id: int
    last_updated_at: datetime
    
    class Config:
        from_attributes = True

class Inventory(InventoryInDBBase):
    pass

# 库存预警
class InventoryAlertBase(BaseModel):
    inventory_id: int
    alert_time: datetime
    alert_status: str
    handler_name: Optional[str] = None
    notes: Optional[str] = None

class InventoryAlertCreate(InventoryAlertBase):
    alert_id: int

class InventoryAlert(InventoryAlertBase):
    alert_id: int
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 