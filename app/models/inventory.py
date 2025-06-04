from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Inventory(Base):
    __tablename__ = "Inventory"
    
    inventory_id = Column(Integer, primary_key=True, comment="库存ID，主键")
    product_id = Column(Integer, ForeignKey("Products.product_id", ondelete="CASCADE"), nullable=False, unique=True, index=True, comment="产品ID")
    current_stock_quantity = Column(Integer, nullable=False, default=0, comment="当前库存量")
    alert_threshold = Column(Integer, nullable=False, default=0, comment="库存预警阈值")
    last_updated_at = Column(DateTime, nullable=False, comment="最后更新时间")
    
    # 关系
    product = relationship("Product", back_populates="inventory")
    alerts = relationship("InventoryAlert", back_populates="inventory")

class InventoryAlert(Base):
    __tablename__ = "InventoryAlerts"
    
    alert_id = Column(Integer, primary_key=True, comment="预警ID，主键")
    inventory_id = Column(Integer, ForeignKey("Inventory.inventory_id"), nullable=False, comment="库存ID")
    alert_time = Column(DateTime, nullable=False, index=True, comment="预警生成时间")
    alert_status = Column(String(50), nullable=False, index=True, comment="预警状态")
    handler_name = Column(String(255), comment="处理人姓名")
    notes = Column(Text, comment="处理备注")
    resolved_at = Column(DateTime, comment="预警解决时间")
    created_at = Column(DateTime, default=func.now(), comment="记录创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="记录更新时间")
    
    # 关系
    inventory = relationship("Inventory", back_populates="alerts") 