#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试数据插入脚本
为电商系统插入测试数据以展示仪表板功能
"""

from datetime import datetime, timedelta
import random
from decimal import Decimal
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.sales_channel import SalesChannel
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.inventory import Inventory, InventoryAlert
from app.models.sales_order import SalesOrder, SalesOrderItem
from app.core.security import get_password_hash

def insert_test_data():
    """插入测试数据"""
    db = SessionLocal()
    
    try:
        print("开始插入测试数据...")
        
        # 1. 插入销售渠道
        print("插入销售渠道数据...")
        channels = [
            SalesChannel(channel_id=1, channel_name="京东", channel_code="JD", created_at=datetime.now()),
            SalesChannel(channel_id=2, channel_name="淘宝", channel_code="TB", created_at=datetime.now()),
            SalesChannel(channel_id=3, channel_name="天猫", channel_code="TM", created_at=datetime.now()),
            SalesChannel(channel_id=4, channel_name="拼多多", channel_code="PDD", created_at=datetime.now()),
            SalesChannel(channel_id=5, channel_name="抖音小店", channel_code="DY", created_at=datetime.now()),
        ]
        
        for channel in channels:
            existing = db.query(SalesChannel).filter(SalesChannel.channel_id == channel.channel_id).first()
            if not existing:
                db.add(channel)
        
        # 2. 插入供应商数据
        print("插入供应商数据...")
        suppliers = [
            Supplier(
                supplier_id="SUP001",
                supplier_name="深圳科技有限公司",
                contact_info="13800138001",
                cooperation_status="合作中",
                address="深圳市南山区科技园",
                email="supplier1@example.com",
                created_at=datetime.now()
            ),
            Supplier(
                supplier_id="SUP002", 
                supplier_name="广州电子制造厂",
                contact_info="13800138002",
                cooperation_status="合作中",
                address="广州市天河区工业园",
                email="supplier2@example.com",
                created_at=datetime.now()
            ),
            Supplier(
                supplier_id="SUP003",
                supplier_name="上海智能设备公司",
                contact_info="13800138003", 
                cooperation_status="合作中",
                address="上海市浦东新区张江高科",
                email="supplier3@example.com",
                created_at=datetime.now()
            ),
        ]
        
        for supplier in suppliers:
            existing = db.query(Supplier).filter(Supplier.supplier_id == supplier.supplier_id).first()
            if not existing:
                db.add(supplier)
        
        # 3. 插入产品数据
        print("插入产品数据...")
        products = [
            Product(
                product_id=1001,
                product_name="iPhone 15 Pro",
                sku="IP15P-128",
                description="苹果手机 128GB",
                unit_price=Decimal("7999.00"),
                category_id=1,
                status="active",
                supplier_id="SUP001"
            ),
            Product(
                product_id=1002,
                product_name="MacBook Air M2",
                sku="MBA-M2-256",
                description="苹果笔记本 256GB",
                unit_price=Decimal("8999.00"),
                category_id=1,
                status="active",
                supplier_id="SUP001"
            ),
            Product(
                product_id=1003,
                product_name="AirPods Pro",
                sku="APP-2023",
                description="苹果无线耳机",
                unit_price=Decimal("1899.00"),
                category_id=1,
                status="active",
                supplier_id="SUP001"
            ),
            Product(
                product_id=1004,
                product_name="小米13 Ultra",
                sku="MI13U-512",
                description="小米手机 512GB",
                unit_price=Decimal("5999.00"),
                category_id=1,
                status="active",
                supplier_id="SUP002"
            ),
            Product(
                product_id=1005,
                product_name="小米平板6",
                sku="MIPD6-256",
                description="小米平板 256GB",
                unit_price=Decimal("2299.00"),
                category_id=1,
                status="active",
                supplier_id="SUP002"
            ),
            Product(
                product_id=1006,
                product_name="华为MatePad Pro",
                sku="HWMPD-256",
                description="华为平板 256GB",
                unit_price=Decimal("3999.00"),
                category_id=1,
                status="active",
                supplier_id="SUP003"
            ),
            Product(
                product_id=1007,
                product_name="华为Watch GT4",
                sku="HWWGT4",
                description="华为智能手表",
                unit_price=Decimal("1588.00"),
                category_id=1,
                status="active",
                supplier_id="SUP003"
            ),
            Product(
                product_id=1008,
                product_name="戴森V15吸尘器",
                sku="DYV15",
                description="戴森无线吸尘器",
                unit_price=Decimal("4490.00"),
                category_id=3,
                status="active",
                supplier_id="SUP001"
            ),
        ]
        
        for product in products:
            existing = db.query(Product).filter(Product.product_id == product.product_id).first()
            if not existing:
                db.add(product)
        
        # 4. 插入库存数据
        print("插入库存数据...")
        inventories = [
            Inventory(inventory_id=1, product_id=1001, current_stock_quantity=150, alert_threshold=20, last_updated_at=datetime.now()),
            Inventory(inventory_id=2, product_id=1002, current_stock_quantity=80, alert_threshold=15, last_updated_at=datetime.now()),
            Inventory(inventory_id=3, product_id=1003, current_stock_quantity=200, alert_threshold=30, last_updated_at=datetime.now()),
            Inventory(inventory_id=4, product_id=1004, current_stock_quantity=120, alert_threshold=25, last_updated_at=datetime.now()),
            Inventory(inventory_id=5, product_id=1005, current_stock_quantity=15, alert_threshold=20, last_updated_at=datetime.now()),  # 库存预警
            Inventory(inventory_id=6, product_id=1006, current_stock_quantity=45, alert_threshold=10, last_updated_at=datetime.now()),
            Inventory(inventory_id=7, product_id=1007, current_stock_quantity=8, alert_threshold=15, last_updated_at=datetime.now()),   # 库存预警
            Inventory(inventory_id=8, product_id=1008, current_stock_quantity=25, alert_threshold=5, last_updated_at=datetime.now()),
        ]
        
        for inventory in inventories:
            existing = db.query(Inventory).filter(Inventory.inventory_id == inventory.inventory_id).first()
            if not existing:
                db.add(inventory)
        
        # 5. 插入库存预警
        print("插入库存预警数据...")
        alerts = [
            InventoryAlert(alert_id=1, inventory_id=5, alert_time=datetime.now(), alert_status="待处理", handler_name="张三"),
            InventoryAlert(alert_id=2, inventory_id=7, alert_time=datetime.now(), alert_status="处理中", handler_name="李四"),
        ]
        
        for alert in alerts:
            existing = db.query(InventoryAlert).filter(InventoryAlert.alert_id == alert.alert_id).first()
            if not existing:
                db.add(alert)
        
        # 6. 插入用户数据
        print("插入用户数据...")
        users = [
            User(username="zhangsan", password_hash=get_password_hash("123456"), full_name="张三", role="operator"),
            User(username="lisi", password_hash=get_password_hash("123456"), full_name="李四", role="operator"),
            User(username="wangwu", password_hash=get_password_hash("123456"), full_name="王五", role="manager"),
            User(username="zhaoliu", password_hash=get_password_hash("123456"), full_name="赵六", role="operator"),
        ]
        
        for user in users:
            existing = db.query(User).filter(User.username == user.username).first()
            if not existing:
                db.add(user)
        
        db.commit()  # 提交前面的数据
        
        # 7. 插入销售订单数据（需要在产品和渠道数据提交后）
        print("插入销售订单数据...")
        
        # 生成最近30天的订单数据
        base_date = datetime.now() - timedelta(days=30)
        order_statuses = ["待支付", "已支付", "已发货", "已完成", "已取消"]
        customer_ids = [f"CUST{i:04d}" for i in range(1, 21)]  # 20个客户
        
        order_id = 10001
        
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            # 每天生成3-8个订单
            daily_orders = random.randint(3, 8)
            
            for _ in range(daily_orders):
                channel_id = random.choice([1, 2, 3, 4, 5])
                customer_id = random.choice(customer_ids)
                status = random.choice(order_statuses)
                
                # 计算订单金额（根据订单项计算）
                order_amount = Decimal("0.00")
                
                order = SalesOrder(
                    order_id=order_id,
                    customer_user_id=customer_id,
                    channel_id=channel_id,
                    order_amount=order_amount,  # 先设为0，后面会更新
                    order_status=status,
                    order_date=current_date,
                    created_at=current_date,
                    updated_at=current_date
                )
                
                db.add(order)
                db.flush()  # 获取order_id
                
                # 为每个订单添加1-3个商品
                item_count = random.randint(1, 3)
                total_amount = Decimal("0.00")
                
                for item_idx in range(item_count):
                    product_id = random.choice([1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008])
                    quantity = random.randint(1, 3)
                    
                    # 获取产品价格
                    product = db.query(Product).filter(Product.product_id == product_id).first()
                    unit_price = product.unit_price
                    total_price = unit_price * quantity
                    total_amount += total_price
                    
                    order_item = SalesOrderItem(
                        order_id=order_id,
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price
                    )
                    
                    db.add(order_item)
                
                # 更新订单总金额
                order.order_amount = total_amount
                order_id += 1
        
        db.commit()
        print("测试数据插入完成！")
        
        # 输出统计信息
        print("\n数据统计:")
        print(f"销售渠道: {db.query(SalesChannel).count()} 个")
        print(f"供应商: {db.query(Supplier).count()} 个")
        print(f"产品: {db.query(Product).count()} 个")
        print(f"库存记录: {db.query(Inventory).count()} 个")
        print(f"用户: {db.query(User).count()} 个")
        print(f"销售订单: {db.query(SalesOrder).count()} 个")
        print(f"订单项: {db.query(SalesOrderItem).count()} 个")
        print(f"库存预警: {db.query(InventoryAlert).count()} 个")
        
        total_revenue = db.query(SalesOrder).filter(SalesOrder.order_status.in_(["已支付", "已发货", "已完成"])).all()
        revenue = sum([order.order_amount for order in total_revenue])
        print(f"总营收: ¥{revenue:,.2f}")
        
    except Exception as e:
        print(f"插入数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data() 