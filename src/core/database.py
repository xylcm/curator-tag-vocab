"""Database connection management."""

import sqlite3
from contextlib import contextmanager
from typing import Optional

from src.core.config import get_config


class Database:
    """Database connection manager."""

    def __init__(self, db_path: Optional[str] = None):
        self._db_path = db_path or get_config().full_database_path
        self._init_db()

    @contextmanager
    def connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database schema."""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tags_vocab (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT NOT NULL,
                    context TEXT DEFAULT '',
                    category TEXT DEFAULT '',
                    sub_category TEXT DEFAULT '',
                    translations TEXT DEFAULT '',
                    available INTEGER DEFAULT 0,
                    is_deleted INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CHECK(available IN (0, 1))
                )
            """
            )

            # Create indexes
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tag_context ON tags_vocab(tag, context)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_available ON tags_vocab(available)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_category ON tags_vocab(category)"
            )
            cursor.execute(
                "DROP TRIGGER IF EXISTS update_tags_vocab_timestamp"
            )


# Global database instance
_db: Optional[Database] = None


def get_db() -> Database:
    """Get or create global database instance."""
    global _db
    if _db is None:
        _db = Database()
    return _db


def init_database(db_path: Optional[str] = None) -> Database:
    """Initialize database with custom path."""
    global _db
    _db = Database(db_path)
    return _db
