from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# 订单项
class SalesOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal

class SalesOrderItemCreate(SalesOrderItemBase):
    pass

class SalesOrderItem(SalesOrderItemBase):
    order_item_id: int
    order_id: int
    
    class Config:
        from_attributes = True

# 订单
class SalesOrderBase(BaseModel):
    customer_user_id: str
    channel_id: int
    order_amount: Decimal
    order_status: str

class SalesOrderCreate(SalesOrderBase):
    order_id: int
    order_items: Optional[List[SalesOrderItemCreate]] = []

class SalesOrderUpdate(BaseModel):
    order_status: Optional[str] = None

class SalesOrderInDBBase(SalesOrderBase):
    order_id: int
    order_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SalesOrder(SalesOrderInDBBase):
    order_items: List[SalesOrderItem] = [] 