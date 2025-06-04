#!/usr/bin/env python3
from sqlalchemy import create_engine
from app.core.config import settings

def test_database_connection():
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        
        # 尝试连接
        with engine.connect() as connection:
            print("✓ 数据库连接成功！")
            print(f"当前使用的数据库URL: {settings.DATABASE_URL}")
            
    except Exception as e:
        print("✗ 数据库连接失败！")
        print(f"错误信息: {str(e)}")
        print(f"当前使用的数据库URL: {settings.DATABASE_URL}")

if __name__ == "__main__":
    test_database_connection() 