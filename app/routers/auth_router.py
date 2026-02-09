from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency để lấy AuthService"""
    return AuthService(db)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    """Đăng ký tài khoản mới"""
    return service.register(user_data)


@router.post("/login", response_model=Token)
def login(
    user_data: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    """Đăng nhập và lấy access token"""
    return service.login(user_data)


@router.post("/login/form", response_model=Token)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
):
    """Đăng nhập bằng form (cho Swagger UI)"""
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    return service.login(user_data)


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
):
    """Lấy thông tin user hiện tại"""
    return service.get_current_user_info(current_user)
