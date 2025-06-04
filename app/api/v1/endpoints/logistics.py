from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.models.logistics import LogisticsInformation
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[schemas.LogisticsInformation])
def read_logistics(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取物流信息列表
    """
    logistics = db.query(LogisticsInformation).offset(skip).limit(limit).all()
    return logistics

@router.post("/", response_model=schemas.LogisticsInformation)
def create_logistics(
    *,
    db: Session = Depends(deps.get_db),
    logistics_in: schemas.LogisticsInformationCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建物流信息
    """
    # 检查物流ID是否已存在
    logistics = db.query(LogisticsInformation).filter(
        LogisticsInformation.logistics_id == logistics_in.logistics_id
    ).first()
    if logistics:
        raise HTTPException(status_code=400, detail="Logistics ID already exists")
    
    logistics = LogisticsInformation(**logistics_in.dict())
    db.add(logistics)
    db.commit()
    db.refresh(logistics)
    return logistics

@router.get("/{logistics_id}", response_model=schemas.LogisticsInformation)
def read_logistics_by_id(
    logistics_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定物流信息
    """
    logistics = db.query(LogisticsInformation).filter(
        LogisticsInformation.logistics_id == logistics_id
    ).first()
    if not logistics:
        raise HTTPException(status_code=404, detail="Logistics information not found")
    return logistics

@router.put("/{logistics_id}", response_model=schemas.LogisticsInformation)
def update_logistics(
    *,
    db: Session = Depends(deps.get_db),
    logistics_id: str,
    logistics_in: schemas.LogisticsInformationUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新物流信息
    """
    logistics = db.query(LogisticsInformation).filter(
        LogisticsInformation.logistics_id == logistics_id
    ).first()
    if not logistics:
        raise HTTPException(status_code=404, detail="Logistics information not found")
    
    update_data = logistics_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(logistics, field, value)
    
    db.add(logistics)
    db.commit()
    db.refresh(logistics)
    return logistics

@router.delete("/{logistics_id}")
def delete_logistics(
    *,
    db: Session = Depends(deps.get_db),
    logistics_id: str,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除物流信息
    """
    logistics = db.query(LogisticsInformation).filter(
        LogisticsInformation.logistics_id == logistics_id
    ).first()
    if not logistics:
        raise HTTPException(status_code=404, detail="Logistics information not found")
    
    db.delete(logistics)
    db.commit()
    return {"message": "Logistics information deleted successfully"} 