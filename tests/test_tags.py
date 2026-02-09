"""
Tests for Tag endpoints
"""
import pytest


class TestCreateTag:
    """Tests for POST /api/v1/tags"""
    
    def test_create_tag_success(self, client, auth_headers):
        """Test successful tag creation"""
        response = client.post(
            "/api/v1/tags",
            headers=auth_headers,
            json={"name": "Work", "color": "#FF5733"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Work"
        assert data["color"] == "#FF5733"
        assert "id" in data
    
    def test_create_tag_default_color(self, client, auth_headers):
        """Test create tag with default color"""
        response = client.post(
            "/api/v1/tags",
            headers=auth_headers,
            json={"name": "Personal"}
        )
        assert response.status_code == 201
        assert response.json()["color"] == "#3B82F6"
    
    def test_create_tag_duplicate_name(self, client, auth_headers, test_tag):
        """Test create tag with duplicate name"""
        response = client.post(
            "/api/v1/tags",
            headers=auth_headers,
            json={"name": "Test Tag"}
        )
        assert response.status_code == 400
        assert "đã tồn tại" in response.json()["detail"]
    
    def test_create_tag_invalid_color(self, client, auth_headers):
        """Test create tag with invalid color format"""
        response = client.post(
            "/api/v1/tags",
            headers=auth_headers,
            json={"name": "Invalid", "color": "red"}  # Not hex format
        )
        assert response.status_code == 422
    
    def test_create_tag_unauthorized(self, client):
        """Test create tag without auth"""
        response = client.post(
            "/api/v1/tags",
            json={"name": "Unauthorized"}
        )
        assert response.status_code == 401


class TestGetTags:
    """Tests for GET /api/v1/tags"""
    
    def test_get_tags_empty(self, client, auth_headers):
        """Test get tags when empty"""
        response = client.get("/api/v1/tags", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_tags_with_data(self, client, auth_headers, test_tag):
        """Test get tags with data"""
        response = client.get("/api/v1/tags", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Tag"


class TestGetTagById:
    """Tests for GET /api/v1/tags/{id}"""
    
    def test_get_tag_success(self, client, auth_headers, test_tag):
        """Test get single tag"""
        response = client.get(
            f"/api/v1/tags/{test_tag.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Test Tag"
    
    def test_get_tag_not_found(self, client, auth_headers):
        """Test get non-existent tag"""
        response = client.get(
            "/api/v1/tags/9999",
            headers=auth_headers
        )
        assert response.status_code == 404


class TestUpdateTag:
    """Tests for PUT /api/v1/tags/{id}"""
    
    def test_update_tag_success(self, client, auth_headers, test_tag):
        """Test update tag"""
        response = client.put(
            f"/api/v1/tags/{test_tag.id}",
            headers=auth_headers,
            json={"name": "Updated Tag", "color": "#00FF00"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Tag"
        assert data["color"] == "#00FF00"
    
    def test_update_tag_not_found(self, client, auth_headers):
        """Test update non-existent tag"""
        response = client.put(
            "/api/v1/tags/9999",
            headers=auth_headers,
            json={"name": "Updated", "color": "#000000"}
        )
        assert response.status_code == 404


class TestDeleteTag:
    """Tests for DELETE /api/v1/tags/{id}"""
    
    def test_delete_tag_success(self, client, auth_headers, test_tag):
        """Test delete tag"""
        response = client.delete(
            f"/api/v1/tags/{test_tag.id}",
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify deleted
        response = client.get(
            f"/api/v1/tags/{test_tag.id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_delete_tag_not_found(self, client, auth_headers):
        """Test delete non-existent tag"""
        response = client.delete(
            "/api/v1/tags/9999",
            headers=auth_headers
        )
        assert response.status_code == 404
