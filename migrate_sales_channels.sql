-- 销售渠道表字段迁移脚本
-- 执行前请备份数据库

USE ECommerce;

-- 为SalesChannels表添加新字段
ALTER TABLE SalesChannels 
ADD COLUMN platform_type VARCHAR(50) NOT NULL DEFAULT 'ecommerce' COMMENT '平台类型：ecommerce/marketplace/social/direct' AFTER channel_code,
ADD COLUMN api_address VARCHAR(500) COMMENT 'API地址' AFTER platform_type,
ADD COLUMN commission_rate DECIMAL(5, 2) DEFAULT 0.0 COMMENT '佣金率（百分比）' AFTER api_address,
ADD COLUMN channel_status VARCHAR(20) DEFAULT 'active' COMMENT '渠道状态：active/inactive' AFTER commission_rate,
ADD COLUMN description TEXT COMMENT '渠道描述' AFTER channel_status,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' AFTER created_at;

-- 添加索引
ALTER TABLE SalesChannels 
ADD INDEX idx_platform_type (platform_type),
ADD INDEX idx_channel_status (channel_status);

-- 更新现有数据的默认值
UPDATE SalesChannels SET 
    platform_type = CASE 
        WHEN channel_name LIKE '%京东%' OR channel_name = '京东' THEN 'marketplace'
        WHEN channel_name LIKE '%淘宝%' OR channel_name = '淘宝' THEN 'marketplace'
        WHEN channel_name LIKE '%天猫%' OR channel_name = '天猫' THEN 'marketplace'
        WHEN channel_name LIKE '%拼多多%' OR channel_name = '拼多多' THEN 'marketplace'
        WHEN channel_name LIKE '%抖音%' OR channel_name = '抖音' THEN 'social'
        ELSE 'ecommerce'
    END,
    api_address = CASE
        WHEN channel_name = '京东' THEN 'https://api.jd.com'
        WHEN channel_name = '淘宝' THEN 'https://eco.taobao.com'
        WHEN channel_name = '天猫' THEN 'https://open.tmall.com'
        WHEN channel_name = '拼多多' THEN 'https://open-api.pinduoduo.com'
        WHEN channel_name = '抖音小店' THEN 'https://openapi.jinritemai.com'
        ELSE NULL
    END,
    commission_rate = CASE
        WHEN channel_name = '京东' THEN 3.5
        WHEN channel_name = '淘宝' THEN 2.8
        WHEN channel_name = '天猫' THEN 4.0
        WHEN channel_name = '拼多多' THEN 2.5
        WHEN channel_name = '抖音小店' THEN 5.0
        ELSE 0.0
    END,
    channel_status = 'active',
    updated_at = NOW()
WHERE channel_id IS NOT NULL;

-- 验证更新结果
SELECT channel_id, channel_name, platform_type, api_address, commission_rate, channel_status 
FROM SalesChannels 
ORDER BY channel_id;

-- 提示信息
SELECT 'SalesChannels表字段迁移完成！请检查上方查询结果确认数据正确性。' AS migration_status; 