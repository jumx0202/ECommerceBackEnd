from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class LogisticsInformationBase(BaseModel):
    supplier_id: str
    order_reference_id: Optional[str] = None
    logistics_status: str
    logistics_details: Optional[str] = None
    tracking_number: Optional[str] = None
    carrier_name: Optional[str] = None
    estimated_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None

class LogisticsInformationCreate(LogisticsInformationBase):
    logistics_id: str
    last_updated_at: datetime

class LogisticsInformationUpdate(LogisticsInformationBase):
    logistics_status: Optional[str] = None
    actual_delivery_date: Optional[date] = None

class LogisticsInformationInDBBase(LogisticsInformationBase):
    logistics_id: str
    last_updated_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class LogisticsInformation(LogisticsInformationInDBBase):
    pass 