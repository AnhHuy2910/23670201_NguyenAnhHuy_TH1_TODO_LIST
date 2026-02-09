from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.todo import TagCreate, TagResponse
from app.repositories.tag_repository import TagRepository


class TagService:
    """Service xử lý business logic cho Tag"""
    
    def __init__(self, db: Session):
        self.repository = TagRepository(db)
    
    def get_tag_or_404(self, tag_id: int, owner_id: int):
        """Lấy Tag theo ID và owner hoặc raise 404"""
        tag = self.repository.get_by_id(tag_id, owner_id)
        if not tag:
            raise HTTPException(status_code=404, detail=f"Tag với id={tag_id} không tìm thấy")
        return tag
    
    def get_tags(self, owner_id: int) -> list[TagResponse]:
        """Lấy tất cả tags của owner"""
        tags = self.repository.get_all(owner_id)
        return [TagResponse.model_validate(tag) for tag in tags]
    
    def get_tag(self, tag_id: int, owner_id: int) -> TagResponse:
        """Lấy chi tiết một tag"""
        tag = self.get_tag_or_404(tag_id, owner_id)
        return TagResponse.model_validate(tag)
    
    def create_tag(self, tag_data: TagCreate, owner_id: int) -> TagResponse:
        """Tạo tag mới"""
        # Kiểm tra tag trùng tên
        existing = self.repository.get_by_name(tag_data.name, owner_id)
        if existing:
            raise HTTPException(status_code=400, detail=f"Tag '{tag_data.name}' đã tồn tại")
        
        tag = self.repository.create(
            name=tag_data.name,
            color=tag_data.color,
            owner_id=owner_id
        )
        return TagResponse.model_validate(tag)
    
    def update_tag(self, tag_id: int, tag_data: TagCreate, owner_id: int) -> TagResponse:
        """Cập nhật tag"""
        tag = self.get_tag_or_404(tag_id, owner_id)
        
        # Kiểm tra trùng tên với tag khác
        existing = self.repository.get_by_name(tag_data.name, owner_id)
        if existing and existing.id != tag_id:
            raise HTTPException(status_code=400, detail=f"Tag '{tag_data.name}' đã tồn tại")
        
        updated_tag = self.repository.update(
            tag,
            name=tag_data.name,
            color=tag_data.color
        )
        return TagResponse.model_validate(updated_tag)
    
    def delete_tag(self, tag_id: int, owner_id: int) -> None:
        """Xóa tag"""
        tag = self.get_tag_or_404(tag_id, owner_id)
        self.repository.delete(tag)
