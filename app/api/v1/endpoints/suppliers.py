from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.models.supplier import Supplier
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[schemas.Supplier])
def read_suppliers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取供应商列表
    """
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers

@router.post("/", response_model=schemas.Supplier)
def create_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_in: schemas.SupplierCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新供应商
    """
    # 检查供应商ID是否已存在
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_in.supplier_id).first()
    if supplier:
        raise HTTPException(status_code=400, detail="Supplier ID already exists")
    
    supplier = Supplier(**supplier_in.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.get("/{supplier_id}", response_model=schemas.Supplier)
def read_supplier(
    supplier_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定供应商信息
    """
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_id: str,
    supplier_in: schemas.SupplierUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新供应商信息
    """
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = supplier_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/{supplier_id}")
def delete_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_id: str,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除供应商
    """
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"} 