"""
Tag repository for database operations.
"""

import json
import logging
from typing import List, Optional, Dict, Any, Tuple

from ..models.tag import Tag, TagCreate, TagUpdate, TagFilter
from .database import DatabaseConnection

logger = logging.getLogger(__name__)


class TagRepository:
    """Repository for tag data access."""

    ALLOWED_FIELDS = {'tag', 'context', 'category', 'sub_category', 'translations', 'available'}

    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def create(self, data: TagCreate) -> int:
        """Create a new tag and return its ID."""
        data.validate()

        translations_json = json.dumps(data.translations, ensure_ascii=False) if data.translations else ''

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tags_vocab (tag, context, category, sub_category, translations, available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.tag.strip(),
                data.context or '',
                data.category or '',
                data.sub_category or '',
                translations_json,
                1 if data.available else 0
            ))
            tag_id = cursor.lastrowid
            logger.info(f"Created tag with ID {tag_id}: {data.tag}")
            return tag_id

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """Get tag by ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags_vocab WHERE id = ?", (tag_id,))
            row = cursor.fetchone()
            return Tag.from_row(dict(row)) if row else None

    def get_by_tag_name(self, tag_name: str) -> Optional[Tag]:
        """Get tag by name."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags_vocab WHERE tag = ? AND is_deleted = 0", (tag_name,))
            row = cursor.fetchone()
            return Tag.from_row(dict(row)) if row else None

    def update(self, tag_id: int, data: TagUpdate) -> bool:
        """Update tag by ID."""
        update_dict = data.to_dict()
        if not update_dict:
            return False

        # Validate fields
        invalid_fields = set(update_dict.keys()) - self.ALLOWED_FIELDS
        if invalid_fields:
            raise ValueError(f"Invalid fields: {invalid_fields}")

        # Handle translations serialization
        if 'translations' in update_dict and isinstance(update_dict['translations'], dict):
            update_dict['translations'] = json.dumps(update_dict['translations'], ensure_ascii=False)

        # Build update query
        set_parts = []
        values = []
        for key, value in update_dict.items():
            if key == 'available':
                set_parts.append(f"{key} = ?")
                values.append(1 if value else 0)
            else:
                set_parts.append(f"{key} = ?")
                values.append(value)

        set_parts.append("updated_at = CURRENT_TIMESTAMP")
        set_clause = ", ".join(set_parts)
        values.append(tag_id)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE tags_vocab SET {set_clause} WHERE id = ?", values)
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Updated tag with ID {tag_id}")
            return success

    def soft_delete(self, tag_id: int) -> bool:
        """Soft delete tag by ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tags_vocab SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (tag_id,)
            )
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Soft deleted tag with ID {tag_id}")
            return success

    def hard_delete(self, tag_id: int) -> bool:
        """Hard delete tag by ID (use with caution)."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tags_vocab WHERE id = ?", (tag_id,))
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Hard deleted tag with ID {tag_id}")
            return success

    def list(self, filter_obj: TagFilter) -> Tuple[List[Tag], int]:
        """List tags with filtering and pagination. Returns (tags, total_count)."""
        conditions = []
        params = []

        # Build where clause
        if filter_obj.available is not None:
            conditions.append('available = ?')
            params.append(1 if filter_obj.available else 0)

        if filter_obj.is_deleted is not None:
            conditions.append('is_deleted = ?')
            params.append(1 if filter_obj.is_deleted else 0)

        if filter_obj.category:
            conditions.append('category = ?')
            params.append(filter_obj.category)

        if filter_obj.search:
            conditions.append(
                "(tag LIKE ? OR context LIKE ? OR json_extract(translations, '$.zh_CN') LIKE ?)"
            )
            search_pattern = f'%{filter_obj.search}%'
            params.extend([search_pattern, search_pattern, search_pattern])

        where_clause = ' AND '.join(conditions) if conditions else '1=1'

        # Get total count
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            count_query = f"SELECT COUNT(*) as count FROM tags_vocab WHERE {where_clause}"
            cursor.execute(count_query, tuple(params))
            total_count = cursor.fetchone()['count']

        # Build order clause
        order_map = {
            'tag': 'tag',
            'translation': "json_extract(translations, '$.zh_CN')",
            'updated_at': 'updated_at',
            'id': 'id',
        }
        order_column = order_map.get(filter_obj.sort_by, 'id')
        order_direction = 'DESC' if filter_obj.order.lower() == 'desc' else 'ASC'
        order_clause = f"{order_column} {order_direction}"

        # Get paginated results
        offset = (filter_obj.page - 1) * filter_obj.limit

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT id, tag, context, category, sub_category, translations,
                       available, is_deleted, created_at, updated_at
                FROM tags_vocab
                WHERE {where_clause}
                ORDER BY {order_clause}
                LIMIT ? OFFSET ?
            """
            cursor.execute(query, tuple(params + [filter_obj.limit, offset]))
            rows = cursor.fetchall()

        tags = [Tag.from_row(dict(row)) for row in rows]
        return tags, total_count

    def get_categories(self) -> List[str]:
        """Get distinct category names."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT category
                FROM tags_vocab
                WHERE category IS NOT NULL AND category != '' AND is_deleted = 0
                ORDER BY category
            """)
            return [row['category'] for row in cursor.fetchall()]

    def get_stats(self, is_deleted: Optional[bool] = None) -> Dict[str, int]:
        """Get tag statistics."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            base_conditions = []
            if is_deleted is not None:
                base_conditions.append(f"is_deleted = {1 if is_deleted else 0}")

            base_where = f"WHERE {' AND '.join(base_conditions)}" if base_conditions else ""

            # Total count
            cursor.execute(f"SELECT COUNT(*) FROM tags_vocab {base_where}")
            total = cursor.fetchone()[0]

            # Available count
            available_where = base_where + " AND " if base_where else "WHERE "
            cursor.execute(f"SELECT COUNT(*) FROM tags_vocab {available_where} available = 1")
            available = cursor.fetchone()[0]

            # Unavailable count
            cursor.execute(f"SELECT COUNT(*) FROM tags_vocab {available_where} available = 0")
            unavailable = cursor.fetchone()[0]

            # Deleted count
            cursor.execute("SELECT COUNT(*) FROM tags_vocab WHERE is_deleted = 1")
            deleted = cursor.fetchone()[0]

            return {
                'total': total,
                'available': available,
                'unavailable': unavailable,
                'deleted': deleted,
            }

    def get_all_active_tags(self) -> List[Tag]:
        """Get all active (available and not deleted) tags."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM tags_vocab
                WHERE is_deleted = 0 AND available = 1
                ORDER BY tag
            """)
            return [Tag.from_row(dict(row)) for row in cursor.fetchall()]

    def clear_all(self) -> int:
        """Clear all tags (use with extreme caution)."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tags_vocab")
            count = cursor.rowcount
            logger.warning(f"Cleared all {count} tags from database")
            return count
