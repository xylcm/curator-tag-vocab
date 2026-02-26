"""
Unit tests for data models.
"""

import pytest
from datetime import datetime

from curator_tag_vocab.models.tag import Tag, TagCreate, TagUpdate, TagFilter
from curator_tag_vocab.models.category import Category, CategoryConfig


class TestTag:
    """Test cases for Tag model."""

    def test_tag_creation(self):
        """Test creating a Tag instance."""
        tag = Tag(
            id=1,
            tag="test-tag",
            context="Test context",
            category="TestCategory",
            sub_category="SubCategory",
            translations={"zh_CN": "测试标签"},
            available=True,
            is_deleted=False,
        )

        assert tag.id == 1
        assert tag.tag == "test-tag"
        assert tag.context == "Test context"
        assert tag.category == "TestCategory"
        assert tag.sub_category == "SubCategory"
        assert tag.translations == {"zh_CN": "测试标签"}
        assert tag.available is True
        assert tag.is_deleted is False

    def test_tag_from_row(self):
        """Test creating Tag from database row."""
        row = {
            'id': 1,
            'tag': 'test-tag',
            'context': 'Test context',
            'category': 'TestCategory',
            'sub_category': 'SubCategory',
            'translations': '{"zh_CN": "测试标签"}',
            'available': 1,
            'is_deleted': 0,
            'created_at': '2024-01-01 00:00:00',
            'updated_at': '2024-01-01 00:00:00',
        }

        tag = Tag.from_row(row)

        assert tag.id == 1
        assert tag.tag == "test-tag"
        assert tag.translations == {"zh_CN": "测试标签"}
        assert tag.available is True
        assert tag.is_deleted is False

    def test_tag_from_row_empty_translations(self):
        """Test creating Tag from row with empty translations."""
        row = {
            'id': 1,
            'tag': 'test-tag',
            'translations': '',
            'available': 0,
            'is_deleted': 0,
        }

        tag = Tag.from_row(row)

        assert tag.translations == {}

    def test_tag_to_dict(self):
        """Test converting Tag to dictionary."""
        tag = Tag(
            id=1,
            tag="test-tag",
            translations={"zh_CN": "测试标签"},
            available=True,
        )

        result = tag.to_dict()

        assert result['id'] == 1
        assert result['tag'] == "test-tag"
        assert result['translations'] == {"zh_CN": "测试标签"}
        assert result['available'] is True


class TestTagCreate:
    """Test cases for TagCreate model."""

    def test_tag_create_valid(self):
        """Test creating valid TagCreate."""
        data = TagCreate(
            tag="new-tag",
            context="Context",
            category="Category",
            translations={"zh_CN": "新标签"},
            available=True,
        )

        data.validate()

        assert data.tag == "new-tag"

    def test_tag_create_invalid_empty_name(self):
        """Test validation with empty tag name."""
        data = TagCreate(tag="")

        with pytest.raises(ValueError, match="Tag name is required"):
            data.validate()

    def test_tag_create_invalid_whitespace_name(self):
        """Test validation with whitespace-only tag name."""
        data = TagCreate(tag="   ")

        with pytest.raises(ValueError, match="Tag name is required"):
            data.validate()

    def test_tag_create_defaults(self):
        """Test TagCreate default values."""
        data = TagCreate(tag="test-tag")

        assert data.context == ''
        assert data.category == ''
        assert data.sub_category == ''
        assert data.translations == {}
        assert data.available is True


class TestTagUpdate:
    """Test cases for TagUpdate model."""

    def test_tag_update_to_dict(self):
        """Test converting TagUpdate to dict."""
        data = TagUpdate(
            tag="updated-tag",
            available=False,
        )

        result = data.to_dict()

        assert result == {'tag': 'updated-tag', 'available': False}

    def test_tag_update_partial(self):
        """Test partial update with only some fields."""
        data = TagUpdate(tag="updated-tag")

        result = data.to_dict()

        assert result == {'tag': 'updated-tag'}
        assert 'available' not in result


class TestTagFilter:
    """Test cases for TagFilter model."""

    def test_tag_filter_defaults(self):
        """Test TagFilter default values."""
        filter_obj = TagFilter()

        assert filter_obj.page == 1
        assert filter_obj.limit == 100
        assert filter_obj.sort_by == 'id'
        assert filter_obj.order == 'asc'

    def test_tag_filter_validation(self):
        """Test TagFilter parameter validation."""
        filter_obj = TagFilter(page=0, limit=0)

        assert filter_obj.page == 1
        assert filter_obj.limit == 100

    def test_tag_filter_max_limit(self):
        """Test TagFilter limit cap."""
        filter_obj = TagFilter(limit=5000)

        assert filter_obj.limit == 1000


class TestCategory:
    """Test cases for Category model."""

    def test_category_creation(self):
        """Test creating a Category instance."""
        category = Category(
            id=1,
            name="TestCategory",
            available=True,
            order=1,
            translations={"zh_CN": "测试分类"},
        )

        assert category.id == 1
        assert category.name == "TestCategory"
        assert category.available is True
        assert category.order == 1

    def test_category_from_config(self):
        """Test creating Category from config data."""
        config_data = {
            'id': 1,
            'category': 'TestCategory',
            'available': True,
            'translations': {'zh_CN': '测试分类'},
        }

        category = Category.from_config(config_data, order=5)

        assert category.id == 1
        assert category.name == 'TestCategory'
        assert category.order == 5

    def test_category_to_dict(self):
        """Test converting Category to dictionary."""
        category = Category(
            id=1,
            name="TestCategory",
            translations={"zh_CN": "测试分类"},
        )

        result = category.to_dict()

        assert result['id'] == 1
        assert result['name'] == 'TestCategory'
        assert result['translations'] == {"zh_CN": "测试分类"}
