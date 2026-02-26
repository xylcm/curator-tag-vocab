"""
模型层测试
"""
import pytest
from datetime import datetime
from src.models import Tag, TagTranslations, Category


class TestTagTranslations:
    """测试标签翻译模型"""

    def test_to_dict(self):
        trans = TagTranslations(zh_CN="测试", en="test")
        result = trans.to_dict()
        assert result == {'zh_CN': '测试', 'en': 'test'}

    def test_to_dict_empty(self):
        trans = TagTranslations()
        result = trans.to_dict()
        assert result == {}

    def test_from_dict(self):
        data = {'zh_CN': '测试', 'en': 'test'}
        trans = TagTranslations.from_dict(data)
        assert trans.zh_CN == '测试'
        assert trans.en == 'test'

    def test_from_dict_none(self):
        trans = TagTranslations.from_dict(None)
        assert trans.zh_CN is None
        assert trans.en is None


class TestTag:
    """测试标签模型"""

    def test_to_dict(self):
        tag = Tag(
            id=1,
            tag="test",
            context="test context",
            category="Test",
            sub_category="Sub",
            translations=TagTranslations(zh_CN="测试"),
            available=True,
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 2, 12, 0, 0)
        )
        result = tag.to_dict()
        assert result['id'] == 1
        assert result['tag'] == 'test'
        assert result['context'] == 'test context'
        assert result['category'] == 'Test'
        assert result['sub_category'] == 'Sub'
        assert result['translations'] == {'zh_CN': '测试'}
        assert result['available'] is True

    def test_from_db_row(self):
        row = {
            'id': 1,
            'tag': 'test',
            'context': 'context',
            'category': 'Category',
            'sub_category': 'Sub',
            'translations': '{"zh_CN": "测试"}',
            'available': 1,
            'is_deleted': 0,
            'created_at': '2024-01-01T12:00:00',
            'updated_at': '2024-01-02T12:00:00'
        }
        tag = Tag.from_db_row(row)
        assert tag.id == 1
        assert tag.tag == 'test'
        assert tag.translations.zh_CN == '测试'
        assert tag.available is True
        assert tag.is_deleted is False

    def test_from_db_row_empty_translations(self):
        row = {
            'id': 1,
            'tag': 'test',
            'translations': '',
            'available': 0,
            'is_deleted': 0
        }
        tag = Tag.from_db_row(row)
        assert tag.translations.zh_CN is None
        assert tag.translations.en is None

    def test_get_translation(self):
        tag = Tag(translations=TagTranslations(zh_CN="测试", en="test"))
        assert tag.get_translation('zh_CN') == '测试'
        assert tag.get_translation('en') == 'test'
        assert tag.get_translation('fr') is None

    def test_set_translation(self):
        tag = Tag()
        tag.set_translation('zh_CN', '测试')
        tag.set_translation('en', 'test')
        assert tag.translations.zh_CN == '测试'
        assert tag.translations.en == 'test'


class TestCategory:
    """测试分类模型"""

    def test_to_dict(self):
        cat = Category(
            id=1,
            category="Test",
            available=True,
            translations={'zh_CN': '测试'},
            order=1
        )
        result = cat.to_dict()
        assert result['id'] == 1
        assert result['category'] == 'Test'
        assert result['available'] is True
        assert result['translations'] == {'zh_CN': '测试'}
        assert result['order'] == 1

    def test_from_dict(self):
        data = {
            'id': 1,
            'category': 'Test',
            'available': True,
            'translations': {'zh_CN': '测试'}
        }
        cat = Category.from_dict(data)
        assert cat.id == 1
        assert cat.category == 'Test'
        assert cat.available is True
        assert cat.translations == {'zh_CN': '测试'}

    def test_get_translation(self):
        cat = Category(
            id=1,
            category="Test",
            available=True,
            translations={'zh_CN': '测试', 'en': 'test'}
        )
        assert cat.get_translation('zh_CN') == '测试'
        assert cat.get_translation('en') == 'test'
        assert cat.get_translation('fr') is None
