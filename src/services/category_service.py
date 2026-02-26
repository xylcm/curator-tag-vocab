"""Category service for managing categories."""

import json
import os
from typing import Dict, List, Any

from src.core.config import get_config
from src.core.exceptions import ValidationException


class CategoryService:
    """Service for category operations."""

    def __init__(self):
        self._config = get_config()
        self._categories_cache: List[Dict[str, Any]] = []
        self._load_categories()

    def _load_categories(self) -> None:
        """Load categories from config file."""
        config_path = self._config.categories_config_path
        if not os.path.exists(config_path):
            self._categories_cache = []
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._categories_cache = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            self._categories_cache = []

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all categories."""
        return self._categories_cache

    def get_by_id(self, category_id: int) -> Dict[str, Any]:
        """Get category by ID."""
        for cat in self._categories_cache:
            if cat.get("id") == category_id:
                return cat
        raise ValidationException(f"Category with ID {category_id} not found")

    def get_by_name(self, category_name: str) -> Dict[str, Any]:
        """Get category by name."""
        for cat in self._categories_cache:
            if cat.get("category") == category_name:
                return cat
        raise ValidationException(f"Category '{category_name}' not found")

    def is_valid_category(self, category_name: str) -> bool:
        """Check if category is valid."""
        try:
            self.get_by_name(category_name)
            return True
        except ValidationException:
            return False

    def get_available_categories(self) -> List[Dict[str, Any]]:
        """Get only available categories."""
        return [cat for cat in self._categories_cache if cat.get("available", True)]
