"""Tests for repositories module."""

import pytest

from src.models.tag import Tag
from src.repositories.tag_repository import TagRepository
from src.core.exceptions import DatabaseException


class TestTagRepository:
    """Test TagRepository."""

    def test_create_tag(self, tag_repo):
        """Test creating a tag."""
        tag_id = tag_repo.create(
            tag="test-tag",
            context="Test context",
            category="TestCategory",
            translations={"zh_CN": "测试"},
            available=1,
        )
        assert tag_id is not None
        assert tag_id > 0

        # Verify tag was created
        tag = tag_repo.get_by_id(tag_id)
        assert tag.tag == "test-tag"
        assert tag.context == "Test context"
        assert tag.translations == {"zh_CN": "测试"}

    def test_get_by_id(self, tag_repo):
        """Test getting tag by ID."""
        # Create a tag first
        tag_id = tag_repo.create(tag="test-tag")

        # Get the tag
        tag = tag_repo.get_by_id(tag_id)
        assert tag is not None
        assert tag.id == tag_id
        assert tag.tag == "test-tag"

    def test_get_by_id_not_found(self, tag_repo):
        """Test getting non-existent tag."""
        tag = tag_repo.get_by_id(99999)
        assert tag is None

    def test_get_by_tag_name(self, tag_repo):
        """Test getting tag by name."""
        tag_repo.create(tag="unique-tag")

        tag = tag_repo.get_by_tag_name("unique-tag")
        assert tag is not None
        assert tag.tag == "unique-tag"

    def test_get_by_tag_name_not_found(self, tag_repo):
        """Test getting non-existent tag by name."""
        tag = tag_repo.get_by_tag_name("non-existent")
        assert tag is None

    def test_list_tags(self, tag_repo):
        """Test listing tags."""
        # Create some tags
        tag_repo.create(tag="tag1", available=1)
        tag_repo.create(tag="tag2", available=0)
        tag_repo.create(tag="tag3", available=1)

        result = tag_repo.list()
        assert len(result.tags) == 3
        assert result.total == 3
        assert result.page == 1

    def test_list_with_filter_available(self, tag_repo):
        """Test listing tags with available filter."""
        tag_repo.create(tag="available-tag", available=1)
        tag_repo.create(tag="unavailable-tag", available=0)

        result = tag_repo.list(available=True)
        assert len(result.tags) == 1
        assert result.tags[0].tag == "available-tag"

    def test_list_with_search(self, tag_repo):
        """Test listing tags with search."""
        tag_repo.create(tag="apple", context="Fruit")
        tag_repo.create(tag="banana", context="Yellow fruit")
        tag_repo.create(tag="car", context="Vehicle")

        result = tag_repo.list(search="fruit")
        assert len(result.tags) == 2

    def test_list_with_category(self, tag_repo):
        """Test listing tags with category filter."""
        tag_repo.create(tag="tag1", category="CategoryA")
        tag_repo.create(tag="tag2", category="CategoryB")

        result = tag_repo.list(category="CategoryA")
        assert len(result.tags) == 1
        assert result.tags[0].tag == "tag1"

    def test_list_pagination(self, tag_repo):
        """Test tag list pagination."""
        # Create 5 tags
        for i in range(5):
            tag_repo.create(tag=f"tag{i}")

        result = tag_repo.list(page=1, page_size=2)
        assert len(result.tags) == 2
        assert result.total == 5
        assert result.total_pages == 3

    def test_update_tag(self, tag_repo):
        """Test updating a tag."""
        tag_id = tag_repo.create(tag="old-tag", context="Old context")

        success = tag_repo.update(tag_id, tag="new-tag", context="New context")
        assert success is True

        tag = tag_repo.get_by_id(tag_id)
        assert tag.tag == "new-tag"
        assert tag.context == "New context"

    def test_update_tag_not_found(self, tag_repo):
        """Test updating non-existent tag."""
        success = tag_repo.update(99999, tag="new-tag")
        assert success is False

    def test_soft_delete(self, tag_repo):
        """Test soft deleting a tag."""
        tag_id = tag_repo.create(tag="to-delete")

        success = tag_repo.soft_delete(tag_id)
        assert success is True

        # Tag should still exist but be marked as deleted
        tag = tag_repo.get_by_id(tag_id)
        assert tag.is_deleted is True

    def test_soft_delete_not_found(self, tag_repo):
        """Test soft deleting non-existent tag."""
        success = tag_repo.soft_delete(99999)
        assert success is False

    def test_hard_delete(self, tag_repo):
        """Test hard deleting a tag."""
        tag_id = tag_repo.create(tag="to-delete")

        success = tag_repo.delete(tag_id)
        assert success is True

        # Tag should no longer exist
        tag = tag_repo.get_by_id(tag_id)
        assert tag is None

    def test_get_stats(self, tag_repo):
        """Test getting statistics."""
        # Create tags with different states
        tag_repo.create(tag="available", available=1)
        tag_repo.create(tag="unavailable", available=0)
        deleted_id = tag_repo.create(tag="deleted")
        tag_repo.soft_delete(deleted_id)

        # Test with is_deleted=False filter
        stats = tag_repo.get_stats(is_deleted=False)
        assert stats.total == 2  # Only non-deleted
        assert stats.available == 1
        assert stats.unavailable == 1
        assert stats.deleted == 1

        # Test without filter (all records)
        stats_all = tag_repo.get_stats()
        assert stats_all.total == 3  # All including deleted
        assert stats_all.deleted == 1

    def test_get_all_available(self, tag_repo):
        """Test getting all available tags."""
        tag_repo.create(tag="available1", available=1)
        tag_repo.create(tag="available2", available=1)
        tag_repo.create(tag="unavailable", available=0)
        deleted_id = tag_repo.create(tag="deleted", available=1)
        tag_repo.soft_delete(deleted_id)

        tags = tag_repo.get_all_available()
        assert len(tags) == 2
        assert all(t.available for t in tags)
        assert all(not t.is_deleted for t in tags)

    def test_get_distinct_categories(self, tag_repo):
        """Test getting distinct categories."""
        tag_repo.create(tag="tag1", category="CategoryA")
        tag_repo.create(tag="tag2", category="CategoryB")
        tag_repo.create(tag="tag3", category="CategoryA")  # Duplicate
        tag_repo.create(tag="tag4", category="")  # Empty
        tag_repo.create(tag="tag5", category=None)  # None

        categories = tag_repo.get_distinct_categories()
        assert len(categories) == 2
        assert "CategoryA" in categories
        assert "CategoryB" in categories

    def test_clear(self, tag_repo):
        """Test clearing all tags."""
        tag_repo.create(tag="tag1")
        tag_repo.create(tag="tag2")

        count = tag_repo.clear()
        assert count == 2

        result = tag_repo.list()
        assert len(result.tags) == 0

    def test_invalid_field_update(self, tag_repo):
        """Test updating with invalid field."""
        tag_id = tag_repo.create(tag="test")

        with pytest.raises(ValueError, match="Invalid fields"):
            tag_repo.update(tag_id, invalid_field="value")
