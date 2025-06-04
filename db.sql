use ECommerce;
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID，主键，自增',
    username VARCHAR(255) NOT NULL UNIQUE COMMENT '用户名，唯一',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希值 (安全考虑，不存储明文密码)',
    full_name VARCHAR(255) COMMENT '用户全名 (可用于"处理人"等场景)',
    role VARCHAR(50) COMMENT '用户角色 (例如: admin, operator)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_username (username)
) COMMENT '系统用户表';

CREATE TABLE SalesChannels (
    channel_id INT PRIMARY KEY COMMENT '渠道ID，主键 (根据示例，手动分配)',
    channel_name VARCHAR(255) NOT NULL UNIQUE COMMENT '渠道名称，唯一',
    channel_code VARCHAR(50) UNIQUE COMMENT '渠道代码 (例如: JD, TB，用于系统内部关联)',
    platform_type VARCHAR(50) NOT NULL COMMENT '平台类型：ecommerce/marketplace/social/direct',
    api_address VARCHAR(500) COMMENT 'API地址',
    commission_rate DECIMAL(5, 2) DEFAULT 0.0 COMMENT '佣金率（百分比）',
    channel_status VARCHAR(20) DEFAULT 'active' COMMENT '渠道状态：active/inactive',
    description TEXT COMMENT '渠道描述',
    created_at DATETIME NOT NULL COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_channel_code (channel_code),
    INDEX idx_platform_type (platform_type),
    INDEX idx_channel_status (channel_status)
) COMMENT '销售渠道表';

CREATE TABLE SalesOrders (
    order_id INT PRIMARY KEY COMMENT '订单ID，主键 (根据示例，例如1001，非自增)',
    customer_user_id VARCHAR(255) NOT NULL COMMENT '客户用户ID (渠道方客户标识，非本系统用户)',
    channel_id INT NOT NULL COMMENT '渠道ID',
    order_amount DECIMAL(10, 2) NOT NULL COMMENT '订单总金额',
    order_status VARCHAR(50) NOT NULL COMMENT '订单状态 (例如: 待支付, 已支付, 已发货)',
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '订单日期 (推断字段，通常订单有关联日期)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    FOREIGN KEY (channel_id) REFERENCES SalesChannels(channel_id),
    INDEX idx_customer_user_id (customer_user_id),
    INDEX idx_order_status (order_status),
    INDEX idx_order_date (order_date)
) COMMENT '销售订单表 (系统内部)';

CREATE TABLE Products (
    product_id INT PRIMARY KEY COMMENT '产品ID，主键 (根据库存表示例，可能为手动分配或来自外部系统)',
    product_name VARCHAR(255) NOT NULL COMMENT '产品名称',
    sku VARCHAR(100) UNIQUE COMMENT '库存单位 (SKU)，唯一，电商常用',
    description TEXT COMMENT '产品描述',
    unit_price DECIMAL(10, 2) COMMENT '标准售价 (实际售价可能记录在订单项中)',
    supplier_id VARCHAR(50) COMMENT '供应商ID (可选，若产品有主供应商，关联Suppliers表)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id), -- 依赖于Suppliers表
    INDEX idx_product_name (product_name),
    INDEX idx_sku (sku)
) COMMENT '产品主数据表';

CREATE TABLE SalesOrderItems (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单项ID，主键，自增',
    order_id INT NOT NULL COMMENT '销售订单ID (关联SalesOrders表)',
    product_id INT NOT NULL COMMENT '产品ID (关联Products表)',
    quantity INT NOT NULL COMMENT '购买数量',
    unit_price DECIMAL(10, 2) NOT NULL COMMENT '售出单价',
    total_price DECIMAL(10, 2) NOT NULL COMMENT '总价 (quantity * unit_price)',
    FOREIGN KEY (order_id) REFERENCES SalesOrders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id), -- 依赖于Products表
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) COMMENT '销售订单商品项表';

CREATE TABLE Products (
    product_id INT PRIMARY KEY COMMENT '产品ID，主键 (根据库存表示例，可能为手动分配或来自外部系统)',
    product_name VARCHAR(255) NOT NULL COMMENT '产品名称',
    sku VARCHAR(100) UNIQUE COMMENT '库存单位 (SKU)，唯一，电商常用',
    description TEXT COMMENT '产品描述',
    unit_price DECIMAL(10, 2) COMMENT '标准售价 (实际售价可能记录在订单项中)',
    supplier_id VARCHAR(50) COMMENT '供应商ID (可选，若产品有主供应商，关联Suppliers表)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id), -- 依赖于Suppliers表
    INDEX idx_product_name (product_name),
    INDEX idx_sku (sku)
) COMMENT '产品主数据表';

CREATE TABLE Inventory (
    inventory_id INT PRIMARY KEY COMMENT '库存ID，主键 (根据示例，例如1, 2, 3，非自增)',
    product_id INT NOT NULL UNIQUE COMMENT '产品ID (每个产品一条库存记录，关联Products表)',
    current_stock_quantity INT NOT NULL DEFAULT 0 COMMENT '当前库存量',
    alert_threshold INT NOT NULL DEFAULT 0 COMMENT '库存预警阈值',
    last_updated_at DATETIME NOT NULL COMMENT '最后更新时间',
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE, -- 依赖于Products表
    INDEX idx_product_id (product_id)
) COMMENT '库存信息表';

CREATE TABLE Suppliers (
    supplier_id VARCHAR(50) PRIMARY KEY COMMENT '供应商ID，主键 (例如: SUP001)',
    supplier_name VARCHAR(255) NOT NULL COMMENT '供应商名称',
    contact_info VARCHAR(255) COMMENT '联系方式',
    cooperation_status VARCHAR(50) NOT NULL COMMENT '合作状态 (例如: 合作中, 已终止, 待审核)',
    address TEXT COMMENT '供应商地址',
    email VARCHAR(255) UNIQUE COMMENT '供应商邮箱',
    created_at DATETIME NOT NULL COMMENT '记录创建时间 (手册中为供应商的创建时间)',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    INDEX idx_supplier_name (supplier_name),
    INDEX idx_cooperation_status (cooperation_status)
) COMMENT '供应商信息表';

CREATE TABLE Inventory (
    inventory_id INT PRIMARY KEY COMMENT '库存ID，主键 (根据示例，例如1, 2, 3，非自增)',
    product_id INT NOT NULL UNIQUE COMMENT '产品ID (每个产品一条库存记录，关联Products表)',
    current_stock_quantity INT NOT NULL DEFAULT 0 COMMENT '当前库存量',
    alert_threshold INT NOT NULL DEFAULT 0 COMMENT '库存预警阈值',
    last_updated_at DATETIME NOT NULL COMMENT '最后更新时间',
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE, -- 依赖于Products表
    INDEX idx_product_id (product_id)
) COMMENT '库存信息表';

CREATE TABLE InventoryAlerts (
    alert_id INT PRIMARY KEY COMMENT '预警ID，主键 (根据示例)',
    inventory_id INT NOT NULL COMMENT '库存ID (关联Inventory表)',
    alert_time DATETIME NOT NULL COMMENT '预警生成时间',
    alert_status VARCHAR(50) NOT NULL COMMENT '预警状态 (例如: 已发送, 未发送, 处理中)',
    handler_name VARCHAR(255) COMMENT '处理人姓名 (如手册所示"张三")',
    notes TEXT COMMENT '处理备注',
    resolved_at DATETIME NULL COMMENT '预警解决时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id),
    INDEX idx_inventory_id (inventory_id),
    INDEX idx_alert_status (alert_status),
    INDEX idx_alert_time (alert_time)
) COMMENT '库存预警记录表';

CREATE TABLE SyncedChannelOrders (
    synced_order_id VARCHAR(255) PRIMARY KEY COMMENT '同步订单ID (渠道方原始订单号，主键)',
    external_customer_user_id VARCHAR(255) COMMENT '外部客户用户ID (渠道方客户标识)',
    external_channel_code VARCHAR(50) NOT NULL COMMENT '外部渠道代码 (例如: JD, TB)',
    order_status_external VARCHAR(100) NOT NULL COMMENT '外部订单状态 (渠道定义的状态)',
    order_amount_external DECIMAL(12, 2) COMMENT '外部订单金额 (若直接提供)',
    order_created_at_external DATETIME NOT NULL COMMENT '外部订单创建时间',
    raw_order_data JSON COMMENT '原始订单数据 (存储从渠道获取的完整JSON/XML报文)',
    internal_sales_order_id INT NULL UNIQUE COMMENT '内部销售订单ID (若已转换并存入SalesOrders表，则关联)',
    sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '数据同步时间戳',
    FOREIGN KEY (internal_sales_order_id) REFERENCES SalesOrders(order_id),
    FOREIGN KEY (external_channel_code) REFERENCES SalesChannels(channel_code), -- 依赖于SalesChannels表中的channel_code
    INDEX idx_external_channel_code (external_channel_code),
    INDEX idx_order_created_at_external (order_created_at_external)
) COMMENT '已同步的渠道订单信息表 (原始或暂存)';

CREATE TABLE SyncedChannelOrderItems (
    synced_order_item_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '同步订单项ID，主键，自增',
    synced_order_id VARCHAR(255) NOT NULL COMMENT '同步订单ID (关联SyncedChannelOrders表)',
    external_product_id VARCHAR(255) COMMENT '外部产品ID (渠道方的产品标识)',
    product_sku VARCHAR(100) COMMENT '产品SKU (若渠道提供)',
    product_name_external VARCHAR(255) COMMENT '外部产品名称',
    quantity INT NOT NULL COMMENT '购买数量',
    unit_price_external DECIMAL(10, 2) NOT NULL COMMENT '外部单价',
    total_price_external DECIMAL(10, 2) NOT NULL COMMENT '外部总价',
    raw_item_data JSON COMMENT '原始订单项数据 (存储从渠道获取的完整JSON/XML报文)',
    FOREIGN KEY (synced_order_id) REFERENCES SyncedChannelOrders(synced_order_id) ON DELETE CASCADE,
    INDEX idx_synced_order_id (synced_order_id),
    INDEX idx_external_product_id (external_product_id),
    INDEX idx_product_sku (product_sku)
) COMMENT '已同步的渠道订单商品项表';

CREATE TABLE OrderSyncLogs (
    log_id VARCHAR(50) PRIMARY KEY COMMENT '日志ID，主键 (例如: LOG0001)',
    synced_order_id VARCHAR(255) NOT NULL COMMENT '同步订单ID (关联SyncedChannelOrders.synced_order_id)',
    external_channel_code VARCHAR(50) NOT NULL COMMENT '外部渠道代码 (例如: JD, PDD)',
    sync_status VARCHAR(50) NOT NULL COMMENT '同步状态 (例如: 成功, 失败, 处理中)',
    sync_time DATETIME NOT NULL COMMENT '同步操作时间',
    message TEXT COMMENT '同步结果消息 (例如错误详情)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    -- 逻辑上应有关联，但手册UI未明确显示为外键，设计时可考虑添加
    -- FOREIGN KEY (synced_order_id) REFERENCES SyncedChannelOrders(synced_order_id),
    -- FOREIGN KEY (external_channel_code) REFERENCES SalesChannels(channel_code),
    INDEX idx_synced_order_id (synced_order_id),
    INDEX idx_external_channel_code (external_channel_code),
    INDEX idx_sync_status (sync_status),
    INDEX idx_sync_time (sync_time)
) COMMENT '渠道订单同步日志表';

CREATE TABLE CommunicationMessages (
    message_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID，主键，自增',
    sender_identifier VARCHAR(255) NOT NULL COMMENT '发送者标识 (例如: "匿名"，或系统用户名/ID)',
    receiver_identifier VARCHAR(255) COMMENT '接收者标识 (例如: "匿名"，群组名，或其他用户标识)',
    message_content TEXT NOT NULL COMMENT '消息内容',
    sent_at DATETIME NOT NULL COMMENT '发送时间',
    status VARCHAR(20) DEFAULT 'sent' COMMENT '消息状态 (例如: sent, delivered, read)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    INDEX idx_sender_identifier (sender_identifier),
    INDEX idx_receiver_identifier (receiver_identifier),
    INDEX idx_sent_at (sent_at)
) COMMENT '内部通信消息表';

CREATE TABLE LogisticsInformation (
    logistics_id VARCHAR(50) PRIMARY KEY COMMENT '物流ID，主键 (例如: LOG001)',
    supplier_id VARCHAR(50) NOT NULL COMMENT '供应商ID (关联Suppliers表)',
    order_reference_id VARCHAR(255) COMMENT '相关订单号 (例如采购订单号，若适用)',
    logistics_status VARCHAR(50) NOT NULL COMMENT '物流状态 (例如: 运输中, 已签收, 运输异常)',
    logistics_details TEXT COMMENT '物流详情描述',
    tracking_number VARCHAR(255) COMMENT '运单号',
    carrier_name VARCHAR(255) COMMENT '承运商名称',
    estimated_delivery_date DATE COMMENT '预计送达日期',
    actual_delivery_date DATE COMMENT '实际送达日期',
    last_updated_at DATETIME NOT NULL COMMENT '信息更新时间 (手册中的"更新时间")',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
    INDEX idx_supplier_id (supplier_id),
    INDEX idx_logistics_status (logistics_status),
    INDEX idx_tracking_number (tracking_number)
) COMMENT '物流协同信息表';

