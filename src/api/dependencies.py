"""Dependency injection for API routes."""

from functools import wraps
from typing import Callable, TypeVar, Optional

from flask import jsonify

from src.core.exceptions import AppException
from src.services.tag_service import TagService
from src.services.export_service import ExportService
from src.services.category_service import CategoryService

# Service instances (singleton pattern)
_tag_service: Optional[TagService] = None
_export_service: Optional[ExportService] = None
_category_service: Optional[CategoryService] = None


def get_tag_service() -> TagService:
    """Get or create TagService instance."""
    global _tag_service
    if _tag_service is None:
        _tag_service = TagService()
    return _tag_service


def get_export_service() -> ExportService:
    """Get or create ExportService instance."""
    global _export_service
    if _export_service is None:
        _export_service = ExportService()
    return _export_service


def get_category_service() -> CategoryService:
    """Get or create CategoryService instance."""
    global _category_service
    if _category_service is None:
        _category_service = CategoryService()
    return _category_service


def reset_services() -> None:
    """Reset all service singletons. Useful for testing."""
    global _tag_service, _export_service, _category_service
    _tag_service = None
    _export_service = None
    _category_service = None


def handle_exceptions(f: Callable) -> Callable:
    """Decorator to handle exceptions in route handlers."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AppException as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper
