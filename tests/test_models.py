"""Tests for models module."""

import pytest
from datetime import datetime

from src.models.tag import Tag, TagList, TagStats
from src.models.schemas import TagCreate, TagUpdate, ExportFormat


class TestTag:
    """Test Tag model."""

    def test_tag_creation(self):
        """Test creating a Tag instance."""
        tag = Tag(
            id=1,
            tag="test-tag",
            context="Test context",
            category="TestCategory",
            sub_category="SubCategory",
            translations={"zh_CN": "测试"},
            available=True,
        )
        assert tag.id == 1
        assert tag.tag == "test-tag"
        assert tag.context == "Test context"
        assert tag.category == "TestCategory"
        assert tag.sub_category == "SubCategory"
        assert tag.translations == {"zh_CN": "测试"}
        assert tag.available is True

    def test_tag_from_row(self):
        """Test creating Tag from database row."""
        row = {
            "id": 1,
            "tag": "test-tag",
            "context": "Test context",
            "category": "TestCategory",
            "sub_category": "SubCategory",
            "translations": '{"zh_CN": "测试"}',
            "available": 1,
            "is_deleted": 0,
            "created_at": "2024-01-01 00:00:00",
            "updated_at": "2024-01-01 00:00:00",
        }
        tag = Tag.from_row(row)
        assert tag.id == 1
        assert tag.tag == "test-tag"
        assert tag.translations == {"zh_CN": "测试"}
        assert tag.available is True
        assert tag.is_deleted is False

    def test_tag_from_row_empty_translations(self):
        """Test creating Tag with empty translations."""
        row = {
            "id": 1,
            "tag": "test-tag",
            "context": None,
            "category": None,
            "sub_category": None,
            "translations": None,
            "available": 0,
            "is_deleted": 0,
        }
        tag = Tag.from_row(row)
        assert tag.translations == {}
        assert tag.context == ""
        assert tag.available is False

    def test_tag_to_dict(self):
        """Test converting Tag to dictionary."""
        tag = Tag(
            id=1,
            tag="test-tag",
            context="Test context",
            category="TestCategory",
            translations={"zh_CN": "测试"},
            available=True,
        )
        data = tag.to_dict()
        assert data["id"] == 1
        assert data["tag"] == "test-tag"
        assert data["translations"] == {"zh_CN": "测试"}
        assert data["available"] is True


class TestTagList:
    """Test TagList model."""

    def test_tag_list_creation(self):
        """Test creating TagList."""
        tags = [
            Tag(id=1, tag="tag1"),
            Tag(id=2, tag="tag2"),
        ]
        tag_list = TagList(tags=tags, page=1, page_size=10, total=20)
        assert tag_list.tags == tags
        assert tag_list.page == 1
        assert tag_list.page_size == 10
        assert tag_list.total == 20

    def test_total_pages_calculation(self):
        """Test total pages calculation."""
        # Exact division
        tag_list = TagList(tags=[], page=1, page_size=10, total=20)
        assert tag_list.total_pages == 2

        # With remainder
        tag_list = TagList(tags=[], page=1, page_size=10, total=25)
        assert tag_list.total_pages == 3

        # Zero total
        tag_list = TagList(tags=[], page=1, page_size=10, total=0)
        assert tag_list.total_pages == 0

    def test_to_dict(self):
        """Test converting TagList to dictionary."""
        tags = [Tag(id=1, tag="tag1")]
        tag_list = TagList(tags=tags, page=1, page_size=10, total=1)
        data = tag_list.to_dict()
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["total"] == 1
        assert data["total_pages"] == 1
        assert len(data["tags"]) == 1


class TestTagStats:
    """Test TagStats model."""

    def test_tag_stats_creation(self):
        """Test creating TagStats."""
        stats = TagStats(total=100, available=80, unavailable=20, deleted=5)
        assert stats.total == 100
        assert stats.available == 80
        assert stats.unavailable == 20
        assert stats.deleted == 5

    def test_tag_stats_defaults(self):
        """Test TagStats default values."""
        stats = TagStats()
        assert stats.total == 0
        assert stats.available == 0
        assert stats.unavailable == 0
        assert stats.deleted == 0

    def test_to_dict(self):
        """Test converting TagStats to dictionary."""
        stats = TagStats(total=100, available=80, unavailable=20, deleted=5)
        data = stats.to_dict()
        assert data == {
            "total": 100,
            "available": 80,
            "unavailable": 20,
            "deleted": 5,
        }


class TestTagCreate:
    """Test TagCreate schema."""

    def test_tag_create_creation(self):
        """Test creating TagCreate."""
        schema = TagCreate(
            tag="test-tag",
            context="Test context",
            category="TestCategory",
            translations={"zh_CN": "测试"},
            available=True,
        )
        assert schema.tag == "test-tag"
        assert schema.context == "Test context"
        assert schema.available is True

    def test_tag_create_defaults(self):
        """Test TagCreate default values."""
        schema = TagCreate(tag="test-tag")
        assert schema.tag == "test-tag"
        assert schema.context == ""
        assert schema.category == ""
        assert schema.translations == {}
        assert schema.available is True

    def test_tag_create_validation(self):
        """Test TagCreate validation."""
        # Valid tag
        schema = TagCreate(tag="valid-tag")
        schema.validate()  # Should not raise

        # Empty tag
        schema = TagCreate(tag="")
        with pytest.raises(ValueError, match="Tag name is required"):
            schema.validate()

        # Whitespace-only tag
        schema = TagCreate(tag="   ")
        with pytest.raises(ValueError, match="Tag name is required"):
            schema.validate()

        # Too long tag
        schema = TagCreate(tag="x" * 256)
        with pytest.raises(ValueError, match="less than 255"):
            schema.validate()


class TestTagUpdate:
    """Test TagUpdate schema."""

    def test_tag_update_creation(self):
        """Test creating TagUpdate."""
        schema = TagUpdate(tag="new-tag", available=False)
        assert schema.tag == "new-tag"
        assert schema.available is False

    def test_tag_update_partial(self):
        """Test partial TagUpdate."""
        schema = TagUpdate(tag="new-tag")
        assert schema.tag == "new-tag"
        assert schema.context is None
        assert schema.available is None

    def test_tag_update_validation(self):
        """Test TagUpdate validation."""
        # Valid update
        schema = TagUpdate(tag="valid-tag")
        schema.validate()  # Should not raise

        # Empty tag
        schema = TagUpdate(tag="")
        with pytest.raises(ValueError, match="cannot be empty"):
            schema.validate()

        # Whitespace-only tag
        schema = TagUpdate(tag="   ")
        with pytest.raises(ValueError, match="cannot be empty"):
            schema.validate()

    def test_to_dict(self):
        """Test converting to dictionary."""
        schema = TagUpdate(tag="new-tag", context="New context", available=True)
        data = schema.to_dict()
        assert data["tag"] == "new-tag"
        assert data["context"] == "New context"
        assert data["available"] == 1

        # None values should be excluded
        schema = TagUpdate(tag="new-tag")
        data = schema.to_dict()
        assert "context" not in data
        assert "available" not in data


class TestExportFormat:
    """Test ExportFormat enum."""

    def test_export_format_values(self):
        """Test export format values."""
        assert ExportFormat.PROTOBUF == "protobuf"
        assert ExportFormat.CSV == "csv"
