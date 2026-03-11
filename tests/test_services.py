"""
服务层测试
"""
import pytest
from src.models import Tag, TagTranslations
from src.dao import TagDAO, DatabaseConnection
from src.services import TagService, CategoryService, ExportService


class TestTagService:
    """测试标签服务"""

    def test_create_tag(self, tag_dao):
        service = TagService(tag_dao)
        tag_id = service.create_tag(
            tag="new_tag",
            context="context",
            category="Category",
            translations={'zh_CN': '测试'},
            available=True
        )
        assert tag_id is not None

    def test_create_tag_empty_name(self, tag_dao):
        service = TagService(tag_dao)
        with pytest.raises(ValueError, match="Tag name is required"):
            service.create_tag(tag="")

    def test_get_tag(self, tag_dao):
        service = TagService(tag_dao)
        tag_id = service.create_tag(tag="get_test", available=True)

        fetched = service.get_tag(tag_id)
        assert fetched is not None
        assert fetched.tag == "get_test"

    def test_update_tag(self, tag_dao):
        service = TagService(tag_dao)
        tag_id = service.create_tag(tag="original", context="original", available=True)

        success = service.update_tag(tag_id, tag="updated", context="updated")
        assert success is True

        fetched = service.get_tag(tag_id)
        assert fetched.tag == "updated"
        assert fetched.context == "updated"

    def test_update_tag_not_found(self, tag_dao):
        service = TagService(tag_dao)
        success = service.update_tag(99999, tag="updated")
        assert success is False

    def test_delete_tag(self, tag_dao):
        service = TagService(tag_dao)
        tag_id = service.create_tag(tag="to_delete", available=True)

        success = service.delete_tag(tag_id)
        assert success is True

        fetched = service.get_tag(tag_id)
        assert fetched.is_deleted is True

    def test_toggle_available(self, tag_dao):
        service = TagService(tag_dao)
        tag_id = service.create_tag(tag="toggle_test", available=True)

        # 切换为不可用
        success = service.toggle_available(tag_id, False)
        assert success is True

        fetched = service.get_tag(tag_id)
        assert fetched.available is False

    def test_list_tags(self, tag_dao):
        service = TagService(tag_dao)
        for i in range(3):
            service.create_tag(tag=f"list_{i}", available=True)

        result = service.list_tags(page=1, limit=10)
        assert 'tags' in result
        assert 'total' in result
        assert 'total_pages' in result
        assert result['page'] == 1

    def test_get_stats(self, tag_dao):
        service = TagService(tag_dao)
        service.create_tag(tag="stat1", available=True)
        service.create_tag(tag="stat2", available=False)

        stats = service.get_stats()
        assert 'total' in stats
        assert 'available' in stats
        assert 'unavailable' in stats
        assert 'deleted' in stats


class TestCategoryService:
    """测试分类服务"""

    def test_get_all_categories(self):
        service = CategoryService()
        categories = service.get_all_categories()
        assert len(categories) > 0

    def test_get_available_categories(self):
        service = CategoryService()
        categories = service.get_available_categories()
        for cat in categories:
            assert cat.available is True

    def test_get_category_names(self):
        service = CategoryService()
        names = service.get_category_names()
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_category_by_name(self):
        service = CategoryService()
        cat = service.get_category_by_name("People")
        assert cat is not None
        assert cat.category == "People"

    def test_get_category_by_name_not_found(self):
        service = CategoryService()
        cat = service.get_category_by_name("NonExistent")
        assert cat is None

    def test_get_category_by_id(self):
        service = CategoryService()
        cat = service.get_category_by_id(10)
        assert cat is not None
        assert cat.id == 10


class TestExportService:
    """测试导出服务"""

    def test_export_to_protobuf(self, tag_dao):
        category_service = CategoryService()
        export_service = ExportService(tag_dao, category_service)

        # 创建测试标签
        tag_dao.create(Tag(tag="export_test", category="People", available=True))

        data, filename = export_service.export_to_protobuf()
        assert data is not None
        assert len(data) > 0
        assert filename.startswith("tags_vocabulary_")
        assert filename.endswith(".pb")

    def test_export_to_csv(self, tag_dao):
        category_service = CategoryService()
        export_service = ExportService(tag_dao, category_service)

        # 创建测试标签
        tag = Tag(tag="csv_test", category="People", available=True)
        tag.translations.zh_CN = "CSV测试"
        tag_dao.create(tag)

        content, filename = export_service.export_to_csv()
        assert content is not None
        assert "en\tzh_CN\tcategory" in content
        assert "csv_test" in content
        assert filename.startswith("tags_vocabulary_")
        assert filename.endswith(".csv")

    def test_export_to_dict(self, tag_dao):
        category_service = CategoryService()
        export_service = ExportService(tag_dao, category_service)

        # 创建测试标签
        tag_dao.create(Tag(tag="dict_test", category="People", available=True))

        result = export_service.export_to_dict()
        assert 'version' in result
        assert 'modified_time' in result
        assert 'vocab_size' in result
        assert 'tags' in result
        assert 'categories' in result
