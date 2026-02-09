"""
Tests for authentication endpoints
"""
import pytest


class TestAuthRegister:
    """Tests for POST /api/v1/auth/register"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "newuser@example.com", "password": "password123"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "hashed_password" not in data
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with existing email"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "password123"}
        )
        assert response.status_code == 400
        assert "đã được sử dụng" in response.json()["detail"]
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "invalid-email", "password": "password123"}
        )
        assert response.status_code == 422
    
    def test_register_short_password(self, client):
        """Test registration with short password"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "user@example.com", "password": "123"}
        )
        assert response.status_code == 422


class TestAuthLogin:
    """Tests for POST /api/v1/auth/login"""
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "không đúng" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"}
        )
        assert response.status_code == 401


class TestAuthMe:
    """Tests for GET /api/v1/auth/me"""
    
    def test_get_me_success(self, client, auth_headers):
        """Test get current user info"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
    
    def test_get_me_unauthorized(self, client):
        """Test get current user without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_get_me_invalid_token(self, client):
        """Test get current user with invalid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
