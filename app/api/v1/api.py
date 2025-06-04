from fastapi import APIRouter
from app.api.v1.endpoints import (
    login,
    users,
    sales_channels,
    products,
    sales_orders,
    inventory,
    suppliers,
    logistics,
    order_sync,
    communication,
    dashboard
)

api_router = APIRouter()

# 认证相关
api_router.include_router(login.router, tags=["认证"])

# 用户管理
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])

# 多渠道销售管理
api_router.include_router(sales_channels.router, prefix="/sales-channels", tags=["销售渠道"])
api_router.include_router(sales_orders.router, prefix="/sales-orders", tags=["销售订单"])

# 产品管理
api_router.include_router(products.router, prefix="/products", tags=["产品管理"])

# 库存管理
api_router.include_router(inventory.router, prefix="/inventory", tags=["库存管理"])

# 供应链协同
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["供应商管理"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["物流协同"])

# 订单同步处理
api_router.include_router(order_sync.router, prefix="/order-sync", tags=["订单同步"])

# 通信
api_router.include_router(communication.router, prefix="/communication", tags=["通信"])

# 数据统计与分析
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["数据统计"]) 