from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # 项目信息
    PROJECT_NAME: str = "电子商务多渠道销售与库存管理一体化系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:jm040202%40@localhost:3306/ECommerce")
    
    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:5173",  # Vite开发服务器默认端口
        "http://localhost:8000"
    ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Redis配置（可选）
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # 初始管理员账户
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
    class Config:
        case_sensitive = True

settings = Settings() 