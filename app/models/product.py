from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Product(Base):
    __tablename__ = "Products"
    
    product_id = Column(Integer, primary_key=True, comment="产品ID，主键")
    product_name = Column(String(255), nullable=False, index=True, comment="产品名称")
    sku = Column(String(100), unique=True, index=True, comment="库存单位(SKU)")
    description = Column(Text, comment="产品描述")
    unit_price = Column(DECIMAL(10, 2), comment="标准售价")
    category_id = Column(Integer, nullable=False, index=True, comment="产品分类ID")
    status = Column(Enum("active", "inactive", name="product_status"), nullable=False, index=True, default="inactive", comment="产品状态")
    supplier_id = Column(String(50), ForeignKey("Suppliers.supplier_id"), comment="供应商ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    supplier = relationship("Supplier", back_populates="products")
    order_items = relationship("SalesOrderItem", back_populates="product")
    inventory = relationship("Inventory", back_populates="product", uselist=False) 