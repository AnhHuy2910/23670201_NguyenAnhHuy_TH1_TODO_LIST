from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoPatch, ToDoResponse, ToDoListResponse
from app.services.todo_service import ToDoService

router = APIRouter(prefix="/todos", tags=["ToDos"])


def get_todo_service(db: Session = Depends(get_db)) -> ToDoService:
    """Dependency để lấy ToDoService"""
    return ToDoService(db)


@router.post("", response_model=ToDoResponse, status_code=201)
def create_todo(
    todo: ToDoCreate,
    service: ToDoService = Depends(get_todo_service)
):
    """Tạo ToDo mới"""
    return service.create_todo(todo)


@router.get("", response_model=ToDoListResponse)
def get_todos(
    is_done: Optional[bool] = Query(None, description="Lọc theo trạng thái hoàn thành"),
    q: Optional[str] = Query(None, description="Tìm kiếm theo tiêu đề"),
    sort: Optional[str] = Query(None, description="Sắp xếp: created_at, -created_at, updated_at, -updated_at"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng kết quả trả về"),
    offset: int = Query(0, ge=0, description="Vị trí bắt đầu"),
    service: ToDoService = Depends(get_todo_service)
):
    """Lấy danh sách ToDo với filter, search, sort và pagination"""
    return service.get_todos(is_done=is_done, q=q, sort=sort, limit=limit, offset=offset)


@router.get("/{todo_id}", response_model=ToDoResponse)
def get_todo(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service)
):
    """Lấy chi tiết một ToDo theo ID"""
    return service.get_todo(todo_id)


@router.put("/{todo_id}", response_model=ToDoResponse)
def update_todo(
    todo_id: int,
    todo_update: ToDoUpdate,
    service: ToDoService = Depends(get_todo_service)
):
    """Cập nhật toàn bộ ToDo theo ID (PUT)"""
    return service.update_todo(todo_id, todo_update)


@router.patch("/{todo_id}", response_model=ToDoResponse)
def patch_todo(
    todo_id: int,
    todo_patch: ToDoPatch,
    service: ToDoService = Depends(get_todo_service)
):
    """Cập nhật một phần ToDo theo ID (PATCH)"""
    return service.patch_todo(todo_id, todo_patch)


@router.post("/{todo_id}/complete", response_model=ToDoResponse)
def complete_todo(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service)
):
    """Đánh dấu ToDo hoàn thành"""
    return service.complete_todo(todo_id)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service)
):
    """Xóa ToDo theo ID"""
    service.delete_todo(todo_id)
    return None
