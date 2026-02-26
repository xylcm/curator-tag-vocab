"""Tag domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass
class Tag:
    """Tag domain model."""

    id: int
    tag: str
    context: str = ""
    category: str = ""
    sub_category: str = ""
    translations: Dict[str, str] = field(default_factory=dict)
    available: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: bool = False

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Tag":
        """Create Tag from database row."""
        import json

        translations = row.get("translations", "")
        if isinstance(translations, str) and translations:
            try:
                translations = json.loads(translations)
            except json.JSONDecodeError:
                translations = {}
        elif translations is None:
            translations = {}

        return cls(
            id=row["id"],
            tag=row["tag"],
            context=row.get("context") or "",
            category=row.get("category") or "",
            sub_category=row.get("sub_category") or "",
            translations=translations,
            available=bool(row.get("available", 0)),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            is_deleted=bool(row.get("is_deleted", 0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tag": self.tag,
            "context": self.context,
            "category": self.category,
            "sub_category": self.sub_category,
            "translations": self.translations,
            "available": self.available,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class TagList:
    """Paginated tag list."""

    tags: List[Tag]
    page: int
    page_size: int
    total: int

    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        return (self.total + self.page_size - 1) // self.page_size

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "tags": [tag.to_dict() for tag in self.tags],
            "page": self.page,
            "page_size": self.page_size,
            "total": self.total,
            "total_pages": self.total_pages,
        }


@dataclass
class TagStats:
    """Tag statistics."""

    total: int = 0
    available: int = 0
    unavailable: int = 0
    deleted: int = 0

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {
            "total": self.total,
            "available": self.available,
            "unavailable": self.unavailable,
            "deleted": self.deleted,
        }
