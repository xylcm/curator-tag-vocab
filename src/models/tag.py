"""
标签实体模型
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class TagTranslations:
    """标签翻译"""
    zh_CN: Optional[str] = None
    en: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        result = {}
        if self.zh_CN:
            result['zh_CN'] = self.zh_CN
        if self.en:
            result['en'] = self.en
        return result

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, str]]) -> 'TagTranslations':
        if not data:
            return cls()
        return cls(
            zh_CN=data.get('zh_CN'),
            en=data.get('en')
        )


@dataclass
class Tag:
    """标签实体"""
    id: Optional[int] = None
    tag: str = ""
    context: str = ""
    category: str = ""
    sub_category: str = ""
    translations: TagTranslations = field(default_factory=TagTranslations)
    available: bool = False
    is_deleted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于API响应）"""
        return {
            'id': self.id,
            'tag': self.tag,
            'context': self.context,
            'category': self.category,
            'sub_category': self.sub_category,
            'translations': self.translations.to_dict(),
            'available': self.available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> 'Tag':
        """从数据库行创建Tag实例"""
        translations = row.get('translations', '{}')
        if isinstance(translations, str):
            try:
                translations = json.loads(translations) if translations else {}
            except json.JSONDecodeError:
                translations = {}

        return cls(
            id=row.get('id'),
            tag=row.get('tag', ''),
            context=row.get('context') or '',
            category=row.get('category') or '',
            sub_category=row.get('sub_category') or '',
            translations=TagTranslations.from_dict(translations),
            available=bool(row.get('available', 0)),
            is_deleted=bool(row.get('is_deleted', 0)),
            created_at=cls._parse_datetime(row.get('created_at')),
            updated_at=cls._parse_datetime(row.get('updated_at'))
        )

    @staticmethod
    def _parse_datetime(value: Any) -> Optional[datetime]:
        """解析日期时间"""
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return None
        return None

    def get_translation(self, lang: str) -> Optional[str]:
        """获取指定语言的翻译"""
        if lang == 'zh_CN':
            return self.translations.zh_CN
        elif lang == 'en':
            return self.translations.en
        return None

    def set_translation(self, lang: str, value: str) -> None:
        """设置指定语言的翻译"""
        if lang == 'zh_CN':
            self.translations.zh_CN = value
        elif lang == 'en':
            self.translations.en = value
