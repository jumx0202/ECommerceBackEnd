from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.models.sales_order import SalesOrder, SalesOrderItem
from app.models.sales_channel import SalesChannel
from app.models.product import Product
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_sales_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取销售订单列表
    """
    # JOIN查询以获取渠道名称
    orders_with_channels = db.query(
        SalesOrder,
        SalesChannel.channel_name
    ).join(
        SalesChannel, SalesOrder.channel_id == SalesChannel.channel_id
    ).offset(skip).limit(limit).all()
    
    # 转换为字典格式
    result = []
    for order, channel_name in orders_with_channels:
        result.append({
            "order_id": order.order_id,
            "customer_user_id": order.customer_user_id,
            "channel_id": order.channel_id,
            "channel_name": channel_name,
            "order_amount": float(order.order_amount),
            "order_status": order.order_status,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "updated_at": order.updated_at.isoformat() if order.updated_at else None
        })
    
    return result

@router.post("/", response_model=schemas.SalesOrder)
def create_sales_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.SalesOrderCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新的销售订单
    """
    # 检查订单ID是否已存在
    order = db.query(SalesOrder).filter(SalesOrder.order_id == order_in.order_id).first()
    if order:
        raise HTTPException(status_code=400, detail="Order ID already exists")
    
    # 创建订单
    order_data = order_in.dict(exclude={"order_items"})
    order = SalesOrder(**order_data)
    db.add(order)
    db.flush()
    
    # 创建订单项
    for item_data in order_in.order_items:
        item = SalesOrderItem(order_id=order.order_id, **item_data.dict())
        db.add(item)
    
    db.commit()
    db.refresh(order)
    return order

@router.get("/{order_id}", response_model=dict)
def read_sales_order(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定的销售订单（包含订单项和产品信息）
    """
    # 获取订单基本信息
    order_with_channel = db.query(
        SalesOrder,
        SalesChannel.channel_name
    ).join(
        SalesChannel, SalesOrder.channel_id == SalesChannel.channel_id
    ).filter(SalesOrder.order_id == order_id).first()
    
    if not order_with_channel:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order, channel_name = order_with_channel
    
    # 获取订单项信息（包含产品信息）
    order_items_with_products = db.query(
        SalesOrderItem,
        Product.product_name
    ).join(
        Product, SalesOrderItem.product_id == Product.product_id
    ).filter(SalesOrderItem.order_id == order_id).all()
    
    # 构造订单项列表
    items = []
    for item, product_name in order_items_with_products:
        items.append({
            "order_item_id": item.order_item_id,
            "product_id": item.product_id,
            "product_name": product_name,
            "quantity": item.quantity,
            "unit_price": float(item.unit_price),
            "total_price": float(item.total_price)
        })
    
    # 返回完整订单信息
    return {
        "order_id": order.order_id,
        "customer_user_id": order.customer_user_id,
        "channel_id": order.channel_id,
        "channel_name": channel_name,
        "order_amount": float(order.order_amount),
        "order_status": order.order_status,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "updated_at": order.updated_at.isoformat() if order.updated_at else None,
        "order_items": items
    }

@router.put("/{order_id}", response_model=schemas.SalesOrder)
def update_sales_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    order_in: schemas.SalesOrderUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新销售订单（主要更新状态）
    """
    order = db.query(SalesOrder).filter(SalesOrder.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = order_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}")
def delete_sales_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除销售订单
    """
    order = db.query(SalesOrder).filter(SalesOrder.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@router.get("/{order_id}/items", response_model=List[schemas.SalesOrderItem])
def read_order_items(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取订单的商品项列表
    """
    items = db.query(SalesOrderItem).filter(SalesOrderItem.order_id == order_id).all()
    return items 