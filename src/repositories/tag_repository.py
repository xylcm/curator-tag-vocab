"""Tag repository for database operations."""

import json
from typing import Dict, List, Optional, Any, Tuple

from src.core.database import Database, get_db
from src.core.exceptions import DatabaseException
from src.models.tag import Tag, TagList, TagStats


class TagRepository:
    """Repository for tag data access."""

    def __init__(self, db: Optional[Database] = None):
        self._db = db or get_db()

    def create(
        self,
        tag: str,
        context: Optional[str] = None,
        category: Optional[str] = None,
        sub_category: Optional[str] = None,
        translations: Optional[Dict[str, str]] = None,
        available: int = 0,
    ) -> int:
        """Create a new tag."""
        translations_json = json.dumps(translations, ensure_ascii=False) if translations else None

        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO tags_vocab (tag, context, category, sub_category, translations, available)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (tag, context, category, sub_category, translations_json, available),
                )
                return cursor.lastrowid
        except Exception as e:
            raise DatabaseException(f"Failed to create tag: {str(e)}")

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """Get tag by ID."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tags_vocab WHERE id = ?", (tag_id,))
                row = cursor.fetchone()
                if row:
                    return Tag.from_row(dict(row))
                return None
        except Exception as e:
            raise DatabaseException(f"Failed to get tag: {str(e)}")

    def get_by_tag_name(self, tag_name: str) -> Optional[Tag]:
        """Get tag by name."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tags_vocab WHERE tag = ? AND is_deleted = 0", (tag_name,))
                row = cursor.fetchone()
                if row:
                    return Tag.from_row(dict(row))
                return None
        except Exception as e:
            raise DatabaseException(f"Failed to get tag: {str(e)}")

    def list(
        self,
        available: Optional[bool] = None,
        is_deleted: Optional[bool] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "id",
        order: str = "asc",
        page: int = 1,
        page_size: int = 100,
    ) -> TagList:
        """List tags with filtering and pagination."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()

                # Build conditions
                conditions = []
                params = []

                if available is not None:
                    conditions.append("available = ?")
                    params.append(1 if available else 0)

                if is_deleted is not None:
                    conditions.append("is_deleted = ?")
                    params.append(1 if is_deleted else 0)

                if category:
                    conditions.append("category = ?")
                    params.append(category)

                if search:
                    conditions.append(
                        "(tag LIKE ? OR context LIKE ? OR json_extract(translations, '$.zh_CN') LIKE ?)"
                    )
                    search_pattern = f"%{search}%"
                    params.extend([search_pattern, search_pattern, search_pattern])

                where_clause = " AND ".join(conditions) if conditions else "1=1"

                # Get total count
                count_query = f"SELECT COUNT(*) as count FROM tags_vocab WHERE {where_clause}"
                cursor.execute(count_query, tuple(params))
                total = cursor.fetchone()["count"]

                # Build order clause
                if sort_by == "tag":
                    order_clause = f"tag {order.upper()}"
                elif sort_by == "translation":
                    order_clause = f"json_extract(translations, '$.zh_CN') {order.upper()}"
                elif sort_by == "updated_at":
                    order_clause = f"updated_at {order.upper()}"
                else:
                    order_clause = "tag ASC"

                # Get paginated results
                offset = (page - 1) * page_size
                query = f"""
                    SELECT id, tag, context, category, sub_category, translations, available, created_at, updated_at
                    FROM tags_vocab
                    WHERE {where_clause}
                    ORDER BY {order_clause}
                    LIMIT ? OFFSET ?
                """
                cursor.execute(query, tuple(params + [page_size, offset]))

                tags = [Tag.from_row(dict(row)) for row in cursor.fetchall()]

                return TagList(tags=tags, page=page, page_size=page_size, total=total)
        except Exception as e:
            raise DatabaseException(f"Failed to list tags: {str(e)}")

    def update(self, tag_id: int, **kwargs) -> bool:
        """Update a tag."""
        if not kwargs:
            return False

        allowed_fields = {"tag", "context", "category", "sub_category", "translations", "available"}
        invalid_fields = set(kwargs.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Invalid fields: {invalid_fields}")

        if "translations" in kwargs and isinstance(kwargs["translations"], dict):
            kwargs["translations"] = json.dumps(kwargs["translations"], ensure_ascii=False)

        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()

                set_parts = []
                values = []
                for key, value in kwargs.items():
                    set_parts.append(f"{key} = ?")
                    values.append(value)

                set_clause = ", ".join(set_parts)
                cursor.execute(
                    f"UPDATE tags_vocab SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    values + [tag_id],
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseException(f"Failed to update tag: {str(e)}")

    def soft_delete(self, tag_id: int) -> bool:
        """Soft delete a tag."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE tags_vocab SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (tag_id,),
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseException(f"Failed to delete tag: {str(e)}")

    def delete(self, tag_id: int) -> bool:
        """Hard delete a tag."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tags_vocab WHERE id = ?", (tag_id,))
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseException(f"Failed to delete tag: {str(e)}")

    def get_stats(
        self, is_deleted: Optional[bool] = None
    ) -> TagStats:
        """Get tag statistics."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()

                # Build conditions
                conditions = []
                params = []

                if is_deleted is not None:
                    conditions.append("is_deleted = ?")
                    params.append(1 if is_deleted else 0)

                where_clause = " AND ".join(conditions) if conditions else "1=1"

                # Get total
                cursor.execute(
                    f"SELECT COUNT(*) as count FROM tags_vocab WHERE {where_clause}",
                    tuple(params),
                )
                total = cursor.fetchone()["count"]

                # Get available count
                available_where = f"{where_clause} AND available = 1"
                cursor.execute(
                    f"SELECT COUNT(*) as count FROM tags_vocab WHERE {available_where}",
                    tuple(params),
                )
                available = cursor.fetchone()["count"]

                # Get unavailable count
                unavailable_where = f"{where_clause} AND available = 0"
                cursor.execute(
                    f"SELECT COUNT(*) as count FROM tags_vocab WHERE {unavailable_where}",
                    tuple(params),
                )
                unavailable = cursor.fetchone()["count"]

                # Get deleted count
                cursor.execute("SELECT COUNT(*) as count FROM tags_vocab WHERE is_deleted = 1")
                deleted = cursor.fetchone()["count"]

                return TagStats(
                    total=total,
                    available=available,
                    unavailable=unavailable,
                    deleted=deleted,
                )
        except Exception as e:
            raise DatabaseException(f"Failed to get stats: {str(e)}")

    def get_all_available(self) -> List[Tag]:
        """Get all available and non-deleted tags."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM tags_vocab WHERE is_deleted = 0 AND available = 1 ORDER BY tag"
                )
                return [Tag.from_row(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            raise DatabaseException(f"Failed to get tags: {str(e)}")

    def get_distinct_categories(self) -> List[str]:
        """Get distinct non-empty categories."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT DISTINCT category
                    FROM tags_vocab
                    WHERE category IS NOT NULL AND category != '' AND is_deleted = 0
                    ORDER BY category
                    """
                )
                return [row["category"] for row in cursor.fetchall()]
        except Exception as e:
            raise DatabaseException(f"Failed to get categories: {str(e)}")

    def clear(self) -> int:
        """Clear all tags (for testing)."""
        try:
            with self._db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tags_vocab")
                return cursor.rowcount
        except Exception as e:
            raise DatabaseException(f"Failed to clear tags: {str(e)}")
