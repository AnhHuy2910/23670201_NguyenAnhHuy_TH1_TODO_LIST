from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash


class UserRepository:
    """Repository quản lý dữ liệu User"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Lấy User theo ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Lấy User theo email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, email: str, password: str) -> User:
        """Tạo User mới"""
        hashed_password = get_password_hash(password)
        new_user = User(email=email, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update(self, user: User, **kwargs) -> User:
        """Cập nhật User"""
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
