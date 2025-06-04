# 电商管理系统后端

## 项目介绍

这是一个基于FastAPI开发的电商管理系统后端，提供了产品管理、库存管理、订单处理、用户管理等核心功能的API接口。

## 技术栈

- **后端框架**: FastAPI
- **数据库**: MySQL
- **ORM**: SQLAlchemy
- **认证**: JWT (JSON Web Tokens)
- **API文档**: Swagger UI / ReDoc (由FastAPI自动生成)

## 功能特性

- 产品管理：产品的增删改查，分类管理
- 库存管理：库存跟踪，库存调整，库存预警
- 订单管理：订单创建，订单状态更新，订单详情查询
- 用户管理：用户认证，权限控制
- 数据分析：销售报表，库存状态分析

## 环境要求

- Python 3.8+
- MySQL 5.7+
- 虚拟环境工具 (推荐使用venv或conda)

## 安装与运行

### 1. 克隆项目

```bash
git clone <项目仓库URL>
cd ECommerce
```

### 2. 创建并激活虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建`.env`文件并配置以下内容：

```
DATABASE_URL=mysql+pymysql://username:password@localhost/ecommerce
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. 初始化数据库

```bash
alembic upgrade head
```

### 6. 运行开发服务器

```bash
uvicorn app.main:app --reload
```

服务将在`http://localhost:8000`上运行。

## API文档

FastAPI自动生成的API文档可通过以下URL访问：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 项目结构

```
app/
├── api/                 # API路由和端点
│   ├── deps.py          # 依赖注入
│   └── v1/              # API v1版本
│       └── endpoints/   # API端点
├── core/                # 核心配置
│   ├── config.py        # 应用配置
│   └── security.py      # 安全相关
├── db/                  # 数据库
│   ├── base.py          # 基础模型
│   └── session.py       # 数据库会话
├── models/              # 数据库模型
├── schemas/             # Pydantic模型
├── crud/                # CRUD操作
└── main.py              # 应用入口

alembic/                 # 数据库迁移
tests/                   # 测试
```

## 开发指南

### 添加新的API端点

1. 在`app/api/v1/endpoints/`下创建新的路由文件
2. 在`app/api/v1/api.py`中注册路由
3. 创建必要的模型、模式和CRUD操作

### 数据库迁移

创建新的迁移：

```bash
alembic revision --autogenerate -m "描述变更内容"
```

应用迁移：

```bash
alembic upgrade head
```

## 测试

运行测试：

```bash
pytest
```

## 部署

本项目可部署到任何支持Python的服务器或云平台。推荐使用Docker进行容器化部署。

### Docker部署

```bash
docker build -t ecommerce-backend .
docker run -p 8000:8000 --env-file .env ecommerce-backend
```

## API端点概览

### 认证
- `POST /api/v1/login/access-token` - 登录获取访问令牌

### 用户管理
- `GET /api/v1/users/` - 获取用户列表
- `POST /api/v1/users/` - 创建新用户
- `GET /api/v1/users/me` - 获取当前用户信息

### 销售渠道
- `GET /api/v1/sales-channels/` - 获取销售渠道列表
- `POST /api/v1/sales-channels/` - 创建销售渠道
- `PUT /api/v1/sales-channels/{channel_id}` - 更新销售渠道

### 销售订单
- `GET /api/v1/sales-orders/` - 获取销售订单列表
- `POST /api/v1/sales-orders/` - 创建销售订单
- `GET /api/v1/sales-orders/{order_id}` - 获取订单详情

### 产品管理
- `GET /api/v1/products/` - 获取产品列表
- `POST /api/v1/products/` - 创建产品
- `PUT /api/v1/products/{product_id}` - 更新产品信息

### 库存管理
- `GET /api/v1/inventory/` - 获取库存列表
- `POST /api/v1/inventory/` - 创建库存记录
- `GET /api/v1/inventory/alerts/` - 获取库存预警列表

### 供应商管理
- `GET /api/v1/suppliers/` - 获取供应商列表
- `POST /api/v1/suppliers/` - 创建供应商
- `PUT /api/v1/suppliers/{supplier_id}` - 更新供应商信息

### 物流协同
- `GET /api/v1/logistics/` - 获取物流信息列表
- `POST /api/v1/logistics/` - 创建物流信息
- `PUT /api/v1/logistics/{logistics_id}` - 更新物流状态

### 数据统计
- `GET /api/v1/dashboard/statistics` - 获取系统统计数据
- `GET /api/v1/dashboard/charts/sales-trend` - 获取销售趋势数据
- `GET /api/v1/dashboard/charts/channel-distribution` - 获取渠道分布数据

## 许可证

本项目采用MIT许可证。 