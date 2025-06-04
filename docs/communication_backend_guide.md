# 通信管理后端API使用指南

## 概述

本文档介绍了电商管理系统通信模块的后端API设计和使用方法。通信模块包含联系人管理、消息收发、消息模板和快捷回复等功能。

## 数据库结构

### 1. 联系人表 (Contacts)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| contact_id | INT | 联系人ID，主键 |
| name | VARCHAR(100) | 联系人姓名 |
| role | VARCHAR(50) | 角色（admin/channel/supplier/customer） |
| contact_info | VARCHAR(255) | 联系方式 |
| avatar_url | VARCHAR(500) | 头像URL |
| status | VARCHAR(20) | 在线状态（online/offline/busy） |
| remark | TEXT | 备注信息 |
| is_active | TINYINT(1) | 是否激活 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 2. 通信消息表 (CommunicationMessages)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| message_id | INT | 消息ID，主键 |
| sender_id | INT | 发送方ID |
| receiver_id | INT | 接收方ID |
| message_content | TEXT | 消息内容 |
| message_type | VARCHAR(20) | 消息类型（text/file/image） |
| file_url | VARCHAR(500) | 文件URL |
| file_name | VARCHAR(255) | 文件名 |
| is_read | TINYINT(1) | 是否已读 |
| sent_at | TIMESTAMP | 发送时间 |
| read_at | TIMESTAMP | 阅读时间 |
| status | VARCHAR(20) | 消息状态（sent/delivered/read） |
| created_at | TIMESTAMP | 创建时间 |

### 3. 消息模板表 (MessageTemplates)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| template_id | INT | 模板ID，主键 |
| title | VARCHAR(100) | 模板标题 |
| content | TEXT | 模板内容 |
| category | VARCHAR(50) | 模板分类 |
| usage_count | INT | 使用次数 |
| is_active | TINYINT(1) | 是否激活 |
| created_by | INT | 创建者ID |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 4. 快捷回复表 (QuickReplies)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| reply_id | INT | 快捷回复ID，主键 |
| text | VARCHAR(500) | 回复文本 |
| sort_order | INT | 排序 |
| usage_count | INT | 使用次数 |
| is_active | TINYINT(1) | 是否激活 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

## API端点

### 联系人管理

#### 1. 获取联系人列表
```
GET /api/v1/communication/contacts
```

**查询参数：**
- `skip`: 跳过记录数
- `limit`: 限制记录数
- `search`: 搜索关键词
- `role`: 角色筛选
- `status`: 状态筛选

**响应示例：**
```json
{
  "contacts": [
    {
      "contact_id": 1,
      "name": "张三",
      "role": "supplier",
      "contact_info": "13800138001",
      "avatar_url": "https://example.com/avatar.jpg",
      "status": "online",
      "remark": "主要供应商",
      "is_active": true,
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T10:00:00",
      "unread_count": 2
    }
  ],
  "total": 10
}
```

#### 2. 创建联系人
```
POST /api/v1/communication/contacts
```

**请求体：**
```json
{
  "name": "张三",
  "role": "supplier",
  "contact_info": "13800138001",
  "avatar_url": "https://example.com/avatar.jpg",
  "status": "online",
  "remark": "主要供应商"
}
```

#### 3. 更新联系人
```
PUT /api/v1/communication/contacts/{contact_id}
```

#### 4. 删除联系人
```
DELETE /api/v1/communication/contacts/{contact_id}
```

### 消息管理

#### 1. 获取聊天记录
```
GET /api/v1/communication/messages/{contact_id}
```

**查询参数：**
- `skip`: 跳过记录数
- `limit`: 限制记录数

**响应示例：**
```json
[
  {
    "message_id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "message_content": "您好，关于库存同步的问题",
    "message_type": "text",
    "is_read": true,
    "sent_at": "2024-01-01T10:00:00",
    "read_at": "2024-01-01T10:05:00",
    "status": "read",
    "created_at": "2024-01-01T10:00:00",
    "sender_name": "张三",
    "sender_avatar": "https://example.com/avatar.jpg",
    "receiver_name": "李四"
  }
]
```

#### 2. 发送消息
```
POST /api/v1/communication/messages
```

**请求体：**
```json
{
  "receiver_id": 2,
  "message_content": "您好，请问具体是什么问题？",
  "message_type": "text"
}
```

#### 3. 标记消息已读
```
PUT /api/v1/communication/messages/{message_id}/read
```

### 消息模板管理

#### 1. 获取消息模板
```
GET /api/v1/communication/templates
```

**查询参数：**
- `skip`: 跳过记录数
- `limit`: 限制记录数
- `category`: 分类筛选

#### 2. 创建消息模板
```
POST /api/v1/communication/templates
```

**请求体：**
```json
{
  "title": "订单确认",
  "content": "您的订单已确认，我们将尽快为您处理。",
  "category": "订单相关",
  "created_by": 1
}
```

### 快捷回复管理

#### 1. 获取快捷回复
```
GET /api/v1/communication/quick-replies
```

#### 2. 创建快捷回复
```
POST /api/v1/communication/quick-replies
```

**请求体：**
```json
{
  "text": "好的，我马上处理",
  "sort_order": 1
}
```

## 部署步骤

### 1. 数据库迁移

首先执行数据库迁移脚本：

```bash
# 1. 更新表结构
mysql -u username -p database_name < migrations/update_communication_tables.sql

# 2. 插入样例数据
mysql -u username -p database_name < migrations/insert_communication_sample_data.sql
```

### 2. 后端模型注册

确保在 `app/models/__init__.py` 中导入新模型：

```python
from .communication import Contact, CommunicationMessage, MessageTemplate, QuickReply
```

### 3. 前端API集成

在前端中导入并使用通信API：

```typescript
import { communicationAPI } from '@/api'

// 获取联系人列表
const contacts = await communicationAPI.getContacts()

// 发送消息
await communicationAPI.sendMessage({
  receiver_id: 1,
  message_content: "Hello",
  message_type: "text"
})
```

## 样例数据

系统包含以下样例数据：

### 联系人
- 张三（供应商）- 在线，有2条未读消息
- 李四（渠道）- 离线
- 王五（管理员）- 忙碌
- 赵六（客户）- 在线
- 等等...

### 消息记录
- 张三与王五关于库存同步的对话
- 李四与王五关于渠道订单的讨论
- 客户与管理员的咨询对话
- 等等...

### 消息模板
- 订单确认、库存更新通知、发货通知
- 付款提醒、欢迎新用户、促销活动通知
- 系统维护通知、供应商协作、渠道合作
- 等等...

### 快捷回复
- "好的，我马上处理"
- "收到，谢谢！"
- "请稍等，我查看一下"
- 等等...

## 注意事项

1. **权限控制**：确保用户只能访问自己有权限的联系人和消息
2. **实时性**：考虑使用WebSocket实现实时消息推送
3. **文件上传**：图片和文件消息需要配置文件存储服务
4. **消息加密**：敏感消息可考虑加密存储
5. **消息归档**：定期归档历史消息以优化性能

## 测试

可以使用以下命令测试API：

```bash
# 获取联系人列表
curl -X GET "http://localhost:8000/api/v1/communication/contacts" \
     -H "Authorization: Bearer YOUR_TOKEN"

# 发送消息
curl -X POST "http://localhost:8000/api/v1/communication/messages" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{"receiver_id": 1, "message_content": "测试消息", "message_type": "text"}'
``` 