from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    role: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password_hash: str 