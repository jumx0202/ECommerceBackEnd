from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas
from app.api import deps
from app.models.inventory import Inventory, InventoryAlert
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=schemas.APIResponse[schemas.Inventory])
def read_inventory(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取库存信息列表
    """
    total = db.query(Inventory).count()
    inventory = db.query(Inventory).offset(skip).limit(limit).all()
    return {
        "data": inventory,
        "total": total,
        "message": "获取库存信息成功"
    }

@router.post("/", response_model=schemas.Inventory)
def create_inventory(
    *,
    db: Session = Depends(deps.get_db),
    inventory_in: schemas.InventoryCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建库存记录
    """
    # 检查库存ID是否已存在
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_in.inventory_id).first()
    if inventory:
        raise HTTPException(status_code=400, detail="Inventory ID already exists")
    
    # 检查产品是否已有库存记录
    inventory = db.query(Inventory).filter(Inventory.product_id == inventory_in.product_id).first()
    if inventory:
        raise HTTPException(status_code=400, detail="Product already has inventory record")
    
    inventory = Inventory(**inventory_in.dict())
    db.add(inventory)
    
    # 如果库存低于预警值，创建预警记录
    if inventory.current_stock_quantity < inventory.alert_threshold:
        alert = InventoryAlert(
            alert_id=int(datetime.now().timestamp()),  # 简单的ID生成
            inventory_id=inventory.inventory_id,
            alert_time=datetime.now(),
            alert_status="未发送"
        )
        db.add(alert)
    
    db.commit()
    db.refresh(inventory)
    return inventory

@router.get("/{inventory_id}", response_model=schemas.Inventory)
def read_inventory_by_id(
    inventory_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定库存信息
    """
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@router.put("/{inventory_id}", response_model=schemas.Inventory)
def update_inventory(
    *,
    db: Session = Depends(deps.get_db),
    inventory_id: int,
    inventory_in: schemas.InventoryUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新库存信息
    """
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    update_data = inventory_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(inventory, field, value)
    
    inventory.last_updated_at = datetime.now()
    
    # 检查是否需要创建预警
    if inventory.current_stock_quantity < inventory.alert_threshold:
        # 检查是否已有未处理的预警
        existing_alert = db.query(InventoryAlert).filter(
            InventoryAlert.inventory_id == inventory_id,
            InventoryAlert.alert_status.in_(["未发送", "已发送", "处理中"])
        ).first()
        
        if not existing_alert:
            alert = InventoryAlert(
                alert_id=int(datetime.now().timestamp()),
                inventory_id=inventory.inventory_id,
                alert_time=datetime.now(),
                alert_status="未发送"
            )
            db.add(alert)
    
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

@router.get("/alerts/", response_model=List[schemas.InventoryAlert])
def read_inventory_alerts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取库存预警记录列表
    """
    alerts = db.query(InventoryAlert).offset(skip).limit(limit).all()
    return alerts

@router.post("/alerts/", response_model=schemas.InventoryAlert)
def create_inventory_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_in: schemas.InventoryAlertCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建库存预警记录
    """
    alert = InventoryAlert(**alert_in.dict())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.put("/alerts/{alert_id}", response_model=schemas.InventoryAlert)
def update_inventory_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_id: int,
    alert_status: str,
    handler_name: str = None,
    notes: str = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新库存预警状态
    """
    alert = db.query(InventoryAlert).filter(InventoryAlert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.alert_status = alert_status
    if handler_name:
        alert.handler_name = handler_name
    if notes:
        alert.notes = notes
    if alert_status in ["已解决", "已处理"]:
        alert.resolved_at = datetime.now()
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert 