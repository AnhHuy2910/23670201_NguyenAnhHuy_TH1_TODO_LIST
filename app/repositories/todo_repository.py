from typing import Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc
from app.models.todo import ToDo, Tag


class ToDoRepository:
    """Repository quản lý dữ liệu ToDo với SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[list[ToDo], int]:
        """Lấy danh sách ToDo của owner với filter, search, sort và pagination từ DB"""
        query = self.db.query(ToDo).options(joinedload(ToDo.tags)).filter(ToDo.owner_id == owner_id)
        
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
    
    def get_overdue(self, owner_id: int) -> list[ToDo]:
        """Lấy danh sách ToDo quá hạn (due_date < today và chưa done)"""
        today = date.today()
        return self.db.query(ToDo).options(joinedload(ToDo.tags)).filter(
            ToDo.owner_id == owner_id,
            ToDo.due_date < today,
            ToDo.is_done == False
        ).order_by(ToDo.due_date).all()
    
    def get_today(self, owner_id: int) -> list[ToDo]:
        """Lấy danh sách ToDo hôm nay (due_date = today)"""
        today = date.today()
        return self.db.query(ToDo).options(joinedload(ToDo.tags)).filter(
            ToDo.owner_id == owner_id,
            ToDo.due_date == today
        ).order_by(ToDo.created_at).all()
    
    def get_by_id(self, todo_id: int, owner_id: int) -> Optional[ToDo]:
        """Lấy ToDo theo ID và owner_id"""
        return self.db.query(ToDo).options(joinedload(ToDo.tags)).filter(
            ToDo.id == todo_id,
            ToDo.owner_id == owner_id
        ).first()
    
    def create(
        self, 
        title: str, 
        owner_id: int, 
        description: Optional[str] = None,
        due_date: Optional[date] = None,
        tag_ids: Optional[list[int]] = None
    ) -> ToDo:
        """Tạo ToDo mới"""
        new_todo = ToDo(
            title=title, 
            description=description, 
            is_done=False, 
            owner_id=owner_id,
            due_date=due_date
        )
        
        # Thêm tags nếu có
        if tag_ids:
            tags = self.db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            new_todo.tags = tags
        
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)
        return new_todo
    
    def update(self, todo: ToDo, tag_ids: Optional[list[int]] = None, **kwargs) -> ToDo:
        """Cập nhật ToDo"""
        for key, value in kwargs.items():
            if value is not None and hasattr(todo, key):
                setattr(todo, key, value)
        
        # Cập nhật tags nếu được chỉ định
        if tag_ids is not None:
            tags = self.db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            todo.tags = tags
        
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def delete(self, todo: ToDo) -> bool:
        """Xóa ToDo"""
        self.db.delete(todo)
        self.db.commit()
        return True
