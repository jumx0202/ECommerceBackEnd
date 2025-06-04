from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SalesChannelBase(BaseModel):
    channel_name: str
    channel_code: Optional[str] = None
    platform_type: str
    api_address: Optional[str] = None
    commission_rate: Optional[float] = 0.0
    channel_status: Optional[str] = "active"
    description: Optional[str] = None

class SalesChannelCreate(SalesChannelBase):
    channel_id: int
    created_at: datetime

class SalesChannelUpdate(BaseModel):
    channel_name: Optional[str] = None
    channel_code: Optional[str] = None
    platform_type: Optional[str] = None
    api_address: Optional[str] = None
    commission_rate: Optional[float] = None
    channel_status: Optional[str] = None
    description: Optional[str] = None

class SalesChannelInDBBase(SalesChannelBase):
    channel_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SalesChannel(SalesChannelInDBBase):
    pass

class SalesChannelResponse(SalesChannelInDBBase):
    """用于API响应的schema"""
    pass 