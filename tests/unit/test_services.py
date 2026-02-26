"""
Unit tests for service layer.
"""

import pytest
from unittest.mock import Mock, MagicMock

from curator_tag_vocab.services.tag_service import TagService
from curator_tag_vocab.services.category_service import CategoryService
from curator_tag_vocab.services.export_service import ExportService
from curator_tag_vocab.models.tag import Tag, TagCreate, TagUpdate, TagFilter
from curator_tag_vocab.models.category import Category


class TestTagService:
    """Test cases for TagService."""

    @pytest.fixture
    def mock_repo(self):
        """Create a mock TagRepository."""
        return Mock()

    @pytest.fixture
    def service(self, mock_repo):
        """Create TagService with mock repository."""
        return TagService(mock_repo)

    def test_create_tag_success(self, service, mock_repo):
        """Test successful tag creation."""
        mock_repo.get_by_tag_name.return_value = None
        mock_repo.create.return_value = 1

        data = TagCreate(tag="new-tag")
        tag_id = service.create_tag(data)

        assert tag_id == 1
        mock_repo.create.assert_called_once()

    def test_create_tag_duplicate(self, service, mock_repo):
        """Test creating duplicate tag."""
        mock_repo.get_by_tag_name.return_value = Mock(id=1, tag="existing-tag")

        data = TagCreate(tag="existing-tag")

        with pytest.raises(ValueError, match="already exists"):
            service.create_tag(data)

    def test_get_tag(self, service, mock_repo):
        """Test getting a tag."""
        expected_tag = Mock(spec=Tag)
        mock_repo.get_by_id.return_value = expected_tag

        result = service.get_tag(1)

        assert result == expected_tag
        mock_repo.get_by_id.assert_called_with(1)

    def test_update_tag_success(self, service, mock_repo):
        """Test successful tag update."""
        mock_repo.get_by_id.return_value = Mock(id=1, tag="old-name")
        mock_repo.get_by_tag_name.return_value = None
        mock_repo.update.return_value = True

        data = TagUpdate(tag="new-name")
        success = service.update_tag(1, data)

        assert success is True
        mock_repo.update.assert_called_once()

    def test_update_tag_not_found(self, service, mock_repo):
        """Test updating non-existent tag."""
        mock_repo.get_by_id.return_value = None

        data = TagUpdate(tag="new-name")

        with pytest.raises(ValueError, match="not found"):
            service.update_tag(999, data)

    def test_delete_tag_success(self, service, mock_repo):
        """Test successful tag deletion."""
        mock_repo.get_by_id.return_value = Mock(id=1)
        mock_repo.soft_delete.return_value = True

        success = service.delete_tag(1)

        assert success is True
        mock_repo.soft_delete.assert_called_with(1)

    def test_toggle_availability(self, service, mock_repo):
        """Test toggling tag availability."""
        mock_repo.get_by_id.return_value = Mock(id=1, available=True)
        mock_repo.update.return_value = True

        success = service.toggle_availability(1, False)

        assert success is True

    def test_get_unique_active_tags(self, service, mock_repo):
        """Test getting unique active tags."""
        # Create mock tags with duplicates
        tag1 = Mock(tag="tag-a")
        tag2 = Mock(tag="tag-b")
        tag3 = Mock(tag="tag-a")  # Duplicate

        mock_repo.get_all_active_tags.return_value = [tag1, tag2, tag3]

        result = service.get_unique_active_tags()

        assert len(result) == 2
        assert result[0].tag == "tag-a"
        assert result[1].tag == "tag-b"


class TestCategoryService:
    """Test cases for CategoryService."""

    def test_get_all_categories(self, tmp_path):
        """Test getting all categories."""
        # Create temp config file
        config_file = tmp_path / "categories.json"
        config_file.write_text('''[
            {"id": 1, "category": "Test1", "available": true, "translations": {}}
        ]''')

        service = CategoryService(str(config_file))
        categories = service.get_all_categories()

        assert len(categories) == 1
        assert categories[0].name == "Test1"

    def test_get_available_categories(self, tmp_path):
        """Test getting only available categories."""
        config_file = tmp_path / "categories.json"
        config_file.write_text('''[
            {"id": 1, "category": "Available", "available": true, "translations": {}},
            {"id": 2, "category": "Unavailable", "available": false, "translations": {}}
        ]''')

        service = CategoryService(str(config_file))
        categories = service.get_available_categories()

        assert len(categories) == 1
        assert categories[0].name == "Available"

    def test_find_category(self, tmp_path):
        """Test finding category by name."""
        config_file = tmp_path / "categories.json"
        config_file.write_text('''[
            {"id": 1, "category": "TestCat", "available": true, "translations": {}}
        ]''')

        service = CategoryService(str(config_file))
        category = service.find_category("TestCat")

        assert category is not None
        assert category.id == 1


class TestExportService:
    """Test cases for ExportService."""

    @pytest.fixture
    def mock_tag_service(self):
        """Create a mock TagService."""
        return Mock()

    @pytest.fixture
    def mock_category_service(self):
        """Create a mock CategoryService."""
        return Mock()

    @pytest.fixture
    def export_service(self, mock_tag_service, mock_category_service):
        """Create ExportService with mock services."""
        return ExportService(mock_tag_service, mock_category_service)

    def test_export_to_csv(self, export_service, mock_tag_service, tmp_path):
        """Test CSV export."""
        # Create mock tags
        tag = Mock(
            tag="test-tag",
            translations={"zh_CN": "测试"},
            category="TestCategory"
        )
        mock_tag_service.get_unique_active_tags.return_value = [tag]

        file_path = export_service.export_to_csv()

        assert file_path.endswith('.csv')

        # Verify file content
        with open(file_path, 'r') as f:
            content = f.read()
            assert 'test-tag' in content
            assert '测试' in content

    def test_get_export_filename(self, export_service):
        """Test export filename generation."""
        filename = export_service.get_export_filename('csv')

        assert filename.startswith('tags_vocabulary_')
        assert filename.endswith('.csv')
