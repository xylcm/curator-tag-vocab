"""
实现对 db.sqlite3 的接口封装
"""

import sqlite3
import json
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

class VocabDB:
    def __init__(self, db_path: str = "vocab.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _connection(self):
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

    def _init_db(self):
        with self._connection() as conn:
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
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tag_context ON tags_vocab(tag, context)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_available ON tags_vocab(available)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON tags_vocab(category)")
            cursor.execute("DROP TRIGGER IF EXISTS update_tags_vocab_timestamp")

    def add(self, tag: str, context: Optional[str] = None,
            category: Optional[str] = None, sub_category: Optional[str] = None,
            translations: Optional[Dict[str, str]] = None, 
            available: int = 0) -> int:
        translations_json = json.dumps(translations, ensure_ascii=False) if translations else None
        
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tags_vocab (tag, context, category, sub_category, translations, available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tag, context, category, sub_category, translations_json, available))
            return cursor.lastrowid

    def delete(self, record_id: Optional[int] = None, tag: Optional[str] = None) -> int:
        if record_id is None and tag is None:
            raise ValueError("Either record_id or tag must be provided")
        
        with self._connection() as conn:
            cursor = conn.cursor()
            if record_id is not None:
                cursor.execute("UPDATE tags_vocab SET is_deleted = 1 WHERE id = ?", (record_id,))
            else:
                cursor.execute("UPDATE tags_vocab SET is_deleted = 1 WHERE tag = ?", (tag,))
            return cursor.rowcount

    def update(self, record_id: Optional[int] = None, filter_tag: Optional[str] = None, 
               **kwargs) -> bool:
        if record_id is None and filter_tag is None:
            raise ValueError("Either record_id or filter_tag must be provided")
        if not kwargs:
            return False
        
        allowed_fields = {'tag', 'context', 'category', 'sub_category', 'translations', 'available'}
        invalid_fields = set(kwargs.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Invalid fields: {invalid_fields}")
        
        if 'translations' in kwargs and isinstance(kwargs['translations'], dict):
            kwargs['translations'] = json.dumps(kwargs['translations'], ensure_ascii=False)
        
        kwargs['updated_at'] = 'CURRENT_TIMESTAMP'
        
        set_parts = []
        values = []
        for key, value in kwargs.items():
            if key == 'updated_at':
                set_parts.append(f"{key} = CURRENT_TIMESTAMP")
            else:
                set_parts.append(f"{key} = ?")
                values.append(value)
        
        set_clause = ", ".join(set_parts)
        
        with self._connection() as conn:
            cursor = conn.cursor()
            if record_id is not None:
                cursor.execute(f"UPDATE tags_vocab SET {set_clause} WHERE id = ?", 
                             values + [record_id])
            else:
                cursor.execute(f"UPDATE tags_vocab SET {set_clause} WHERE tag = ?", 
                             values + [filter_tag])
            return cursor.rowcount > 0

    def query(self, sql: Optional[str] = None, params: tuple = (), fetch_one: bool = False,
              record_id: Optional[int] = None, tag: Optional[str] = None, 
              available: Optional[int] = None, is_deleted: Optional[int] = None,
              limit: Optional[int] = None, offset: int = 0) -> Optional[Any]:
        with self._connection() as conn:
            cursor = conn.cursor()
            
            if sql:
                cursor.execute(sql, params)
            else:
                conditions = []
                query_params = []
                
                if record_id is not None:
                    conditions.append("id = ?")
                    query_params.append(record_id)
                if tag is not None:
                    conditions.append("tag = ?")
                    query_params.append(tag)
                if available is not None:
                    conditions.append("available = ?")
                    query_params.append(available)
                if is_deleted is not None:
                    conditions.append("is_deleted = ?")
                    query_params.append(is_deleted)
                
                query = "SELECT * FROM tags_vocab"
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                query += " ORDER BY id"
                if limit:
                    query += f" LIMIT {limit} OFFSET {offset}"
                
                cursor.execute(query, tuple(query_params))
            
            if sql and not sql.strip().upper().startswith('SELECT'):
                return cursor.rowcount
            
            if fetch_one:
                row = cursor.fetchone()
                if row:
                    result = dict(row)
                    if result.get('translations'):
                        result['translations'] = json.loads(result['translations'])
                    return result
                return None
            else:
                results = []
                for row in cursor.fetchall():
                    result = dict(row)
                    if result.get('translations'):
                        result['translations'] = json.loads(result['translations'])
                    results.append(result)
                return results

    def clear(self) -> int:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tags_vocab")
            return cursor.rowcount

    def count(self, available: Optional[int] = None, is_deleted: Optional[int] = None) -> int:
        with self._connection() as conn:
            cursor = conn.cursor()
            
            conditions = []
            params = []
            
            if available is not None:
                conditions.append("available = ?")
                params.append(available)
            
            if is_deleted is not None:
                conditions.append("is_deleted = ?")
                params.append(is_deleted)
            
            query = "SELECT COUNT(*) as count FROM tags_vocab"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            cursor.execute(query, tuple(params))
            return cursor.fetchone()['count']

    def load_tag_names(self) -> List[str]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tag FROM tags_vocab WHERE is_deleted = 0 AND available = 1")
            return [row["tag"] for row in cursor.fetchall()]