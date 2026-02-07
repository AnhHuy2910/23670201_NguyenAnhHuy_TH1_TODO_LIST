from fastapi import FastAPI

app = FastAPI(title="Hello To-Do API")


@app.get("/")
def root():
    """Endpoint chào mừng"""
    return {"message": "Chào mừng đến với To-Do API!"}


@app.get("/health")
def health_check():
    """Endpoint kiểm tra trạng thái server"""
    return {"status": "ok"}
