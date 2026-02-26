"""
分类实体模型
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Category:
    """分类实体"""
    id: int
    category: str
    available: bool
    translations: Dict[str, str]
    order: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'category': self.category,
            'available': self.available,
            'translations': self.translations,
            'order': self.order
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Category':
        """从字典创建Category实例"""
        return cls(
            id=data.get('id', 0),
            category=data.get('category', ''),
            available=data.get('available', True),
            translations=data.get('translations', {}),
            order=data.get('order')
        )

    def get_translation(self, lang: str) -> Optional[str]:
        """获取指定语言的翻译"""
        return self.translations.get(lang)
