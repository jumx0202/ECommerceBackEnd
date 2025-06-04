from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SyncedChannelOrder(Base):
    __tablename__ = "SyncedChannelOrders"
    
    synced_order_id = Column(String(255), primary_key=True, comment="同步订单ID")
    external_customer_user_id = Column(String(255), comment="外部客户用户ID")
    external_channel_code = Column(String(50), ForeignKey("SalesChannels.channel_code"), nullable=False, index=True, comment="外部渠道代码")
    order_status_external = Column(String(100), nullable=False, comment="外部订单状态")
    order_amount_external = Column(DECIMAL(12, 2), comment="外部订单金额")
    order_created_at_external = Column(DateTime, nullable=False, index=True, comment="外部订单创建时间")
    raw_order_data = Column(JSON, comment="原始订单数据")
    internal_sales_order_id = Column(Integer, ForeignKey("SalesOrders.order_id"), unique=True, comment="内部销售订单ID")
    sync_timestamp = Column(DateTime, default=func.now(), comment="数据同步时间戳")
    
    # 关系
    order_items = relationship("SyncedChannelOrderItem", back_populates="synced_order", cascade="all, delete-orphan")

class SyncedChannelOrderItem(Base):
    __tablename__ = "SyncedChannelOrderItems"
    
    synced_order_item_id = Column(Integer, primary_key=True, autoincrement=True, comment="同步订单项ID")
    synced_order_id = Column(String(255), ForeignKey("SyncedChannelOrders.synced_order_id"), nullable=False, index=True, comment="同步订单ID")
    external_product_id = Column(String(255), index=True, comment="外部产品ID")
    product_sku = Column(String(100), index=True, comment="产品SKU")
    product_name_external = Column(String(255), comment="外部产品名称")
    quantity = Column(Integer, nullable=False, comment="购买数量")
    unit_price_external = Column(DECIMAL(10, 2), nullable=False, comment="外部单价")
    total_price_external = Column(DECIMAL(10, 2), nullable=False, comment="外部总价")
    raw_item_data = Column(JSON, comment="原始订单项数据")
    
    # 关系
    synced_order = relationship("SyncedChannelOrder", back_populates="order_items") 