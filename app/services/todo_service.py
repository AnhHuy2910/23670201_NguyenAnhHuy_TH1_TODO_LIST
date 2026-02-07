from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoPatch, ToDoResponse, ToDoListResponse
from app.repositories.todo_repository import ToDoRepository


class ToDoService:
    """Service xử lý business logic cho ToDo"""
    
    def __init__(self, db: Session):
        self.repository = ToDoRepository(db)
    
    def get_todo_or_404(self, todo_id: int):
        """Lấy ToDo theo ID hoặc raise 404"""
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail=f"ToDo với id={todo_id} không tìm thấy")
        return todo
    
    def get_todos(
        self,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> ToDoListResponse:
        """Lấy danh sách ToDo với filter, search, sort và pagination"""
        todos, total = self.repository.get_all(
            is_done=is_done,
            q=q,
            sort=sort,
            limit=limit,
            offset=offset
        )
        
        items = [ToDoResponse.model_validate(todo) for todo in todos]
        return ToDoListResponse(items=items, total=total, limit=limit, offset=offset)
    
    def get_todo(self, todo_id: int) -> ToDoResponse:
        """Lấy chi tiết một ToDo"""
        todo = self.get_todo_or_404(todo_id)
        return ToDoResponse.model_validate(todo)
    
    def create_todo(self, todo_data: ToDoCreate) -> ToDoResponse:
        """Tạo ToDo mới"""
        todo = self.repository.create(
            title=todo_data.title,
            description=todo_data.description
        )
        return ToDoResponse.model_validate(todo)
    
    def update_todo(self, todo_id: int, todo_data: ToDoUpdate) -> ToDoResponse:
        """Cập nhật toàn bộ ToDo (PUT)"""
        todo = self.get_todo_or_404(todo_id)
        updated_todo = self.repository.update(
            todo,
            title=todo_data.title,
            description=todo_data.description,
            is_done=todo_data.is_done
        )
        return ToDoResponse.model_validate(updated_todo)
    
    def patch_todo(self, todo_id: int, todo_data: ToDoPatch) -> ToDoResponse:
        """Cập nhật một phần ToDo (PATCH)"""
        todo = self.get_todo_or_404(todo_id)
        
        update_data = todo_data.model_dump(exclude_unset=True)
        updated_todo = self.repository.update(todo, **update_data)
        return ToDoResponse.model_validate(updated_todo)
    
    def complete_todo(self, todo_id: int) -> ToDoResponse:
        """Đánh dấu ToDo hoàn thành"""
        todo = self.get_todo_or_404(todo_id)
        updated_todo = self.repository.update(todo, is_done=True)
        return ToDoResponse.model_validate(updated_todo)
    
    def delete_todo(self, todo_id: int) -> None:
        """Xóa ToDo"""
        todo = self.get_todo_or_404(todo_id)
        self.repository.delete(todo)
