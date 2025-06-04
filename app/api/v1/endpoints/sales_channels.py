from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.models.sales_channel import SalesChannel
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_sales_channels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取销售渠道列表
    """
    channels = db.query(SalesChannel).offset(skip).limit(limit).all()
    
    # 直接从数据库字段读取数据
    result = []
    for channel in channels:
        result.append({
            "channel_id": channel.channel_id,
            "channel_name": channel.channel_name,
            "channel_code": channel.channel_code,
            "platform_type": channel.platform_type or "其他",
            "api_address": channel.api_address or "",
            "commission_rate": channel.commission_rate or 0.0,
            "channel_status": channel.channel_status or "active",
            "description": channel.description or "",
            "createTime": channel.created_at.strftime("%Y-%m-%d %H:%M:%S") if channel.created_at else "",
            "updateTime": channel.updated_at.strftime("%Y-%m-%d %H:%M:%S") if channel.updated_at else ""
        })
    
    return result

@router.post("/", response_model=schemas.SalesChannel)
def create_sales_channel(
    *,
    db: Session = Depends(deps.get_db),
    channel_in: schemas.SalesChannelCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新的销售渠道
    """
    # 检查渠道ID是否已存在
    channel = db.query(SalesChannel).filter(SalesChannel.channel_id == channel_in.channel_id).first()
    if channel:
        raise HTTPException(status_code=400, detail="Channel ID already exists")
    
    # 检查渠道名称是否已存在
    channel = db.query(SalesChannel).filter(SalesChannel.channel_name == channel_in.channel_name).first()
    if channel:
        raise HTTPException(status_code=400, detail="Channel name already exists")
    
    channel = SalesChannel(**channel_in.dict())
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

@router.get("/{channel_id}", response_model=schemas.SalesChannel)
def read_sales_channel(
    channel_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定的销售渠道
    """
    channel = db.query(SalesChannel).filter(SalesChannel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.put("/{channel_id}", response_model=schemas.SalesChannel)
def update_sales_channel(
    *,
    db: Session = Depends(deps.get_db),
    channel_id: int,
    channel_in: schemas.SalesChannelUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新销售渠道
    """
    channel = db.query(SalesChannel).filter(SalesChannel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    update_data = channel_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(channel, field, value)
    
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

@router.delete("/{channel_id}")
def delete_sales_channel(
    *,
    db: Session = Depends(deps.get_db),
    channel_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除销售渠道
    """
    channel = db.query(SalesChannel).filter(SalesChannel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    db.delete(channel)
    db.commit()
    return {"message": "Channel deleted successfully"} 