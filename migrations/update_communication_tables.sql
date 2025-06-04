-- 通信管理数据库迁移脚本
-- 执行时间：2024年

-- 1. 创建联系人表
CREATE TABLE IF NOT EXISTS Contacts (
    contact_id INT NOT NULL AUTO_INCREMENT COMMENT '联系人ID，主键',
    name VARCHAR(100) NOT NULL COMMENT '联系人姓名',
    role VARCHAR(50) NOT NULL COMMENT '角色（admin/channel/supplier/customer）',
    contact_info VARCHAR(255) NOT NULL COMMENT '联系方式（手机号/邮箱等）',
    avatar_url VARCHAR(500) NULL COMMENT '头像URL',
    status VARCHAR(20) DEFAULT 'offline' COMMENT '在线状态（online/offline/busy）',
    remark TEXT NULL COMMENT '备注信息',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (contact_id),
    INDEX idx_contacts_role (role),
    INDEX idx_contacts_status (status),
    INDEX idx_contacts_contact_info (contact_info),
    INDEX idx_contacts_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='联系人表';

-- 2. 修改现有的通信消息表结构
-- 首先备份现有数据
CREATE TABLE IF NOT EXISTS CommunicationMessages_backup AS 
SELECT * FROM CommunicationMessages WHERE 1=0;

-- 插入现有数据到备份表（如果有的话）
INSERT INTO CommunicationMessages_backup 
SELECT * FROM CommunicationMessages;

-- 删除原表
DROP TABLE IF EXISTS CommunicationMessages;

-- 3. 重新创建通信消息表（新结构）
CREATE TABLE CommunicationMessages (
    message_id INT NOT NULL AUTO_INCREMENT COMMENT '消息ID，主键',
    sender_id INT NOT NULL COMMENT '发送方ID',
    receiver_id INT NOT NULL COMMENT '接收方ID',
    message_content TEXT NOT NULL COMMENT '消息内容',
    message_type VARCHAR(20) DEFAULT 'text' COMMENT '消息类型（text/file/image）',
    file_url VARCHAR(500) NULL COMMENT '文件URL（当消息类型为file/image时）',
    file_name VARCHAR(255) NULL COMMENT '文件名（当消息类型为file时）',
    is_read TINYINT(1) DEFAULT 0 COMMENT '是否已读',
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    read_at TIMESTAMP NULL COMMENT '阅读时间',
    status VARCHAR(20) DEFAULT 'sent' COMMENT '消息状态（sent/delivered/read）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (message_id),
    FOREIGN KEY (sender_id) REFERENCES Contacts(contact_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Contacts(contact_id) ON DELETE CASCADE,
    INDEX idx_sender_id (sender_id),
    INDEX idx_receiver_id (receiver_id),
    INDEX idx_sent_at (sent_at),
    INDEX idx_is_read (is_read),
    INDEX idx_status (status),
    INDEX idx_message_type (message_type),
    INDEX idx_sender_receiver (sender_id, receiver_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通信消息表';

-- 4. 创建消息模板表
CREATE TABLE IF NOT EXISTS MessageTemplates (
    template_id INT NOT NULL AUTO_INCREMENT COMMENT '模板ID，主键',
    title VARCHAR(100) NOT NULL COMMENT '模板标题',
    content TEXT NOT NULL COMMENT '模板内容',
    category VARCHAR(50) NULL COMMENT '模板分类',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否激活',
    created_by INT NULL COMMENT '创建者',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (template_id),
    FOREIGN KEY (created_by) REFERENCES Contacts(contact_id) ON DELETE SET NULL,
    INDEX idx_templates_category (category),
    INDEX idx_templates_is_active (is_active),
    INDEX idx_templates_usage_count (usage_count),
    INDEX idx_templates_created_by (created_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息模板表';

-- 5. 创建快捷回复表
CREATE TABLE IF NOT EXISTS QuickReplies (
    reply_id INT NOT NULL AUTO_INCREMENT COMMENT '快捷回复ID，主键',
    text VARCHAR(500) NOT NULL COMMENT '回复文本',
    sort_order INT DEFAULT 0 COMMENT '排序',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (reply_id),
    INDEX idx_quick_replies_sort_order (sort_order),
    INDEX idx_quick_replies_is_active (is_active),
    INDEX idx_quick_replies_usage_count (usage_count)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='快捷回复表'; 