"""
Category data models.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class Category:
    """Category model."""
    id: int
    name: str
    available: bool = True
    order: int = 0
    translations: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'available': self.available,
            'order': self.order,
            'translations': self.translations,
        }

    @classmethod
    def from_config(cls, data: Dict[str, Any], order: int = 0) -> 'Category':
        """Create Category from configuration data."""
        return cls(
            id=data.get('id', 0),
            name=data.get('category', ''),
            available=data.get('available', True),
            order=order,
            translations=data.get('translations', {}),
        )


@dataclass
class CategoryConfig:
    """Category configuration manager."""
    categories: List[Category] = field(default_factory=list)

    @classmethod
    def from_file(cls, config_path: str) -> 'CategoryConfig':
        """Load category configuration from JSON file."""
        import json

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            categories = [
                Category.from_config(cat, i + 1)
                for i, cat in enumerate(data)
            ]
            return cls(categories=categories)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load category config: {e}")

    def get_available_categories(self) -> List[Category]:
        """Get only available categories."""
        return [cat for cat in self.categories if cat.available]

    def get_category_names(self) -> List[str]:
        """Get list of category names."""
        return [cat.name for cat in self.categories if cat.name]

    def find_by_name(self, name: str) -> Optional[Category]:
        """Find category by name."""
        for cat in self.categories:
            if cat.name == name:
                return cat
        return None
