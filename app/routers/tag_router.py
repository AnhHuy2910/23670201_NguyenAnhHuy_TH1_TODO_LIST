from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.todo import TagCreate, TagResponse
from app.services.tag_service import TagService
from app.models.user import User

router = APIRouter(prefix="/tags", tags=["Tags"])


def get_tag_service(db: Session = Depends(get_db)) -> TagService:
    """Dependency để lấy TagService"""
    return TagService(db)


@router.post("", response_model=TagResponse, status_code=201)
def create_tag(
    tag: TagCreate,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Tạo tag mới"""
    return service.create_tag(tag, owner_id=current_user.id)


@router.get("", response_model=list[TagResponse])
def get_tags(
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Lấy danh sách tags của user"""
    return service.get_tags(owner_id=current_user.id)


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Lấy chi tiết một tag"""
    return service.get_tag(tag_id, owner_id=current_user.id)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag_update: TagCreate,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Cập nhật tag"""
    return service.update_tag(tag_id, tag_update, owner_id=current_user.id)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Xóa tag"""
    service.delete_tag(tag_id, owner_id=current_user.id)
    return None
