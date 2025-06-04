from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base_class import Base

class OrderSyncLog(Base):
    __tablename__ = "OrderSyncLogs"
    
    log_id = Column(String(50), primary_key=True, comment="日志ID，主键")
    synced_order_id = Column(String(255), nullable=False, index=True, comment="同步订单ID")
    external_channel_code = Column(String(50), nullable=False, index=True, comment="外部渠道代码")
    sync_status = Column(String(50), nullable=False, index=True, comment="同步状态")
    sync_time = Column(DateTime, nullable=False, index=True, comment="同步操作时间")
    message = Column(Text, comment="同步结果消息")
    created_at = Column(DateTime, default=func.now(), comment="记录创建时间") 