"""
分类服务 - 业务逻辑层
"""
import os
import json
from typing import List, Optional, Dict, Any
from src.models import Category


class CategoryService:
    """分类业务服务"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # 默认配置路径
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_dir, 'config', 'categories.json')
        self.config_path = config_path
        self._categories_cache: Optional[List[Category]] = None

    def _load_config(self) -> List[Dict[str, Any]]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def get_all_categories(self) -> List[Category]:
        """获取所有分类配置"""
        if self._categories_cache is None:
            data = self._load_config()
            self._categories_cache = [
                Category.from_dict(item) for item in data
            ]
        return self._categories_cache

    def get_available_categories(self) -> List[Category]:
        """获取可用的分类"""
        return [cat for cat in self.get_all_categories() if cat.available]

    def get_category_names(self) -> List[str]:
        """获取分类名称列表"""
        return [cat.category for cat in self.get_available_categories()]

    def get_category_by_name(self, name: str) -> Optional[Category]:
        """根据名称获取分类"""
        for cat in self.get_all_categories():
            if cat.category == name:
                return cat
        return None

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """根据ID获取分类"""
        for cat in self.get_all_categories():
            if cat.id == category_id:
                return cat
        return None

    def to_dict_list(self) -> List[Dict[str, Any]]:
        """转换为字典列表"""
        return [cat.to_dict() for cat in self.get_all_categories()]
