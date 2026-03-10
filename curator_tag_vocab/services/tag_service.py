"""
Tag service for business logic.
"""

import logging
from typing import List, Optional, Dict, Any, Tuple

from ..models.tag import Tag, TagCreate, TagUpdate, TagFilter
from ..repositories.tag_repository import TagRepository

logger = logging.getLogger(__name__)


class TagService:
    """Service for tag-related business logic."""

    def __init__(self, repository: TagRepository):
        self.repository = repository

    def create_tag(self, data: TagCreate) -> int:
        """Create a new tag with validation."""
        # Check for duplicate tag names
        existing = self.repository.get_by_tag_name(data.tag)
        if existing:
            raise ValueError(f"Tag '{data.tag}' already exists")

        return self.repository.create(data)

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        """Get tag by ID."""
        return self.repository.get_by_id(tag_id)

    def update_tag(self, tag_id: int, data: TagUpdate) -> bool:
        """Update tag with validation."""
        # Check if tag exists
        existing = self.repository.get_by_id(tag_id)
        if not existing:
            raise ValueError(f"Tag with ID {tag_id} not found")

        # Check for duplicate name if changing name
        if data.tag and data.tag != existing.tag:
            duplicate = self.repository.get_by_tag_name(data.tag)
            if duplicate and duplicate.id != tag_id:
                raise ValueError(f"Tag '{data.tag}' already exists")

        return self.repository.update(tag_id, data)

    def delete_tag(self, tag_id: int) -> bool:
        """Soft delete tag."""
        existing = self.repository.get_by_id(tag_id)
        if not existing:
            raise ValueError(f"Tag with ID {tag_id} not found")

        return self.repository.soft_delete(tag_id)

    def toggle_availability(self, tag_id: int, available: bool) -> bool:
        """Toggle tag availability."""
        existing = self.repository.get_by_id(tag_id)
        if not existing:
            raise ValueError(f"Tag with ID {tag_id} not found")

        return self.repository.update(tag_id, TagUpdate(available=available))

    def list_tags(self, filter_obj: TagFilter) -> Tuple[List[Tag], int]:
        """List tags with filtering."""
        return self.repository.list(filter_obj)

    def get_categories(self) -> List[str]:
        """Get all distinct categories."""
        return self.repository.get_categories()

    def get_stats(self, deleted_filter: Optional[str] = None) -> Dict[str, int]:
        """Get tag statistics."""
        is_deleted = None
        if deleted_filter == 'active':
            is_deleted = False
        elif deleted_filter == 'deleted':
            is_deleted = True

        return self.repository.get_stats(is_deleted)

    def get_unique_active_tags(self) -> List[Tag]:
        """Get unique active tags (for export)."""
        all_tags = self.repository.get_all_active_tags()

        # Remove duplicates by tag name
        seen = set()
        unique_tags = []
        for tag in all_tags:
            if tag.tag not in seen:
                seen.add(tag.tag)
                unique_tags.append(tag)

        # Sort by tag name
        unique_tags.sort(key=lambda t: t.tag)
        return unique_tags
