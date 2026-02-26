"""Tests for API routes."""

import json
import pytest


class TestIndexRoute:
    """Test index route."""

    def test_index_page(self, client):
        """Test main page loads."""
        response = client.get("/tagging/vocab/")
        assert response.status_code == 200


class TestStatsRoutes:
    """Test stats routes."""

    def test_get_stats(self, client, tag_repo):
        """Test getting statistics."""
        # Create some tags
        tag_repo.create(tag="tag1", available=1)
        tag_repo.create(tag="tag2", available=0)

        response = client.get("/tagging/vocab/api/stats")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "total" in data
        assert "available" in data
        assert "unavailable" in data
        assert "deleted" in data

    def test_get_stats_with_filter(self, client, tag_repo):
        """Test getting stats with deleted filter."""
        tag_repo.create(tag="tag1")
        deleted_id = tag_repo.create(tag="deleted-tag")
        tag_repo.soft_delete(deleted_id)

        response = client.get("/tagging/vocab/api/stats?deleted=deleted")
        assert response.status_code == 200


class TestCategoryRoutes:
    """Test category routes."""

    def test_get_categories(self, client, tag_repo):
        """Test getting categories from tags."""
        tag_repo.create(tag="tag1", category="CategoryA")
        tag_repo.create(tag="tag2", category="CategoryB")

        response = client.get("/tagging/vocab/api/categories")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "categories" in data
        assert "CategoryA" in data["categories"]
        assert "CategoryB" in data["categories"]

    def test_get_categories_config(self, client):
        """Test getting categories config."""
        response = client.get("/tagging/vocab/api/categories/config")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "categories" in data


class TestTagRoutes:
    """Test tag CRUD routes."""

    def test_list_tags(self, client, tag_repo):
        """Test listing tags."""
        tag_repo.create(tag="tag1", available=1)
        tag_repo.create(tag="tag2", available=1)

        response = client.get("/tagging/vocab/api/tags")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "tags" in data
        assert "total" in data
        assert "page" in data
        assert data["total"] == 2

    def test_list_tags_with_pagination(self, client, tag_repo):
        """Test tag list pagination."""
        for i in range(5):
            tag_repo.create(tag=f"tag{i}")

        response = client.get("/tagging/vocab/api/tags?page=1&limit=2")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data["tags"]) == 2
        assert data["total_pages"] == 3

    def test_list_tags_with_search(self, client, tag_repo):
        """Test searching tags."""
        tag_repo.create(tag="apple", context="Fruit")
        tag_repo.create(tag="banana", context="Yellow fruit")
        tag_repo.create(tag="car", context="Vehicle")

        response = client.get("/tagging/vocab/api/tags?search=fruit")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["total"] == 2

    def test_create_tag(self, client):
        """Test creating a tag."""
        import uuid
        payload = {
            "tag": f"new-tag-{uuid.uuid4().hex[:8]}",
            "context": "Test context",
            "category": "TestCategory",
            "available": True,
        }

        response = client.post(
            "/tagging/vocab/api/tags",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data["success"] is True
        assert "id" in data

    def test_create_tag_no_data(self, client):
        """Test creating tag without data."""
        response = client.post(
            "/tagging/vocab/api/tags",
            data="",
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_create_tag_validation_error(self, client):
        """Test creating tag with invalid data."""
        payload = {"tag": ""}

        response = client.post(
            "/tagging/vocab/api/tags",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_get_tag(self, client, tag_repo):
        """Test getting a single tag."""
        tag_id = tag_repo.create(tag="test-tag", available=1)

        response = client.get(f"/tagging/vocab/api/tags/{tag_id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["tag"] == "test-tag"

    def test_get_tag_not_found(self, client):
        """Test getting non-existent tag."""
        response = client.get("/tagging/vocab/api/tags/99999")
        assert response.status_code == 404

    def test_update_tag(self, client, tag_repo):
        """Test updating a tag."""
        tag_id = tag_repo.create(tag="old-tag", available=1)

        payload = {"tag": "updated-tag", "context": "Updated context"}

        response = client.put(
            f"/tagging/vocab/api/tags/{tag_id}",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True

    def test_update_tag_not_found(self, client):
        """Test updating non-existent tag."""
        payload = {"tag": "new-tag"}

        response = client.put(
            "/tagging/vocab/api/tags/99999",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_update_tag_no_data(self, client, tag_repo):
        """Test updating tag without data."""
        tag_id = tag_repo.create(tag="test-tag")

        response = client.put(
            f"/tagging/vocab/api/tags/{tag_id}",
            data="",
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_delete_tag(self, client, tag_repo):
        """Test deleting a tag."""
        tag_id = tag_repo.create(tag="to-delete", available=1)

        response = client.delete(f"/tagging/vocab/api/tags/{tag_id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True

        # Verify tag is soft deleted
        tag = tag_repo.get_by_id(tag_id)
        assert tag.is_deleted is True

    def test_delete_tag_not_found(self, client):
        """Test deleting non-existent tag."""
        response = client.delete("/tagging/vocab/api/tags/99999")
        assert response.status_code == 404


class TestExportRoutes:
    """Test export routes."""

    def test_export_csv(self, client, tag_repo):
        """Test CSV export."""
        tag_repo.create(tag="test-tag", available=1)

        response = client.get("/tagging/vocab/api/export/csv")
        assert response.status_code == 200
        assert response.content_type == "text/csv; charset=utf-8"

    def test_export_protobuf(self, client, tag_repo):
        """Test Protobuf export."""
        tag_repo.create(tag="test-tag", available=1)

        response = client.get("/tagging/vocab/api/export/protobuf")
        assert response.status_code == 200
        assert response.content_type == "application/octet-stream"


class TestErrorHandling:
    """Test error handling."""

    def test_not_found_error(self, client):
        """Test 404 error handling."""
        response = client.get("/tagging/vocab/api/tags/99999")
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "error" in data

    def test_validation_error(self, client):
        """Test validation error handling."""
        payload = {"tag": ""}

        response = client.post(
            "/tagging/vocab/api/tags",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "error" in data
