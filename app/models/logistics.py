from sqlalchemy import Column, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class LogisticsInformation(Base):
    __tablename__ = "LogisticsInformation"
    
    logistics_id = Column(String(50), primary_key=True, comment="物流ID，主键")
    supplier_id = Column(String(50), ForeignKey("Suppliers.supplier_id"), nullable=False, index=True, comment="供应商ID")
    order_reference_id = Column(String(255), comment="相关订单号")
    logistics_status = Column(String(50), nullable=False, index=True, comment="物流状态")
    logistics_details = Column(Text, comment="物流详情描述")
    tracking_number = Column(String(255), index=True, comment="运单号")
    carrier_name = Column(String(255), comment="承运商名称")
    estimated_delivery_date = Column(Date, comment="预计送达日期")
    actual_delivery_date = Column(Date, comment="实际送达日期")
    last_updated_at = Column(DateTime, nullable=False, comment="信息更新时间")
    created_at = Column(DateTime, default=func.now(), comment="记录创建时间")
    
    # 关系
    supplier = relationship("Supplier", back_populates="logistics") 