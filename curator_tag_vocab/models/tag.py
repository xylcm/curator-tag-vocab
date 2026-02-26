"""
Tag data models.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Tag:
    """Tag model representing a vocabulary entry."""
    id: int
    tag: str
    context: str = ''
    category: str = ''
    sub_category: str = ''
    translations: Dict[str, str] = field(default_factory=dict)
    available: bool = False
    is_deleted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert tag to dictionary."""
        def format_datetime(dt):
            if dt is None:
                return None
            if isinstance(dt, datetime):
                return dt.isoformat()
            return str(dt)  # Handle string timestamps from database

        return {
            'id': self.id,
            'tag': self.tag,
            'context': self.context,
            'category': self.category,
            'sub_category': self.sub_category,
            'translations': self.translations,
            'available': self.available,
            'is_deleted': self.is_deleted,
            'created_at': format_datetime(self.created_at),
            'updated_at': format_datetime(self.updated_at),
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> 'Tag':
        """Create Tag from database row."""
        import json

        translations = row.get('translations', '{}')
        if isinstance(translations, str):
            try:
                translations = json.loads(translations)
            except json.JSONDecodeError:
                translations = {}

        return cls(
            id=row['id'],
            tag=row['tag'],
            context=row.get('context', ''),
            category=row.get('category', ''),
            sub_category=row.get('sub_category', ''),
            translations=translations,
            available=bool(row.get('available', 0)),
            is_deleted=bool(row.get('is_deleted', 0)),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at'),
        )


@dataclass
class TagCreate:
    """Data required to create a new tag."""
    tag: str
    context: str = ''
    category: str = ''
    sub_category: str = ''
    translations: Dict[str, str] = field(default_factory=dict)
    available: bool = True

    def validate(self) -> None:
        """Validate tag creation data."""
        if not self.tag or not self.tag.strip():
            raise ValueError("Tag name is required")


@dataclass
class TagUpdate:
    """Data for updating an existing tag."""
    tag: Optional[str] = None
    context: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    translations: Optional[Dict[str, str]] = None
    available: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with only set fields."""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                result[key] = value
        return result


@dataclass
class TagFilter:
    """Filter options for tag queries."""
    available: Optional[bool] = None
    is_deleted: Optional[bool] = None
    category: Optional[str] = None
    search: Optional[str] = None
    sort_by: str = 'id'
    order: str = 'asc'
    page: int = 1
    limit: int = 100

    def __post_init__(self):
        """Validate filter parameters."""
        if self.page < 1:
            self.page = 1
        if self.limit < 1:
            self.limit = 100
        if self.limit > 1000:
            self.limit = 1000
