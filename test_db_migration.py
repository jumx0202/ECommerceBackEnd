#!/usr/bin/env python3
"""
数据库迁移测试脚本
用于检查数据库连接并执行通信管理相关的表创建
"""

import mysql.connector
from mysql.connector import Error
import os

def connect_to_database():
    """连接到MySQL数据库"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ECommerce',
            user='root',
            password=''  # 如果有密码请修改这里
        )
        
        if connection.is_connected():
            print("✓ 成功连接到MySQL数据库")
            return connection
    except Error as e:
        print(f"✗ 连接数据库失败: {e}")
        return None

def execute_sql_file(connection, file_path):
    """执行SQL文件"""
    try:
        cursor = connection.cursor()
        
        # 读取SQL文件
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # 分割SQL语句（按分号分割）
        statements = sql_content.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement:  # 跳过空语句
                try:
                    cursor.execute(statement)
                    print(f"✓ 执行SQL语句成功")
                except Error as e:
                    print(f"✗ 执行SQL语句失败: {e}")
                    print(f"语句: {statement[:100]}...")
        
        connection.commit()
        print(f"✓ 成功执行SQL文件: {file_path}")
        
    except Error as e:
        print(f"✗ 执行SQL文件失败: {e}")
    except FileNotFoundError:
        print(f"✗ 文件不存在: {file_path}")

def check_tables(connection):
    """检查创建的表"""
    try:
        cursor = connection.cursor()
        
        tables = ['Contacts', 'CommunicationMessages', 'MessageTemplates', 'QuickReplies']
        
        for table in tables:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            if result:
                print(f"✓ 表 {table} 存在")
                
                # 显示表结构
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                print(f"  列数: {len(columns)}")
            else:
                print(f"✗ 表 {table} 不存在")
        
    except Error as e:
        print(f"✗ 检查表失败: {e}")

def main():
    print("=== 通信管理数据库迁移测试 ===\n")
    
    # 连接数据库
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        # 执行表结构迁移
        print("\n1. 执行表结构迁移...")
        execute_sql_file(connection, 'migrations/update_communication_tables.sql')
        
        # 检查表是否创建成功
        print("\n2. 检查表结构...")
        check_tables(connection)
        
        # 执行样例数据插入
        print("\n3. 插入样例数据...")
        execute_sql_file(connection, 'migrations/insert_communication_sample_data.sql')
        
        print("\n=== 迁移完成 ===")
        
    except Exception as e:
        print(f"执行过程中出错: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    main() 