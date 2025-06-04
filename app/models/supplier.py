from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Supplier(Base):
    __tablename__ = "Suppliers"
    
    supplier_id = Column(String(50), primary_key=True, comment="供应商ID，主键")
    supplier_name = Column(String(255), nullable=False, index=True, comment="供应商名称")
    contact_info = Column(String(255), comment="联系方式")
    cooperation_status = Column(String(50), nullable=False, index=True, comment="合作状态")
    address = Column(Text, comment="供应商地址")
    email = Column(String(255), unique=True, comment="供应商邮箱")
    created_at = Column(DateTime, nullable=False, comment="记录创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="记录更新时间")
    
    # 关系
    products = relationship("Product", back_populates="supplier")
    logistics = relationship("LogisticsInformation", back_populates="supplier") 