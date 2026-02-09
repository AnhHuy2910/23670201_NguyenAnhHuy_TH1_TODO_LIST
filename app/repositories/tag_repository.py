from typing import Optional
from sqlalchemy.orm import Session
from app.models.todo import Tag


class TagRepository:
    """Repository quản lý dữ liệu Tag với SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, owner_id: int) -> list[Tag]:
        """Lấy tất cả tags của owner"""
        return self.db.query(Tag).filter(Tag.owner_id == owner_id).all()
    
    def get_by_id(self, tag_id: int, owner_id: int) -> Optional[Tag]:
        """Lấy tag theo ID và owner_id"""
        return self.db.query(Tag).filter(
            Tag.id == tag_id,
            Tag.owner_id == owner_id
        ).first()
    
    def get_by_name(self, name: str, owner_id: int) -> Optional[Tag]:
        """Tìm tag theo tên"""
        return self.db.query(Tag).filter(
            Tag.name == name,
            Tag.owner_id == owner_id
        ).first()
    
    def create(self, name: str, owner_id: int, color: str = "#3B82F6") -> Tag:
        """Tạo tag mới"""
        new_tag = Tag(name=name, color=color, owner_id=owner_id)
        self.db.add(new_tag)
        self.db.commit()
        self.db.refresh(new_tag)
        return new_tag
    
    def update(self, tag: Tag, **kwargs) -> Tag:
        """Cập nhật tag"""
        for key, value in kwargs.items():
            if value is not None and hasattr(tag, key):
                setattr(tag, key, value)
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def delete(self, tag: Tag) -> bool:
        """Xóa tag"""
        self.db.delete(tag)
        self.db.commit()
        return True
