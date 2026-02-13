from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoPatch, ToDoResponse, ToDoListResponse
from app.services.todo_service import ToDoService
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["ToDos"])


def get_todo_service(db: Session = Depends(get_db)) -> ToDoService:
    """Dependency để lấy ToDoService"""
    return ToDoService(db)


@router.get("/overdue", response_model=list[ToDoResponse])
def get_overdue_todos(
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Lấy danh sách ToDo quá hạn (due_date < today và chưa hoàn thành)"""
    return service.get_overdue_todos(owner_id=current_user.id)


@router.get("/today", response_model=list[ToDoResponse])
def get_today_todos(
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Lấy danh sách ToDo hôm nay (due_date = today)"""
    return service.get_today_todos(owner_id=current_user.id)


@router.get("/trash", response_model=list[ToDoResponse])
def get_deleted_todos(
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Lấy danh sách ToDo đã xóa (thùng rác)"""
    return service.get_deleted_todos(owner_id=current_user.id)


@router.post("/{todo_id}/restore", response_model=ToDoResponse)
def restore_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Khôi phục ToDo từ thùng rác"""
    return service.restore_todo(todo_id, owner_id=current_user.id)


@router.delete("/{todo_id}/permanent", status_code=204)
def hard_delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Xóa vĩnh viễn ToDo (không thể khôi phục)"""
    service.hard_delete_todo(todo_id, owner_id=current_user.id)
    return None


@router.post("", response_model=ToDoResponse, status_code=201)
def create_todo(
    todo: ToDoCreate,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Tạo ToDo mới (yêu cầu đăng nhập)"""
    return service.create_todo(todo, owner_id=current_user.id)


@router.get("", response_model=ToDoListResponse)
def get_todos(
    is_done: Optional[bool] = Query(None, description="Lọc theo trạng thái hoàn thành"),
    q: Optional[str] = Query(None, description="Tìm kiếm theo tiêu đề"),
    sort: Optional[str] = Query(None, description="Sắp xếp: created_at, -created_at, updated_at, -updated_at"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng kết quả trả về"),
    offset: int = Query(0, ge=0, description="Vị trí bắt đầu"),
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Lấy danh sách ToDo của user hiện tại"""
    return service.get_todos(owner_id=current_user.id, is_done=is_done, q=q, sort=sort, limit=limit, offset=offset)


@router.get("/{todo_id}", response_model=ToDoResponse)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Lấy chi tiết một ToDo theo ID (chỉ của user hiện tại)"""
    return service.get_todo(todo_id, owner_id=current_user.id)


@router.put("/{todo_id}", response_model=ToDoResponse)
def update_todo(
    todo_id: int,
    todo_update: ToDoUpdate,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Cập nhật toàn bộ ToDo theo ID (PUT)"""
    return service.update_todo(todo_id, todo_update, owner_id=current_user.id)


@router.patch("/{todo_id}", response_model=ToDoResponse)
def patch_todo(
    todo_id: int,
    todo_patch: ToDoPatch,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Cập nhật một phần ToDo theo ID (PATCH)"""
    return service.patch_todo(todo_id, todo_patch, owner_id=current_user.id)


@router.post("/{todo_id}/complete", response_model=ToDoResponse)
def complete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Đánh dấu ToDo hoàn thành"""
    return service.complete_todo(todo_id, owner_id=current_user.id)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    service: ToDoService = Depends(get_todo_service)
):
    """Xóa ToDo theo ID (chỉ của user hiện tại)"""
    service.delete_todo(todo_id, owner_id=current_user.id)
    return None
