from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class User(Base):
    __tablename__ = "Users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID，主键，自增")
    username = Column(String(255), nullable=False, unique=True, index=True, comment="用户名，唯一")
    password_hash = Column(String(255), nullable=False, comment="密码哈希值")
    full_name = Column(String(255), comment="用户全名")
    role = Column(String(50), comment="用户角色")
    created_at = Column(DateTime, default=func.now(), comment="创建时间") 