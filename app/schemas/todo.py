from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


# ============== Tag Schemas ==============
class TagCreate(BaseModel):
    """Model để tạo Tag mới"""
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field("#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")


class TagResponse(BaseModel):
    """Model response cho Tag"""
    id: int
    name: str
    color: str
    
    class Config:
        from_attributes = True


# ============== ToDo Schemas ==============
class ToDoCreate(BaseModel):
    """Model để tạo ToDo mới"""
    title: str = Field(..., min_length=3, max_length=100, description="Tiêu đề ToDo (3-100 ký tự)")
    description: Optional[str] = Field(None, description="Mô tả chi tiết")
    due_date: Optional[date] = Field(None, description="Deadline (YYYY-MM-DD)")
    tag_ids: Optional[list[int]] = Field(None, description="Danh sách ID các tag")


class ToDoUpdate(BaseModel):
    """Model để cập nhật toàn bộ ToDo (PUT)"""
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="Tiêu đề ToDo (3-100 ký tự)")
    description: Optional[str] = Field(None, description="Mô tả chi tiết")
    is_done: Optional[bool] = None
    due_date: Optional[date] = Field(None, description="Deadline (YYYY-MM-DD)")
    tag_ids: Optional[list[int]] = Field(None, description="Danh sách ID các tag")


class ToDoPatch(BaseModel):
    """Model để cập nhật một phần ToDo (PATCH)"""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[date] = None
    tag_ids: Optional[list[int]] = None


class ToDoResponse(BaseModel):
    """Model response cho ToDo"""
    id: int
    title: str
    description: Optional[str] = None
    is_done: bool
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    tags: list[TagResponse] = []
    
    class Config:
        from_attributes = True


class ToDoListResponse(BaseModel):
    """Model response cho danh sách ToDo với pagination"""
    items: list[ToDoResponse]
    total: int
    limit: int
    offset: int
