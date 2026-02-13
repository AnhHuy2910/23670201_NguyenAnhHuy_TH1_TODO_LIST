from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoPatch, ToDoResponse, ToDoListResponse
from app.repositories.todo_repository import ToDoRepository
from app.models.user import User


class ToDoService:
    """Service xử lý business logic cho ToDo"""
    
    def __init__(self, db: Session):
        self.repository = ToDoRepository(db)
    
    def get_todo_or_404(self, todo_id: int, owner_id: int):
        """Lấy ToDo theo ID và owner hoặc raise 404"""
        todo = self.repository.get_by_id(todo_id, owner_id)
        if not todo:
            raise HTTPException(status_code=404, detail=f"ToDo với id={todo_id} không tìm thấy")
        return todo
    
    def get_todos(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> ToDoListResponse:
        """Lấy danh sách ToDo của owner với filter, search, sort và pagination"""
        todos, total = self.repository.get_all(
            owner_id=owner_id,
            is_done=is_done,
            q=q,
            sort=sort,
            limit=limit,
            offset=offset
        )
        
        items = [ToDoResponse.model_validate(todo) for todo in todos]
        return ToDoListResponse(items=items, total=total, limit=limit, offset=offset)
    
    def get_overdue_todos(self, owner_id: int) -> list[ToDoResponse]:
        """Lấy danh sách ToDo quá hạn"""
        todos = self.repository.get_overdue(owner_id)
        return [ToDoResponse.model_validate(todo) for todo in todos]
    
    def get_today_todos(self, owner_id: int) -> list[ToDoResponse]:
        """Lấy danh sách ToDo hôm nay"""
        todos = self.repository.get_today(owner_id)
        return [ToDoResponse.model_validate(todo) for todo in todos]
    
    def get_deleted_todos(self, owner_id: int) -> list[ToDoResponse]:
        """Lấy danh sách ToDo đã xóa (trash)"""
        todos = self.repository.get_deleted(owner_id)
        return [ToDoResponse.model_validate(todo) for todo in todos]
    
    def get_todo(self, todo_id: int, owner_id: int) -> ToDoResponse:
        """Lấy chi tiết một ToDo"""
        todo = self.get_todo_or_404(todo_id, owner_id)
        return ToDoResponse.model_validate(todo)
    
    def create_todo(self, todo_data: ToDoCreate, owner_id: int) -> ToDoResponse:
        """Tạo ToDo mới"""
        todo = self.repository.create(
            title=todo_data.title,
            description=todo_data.description,
            owner_id=owner_id,
            due_date=todo_data.due_date,
            tag_ids=todo_data.tag_ids
        )
        return ToDoResponse.model_validate(todo)
    
    def update_todo(self, todo_id: int, todo_data: ToDoUpdate, owner_id: int) -> ToDoResponse:
        """Cập nhật toàn bộ ToDo (PUT)"""
        todo = self.get_todo_or_404(todo_id, owner_id)
        updated_todo = self.repository.update(
            todo,
            tag_ids=todo_data.tag_ids,
            title=todo_data.title,
            description=todo_data.description,
            is_done=todo_data.is_done,
            due_date=todo_data.due_date
        )
        return ToDoResponse.model_validate(updated_todo)
    
    def patch_todo(self, todo_id: int, todo_data: ToDoPatch, owner_id: int) -> ToDoResponse:
        """Cập nhật một phần ToDo (PATCH)"""
        todo = self.get_todo_or_404(todo_id, owner_id)
        
        update_data = todo_data.model_dump(exclude_unset=True)
        tag_ids = update_data.pop('tag_ids', None)
        updated_todo = self.repository.update(todo, tag_ids=tag_ids, **update_data)
        return ToDoResponse.model_validate(updated_todo)
    
    def complete_todo(self, todo_id: int, owner_id: int) -> ToDoResponse:
        """Đánh dấu ToDo hoàn thành"""
        todo = self.get_todo_or_404(todo_id, owner_id)
        updated_todo = self.repository.update(todo, is_done=True)
        return ToDoResponse.model_validate(updated_todo)
    
    def delete_todo(self, todo_id: int, owner_id: int) -> None:
        """Xóa ToDo (soft delete)"""
        todo = self.get_todo_or_404(todo_id, owner_id)
        self.repository.delete(todo)
    
    def restore_todo(self, todo_id: int, owner_id: int) -> ToDoResponse:
        """Khôi phục ToDo đã xóa"""
        todo = self.repository.get_by_id(todo_id, owner_id, include_deleted=True)
        if not todo:
            raise HTTPException(status_code=404, detail=f"ToDo với id={todo_id} không tìm thấy")
        if todo.deleted_at is None:
            raise HTTPException(status_code=400, detail="ToDo chưa bị xóa")
        restored_todo = self.repository.restore(todo)
        return ToDoResponse.model_validate(restored_todo)
    
    def hard_delete_todo(self, todo_id: int, owner_id: int) -> None:
        """Xóa vĩnh viễn ToDo"""
        todo = self.repository.get_by_id(todo_id, owner_id, include_deleted=True)
        if not todo:
            raise HTTPException(status_code=404, detail=f"ToDo với id={todo_id} không tìm thấy")
        self.repository.hard_delete(todo)
