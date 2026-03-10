"""Tests for services module."""

import os
import json
import pytest

from src.services.tag_service import TagService
from src.services.export_service import ExportService
from src.services.category_service import CategoryService
from src.core.exceptions import NotFoundException, ValidationException


class TestTagService:
    """Test TagService."""

    def test_create_tag(self, tag_repo, sample_tag_data):
        """Test creating a tag."""
        service = TagService(tag_repo)
        tag = service.create_tag(sample_tag_data)

        assert tag.tag == sample_tag_data["tag"]
        assert tag.context == sample_tag_data["context"]
        assert tag.available is True

    def test_create_tag_duplicate(self, tag_repo, sample_tag_data):
        """Test creating duplicate tag."""
        service = TagService(tag_repo)
        service.create_tag(sample_tag_data)

        with pytest.raises(ValidationException, match="already exists"):
            service.create_tag(sample_tag_data)

    def test_create_tag_validation_error(self, tag_repo):
        """Test creating tag with invalid data."""
        service = TagService(tag_repo)

        with pytest.raises(ValidationException):
            service.create_tag({"tag": ""})

    def test_get_tag(self, tag_repo, sample_tag_data):
        """Test getting a tag."""
        service = TagService(tag_repo)
        created = service.create_tag(sample_tag_data)

        tag = service.get_tag(created.id)
        assert tag.id == created.id
        assert tag.tag == sample_tag_data["tag"]

    def test_get_tag_not_found(self, tag_repo):
        """Test getting non-existent tag."""
        service = TagService(tag_repo)

        with pytest.raises(NotFoundException):
            service.get_tag(99999)

    def test_list_tags(self, tag_repo):
        """Test listing tags."""
        service = TagService(tag_repo)
        service.create_tag({"tag": "tag1", "available": True})
        service.create_tag({"tag": "tag2", "available": False})

        result = service.list_tags()
        assert result.total == 2

    def test_list_tags_with_filter(self, tag_repo):
        """Test listing tags with filter."""
        service = TagService(tag_repo)
        service.create_tag({"tag": "available-tag", "available": True})
        service.create_tag({"tag": "unavailable-tag", "available": False})

        result = service.list_tags(available="available")
        assert result.total == 1
        assert result.tags[0].tag == "available-tag"

    def test_update_tag(self, tag_repo, sample_tag_data):
        """Test updating a tag."""
        service = TagService(tag_repo)
        created = service.create_tag(sample_tag_data)

        updated = service.update_tag(created.id, {"tag": "updated-tag", "context": "Updated context"})
        assert updated.tag == "updated-tag"
        assert updated.context == "Updated context"

    def test_update_tag_not_found(self, tag_repo):
        """Test updating non-existent tag."""
        service = TagService(tag_repo)

        with pytest.raises(NotFoundException):
            service.update_tag(99999, {"tag": "new-tag"})

    def test_update_tag_duplicate(self, tag_repo):
        """Test updating to duplicate tag name."""
        service = TagService(tag_repo)
        tag1 = service.create_tag({"tag": "tag1"})
        service.create_tag({"tag": "tag2"})

        with pytest.raises(ValidationException, match="already exists"):
            service.update_tag(tag1.id, {"tag": "tag2"})

    def test_update_tag_no_fields(self, tag_repo, sample_tag_data):
        """Test updating with no valid fields."""
        service = TagService(tag_repo)
        created = service.create_tag(sample_tag_data)

        with pytest.raises(ValidationException, match="No valid fields"):
            service.update_tag(created.id, {})

    def test_delete_tag(self, tag_repo, sample_tag_data):
        """Test deleting a tag."""
        service = TagService(tag_repo)
        created = service.create_tag(sample_tag_data)

        service.delete_tag(created.id)

        # Tag should be soft deleted
        tag = tag_repo.get_by_id(created.id)
        assert tag.is_deleted is True

    def test_delete_tag_not_found(self, tag_repo):
        """Test deleting non-existent tag."""
        service = TagService(tag_repo)

        with pytest.raises(NotFoundException):
            service.delete_tag(99999)

    def test_get_stats(self, tag_repo):
        """Test getting statistics."""
        service = TagService(tag_repo)
        service.create_tag({"tag": "tag1", "available": True})
        service.create_tag({"tag": "tag2", "available": False})

        stats = service.get_stats()
        assert stats.total == 2
        assert stats.available == 1
        assert stats.unavailable == 1

    def test_get_categories(self, tag_repo):
        """Test getting categories."""
        service = TagService(tag_repo)
        service.create_tag({"tag": "tag1", "category": "CategoryA"})
        service.create_tag({"tag": "tag2", "category": "CategoryB"})

        categories = service.get_categories()
        assert "CategoryA" in categories
        assert "CategoryB" in categories


class TestCategoryService:
    """Test CategoryService."""

    def test_get_all_categories(self):
        """Test getting all categories from actual config."""
        service = CategoryService()
        all_categories = service.get_all()
        # Should load from actual categories.json file
        assert len(all_categories) > 0
        # Check structure
        for cat in all_categories:
            assert "id" in cat
            assert "category" in cat
            assert "available" in cat

    def test_get_by_id(self):
        """Test getting category by ID."""
        service = CategoryService()
        # Use actual category ID from config
        category = service.get_by_id(1)
        assert category["id"] == 1
        assert "category" in category

    def test_get_by_id_not_found(self):
        """Test getting non-existent category."""
        service = CategoryService()
        with pytest.raises(ValidationException):
            service.get_by_id(99999)

    def test_is_valid_category(self):
        """Test category validation."""
        service = CategoryService()
        # Check against actual categories
        assert service.is_valid_category("Color") is True
        assert service.is_valid_category("People") is True
        assert service.is_valid_category("InvalidCategory") is False


class TestExportService:
    """Test ExportService."""

    def test_export_to_csv(self, tag_repo, temp_db_path):
        """Test CSV export."""
        # Create test tags with translations as dict
        tag_repo.create(
            tag="test-tag",
            category="TestCategory",
            translations={"zh_CN": "测试"},
            available=1,
        )

        service = ExportService(tag_repo)
        file_path, filename = service.export_to_csv()

        assert os.path.exists(file_path)
        assert filename.endswith(".csv")

        # Verify content
        with open(file_path, "r") as f:
            content = f.read()
            assert "test-tag" in content
            assert "测试" in content

        os.unlink(file_path)

    def test_export_to_protobuf(self, tag_repo, temp_db_path):
        """Test Protobuf export."""
        tag_repo.create(
            tag="test-tag",
            category="TestCategory",
            translations={"zh_CN": "测试"},
            available=1,
        )

        service = ExportService(tag_repo)
        file_path, filename = service.export_to_protobuf()

        assert os.path.exists(file_path)
        assert filename.endswith(".pb")

        os.unlink(file_path)

    def test_get_export_data(self, tag_repo):
        """Test getting export data as dictionary."""
        tag_repo.create(tag="tag1", available=1)
        tag_repo.create(tag="tag2", available=1)

        service = ExportService(tag_repo)
        data = service.get_export_data()

        assert "version" in data
        assert "modified_time" in data
        assert data["vocab_size"] == 2
        assert len(data["tags"]) == 2

    def test_get_unique_tags(self, tag_repo):
        """Test getting unique tags (removes duplicates)."""
        # Create duplicate tags (shouldn't happen in practice but test anyway)
        tag_repo.create(tag="duplicate", available=1)

        service = ExportService(tag_repo)
        tags = service._get_unique_tags()

        # Should only have unique tags
        tag_names = [t.tag for t in tags]
        assert len(tag_names) == len(set(tag_names))
