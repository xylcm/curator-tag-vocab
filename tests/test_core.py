"""Tests for core module."""

import os
import pytest

from src.core.config import Config, get_config, init_config
from src.core.database import Database, get_db, init_database
from src.core.exceptions import (
    AppException,
    NotFoundException,
    ValidationException,
    DatabaseException,
)


class TestConfig:
    """Test configuration management."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.database_path == "vocab.db"
        assert config.secret_key == "dev-secret-key-change-in-production"
        assert config.debug is True
        assert config.session_cookie_httponly is True
        assert config.session_cookie_samesite == "Lax"

    def test_custom_config(self):
        """Test custom configuration values."""
        config = Config(
            database_path="custom.db",
            secret_key="custom-key",
            debug=False,
        )
        assert config.database_path == "custom.db"
        assert config.secret_key == "custom-key"
        assert config.debug is False

    def test_config_paths(self):
        """Test configuration paths."""
        config = Config()
        assert config.categories_config_path.endswith("config/categories.json")
        assert config.full_template_folder.endswith("templates")
        assert config.full_static_folder.endswith("static")

    def test_init_config(self):
        """Test config initialization."""
        config = init_config(
            database_path="test.db",
            secret_key="test-key",
            debug=False,
        )
        assert config.database_path == "test.db"
        assert config.secret_key == "test-key"
        assert config.debug is False
        # Verify global instance is set
        assert get_config() == config


class TestDatabase:
    """Test database management."""

    def test_database_initialization(self, temp_db_path):
        """Test database initialization."""
        db = Database(temp_db_path)
        assert db._db_path == temp_db_path
        # Verify table was created
        with db.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='tags_vocab'"
            )
            assert cursor.fetchone() is not None

    def test_database_connection(self, temp_db_path):
        """Test database connection context manager."""
        db = Database(temp_db_path)
        with db.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1

    def test_init_database(self, temp_db_path):
        """Test database initialization function."""
        db = init_database(temp_db_path)
        assert db._db_path == temp_db_path
        assert get_db() == db


class TestExceptions:
    """Test custom exceptions."""

    def test_app_exception(self):
        """Test base application exception."""
        exc = AppException("Test error", status_code=400)
        assert exc.message == "Test error"
        assert exc.status_code == 400
        assert str(exc) == "Test error"

    def test_not_found_exception(self):
        """Test not found exception."""
        exc = NotFoundException("Resource not found")
        assert exc.message == "Resource not found"
        assert exc.status_code == 404

        # Test default message
        exc_default = NotFoundException()
        assert exc_default.message == "Resource not found"

    def test_validation_exception(self):
        """Test validation exception."""
        exc = ValidationException("Invalid input")
        assert exc.message == "Invalid input"
        assert exc.status_code == 400

    def test_database_exception(self):
        """Test database exception."""
        exc = DatabaseException("DB error")
        assert exc.message == "DB error"
        assert exc.status_code == 500
