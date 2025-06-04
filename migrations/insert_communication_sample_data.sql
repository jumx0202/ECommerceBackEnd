-- 通信管理样例数据插入脚本
-- 执行前请确保已经运行了 update_communication_tables.sql

-- 1. 插入联系人数据
INSERT INTO Contacts (name, role, contact_info, avatar_url, status, remark) VALUES
('张三', 'supplier', '13800138001', 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', 'online', '主要供应商，负责电子产品类目'),
('李四', 'channel', '13800138002', 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png', 'offline', '渠道合作伙伴，主要负责线上销售'),
('王五', 'admin', '13800138003', 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', 'busy', '系统管理员，负责平台维护'),
('赵六', 'customer', '13800138004', 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48png.png', 'online', '重要客户，月采购量较大'),
('钱七', 'supplier', '13800138005', 'https://cube.elemecdn.com/8/ec/5299b3df3e68cc147b52b3226e7e7png.png', 'offline', '服装类供应商'),
('孙八', 'channel', '13800138006', 'https://cube.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0png.png', 'online', '线下渠道合作伙伴'),
('周九', 'admin', 'admin@ecommerce.com', 'https://cube.elemecdn.com/5/64/6c21fdee3fc6d1ef356acb85d5cd4png.png', 'online', '超级管理员'),
('吴十', 'customer', 'customer@example.com', 'https://cube.elemecdn.com/7/89/389d0b5b2bafeaa6e37de44bb9c63png.png', 'busy', '企业客户，批量采购');

-- 2. 插入聊天消息数据
INSERT INTO CommunicationMessages (sender_id, receiver_id, message_content, message_type, sent_at, status) VALUES
-- 张三与系统管理员(王五)的对话
(1, 3, '您好，关于库存同步的问题', 'text', DATE_SUB(NOW(), INTERVAL 3 HOUR), 'read'),
(3, 1, '您好，请问具体是什么问题？', 'text', DATE_SUB(NOW(), INTERVAL 2 HOUR), 'read'),
(1, 3, '我这边的库存数据更新后，系统显示的库存量不正确', 'text', DATE_SUB(NOW(), INTERVAL 2 HOUR), 'read'),
(3, 1, '我来帮您检查一下，请稍等', 'text', DATE_SUB(NOW(), INTERVAL 1 HOUR), 'read'),
(3, 1, '问题已经解决，是同步延迟导致的，现在应该正常了', 'text', DATE_SUB(NOW(), INTERVAL 30 MINUTE), 'sent'),

-- 李四与系统管理员(王五)的对话
(2, 3, '渠道订单数据需要更新', 'text', DATE_SUB(NOW(), INTERVAL 8 HOUR), 'read'),
(3, 2, '好的，我马上处理', 'text', DATE_SUB(NOW(), INTERVAL 7 HOUR), 'sent'),

-- 赵六（客户）与周九（超级管理员）的对话
(4, 7, '我想咨询一下批量采购的优惠政策', 'text', DATE_SUB(NOW(), INTERVAL 1 DAY), 'read'),
(7, 4, '感谢您的咨询，我们有针对大客户的优惠方案', 'text', DATE_SUB(NOW(), INTERVAL 1 DAY), 'read'),
(4, 7, '具体的优惠幅度是多少？', 'text', DATE_SUB(NOW(), INTERVAL 1 DAY), 'read'),
(7, 4, '根据采购量可以享受5%-15%不等的折扣', 'text', DATE_SUB(NOW(), INTERVAL 20 HOUR), 'sent'),

-- 钱七（供应商）与李四（渠道）的对话
(5, 2, '新款服装已经上架，请查看', 'text', DATE_SUB(NOW(), INTERVAL 2 DAY), 'read'),
(2, 5, '收到，我会安排推广', 'text', DATE_SUB(NOW(), INTERVAL 2 DAY), 'read'),

-- 孙八（渠道）与吴十（客户）的对话
(6, 8, '您订购的商品已发货', 'text', DATE_SUB(NOW(), INTERVAL 1 DAY), 'read'),
(8, 6, '好的，大概什么时候能到？', 'text', DATE_SUB(NOW(), INTERVAL 1 DAY), 'read'),
(6, 8, '预计明天下午送达', 'text', DATE_SUB(NOW(), INTERVAL 20 HOUR), 'sent'),

-- 一些未读消息（给张三）
(3, 1, '请及时关注库存预警信息', 'text', DATE_SUB(NOW(), INTERVAL 10 MINUTE), 'sent'),
(7, 1, '新的供应商合作协议请查收', 'text', DATE_SUB(NOW(), INTERVAL 5 MINUTE), 'sent');

-- 3. 插入消息模板数据
INSERT INTO MessageTemplates (title, content, category, created_by) VALUES
('订单确认', '您的订单已确认，我们将尽快为您处理。如有疑问请联系客服。', '订单相关', 7),
('库存更新通知', '库存信息已更新，请查看最新数据。如有异常请及时联系管理员。', '库存相关', 3),
('发货通知', '您的订单已发货，快递单号：${tracking_number}，预计${delivery_date}送达。', '物流相关', 6),
('付款提醒', '您的订单待付款，请在24小时内完成支付，超时将自动取消订单。', '支付相关', 7),
('欢迎新用户', '欢迎加入我们的平台！如有任何问题，请随时联系客服。', '客服相关', 7),
('促销活动通知', '亲爱的客户，我们正在举行促销活动，详情请查看官网。', '营销推广', 2),
('系统维护通知', '系统将于${maintenance_time}进行维护，预计持续${duration}，期间可能影响正常使用。', '系统通知', 3),
('供应商协作', '请确认最新的供货计划，并及时更新库存信息。', '供应链', 3),
('渠道合作', '本月销售数据已发送，请查收并确认分成结算。', '渠道管理', 3),
('客户回访', '感谢您的购买，请对我们的服务进行评价，您的建议对我们很重要。', '客户服务', 7);

-- 4. 插入快捷回复数据
INSERT INTO QuickReplies (text, sort_order) VALUES
('好的，我马上处理', 1),
('收到，谢谢！', 2),
('请稍等，我查看一下', 3),
('问题已解决', 4),
('请提供更多详细信息', 5),
('感谢您的反馈', 6),
('我会尽快回复您', 7),
('如有其他问题请随时联系', 8),
('祝您工作愉快！', 9),
('已为您记录，会及时跟进', 10),
('您说得对，我们会改进', 11),
('这个功能正在开发中', 12),
('请查看邮件，已发送详细信息', 13),
('明白了，我会转达给相关部门', 14),
('欢迎随时沟通交流', 15);

-- 5. 更新消息模板的使用次数（模拟历史使用）
UPDATE MessageTemplates SET usage_count = FLOOR(RAND() * 50) + 1;

-- 6. 更新快捷回复的使用次数（模拟历史使用）
UPDATE QuickReplies SET usage_count = FLOOR(RAND() * 100) + 5;

-- 7. 查看插入结果
SELECT '联系人数据:' AS info;
SELECT contact_id, name, role, status, unread_count FROM Contacts;

SELECT '消息数据统计:' AS info;
SELECT 
    c1.name AS sender,
    c2.name AS receiver,
    COUNT(*) AS message_count,
    SUM(CASE WHEN is_read = 0 THEN 1 ELSE 0 END) AS unread_count
FROM CommunicationMessages cm
JOIN Contacts c1 ON cm.sender_id = c1.contact_id
JOIN Contacts c2 ON cm.receiver_id = c2.contact_id
GROUP BY cm.sender_id, cm.receiver_id
ORDER BY message_count DESC;

SELECT '消息模板:' AS info;
SELECT template_id, title, category, usage_count FROM MessageTemplates LIMIT 5;

SELECT '快捷回复:' AS info;
SELECT reply_id, text, usage_count FROM QuickReplies ORDER BY sort_order LIMIT 5; 