"""
标签数据访问对象
"""
import json
from typing import Optional, List, Dict, Any, Tuple
from src.models import Tag
from .base import DatabaseConnection


class TagDAO:
    """标签数据访问对象"""

    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def create(self, tag: Tag) -> int:
        """创建新标签，返回标签ID"""
        translations_json = json.dumps(tag.translations.to_dict(), ensure_ascii=False)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tags_vocab (tag, context, category, sub_category, translations, available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tag.tag, tag.context, tag.category, tag.sub_category,
                  translations_json, 1 if tag.available else 0))
            return cursor.lastrowid

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """根据ID获取标签"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags_vocab WHERE id = ?", (tag_id,))
            row = cursor.fetchone()
            return Tag.from_db_row(dict(row)) if row else None

    def get_by_tag_name(self, tag_name: str) -> Optional[Tag]:
        """根据标签名获取标签"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags_vocab WHERE tag = ?", (tag_name,))
            row = cursor.fetchone()
            return Tag.from_db_row(dict(row)) if row else None

    def update(self, tag_id: int, **kwargs) -> bool:
        """更新标签"""
        allowed_fields = {'tag', 'context', 'category', 'sub_category', 'translations', 'available'}
        invalid_fields = set(kwargs.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Invalid fields: {invalid_fields}")

        if not kwargs:
            return False

        # 处理 translations 字段
        if 'translations' in kwargs and isinstance(kwargs['translations'], dict):
            kwargs['translations'] = json.dumps(kwargs['translations'], ensure_ascii=False)

        set_parts = []
        values = []
        for key, value in kwargs.items():
            if key == 'available':
                set_parts.append(f"{key} = ?")
                values.append(1 if value else 0)
            else:
                set_parts.append(f"{key} = ?")
                values.append(value)

        set_clause = ", ".join(set_parts)
        values.append(tag_id)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE tags_vocab
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, values)
            return cursor.rowcount > 0

    def soft_delete(self, tag_id: int) -> bool:
        """软删除标签"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tags_vocab SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (tag_id,))
            return cursor.rowcount > 0

    def hard_delete(self, tag_id: int) -> bool:
        """硬删除标签"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tags_vocab WHERE id = ?", (tag_id,))
            return cursor.rowcount > 0

    def list_tags(
        self,
        available: Optional[bool] = None,
        is_deleted: Optional[bool] = None,
        category: Optional[str] = None,
        search_keyword: Optional[str] = None,
        sort_by: str = 'id',
        order: str = 'asc',
        page: int = 1,
        limit: int = 100
    ) -> Tuple[List[Tag], int]:
        """
        获取标签列表
        返回: (标签列表, 总数量)
        """
        offset = (page - 1) * limit

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # 构建查询条件
            conditions = []
            params = []

            if available is not None:
                conditions.append('available = ?')
                params.append(1 if available else 0)

            if is_deleted is not None:
                conditions.append('is_deleted = ?')
                params.append(1 if is_deleted else 0)

            if category:
                conditions.append('category = ?')
                params.append(category)

            if search_keyword:
                conditions.append(
                    "(tag LIKE ? OR context LIKE ? OR json_extract(translations, '$.zh_CN') LIKE ?)"
                )
                search_pattern = f'%{search_keyword}%'
                params.extend([search_pattern, search_pattern, search_pattern])

            where_clause = ' AND '.join(conditions) if conditions else '1=1'

            # 计算总数
            count_query = f"SELECT COUNT(*) as count FROM tags_vocab WHERE {where_clause}"
            cursor.execute(count_query, tuple(params))
            total_count = cursor.fetchone()['count']

            # 构建排序
            order_clause = self._build_order_clause(sort_by, order)

            # 查询数据
            query = f"""
                SELECT id, tag, context, category, sub_category, translations, available, created_at, updated_at
                FROM tags_vocab
                WHERE {where_clause}
                ORDER BY {order_clause}
                LIMIT ? OFFSET ?
            """
            cursor.execute(query, tuple(params) + (limit, offset))
            rows = cursor.fetchall()

            tags = [Tag.from_db_row(dict(row)) for row in rows]
            return tags, total_count

    def _build_order_clause(self, sort_by: str, order: str) -> str:
        """构建排序子句"""
        order = order.upper()
        if sort_by == 'tag':
            return f'tag {order}'
        elif sort_by == 'translation':
            return f"json_extract(translations, '$.zh_CN') {order}"
        elif sort_by == 'updated_at':
            return f'updated_at {order}'
        else:
            return f'id {order}'

    def get_all_active_tags(self) -> List[Tag]:
        """获取所有可用且未删除的标签"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM tags_vocab
                WHERE is_deleted = 0 AND available = 1
                ORDER BY tag
            """)
            rows = cursor.fetchall()
            return [Tag.from_db_row(dict(row)) for row in rows]

    def get_unique_active_tags(self) -> List[Tag]:
        """获取去重后的可用标签（按tag名称去重）"""
        tags = self.get_all_active_tags()
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag.tag not in seen:
                seen.add(tag.tag)
                unique_tags.append(tag)
        return unique_tags

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT category
                FROM tags_vocab
                WHERE category IS NOT NULL AND category != '' AND is_deleted = 0
                ORDER BY category
            """)
            return [row['category'] for row in cursor.fetchall()]

    def count(
        self,
        available: Optional[bool] = None,
        is_deleted: Optional[bool] = None
    ) -> int:
        """统计标签数量"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            conditions = []
            params = []

            if available is not None:
                conditions.append("available = ?")
                params.append(1 if available else 0)

            if is_deleted is not None:
                conditions.append("is_deleted = ?")
                params.append(1 if is_deleted else 0)

            query = "SELECT COUNT(*) as count FROM tags_vocab"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, tuple(params))
            return cursor.fetchone()['count']

    def clear_all(self) -> int:
        """清空所有标签（危险操作）"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tags_vocab")
            return cursor.rowcount
