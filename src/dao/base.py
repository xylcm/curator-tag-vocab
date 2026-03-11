"""
数据库连接管理
"""
import sqlite3
from contextlib import contextmanager
from typing import Optional


class DatabaseConnection:
    """数据库连接管理器"""

    def __init__(self, db_path: str = "vocab.db"):
        self.db_path = db_path
        self._init_database()

    @contextmanager
    def get_connection(self):
        """获取数据库连接（上下文管理器）"""
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

    def _init_database(self):
        """初始化数据库表结构"""
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

            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tag_context ON tags_vocab(tag, context)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_available ON tags_vocab(available)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON tags_vocab(category)")

            # 删除旧触发器（如果存在）
            cursor.execute("DROP TRIGGER IF EXISTS update_tags_vocab_timestamp")


# 全局数据库连接实例
_db_connection: Optional[DatabaseConnection] = None


def get_db_connection(db_path: str = "vocab.db") -> DatabaseConnection:
    """获取全局数据库连接实例"""
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection(db_path)
    return _db_connection
