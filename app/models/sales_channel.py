from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SalesChannel(Base):
    __tablename__ = "SalesChannels"
    
    channel_id = Column(Integer, primary_key=True, comment="渠道ID，主键")
    channel_name = Column(String(255), nullable=False, unique=True, comment="渠道名称，唯一")
    channel_code = Column(String(50), unique=True, index=True, comment="渠道代码")
    platform_type = Column(String(50), nullable=False, comment="平台类型：ecommerce/marketplace/social/direct")
    api_address = Column(String(500), comment="API地址")
    commission_rate = Column(Float, default=0.0, comment="佣金率（百分比）")
    channel_status = Column(String(20), default="active", comment="渠道状态：active/inactive")
    description = Column(Text, comment="渠道描述")
    created_at = Column(DateTime, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, comment="更新时间")
    
    # 关系
    sales_orders = relationship("SalesOrder", back_populates="channel") 