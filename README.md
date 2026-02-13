# ToDo API - FastAPI

REST API quản lý ToDo với FastAPI, SQLAlchemy, JWT Authentication.

## Tính năng

- **CRUD ToDo** - Tạo, đọc, cập nhật, xóa việc cần làm
- **Authentication** - Đăng ký, đăng nhập với JWT
- **Tags** - Gắn nhãn cho các ToDo
- **Due Date** - Đặt deadline cho ToDo
- **Overdue/Today** - Xem việc quá hạn và việc hôm nay
- **Filter/Search/Sort** - Lọc, tìm kiếm, sắp xếp
- **Pagination** - Phân trang kết quả

## Cài đặt

### Yêu cầu

- Python 3.10+
- pip

### Cách 1: Chạy local

```bash
# Clone repository
git clone <repository-url>
cd TH1_TODO_LIST

# Tạo virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
uvicorn main:app --reload
```

Truy cập: http://localhost:8000/docs

### Cách 2: Docker

```bash
# Build và chạy với Docker Compose
docker-compose up -d

# Xem logs
docker-compose logs -f api
```

Truy cập: http://localhost:8000/docs

## API Endpoints

### Authentication

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/v1/auth/register` | Đăng ký tài khoản |
| POST | `/api/v1/auth/login` | Đăng nhập |
| GET | `/api/v1/auth/me` | Thông tin user hiện tại |

### ToDos

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/todos` | Danh sách ToDo (có filter, search, sort, pagination) |
| GET | `/api/v1/todos/overdue` | Danh sách ToDo quá hạn |
| GET | `/api/v1/todos/today` | Danh sách ToDo hôm nay |
| POST | `/api/v1/todos` | Tạo ToDo mới |
| GET | `/api/v1/todos/{id}` | Chi tiết ToDo |
| PUT | `/api/v1/todos/{id}` | Cập nhật toàn bộ ToDo |
| PATCH | `/api/v1/todos/{id}` | Cập nhật một phần ToDo |
| POST | `/api/v1/todos/{id}/complete` | Đánh dấu hoàn thành |
| DELETE | `/api/v1/todos/{id}` | Xóa ToDo |

### Tags

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/tags` | Danh sách Tags |
| POST | `/api/v1/tags` | Tạo Tag mới |
| GET | `/api/v1/tags/{id}` | Chi tiết Tag |
| PUT | `/api/v1/tags/{id}` | Cập nhật Tag |
| DELETE | `/api/v1/tags/{id}` | Xóa Tag |

## Sử dụng

### 1. Đăng ký tài khoản

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Đăng nhập

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Tạo ToDo

```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "Hoàn thành báo cáo",
    "description": "Báo cáo quý 1",
    "due_date": "2026-02-15",
    "tag_ids": [1]
  }'
```

### 4. Lấy danh sách ToDo

```bash
# Tất cả
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/todos

# Lọc chưa hoàn thành
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/todos?is_done=false"

# Tìm kiếm
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/todos?q=báo cáo"

# Sắp xếp theo deadline
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/todos?sort=due_date"
```

## Testing

```bash
# Chạy tất cả tests
pytest

# Chạy với coverage
pytest --cov=app --cov-report=html

# Chạy specific test file
pytest tests/test_todos.py -v
```

## Cấu trúc dự án

```
TH1_TODO_LIST/
├── app/
│   ├── core/           # Config, database, security
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── repositories/   # Data access layer
│   ├── services/       # Business logic
│   └── routers/        # API endpoints
├── tests/              # Test files
├── alembic/            # Database migrations
├── main.py             # Entry point
├── requirements.txt    # Dependencies
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Environment Variables

| Variable | Default | Mô tả |
|----------|---------|-------|
| `DATABASE_URL` | `sqlite:///./todo.db` | Database connection string |
| `SECRET_KEY` | `secret` | JWT secret key |
| `DEBUG` | `true` | Debug mode |

## License

MIT
