from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SalesOrder(Base):
    __tablename__ = "SalesOrders"
    
    order_id = Column(Integer, primary_key=True, comment="订单ID，主键")
    customer_user_id = Column(String(255), nullable=False, index=True, comment="客户用户ID")
    channel_id = Column(Integer, ForeignKey("SalesChannels.channel_id"), nullable=False, comment="渠道ID")
    order_amount = Column(DECIMAL(10, 2), nullable=False, comment="订单总金额")
    order_status = Column(String(50), nullable=False, index=True, comment="订单状态")
    order_date = Column(DateTime, default=func.now(), index=True, comment="订单日期")
    created_at = Column(DateTime, default=func.now(), comment="记录创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="记录更新时间")
    
    # 关系
    channel = relationship("SalesChannel", back_populates="sales_orders")
    order_items = relationship("SalesOrderItem", back_populates="order", cascade="all, delete-orphan")

class SalesOrderItem(Base):
    __tablename__ = "SalesOrderItems"
    
    order_item_id = Column(Integer, primary_key=True, autoincrement=True, comment="订单项ID")
    order_id = Column(Integer, ForeignKey("SalesOrders.order_id"), nullable=False, index=True, comment="销售订单ID")
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False, index=True, comment="产品ID")
    quantity = Column(Integer, nullable=False, comment="购买数量")
    unit_price = Column(DECIMAL(10, 2), nullable=False, comment="售出单价")
    total_price = Column(DECIMAL(10, 2), nullable=False, comment="总价")
    
    # 关系
    order = relationship("SalesOrder", back_populates="order_items")
    product = relationship("Product", back_populates="order_items") 