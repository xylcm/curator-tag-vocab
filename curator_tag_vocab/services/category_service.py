"""
Category service for managing category configuration.
"""

import os
import logging
from typing import List, Optional

from ..models.category import Category, CategoryConfig

logger = logging.getLogger(__name__)


class CategoryService:
    """Service for category-related operations."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Default path relative to project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_dir, 'config', 'categories.json')

        self.config_path = config_path
        self._config: Optional[CategoryConfig] = None

    def _load_config(self) -> CategoryConfig:
        """Lazy load category configuration."""
        if self._config is None:
            self._config = CategoryConfig.from_file(self.config_path)
        return self._config

    def get_all_categories(self) -> List[Category]:
        """Get all categories from configuration."""
        return self._load_config().categories

    def get_available_categories(self) -> List[Category]:
        """Get only available categories."""
        return self._load_config().get_available_categories()

    def get_category_names(self) -> List[str]:
        """Get list of category names."""
        return self._load_config().get_category_names()

    def find_category(self, name: str) -> Optional[Category]:
        """Find category by name."""
        return self._load_config().find_by_name(name)

    def reload_config(self) -> None:
        """Reload configuration from file."""
        self._config = None
        self._load_config()
        logger.info("Category configuration reloaded")
