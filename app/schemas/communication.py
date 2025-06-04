from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# 联系人基础模式
class ContactBase(BaseModel):
    name: str
    role: str  # admin/channel/supplier/customer
    contact_info: str
    avatar_url: Optional[str] = None
    status: Optional[str] = 'offline'  # online/offline/busy
    remark: Optional[str] = None
    is_active: Optional[bool] = True

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    contact_info: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None
    is_active: Optional[bool] = None

class Contact(ContactBase):
    contact_id: int
    created_at: datetime
    updated_at: datetime
    unread_count: Optional[int] = 0

    class Config:
        from_attributes = True

# 消息基础模式
class MessageBase(BaseModel):
    receiver_id: int
    message_content: str
    message_type: Optional[str] = 'text'  # text/file/image
    file_url: Optional[str] = None
    file_name: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    is_read: Optional[bool] = None
    status: Optional[str] = None

class Message(MessageBase):
    message_id: int
    sender_id: int
    is_read: bool
    sent_at: datetime
    read_at: Optional[datetime] = None
    status: str
    created_at: datetime
    sender_name: Optional[str] = None
    sender_avatar: Optional[str] = None
    receiver_name: Optional[str] = None

    class Config:
        from_attributes = True

# 消息模板基础模式
class MessageTemplateBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    is_active: Optional[bool] = True

class MessageTemplateCreate(MessageTemplateBase):
    created_by: Optional[int] = None

class MessageTemplateUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class MessageTemplate(MessageTemplateBase):
    template_id: int
    usage_count: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 快捷回复基础模式
class QuickReplyBase(BaseModel):
    text: str
    sort_order: Optional[int] = 0
    is_active: Optional[bool] = True

class QuickReplyCreate(QuickReplyBase):
    pass

class QuickReplyUpdate(BaseModel):
    text: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None

class QuickReply(QuickReplyBase):
    reply_id: int
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 聊天会话
class ChatSession(BaseModel):
    contact: Contact
    messages: List[Message]
    unread_count: int

# 联系人列表响应
class ContactListResponse(BaseModel):
    contacts: List[Contact]
    total: int 