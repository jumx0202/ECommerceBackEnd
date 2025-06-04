from typing import Any, List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import schemas
from app.api import deps
from app.models.product import Product
from app.models.user import User
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=schemas.APIResponse[schemas.Product])
async def read_products(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str = Query(default=""),
    category: Optional[int] = Query(default=None),
    status: Optional[str] = Query(default=None),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取产品列表，支持分页和过滤
    """
    # 记录请求信息
    query_params = dict(request.query_params)
    logger.debug(f"请求参数: {query_params}")
    
    query = db.query(Product)
    
    # 应用过滤条件
    if name:
        query = query.filter(Product.product_name.ilike(f"%{name}%"))
    if category is not None:
        query = query.filter(Product.category_id == category)
    if status:
        logger.debug(f"状态过滤条件: {status}")
        if status in ["active", "inactive"]:
            query = query.filter(Product.status == status)
        else:
            logger.warning(f"无效的状态值: {status}")
    
    # 获取总数
    total = query.count()
    logger.debug(f"查询到的总记录数: {total}")
    
    # 应用分页
    products = query.offset(skip).limit(limit).all()
    logger.debug(f"返回的记录数: {len(products)}")
    
    # 记录返回的数据结构
    for product in products:
        logger.debug(f"产品数据: id={product.product_id}, name={product.product_name}, status={product.status}")
    
    return {
        "data": products,
        "total": total,
        "message": "获取产品列表成功"
    }

@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新产品
    """
    # 检查SKU是否已存在
    product = db.query(Product).filter(Product.sku == product_in.sku).first()
    if product:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    product = Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定产品
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: schemas.ProductUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新产品信息
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 如果更新SKU，检查新SKU是否已存在
    if product_in.sku and product_in.sku != product.sku:
        existing = db.query(Product).filter(Product.sku == product_in.sku).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already exists")
    
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除产品
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"} 