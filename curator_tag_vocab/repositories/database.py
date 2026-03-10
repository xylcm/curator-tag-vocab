"""
Database connection management with context manager.
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional, Generator


class DatabaseConnection:
    """Manages SQLite database connections."""

    def __init__(self, db_path: str = "vocab.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
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
            """)

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
                "CREATE INDEX IF NOT EXISTS idx_is_deleted ON tags_vocab(is_deleted)"
            )

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
