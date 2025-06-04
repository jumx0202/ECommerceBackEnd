from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas
from app.api import deps
from app.models.synced_order import SyncedChannelOrder
from app.models.order_sync_log import OrderSyncLog
from app.models.user import User

router = APIRouter()

@router.get("/orders", response_model=List[dict])
def read_synced_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取已同步的渠道订单列表
    """
    orders = db.query(SyncedChannelOrder).offset(skip).limit(limit).all()
    return [{"synced_order_id": o.synced_order_id, 
             "external_channel_code": o.external_channel_code,
             "order_status_external": o.order_status_external,
             "sync_timestamp": o.sync_timestamp} for o in orders]

@router.get("/logs", response_model=List[dict])
def read_sync_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取订单同步日志
    """
    logs = db.query(OrderSyncLog).offset(skip).limit(limit).all()
    return [{"log_id": l.log_id,
             "synced_order_id": l.synced_order_id,
             "sync_status": l.sync_status,
             "sync_time": l.sync_time,
             "message": l.message} for l in logs]

@router.post("/sync/{channel_code}")
def sync_channel_orders(
    channel_code: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    触发指定渠道的订单同步
    """
    # 这里应该调用实际的渠道API进行同步
    # 这是一个模拟的实现
    return {"message": f"Started syncing orders from channel {channel_code}",
            "status": "processing"} 