from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.user import User
from app.models.sales_order import SalesOrder
from app.models.product import Product
from app.models.inventory import Inventory, InventoryAlert
from app.models.supplier import Supplier

router = APIRouter()

@router.get("/statistics", response_model=Dict[str, Any])
def get_statistics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取系统统计数据
    """
    # 订单统计
    total_orders = db.query(func.count(SalesOrder.order_id)).scalar()
    total_revenue = db.query(func.sum(SalesOrder.order_amount)).scalar() or 0
    
    # 产品统计
    total_products = db.query(func.count(Product.product_id)).scalar()
    
    # 用户统计
    total_users = db.query(func.count(User.user_id)).scalar()
    
    # 库存统计
    total_inventory_value = db.query(
        func.sum(Inventory.current_stock_quantity * Product.unit_price)
    ).join(Product).scalar() or 0
    
    # 预警统计
    active_alerts = db.query(func.count(InventoryAlert.alert_id)).filter(
        InventoryAlert.alert_status.in_(["未发送", "已发送", "处理中", "待处理", "处理中"])
    ).scalar()
    
    # 供应商统计
    active_suppliers = db.query(func.count(Supplier.supplier_id)).filter(
        Supplier.cooperation_status == "合作中"
    ).scalar()
    
    # 订单状态分布
    order_status_distribution = db.query(
        SalesOrder.order_status,
        func.count(SalesOrder.order_id)
    ).group_by(SalesOrder.order_status).all()
    
    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "total_products": total_products,
        "total_users": total_users,
        "total_inventory_value": float(total_inventory_value),
        "active_alerts": active_alerts,
        "active_suppliers": active_suppliers,
        "order_status_distribution": {
            status: count for status, count in order_status_distribution
        }
    }

@router.get("/charts/sales-trend")
def get_sales_trend(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取销售趋势数据
    """
    # 按日期统计销售额
    sales_by_date = db.query(
        func.date(SalesOrder.order_date).label("date"),
        func.sum(SalesOrder.order_amount).label("amount")
    ).group_by(func.date(SalesOrder.order_date)).order_by("date").all()
    
    return {
        "dates": [str(row.date) for row in sales_by_date],
        "amounts": [float(row.amount) for row in sales_by_date]
    }

@router.get("/charts/channel-distribution")
def get_channel_distribution(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取渠道销售分布数据
    """
    from app.models.sales_channel import SalesChannel
    
    channel_sales = db.query(
        SalesChannel.channel_name,
        func.sum(SalesOrder.order_amount).label("amount")
    ).join(SalesOrder).group_by(SalesChannel.channel_id).all()
    
    return {
        "channels": [row.channel_name for row in channel_sales],
        "amounts": [float(row.amount) for row in channel_sales]
    }

@router.get("/inventory/alerts")
def get_inventory_alerts(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取库存预警数据用于图表显示
    """
    # 获取所有有预警的库存信息
    alerts_query = db.query(
        Inventory.inventory_id,
        Inventory.current_stock_quantity,
        Inventory.alert_threshold,
        Product.product_name
    ).join(Product).filter(
        Inventory.current_stock_quantity < Inventory.alert_threshold
    ).all()
    
    product_names = []
    current_stocks = []
    alert_thresholds = []
    
    for alert in alerts_query:
        product_names.append(alert.product_name)
        current_stocks.append(alert.current_stock_quantity)
        alert_thresholds.append(alert.alert_threshold)
    
    return {
        "product_names": product_names,
        "current_stocks": current_stocks,
        "alert_thresholds": alert_thresholds
    }

@router.get("/recent-orders")
def get_recent_orders(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    limit: int = 10
) -> Any:
    """
    获取最近订单数据
    """
    from app.models.sales_channel import SalesChannel
    
    recent_orders = db.query(
        SalesOrder.order_id,
        SalesOrder.customer_user_id,
        SalesOrder.order_amount,
        SalesOrder.order_status,
        SalesOrder.order_date,
        SalesChannel.channel_name
    ).join(SalesChannel).order_by(
        SalesOrder.order_date.desc()
    ).limit(limit).all()
    
    orders_data = []
    for order in recent_orders:
        orders_data.append({
            "order_id": order.order_id,
            "customer_id": order.customer_user_id,
            "channel": order.channel_name,
            "amount": float(order.order_amount),
            "status": order.order_status,
            "order_date": order.order_date.isoformat() if order.order_date else None
        })
    
    return orders_data 