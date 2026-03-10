"""Configuration management."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Config:
    """Application configuration."""

    # Database
    database_path: str = "vocab.db"

    # Flask
    secret_key: str = "dev-secret-key-change-in-production"
    debug: bool = True

    # Security
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "Lax"

    # Paths
    base_dir: str = ""
    config_dir: str = "config"
    template_folder: str = "templates"
    static_folder: str = "static"

    # Pagination
    default_page_size: int = 100
    max_page_size: int = 1000

    def __post_init__(self):
        # Ensure base_dir is set
        if not self.base_dir:
            object.__setattr__(
                self, "base_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )

    @property
    def categories_config_path(self) -> str:
        """Get categories config file path."""
        return os.path.join(
            os.path.dirname(self.base_dir), self.config_dir, "categories.json"
        )

    @property
    def full_template_folder(self) -> str:
        """Get full template folder path."""
        return os.path.join(self.base_dir, self.template_folder)

    @property
    def full_static_folder(self) -> str:
        """Get full static folder path."""
        return os.path.join(self.base_dir, self.static_folder)

    @property
    def full_database_path(self) -> str:
        """Get full database path."""
        if os.path.isabs(self.database_path):
            return self.database_path
        return os.path.join(os.path.dirname(self.base_dir), self.database_path)


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def init_config(
    database_path: Optional[str] = None,
    secret_key: Optional[str] = None,
    debug: Optional[bool] = None,
) -> Config:
    """Initialize config with custom values."""
    global _config

    kwargs = {}
    if database_path is not None:
        kwargs["database_path"] = database_path
    if secret_key is not None:
        kwargs["secret_key"] = secret_key
    if debug is not None:
        kwargs["debug"] = debug

    _config = Config(**kwargs)
    return _config
