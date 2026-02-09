from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Model để đăng ký user mới"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Mật khẩu (ít nhất 6 ký tự)")


class UserLogin(BaseModel):
    """Model để đăng nhập"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Model response cho User"""
    id: int
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Model cho JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Model cho data trong token"""
    user_id: Optional[int] = None
