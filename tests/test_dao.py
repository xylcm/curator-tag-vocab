"""
数据访问层测试
"""
import pytest
from src.models import Tag, TagTranslations
from src.dao import TagDAO, DatabaseConnection


class TestDatabaseConnection:
    """测试数据库连接"""

    def test_init_creates_tables(self, temp_db_path):
        conn = DatabaseConnection(temp_db_path)
        with conn.get_connection() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='tags_vocab'"
            )
            assert cursor.fetchone() is not None

    def test_init_creates_indexes(self, temp_db_path):
        conn = DatabaseConnection(temp_db_path)
        with conn.get_connection() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
            )
            indexes = [row['name'] for row in cursor.fetchall()]
            assert 'idx_tag_context' in indexes
            assert 'idx_available' in indexes
            assert 'idx_category' in indexes


class TestTagDAO:
    """测试标签DAO"""

    def test_create(self, tag_dao):
        tag = Tag(
            tag="test_tag",
            context="test context",
            category="Test",
            translations=TagTranslations(zh_CN="测试"),
            available=True
        )
        tag_id = tag_dao.create(tag)
        assert tag_id is not None
        assert tag_id > 0

    def test_get_by_id(self, tag_dao):
        # 创建标签
        tag = Tag(tag="test_get", available=True)
        tag_id = tag_dao.create(tag)

        # 获取标签
        fetched = tag_dao.get_by_id(tag_id)
        assert fetched is not None
        assert fetched.id == tag_id
        assert fetched.tag == "test_get"

    def test_get_by_id_not_found(self, tag_dao):
        fetched = tag_dao.get_by_id(99999)
        assert fetched is None

    def test_update(self, tag_dao):
        # 创建标签
        tag = Tag(tag="original", context="original context", available=True)
        tag_id = tag_dao.create(tag)

        # 更新
        success = tag_dao.update(tag_id, tag="updated", context="updated context")
        assert success is True

        # 验证
        fetched = tag_dao.get_by_id(tag_id)
        assert fetched.tag == "updated"
        assert fetched.context == "updated context"

    def test_update_translations(self, tag_dao):
        # 创建标签
        tag = Tag(tag="test_trans", available=True)
        tag_id = tag_dao.create(tag)

        # 更新翻译
        success = tag_dao.update(tag_id, translations={'zh_CN': '中文', 'en': 'English'})
        assert success is True

        # 验证
        fetched = tag_dao.get_by_id(tag_id)
        assert fetched.translations.zh_CN == '中文'
        assert fetched.translations.en == 'English'

    def test_soft_delete(self, tag_dao):
        # 创建标签
        tag = Tag(tag="to_delete", available=True)
        tag_id = tag_dao.create(tag)

        # 软删除
        success = tag_dao.soft_delete(tag_id)
        assert success is True

        # 验证
        fetched = tag_dao.get_by_id(tag_id)
        assert fetched.is_deleted is True

    def test_list_tags(self, tag_dao):
        # 创建多个标签
        for i in range(5):
            tag = Tag(tag=f"list_test_{i}", available=(i % 2 == 0))
            tag_dao.create(tag)

        tags, total = tag_dao.list_tags(page=1, limit=10)
        assert total >= 5
        assert len(tags) >= 5

    def test_list_tags_with_filter(self, tag_dao):
        # 创建标签
        tag_dao.create(Tag(tag="available_tag", available=True))
        tag_dao.create(Tag(tag="unavailable_tag", available=False))

        # 过滤可用标签
        tags, total = tag_dao.list_tags(available=True)
        for tag in tags:
            assert tag.available is True

    def test_list_tags_with_search(self, tag_dao):
        # 创建标签
        tag_dao.create(Tag(tag="search_me", context="unique context", available=True))
        tag_dao.create(Tag(tag="other", available=True))

        # 搜索
        tags, total = tag_dao.list_tags(search_keyword="search")
        assert total >= 1

    def test_get_categories(self, tag_dao):
        # 创建带分类的标签
        tag_dao.create(Tag(tag="cat1", category="Category A", available=True))
        tag_dao.create(Tag(tag="cat2", category="Category B", available=True))
        tag_dao.create(Tag(tag="cat3", category="Category A", available=True))

        categories = tag_dao.get_categories()
        assert "Category A" in categories
        assert "Category B" in categories

    def test_count(self, tag_dao):
        # 创建标签
        tag_dao.create(Tag(tag="count1", available=True))
        tag_dao.create(Tag(tag="count2", available=False))

        total = tag_dao.count()
        assert total >= 2

        available_count = tag_dao.count(available=True)
        unavailable_count = tag_dao.count(available=False)
        assert available_count + unavailable_count >= 2

    def test_get_unique_active_tags(self, tag_dao):
        # 创建重复标签名的标签
        tag_dao.create(Tag(tag="duplicate", available=True))
        tag_dao.create(Tag(tag="duplicate", available=True))
        tag_dao.create(Tag(tag="unique", available=True))

        unique_tags = tag_dao.get_unique_active_tags()
        tag_names = [t.tag for t in unique_tags]
        # 去重后应该只有一个 "duplicate"
        assert tag_names.count("duplicate") == 1
        assert "unique" in tag_names
