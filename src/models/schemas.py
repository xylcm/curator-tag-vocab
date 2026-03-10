"""Pydantic schemas for validation."""

from enum import Enum
from typing import Dict, List, Optional, Any


class ExportFormat(str, Enum):
    """Export format enum."""

    PROTOBUF = "protobuf"
    CSV = "csv"


class TagCreate:
    """Schema for creating a tag."""

    def __init__(
        self,
        tag: str,
        context: str = "",
        category: str = "",
        sub_category: str = "",
        translations: Optional[Dict[str, str]] = None,
        available: bool = True,
    ):
        self.tag = tag.strip() if tag else ""
        self.context = context or ""
        self.category = category or ""
        self.sub_category = sub_category or ""
        self.translations = translations or {}
        self.available = available

    def validate(self) -> None:
        """Validate the schema."""
        if not self.tag:
            raise ValueError("Tag name is required")
        if len(self.tag) > 255:
            raise ValueError("Tag name must be less than 255 characters")


class TagUpdate:
    """Schema for updating a tag."""

    def __init__(
        self,
        tag: Optional[str] = None,
        context: Optional[str] = None,
        category: Optional[str] = None,
        sub_category: Optional[str] = None,
        translations: Optional[Dict[str, str]] = None,
        available: Optional[bool] = None,
    ):
        self.tag = tag
        self.context = context
        self.category = category
        self.sub_category = sub_category
        self.translations = translations
        self.available = available

    def validate(self) -> None:
        """Validate the schema."""
        if self.tag is not None:
            if not self.tag.strip():
                raise ValueError("Tag name cannot be empty")
            if len(self.tag) > 255:
                raise ValueError("Tag name must be less than 255 characters")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary of non-None values."""
        result = {}
        if self.tag is not None:
            result["tag"] = self.tag.strip()
        if self.context is not None:
            result["context"] = self.context
        if self.category is not None:
            result["category"] = self.category
        if self.sub_category is not None:
            result["sub_category"] = self.sub_category
        if self.translations is not None:
            result["translations"] = self.translations
        if self.available is not None:
            result["available"] = 1 if self.available else 0
        return result


class TagResponse:
    """Schema for tag response."""

    def __init__(self, tag: Dict[str, Any]):
        self.data = tag

    def to_dict(self) -> Dict[str, Any]:
        return {"success": True, "data": self.data}


class TagListResponse:
    """Schema for tag list response."""

    def __init__(
        self,
        tags: List[Dict[str, Any]],
        page: int,
        page_size: int,
        total: int,
        total_pages: int,
    ):
        self.tags = tags
        self.page = page
        self.page_size = page_size
        self.total = total
        self.total_pages = total_pages

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tags": self.tags,
            "page": self.page,
            "page_size": self.page_size,
            "total": self.total,
            "total_pages": self.total_pages,
        }


class Category:
    """Category schema."""

    def __init__(
        self,
        id: int,
        category: str,
        available: bool,
        translations: Dict[str, str],
    ):
        self.id = id
        self.category = category
        self.available = available
        self.translations = translations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "available": self.available,
            "translations": self.translations,
        }
