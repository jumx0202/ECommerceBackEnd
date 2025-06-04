#!/usr/bin/env python3
"""
销售渠道表字段迁移脚本
执行前请确保已备份数据库
"""

import sys
import mysql.connector
import os
from typing import List

def get_database_config():
    """获取数据库配置"""
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'jm040202@',
        'database': 'ECommerce',
        'charset': 'utf8mb4',
        'autocommit': False
    }

def read_migration_file(file_path: str) -> List[str]:
    """读取迁移文件并分割SQL语句"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 分割SQL语句（以分号结尾）
        statements = []
        current_statement = ""
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            current_statement += line + "\n"
            
            if line.endswith(';'):
                statements.append(current_statement.strip())
                current_statement = ""
        
        return statements
    
    except FileNotFoundError:
        print(f"❌ 迁移文件未找到: {file_path}")
        return []
    except Exception as e:
        print(f"❌ 读取迁移文件时出错: {e}")
        return []

def execute_migration():
    """执行数据库迁移"""
    migration_file = "migrate_sales_channels.sql"
    
    if not os.path.exists(migration_file):
        print(f"❌ 迁移文件不存在: {migration_file}")
        return False
    
    # 读取SQL语句
    statements = read_migration_file(migration_file)
    if not statements:
        print("❌ 没有找到有效的SQL语句")
        return False
    
    connection = None
    cursor = None
    
    try:
        # 连接数据库
        connection = mysql.connector.connect(**get_database_config())
        cursor = connection.cursor()
        
        print(f"已连接到数据库: {get_database_config()['database']}")
        print("开始执行迁移...")
        
        # 执行每个SQL语句
        for i, statement in enumerate(statements, 1):
            try:
                # 显示要执行的语句（截断显示）
                display_statement = statement[:50].replace('\n', ' ') + "..." if len(statement) > 50 else statement
                print(f"执行语句 {i}: {display_statement}")
                
                # 执行语句
                cursor.execute(statement)
                
                # 如果是SELECT语句，需要读取结果
                if statement.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    print(f"  ✓ 查询返回 {len(results)} 行数据")
                    
                    # 显示查询结果（仅显示前几行）
                    if results:
                        print("  验证结果:")
                        for j, row in enumerate(results[:3]):  # 只显示前3行
                            print(f"    行{j+1}: {row}")
                        if len(results) > 3:
                            print(f"    ... 还有 {len(results) - 3} 行")
                else:
                    # 对于非SELECT语句，显示受影响的行数
                    affected_rows = cursor.rowcount
                    print(f"  ✓ 影响行数: {affected_rows}")
                
            except mysql.connector.Error as e:
                print(f"❌ 执行语句 {i} 时出错: {e}")
                return False
        
        # 提交事务
        connection.commit()
        print("\n✅ 迁移执行完成！")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ 数据库错误: {e}")
        if connection:
            connection.rollback()
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def main():
    """主函数"""
    print("=" * 50)
    print("销售渠道表字段迁移工具")
    print("=" * 50)
    
    # 确认执行
    confirm = input("是否确认执行迁移？请确保已备份数据库 (y/N): ")
    if confirm.lower() != 'y':
        print("迁移已取消")
        return
    
    # 执行迁移
    success = execute_migration()
    
    if success:
        print("\n🎉 数据库迁移成功完成！")
        print("现在可以重启FastAPI服务以使用新的字段结构。")
    else:
        print("\n❌ 迁移失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main() 