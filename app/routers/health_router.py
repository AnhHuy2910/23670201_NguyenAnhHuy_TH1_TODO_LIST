from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def root():
    """Endpoint chào mừng"""
    return {"message": "Chào mừng đến với To-Do API!"}


@router.get("/health")
def health_check():
    """Endpoint kiểm tra trạng thái server"""
    return {"status": "ok"}
