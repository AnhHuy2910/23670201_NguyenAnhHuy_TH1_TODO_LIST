from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ToDoCreate(BaseModel):
    """Model để tạo ToDo mới"""
    title: str = Field(..., min_length=3, max_length=100, description="Tiêu đề ToDo (3-100 ký tự)")
    description: Optional[str] = Field(None, description="Mô tả chi tiết")


class ToDoUpdate(BaseModel):
    """Model để cập nhật toàn bộ ToDo (PUT)"""
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="Tiêu đề ToDo (3-100 ký tự)")
    description: Optional[str] = Field(None, description="Mô tả chi tiết")
    is_done: Optional[bool] = None


class ToDoPatch(BaseModel):
    """Model để cập nhật một phần ToDo (PATCH)"""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None


class ToDoResponse(BaseModel):
    """Model response cho ToDo"""
    id: int
    title: str
    description: Optional[str] = None
    is_done: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ToDoListResponse(BaseModel):
    """Model response cho danh sách ToDo với pagination"""
    items: list[ToDoResponse]
    total: int
    limit: int
    offset: int
