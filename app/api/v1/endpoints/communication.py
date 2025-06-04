from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, desc

from app import models, schemas
from app.api import deps
from app.models.user import User
from app.models.communication import Contact, CommunicationMessage, MessageTemplate, QuickReply

router = APIRouter()

@router.get("/contacts", response_model=schemas.communication.ContactListResponse)
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    role: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取联系人列表
    """
    query = db.query(Contact).filter(Contact.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                Contact.name.contains(search),
                Contact.contact_info.contains(search)
            )
        )
    
    if role:
        query = query.filter(Contact.role == role)
    
    if status:
        query = query.filter(Contact.status == status)
    
    # 简化查询，先获取联系人列表，然后单独计算未读消息数
    contacts = query.order_by(Contact.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    # 构造响应数据
    result_contacts = []
    for contact in contacts:
        # 计算每个联系人的未读消息数
        unread_count = db.query(CommunicationMessage).filter(
            and_(
                CommunicationMessage.receiver_id == contact.contact_id,
                CommunicationMessage.is_read == False
            )
        ).count()
        
        contact_dict = {
            "contact_id": contact.contact_id,
            "name": contact.name,
            "role": contact.role,
            "contact_info": contact.contact_info,
            "avatar_url": contact.avatar_url,
            "status": contact.status,
            "remark": contact.remark,
            "is_active": contact.is_active,
            "created_at": contact.created_at,
            "updated_at": contact.updated_at,
            "unread_count": unread_count
        }
        result_contacts.append(schemas.communication.Contact(**contact_dict))
    
    return {"contacts": result_contacts, "total": total}

@router.post("/contacts", response_model=schemas.communication.Contact)
def create_contact(
    contact_in: schemas.communication.ContactCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新联系人
    """
    # 检查联系人是否已存在
    existing_contact = db.query(Contact).filter(
        or_(
            Contact.name == contact_in.name,
            Contact.contact_info == contact_in.contact_info
        )
    ).first()
    
    if existing_contact:
        raise HTTPException(
            status_code=400,
            detail="联系人已存在"
        )
    
    contact = Contact(**contact_in.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    # 添加未读消息数
    contact_dict = {
        **contact.__dict__,
        "unread_count": 0
    }
    
    return schemas.communication.Contact(**contact_dict)

@router.put("/contacts/{contact_id}", response_model=schemas.communication.Contact)
def update_contact(
    contact_id: int,
    contact_in: schemas.communication.ContactUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新联系人信息
    """
    contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    
    update_data = contact_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    
    # 计算未读消息数
    unread_count = db.query(CommunicationMessage).filter(
        and_(
            CommunicationMessage.receiver_id == contact_id,
            CommunicationMessage.is_read == False
        )
    ).count()
    
    contact_dict = {
        **contact.__dict__,
        "unread_count": unread_count
    }
    
    return schemas.communication.Contact(**contact_dict)

@router.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    删除联系人（软删除）
    """
    contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    
    contact.is_active = False
    db.commit()
    
    return {"message": "联系人已删除"}

@router.get("/messages/{contact_id}", response_model=List[schemas.communication.Message])
def read_messages(
    contact_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取与指定联系人的聊天记录
    """
    # 这里需要确定当前用户的联系人ID，简化处理，假设当前用户ID为1
    current_contact_id = 1  # 实际应该从用户信息中获取
    
    messages = (
        db.query(CommunicationMessage)
        .filter(
            or_(
                and_(
                    CommunicationMessage.sender_id == current_contact_id,
                    CommunicationMessage.receiver_id == contact_id
                ),
                and_(
                    CommunicationMessage.sender_id == contact_id,
                    CommunicationMessage.receiver_id == current_contact_id
                )
            )
        )
        .order_by(CommunicationMessage.sent_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # 获取发送者和接收者信息
    result = []
    for message in messages:
        sender = db.query(Contact).filter(Contact.contact_id == message.sender_id).first()
        receiver = db.query(Contact).filter(Contact.contact_id == message.receiver_id).first()
        
        message_dict = {
            **message.__dict__,
            "sender_name": sender.name if sender else "未知用户",
            "sender_avatar": sender.avatar_url if sender else None,
            "receiver_name": receiver.name if receiver else "未知用户"
        }
        result.append(schemas.communication.Message(**message_dict))
    
    # 标记消息为已读
    db.query(CommunicationMessage).filter(
        and_(
            CommunicationMessage.sender_id == contact_id,
            CommunicationMessage.receiver_id == current_contact_id,
            CommunicationMessage.is_read == False
        )
    ).update({"is_read": True, "read_at": func.now()})
    db.commit()
    
    return result

@router.post("/messages", response_model=schemas.communication.Message)
def send_message(
    message_in: schemas.communication.MessageCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    发送消息
    """
    # 这里需要确定当前用户的联系人ID，简化处理，假设当前用户ID为1
    current_contact_id = 1  # 实际应该从用户信息中获取
    
    # 检查接收方是否存在
    receiver = db.query(Contact).filter(
        and_(
            Contact.contact_id == message_in.receiver_id,
            Contact.is_active == True
        )
    ).first()
    
    if not receiver:
        raise HTTPException(status_code=404, detail="接收方不存在")
    
    message = CommunicationMessage(
        sender_id=current_contact_id,
        **message_in.dict()
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # 获取发送者信息
    sender = db.query(Contact).filter(Contact.contact_id == current_contact_id).first()
    
    message_dict = {
        **message.__dict__,
        "sender_name": sender.name if sender else "未知用户",
        "sender_avatar": sender.avatar_url if sender else None,
        "receiver_name": receiver.name
    }
    
    return schemas.communication.Message(**message_dict)

@router.get("/templates", response_model=List[schemas.communication.MessageTemplate])
def read_message_templates(
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取消息模板列表
    """
    query = db.query(MessageTemplate).filter(MessageTemplate.is_active == True)
    
    if category:
        query = query.filter(MessageTemplate.category == category)
    
    templates = (
        query
        .order_by(MessageTemplate.usage_count.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return templates

@router.post("/templates", response_model=schemas.communication.MessageTemplate)
def create_message_template(
    template_in: schemas.communication.MessageTemplateCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建消息模板
    """
    template = MessageTemplate(**template_in.dict())
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return template

@router.get("/quick-replies", response_model=List[schemas.communication.QuickReply])
def read_quick_replies(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取快捷回复列表
    """
    quick_replies = (
        db.query(QuickReply)
        .filter(QuickReply.is_active == True)
        .order_by(QuickReply.sort_order.asc(), QuickReply.usage_count.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return quick_replies

@router.post("/quick-replies", response_model=schemas.communication.QuickReply)
def create_quick_reply(
    reply_in: schemas.communication.QuickReplyCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建快捷回复
    """
    quick_reply = QuickReply(**reply_in.dict())
    db.add(quick_reply)
    db.commit()
    db.refresh(quick_reply)
    
    return quick_reply

@router.put("/messages/{message_id}/read")
def mark_message_read(
    message_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    标记消息为已读
    """
    message = db.query(CommunicationMessage).filter(
        CommunicationMessage.message_id == message_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    
    message.is_read = True
    message.read_at = func.now()
    message.status = 'read'
    
    db.commit()
    
    return {"message": "消息已标记为已读"} 