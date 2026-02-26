"""
标签服务 - 业务逻辑层
"""
from typing import Optional, List, Dict, Any, Tuple
from src.models import Tag, TagTranslations
from src.dao import TagDAO


class TagService:
    """标签业务服务"""

    def __init__(self, tag_dao: TagDAO):
        self.tag_dao = tag_dao

    def create_tag(
        self,
        tag: str,
        context: str = "",
        category: str = "",
        sub_category: str = "",
        translations: Optional[Dict[str, str]] = None,
        available: bool = True
    ) -> int:
        """创建新标签"""
        if not tag or not tag.strip():
            raise ValueError("Tag name is required")

        new_tag = Tag(
            tag=tag.strip(),
            context=context.strip(),
            category=category.strip(),
            sub_category=sub_category.strip(),
            translations=TagTranslations.from_dict(translations or {}),
            available=available
        )
        return self.tag_dao.create(new_tag)

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        """获取单个标签"""
        return self.tag_dao.get_by_id(tag_id)

    def update_tag(self, tag_id: int, **kwargs) -> bool:
        """更新标签"""
        # 验证标签存在
        existing = self.tag_dao.get_by_id(tag_id)
        if not existing:
            return False

        # 过滤空值和无效字段
        update_data = {}
        allowed_fields = {'tag', 'context', 'category', 'sub_category', 'translations', 'available'}

        for key, value in kwargs.items():
            if key not in allowed_fields:
                continue
            if key == 'tag' and value:
                update_data[key] = value.strip()
            elif key == 'translations':
                if isinstance(value, dict):
                    update_data[key] = value
            elif key == 'available':
                update_data[key] = bool(value)
            elif isinstance(value, str):
                update_data[key] = value.strip()
            else:
                update_data[key] = value

        if not update_data:
            return False

        return self.tag_dao.update(tag_id, **update_data)

    def delete_tag(self, tag_id: int) -> bool:
        """软删除标签"""
        return self.tag_dao.soft_delete(tag_id)

    def toggle_available(self, tag_id: int, available: bool) -> bool:
        """切换标签可用状态"""
        return self.tag_dao.update(tag_id, available=available)

    def list_tags(
        self,
        available: Optional[str] = None,
        deleted: str = 'active',
        category: Optional[str] = None,
        search_keyword: Optional[str] = None,
        sort_by: str = 'id',
        order: str = 'asc',
        page: int = 1,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        获取标签列表（支持分页和过滤）

        Args:
            available: 'available'|'unavailable'|None
            deleted: 'active'|'deleted'|'all'
            category: 分类过滤
            search_keyword: 搜索关键词
            sort_by: 排序字段
            order: asc|desc
            page: 页码
            limit: 每页数量
        """
        # 转换过滤条件
        available_filter = None
        if available == 'available':
            available_filter = True
        elif available == 'unavailable':
            available_filter = False

        is_deleted_filter = None
        if deleted == 'active':
            is_deleted_filter = False
        elif deleted == 'deleted':
            is_deleted_filter = True

        tags, total = self.tag_dao.list_tags(
            available=available_filter,
            is_deleted=is_deleted_filter,
            category=category,
            search_keyword=search_keyword,
            sort_by=sort_by,
            order=order,
            page=page,
            limit=limit
        )

        total_pages = (total + limit - 1) // limit

        return {
            'tags': [tag.to_dict() for tag in tags],
            'page': page,
            'page_size': limit,
            'total': total,
            'total_pages': total_pages
        }

    def get_stats(self, deleted: str = 'active') -> Dict[str, int]:
        """获取统计信息"""
        is_deleted_filter = None
        if deleted == 'active':
            is_deleted_filter = False
        elif deleted == 'deleted':
            is_deleted_filter = True

        total = self.tag_dao.count(is_deleted=is_deleted_filter)
        available = self.tag_dao.count(available=True, is_deleted=is_deleted_filter)
        unavailable = self.tag_dao.count(available=False, is_deleted=is_deleted_filter)
        deleted_count = self.tag_dao.count(is_deleted=True)

        return {
            'total': total,
            'available': available,
            'unavailable': unavailable,
            'deleted': deleted_count
        }

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return self.tag_dao.get_categories()

    def get_all_active_tags(self) -> List[Tag]:
        """获取所有可用标签"""
        return self.tag_dao.get_all_active_tags()

    def get_unique_active_tags(self) -> List[Tag]:
        """获取去重后的可用标签"""
        return self.tag_dao.get_unique_active_tags()
