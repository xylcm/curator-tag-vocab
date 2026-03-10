"""
Unit tests for repository layer.
"""

import pytest
import sqlite3

from curator_tag_vocab.repositories.database import DatabaseConnection
from curator_tag_vocab.repositories.tag_repository import TagRepository
from curator_tag_vocab.models.tag import TagCreate, TagUpdate, TagFilter


class TestDatabaseConnection:
    """Test cases for DatabaseConnection."""

    def test_init_database(self, tmp_path):
        """Test database initialization."""
        db_path = tmp_path / "test.db"
        db = DatabaseConnection(str(db_path))

        # Verify table was created
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='tags_vocab'"
            )
            assert cursor.fetchone() is not None

    def test_connection_context_manager(self, tmp_path):
        """Test connection context manager."""
        db_path = tmp_path / "test.db"
        db = DatabaseConnection(str(db_path))

        with db.get_connection() as conn:
            assert isinstance(conn, sqlite3.Connection)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            assert cursor.fetchone()[0] == 1


class TestTagRepository:
    """Test cases for TagRepository."""

    @pytest.fixture
    def repo(self, tmp_path):
        """Create a TagRepository with temporary database."""
        db_path = tmp_path / "test.db"
        db = DatabaseConnection(str(db_path))
        return TagRepository(db)

    def test_create_tag(self, repo):
        """Test creating a tag."""
        data = TagCreate(
            tag="test-tag",
            context="Test context",
            category="TestCategory",
            translations={"zh_CN": "测试标签"},
            available=True,
        )

        tag_id = repo.create(data)

        assert tag_id > 0

        # Verify tag was created
        tag = repo.get_by_id(tag_id)
        assert tag is not None
        assert tag.tag == "test-tag"
        assert tag.context == "Test context"

    def test_create_tag_validation_error(self, repo):
        """Test creating tag with invalid data."""
        data = TagCreate(tag="")

        with pytest.raises(ValueError):
            repo.create(data)

    def test_get_by_id_not_found(self, repo):
        """Test getting non-existent tag."""
        tag = repo.get_by_id(99999)
        assert tag is None

    def test_get_by_tag_name(self, repo):
        """Test getting tag by name."""
        data = TagCreate(tag="unique-tag")
        tag_id = repo.create(data)

        tag = repo.get_by_tag_name("unique-tag")

        assert tag is not None
        assert tag.id == tag_id
        assert tag.tag == "unique-tag"

    def test_update_tag(self, repo):
        """Test updating a tag."""
        # Create tag
        data = TagCreate(tag="original-tag", context="Original")
        tag_id = repo.create(data)

        # Update tag
        update_data = TagUpdate(tag="updated-tag", context="Updated")
        success = repo.update(tag_id, update_data)

        assert success is True

        # Verify update
        tag = repo.get_by_id(tag_id)
        assert tag.tag == "updated-tag"
        assert tag.context == "Updated"

    def test_update_nonexistent_tag(self, repo):
        """Test updating non-existent tag."""
        update_data = TagUpdate(tag="new-name")
        success = repo.update(99999, update_data)

        assert success is False

    def test_soft_delete(self, repo):
        """Test soft deleting a tag."""
        # Create tag
        data = TagCreate(tag="delete-me")
        tag_id = repo.create(data)

        # Soft delete
        success = repo.soft_delete(tag_id)

        assert success is True

        # Verify tag is marked as deleted
        tag = repo.get_by_id(tag_id)
        assert tag.is_deleted is True

    def test_list_tags(self, repo):
        """Test listing tags."""
        # Create test tags
        for i in range(5):
            data = TagCreate(tag=f"tag-{i}", available=True)
            repo.create(data)

        filter_obj = TagFilter(page=1, limit=10)
        tags, total = repo.list(filter_obj)

        assert len(tags) == 5
        assert total == 5

    def test_list_tags_with_filter(self, repo):
        """Test listing tags with filter."""
        # Create available and unavailable tags
        repo.create(TagCreate(tag="available-tag", available=True))
        repo.create(TagCreate(tag="unavailable-tag", available=False))

        filter_obj = TagFilter(available=True)
        tags, total = repo.list(filter_obj)

        assert len(tags) == 1
        assert tags[0].tag == "available-tag"

    def test_list_tags_pagination(self, repo):
        """Test tag pagination."""
        # Create 10 tags
        for i in range(10):
            repo.create(TagCreate(tag=f"tag-{i}"))

        # Get page 1 with 5 items
        filter_obj = TagFilter(page=1, limit=5)
        tags, total = repo.list(filter_obj)

        assert len(tags) == 5
        assert total == 10

        # Get page 2
        filter_obj = TagFilter(page=2, limit=5)
        tags, total = repo.list(filter_obj)

        assert len(tags) == 5

    def test_get_stats(self, repo):
        """Test getting statistics."""
        # Create tags
        repo.create(TagCreate(tag="tag-1", available=True))
        repo.create(TagCreate(tag="tag-2", available=True))
        repo.create(TagCreate(tag="tag-3", available=False))

        stats = repo.get_stats()

        assert stats['total'] == 3
        assert stats['available'] == 2
        assert stats['unavailable'] == 1

    def test_get_categories(self, repo):
        """Test getting distinct categories."""
        repo.create(TagCreate(tag="tag-1", category="Category A"))
        repo.create(TagCreate(tag="tag-2", category="Category B"))
        repo.create(TagCreate(tag="tag-3", category="Category A"))

        categories = repo.get_categories()

        assert len(categories) == 2
        assert "Category A" in categories
        assert "Category B" in categories

    def test_get_all_active_tags(self, repo):
        """Test getting all active tags."""
        # Create active tag
        repo.create(TagCreate(tag="active-tag", available=True))

        # Create inactive tag
        repo.create(TagCreate(tag="inactive-tag", available=False))

        # Create deleted tag
        data = TagCreate(tag="deleted-tag", available=True)
        tag_id = repo.create(data)
        repo.soft_delete(tag_id)

        active_tags = repo.get_all_active_tags()

        assert len(active_tags) == 1
        assert active_tags[0].tag == "active-tag"

    def test_clear_all(self, repo):
        """Test clearing all tags."""
        # Create tags
        for i in range(5):
            repo.create(TagCreate(tag=f"tag-{i}"))

        count = repo.clear_all()

        assert count == 5

        # Verify all tags are gone
        tags, total = repo.list(TagFilter())
        assert total == 0
