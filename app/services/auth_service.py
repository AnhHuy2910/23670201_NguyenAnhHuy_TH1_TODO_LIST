from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.config import settings


class AuthService:
    """Service xử lý authentication"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register(self, user_data: UserCreate) -> UserResponse:
        """Đăng ký user mới"""
        # Kiểm tra email đã tồn tại
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã được sử dụng"
            )
        
        user = self.repository.create(
            email=user_data.email,
            password=user_data.password
        )
        return UserResponse.model_validate(user)
    
    def login(self, user_data: UserLogin) -> Token:
        """Đăng nhập và trả về token"""
        user = self.repository.get_by_email(user_data.email)
        
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không đúng",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tài khoản đã bị vô hiệu hóa"
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    def get_current_user_info(self, user) -> UserResponse:
        """Lấy thông tin user hiện tại"""
        return UserResponse.model_validate(user)
