from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Contact(Base):
    __tablename__ = "Contacts"
    
    contact_id = Column(Integer, primary_key=True, autoincrement=True, comment="联系人ID，主键")
    name = Column(String(100), nullable=False, comment="联系人姓名")
    role = Column(String(50), nullable=False, comment="角色（admin/channel/supplier/customer）")
    contact_info = Column(String(255), nullable=False, comment="联系方式（手机号/邮箱等）")
    avatar_url = Column(String(500), comment="头像URL")
    status = Column(String(20), default='offline', comment="在线状态（online/offline/busy）")
    remark = Column(Text, comment="备注信息")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    sent_messages = relationship("CommunicationMessage", foreign_keys="CommunicationMessage.sender_id", back_populates="sender")
    received_messages = relationship("CommunicationMessage", foreign_keys="CommunicationMessage.receiver_id", back_populates="receiver")

class CommunicationMessage(Base):
    __tablename__ = "CommunicationMessages"
    
    message_id = Column(Integer, primary_key=True, autoincrement=True, comment="消息ID，主键")
    sender_id = Column(Integer, ForeignKey("Contacts.contact_id"), nullable=False, comment="发送方ID")
    receiver_id = Column(Integer, ForeignKey("Contacts.contact_id"), nullable=False, comment="接收方ID")
    message_content = Column(Text, nullable=False, comment="消息内容")
    message_type = Column(String(20), default='text', comment="消息类型（text/file/image）")
    file_url = Column(String(500), comment="文件URL（当消息类型为file/image时）")
    file_name = Column(String(255), comment="文件名（当消息类型为file时）")
    is_read = Column(Boolean, default=False, comment="是否已读")
    sent_at = Column(DateTime, default=func.now(), comment="发送时间")
    read_at = Column(DateTime, comment="阅读时间")
    status = Column(String(20), default='sent', comment="消息状态（sent/delivered/read）")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关系
    sender = relationship("Contact", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("Contact", foreign_keys=[receiver_id], back_populates="received_messages")

class MessageTemplate(Base):
    __tablename__ = "MessageTemplates"
    
    template_id = Column(Integer, primary_key=True, autoincrement=True, comment="模板ID，主键")
    title = Column(String(100), nullable=False, comment="模板标题")
    content = Column(Text, nullable=False, comment="模板内容")
    category = Column(String(50), comment="模板分类")
    usage_count = Column(Integer, default=0, comment="使用次数")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_by = Column(Integer, ForeignKey("Contacts.contact_id"), comment="创建者")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

class QuickReply(Base):
    __tablename__ = "QuickReplies"
    
    reply_id = Column(Integer, primary_key=True, autoincrement=True, comment="快捷回复ID，主键")
    text = Column(String(500), nullable=False, comment="回复文本")
    sort_order = Column(Integer, default=0, comment="排序")
    usage_count = Column(Integer, default=0, comment="使用次数")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间") 