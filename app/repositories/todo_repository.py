from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.todo import ToDo


class ToDoRepository:
    """Repository quản lý dữ liệu ToDo với SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[list[ToDo], int]:
        """Lấy danh sách ToDo với filter, search, sort và pagination từ DB"""
        query = self.db.query(ToDo)
        
        # Filter by is_done
        if is_done is not None:
            query = query.filter(ToDo.is_done == is_done)
        
        # Search by title
        if q:
            query = query.filter(ToDo.title.ilike(f"%{q}%"))
        
        # Get total count before pagination
        total = query.count()
        
        # Sort
        if sort:
            if sort.startswith("-"):
                sort_field = sort.lstrip("-")
                if hasattr(ToDo, sort_field):
                    query = query.order_by(desc(getattr(ToDo, sort_field)))
            else:
                if hasattr(ToDo, sort):
                    query = query.order_by(asc(getattr(ToDo, sort)))
        else:
            # Default sort by created_at desc
            query = query.order_by(desc(ToDo.created_at))
        
        # Pagination
        todos = query.offset(offset).limit(limit).all()
        
        return todos, total
    
    def get_by_id(self, todo_id: int) -> Optional[ToDo]:
        """Lấy ToDo theo ID"""
        return self.db.query(ToDo).filter(ToDo.id == todo_id).first()
    
    def create(self, title: str, description: Optional[str] = None) -> ToDo:
        """Tạo ToDo mới"""
        new_todo = ToDo(title=title, description=description, is_done=False)
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)
        return new_todo
    
    def update(self, todo: ToDo, **kwargs) -> ToDo:
        """Cập nhật ToDo"""
        for key, value in kwargs.items():
            if value is not None and hasattr(todo, key):
                setattr(todo, key, value)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def delete(self, todo: ToDo) -> bool:
        """Xóa ToDo"""
        self.db.delete(todo)
        self.db.commit()
        return True
