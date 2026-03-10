"""Tag service for business logic."""

from typing import Dict, List, Optional, Any

from src.core.exceptions import NotFoundException, ValidationException
from src.models.tag import Tag, TagList, TagStats
from src.models.schemas import TagCreate, TagUpdate
from src.repositories.tag_repository import TagRepository


class TagService:
    """Service for tag business logic."""

    def __init__(self, repository: Optional[TagRepository] = None):
        self._repo = repository or TagRepository()

    def create_tag(self, data: Dict[str, Any]) -> Tag:
        """Create a new tag."""
        # Validate input
        try:
            schema = TagCreate(
                tag=data.get("tag", ""),
                context=data.get("context"),
                category=data.get("category"),
                sub_category=data.get("sub_category"),
                translations=data.get("translations"),
                available=data.get("available", True),
            )
            schema.validate()
        except ValueError as e:
            raise ValidationException(str(e))

        # Check for duplicate
        existing = self._repo.get_by_tag_name(schema.tag)
        if existing:
            raise ValidationException(f"Tag '{schema.tag}' already exists")

        # Create tag
        tag_id = self._repo.create(
            tag=schema.tag,
            context=schema.context,
            category=schema.category,
            sub_category=schema.sub_category,
            translations=schema.translations,
            available=1 if schema.available else 0,
        )

        return self._repo.get_by_id(tag_id)

    def get_tag(self, tag_id: int) -> Tag:
        """Get a tag by ID."""
        tag = self._repo.get_by_id(tag_id)
        if not tag:
            raise NotFoundException(f"Tag with ID {tag_id} not found")
        return tag

    def list_tags(
        self,
        available: Optional[str] = None,
        deleted: str = "active",
        category: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "id",
        order: str = "asc",
        page: int = 1,
        page_size: int = 100,
    ) -> TagList:
        """List tags with filtering and pagination."""
        # Parse filters
        available_filter = None
        if available == "available":
            available_filter = True
        elif available == "unavailable":
            available_filter = False

        is_deleted_filter = None
        if deleted == "active":
            is_deleted_filter = False
        elif deleted == "deleted":
            is_deleted_filter = True

        return self._repo.list(
            available=available_filter,
            is_deleted=is_deleted_filter,
            category=category,
            search=search,
            sort_by=sort_by,
            order=order,
            page=page,
            page_size=page_size,
        )

    def update_tag(self, tag_id: int, data: Dict[str, Any]) -> Tag:
        """Update a tag."""
        # Check if tag exists
        existing = self._repo.get_by_id(tag_id)
        if not existing:
            raise NotFoundException(f"Tag with ID {tag_id} not found")

        # Validate input
        try:
            schema = TagUpdate(
                tag=data.get("tag"),
                context=data.get("context"),
                category=data.get("category"),
                sub_category=data.get("sub_category"),
                translations=data.get("translations"),
                available=data.get("available"),
            )
            schema.validate()
        except ValueError as e:
            raise ValidationException(str(e))

        update_data = schema.to_dict()
        if not update_data:
            raise ValidationException("No valid fields to update")

        # Check for duplicate if tag name is being changed
        if schema.tag and schema.tag != existing.tag:
            duplicate = self._repo.get_by_tag_name(schema.tag)
            if duplicate:
                raise ValidationException(f"Tag '{schema.tag}' already exists")

        # Update tag
        self._repo.update(tag_id, **update_data)
        return self._repo.get_by_id(tag_id)

    def delete_tag(self, tag_id: int) -> None:
        """Soft delete a tag."""
        existing = self._repo.get_by_id(tag_id)
        if not existing:
            raise NotFoundException(f"Tag with ID {tag_id} not found")

        self._repo.soft_delete(tag_id)

    def get_stats(self, deleted: str = "active") -> TagStats:
        """Get tag statistics."""
        is_deleted_filter = None
        if deleted == "active":
            is_deleted_filter = False
        elif deleted == "deleted":
            is_deleted_filter = True

        return self._repo.get_stats(is_deleted=is_deleted_filter)

    def get_categories(self) -> List[str]:
        """Get distinct categories."""
        return self._repo.get_distinct_categories()
