from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import todo_router, health_router, auth_router

# Tạo tất cả tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Include routers
app.include_router(health_router)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(todo_router, prefix=settings.API_V1_PREFIX)
