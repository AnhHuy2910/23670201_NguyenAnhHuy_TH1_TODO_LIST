"""
Tests for ToDo CRUD endpoints
"""
import pytest
from datetime import date, timedelta


class TestCreateTodo:
    """Tests for POST /api/v1/todos"""
    
    def test_create_todo_success(self, client, auth_headers):
        """Test successful todo creation"""
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "New Todo", "description": "Description"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Todo"
        assert data["description"] == "Description"
        assert data["is_done"] == False
        assert "id" in data
        assert "created_at" in data
    
    def test_create_todo_with_due_date(self, client, auth_headers):
        """Test create todo with due date"""
        due = (date.today() + timedelta(days=7)).isoformat()
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Todo with deadline", "due_date": due}
        )
        assert response.status_code == 201
        assert response.json()["due_date"] == due
    
    def test_create_todo_with_tags(self, client, auth_headers, test_tag):
        """Test create todo with tags"""
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Todo with tag", "tag_ids": [test_tag.id]}
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data["tags"]) == 1
        assert data["tags"][0]["name"] == "Test Tag"
    
    def test_create_todo_validation_title_too_short(self, client, auth_headers):
        """Test create todo with title too short"""
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "AB"}  # < 3 chars
        )
        assert response.status_code == 422
    
    def test_create_todo_validation_title_too_long(self, client, auth_headers):
        """Test create todo with title too long"""
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "A" * 101}  # > 100 chars
        )
        assert response.status_code == 422
    
    def test_create_todo_unauthorized(self, client):
        """Test create todo without auth"""
        response = client.post(
            "/api/v1/todos",
            json={"title": "Unauthorized Todo"}
        )
        assert response.status_code == 401


class TestGetTodos:
    """Tests for GET /api/v1/todos"""
    
    def test_get_todos_empty(self, client, auth_headers):
        """Test get todos when empty"""
        response = client.get("/api/v1/todos", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
    
    def test_get_todos_with_data(self, client, auth_headers, test_todo):
        """Test get todos with data"""
        response = client.get("/api/v1/todos", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Test Todo"
    
    def test_get_todos_filter_is_done(self, client, auth_headers, test_todo):
        """Test filter todos by is_done"""
        response = client.get(
            "/api/v1/todos?is_done=false",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["total"] == 1
        
        response = client.get(
            "/api/v1/todos?is_done=true",
            headers=auth_headers
        )
        assert response.json()["total"] == 0
    
    def test_get_todos_search(self, client, auth_headers, test_todo):
        """Test search todos by title"""
        response = client.get(
            "/api/v1/todos?q=Test",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["total"] == 1
        
        response = client.get(
            "/api/v1/todos?q=NotFound",
            headers=auth_headers
        )
        assert response.json()["total"] == 0
    
    def test_get_todos_pagination(self, client, auth_headers):
        """Test todos pagination"""
        # Create 5 todos
        for i in range(5):
            client.post(
                "/api/v1/todos",
                headers=auth_headers,
                json={"title": f"Todo {i+1}"}
            )
        
        response = client.get(
            "/api/v1/todos?limit=2&offset=0",
            headers=auth_headers
        )
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5


class TestGetTodoById:
    """Tests for GET /api/v1/todos/{id}"""
    
    def test_get_todo_success(self, client, auth_headers, test_todo):
        """Test get single todo"""
        response = client.get(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Test Todo"
    
    def test_get_todo_not_found(self, client, auth_headers):
        """Test get non-existent todo"""
        response = client.get(
            "/api/v1/todos/9999",
            headers=auth_headers
        )
        assert response.status_code == 404


class TestUpdateTodo:
    """Tests for PUT /api/v1/todos/{id}"""
    
    def test_update_todo_success(self, client, auth_headers, test_todo):
        """Test update todo"""
        response = client.put(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers,
            json={"title": "Updated Title", "is_done": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["is_done"] == True
    
    def test_update_todo_not_found(self, client, auth_headers):
        """Test update non-existent todo"""
        response = client.put(
            "/api/v1/todos/9999",
            headers=auth_headers,
            json={"title": "Updated"}
        )
        assert response.status_code == 404


class TestPatchTodo:
    """Tests for PATCH /api/v1/todos/{id}"""
    
    def test_patch_todo_partial(self, client, auth_headers, test_todo):
        """Test partial update todo"""
        response = client.patch(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers,
            json={"is_done": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_done"] == True
        assert data["title"] == "Test Todo"  # unchanged


class TestCompleteTodo:
    """Tests for POST /api/v1/todos/{id}/complete"""
    
    def test_complete_todo(self, client, auth_headers, test_todo):
        """Test mark todo as complete"""
        response = client.post(
            f"/api/v1/todos/{test_todo.id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["is_done"] == True


class TestDeleteTodo:
    """Tests for DELETE /api/v1/todos/{id}"""
    
    def test_delete_todo_success(self, client, auth_headers, test_todo):
        """Test delete todo"""
        response = client.delete(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify deleted
        response = client.get(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_delete_todo_not_found(self, client, auth_headers):
        """Test delete non-existent todo"""
        response = client.delete(
            "/api/v1/todos/9999",
            headers=auth_headers
        )
        assert response.status_code == 404


class TestOverdueAndToday:
    """Tests for overdue and today endpoints"""
    
    def test_get_overdue_todos(self, client, auth_headers):
        """Test get overdue todos"""
        # Create overdue todo
        past_date = (date.today() - timedelta(days=1)).isoformat()
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Overdue todo", "due_date": past_date}
        )
        
        response = client.get("/api/v1/todos/overdue", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1
    
    def test_get_today_todos(self, client, auth_headers):
        """Test get today todos"""
        today = date.today().isoformat()
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Today todo", "due_date": today}
        )
        
        response = client.get("/api/v1/todos/today", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1
