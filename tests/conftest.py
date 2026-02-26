"""Pytest configuration and fixtures."""

import os
import tempfile
import pytest

from src.app import create_app
from src.core.config import Config, init_config
from src.core.database import init_database
from src.api.dependencies import reset_services
from src.repositories.tag_repository import TagRepository


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset all singleton instances before each test."""
    # Import and reset module-level variables
    import src.core.config
    import src.core.database
    src.core.config._config = None
    src.core.database._db = None
    reset_services()
    yield
    # Reset after test as well
    src.core.config._config = None
    src.core.database._db = None
    reset_services()


@pytest.fixture
def temp_db_path():
    """Create temporary database file."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    os.unlink(path)


@pytest.fixture
def app(temp_db_path):
    """Create application with test configuration."""
    # Reset singletons before creating app
    import src.core.config
    import src.core.database
    src.core.config._config = None
    src.core.database._db = None
    reset_services()

    config = Config(
        database_path=temp_db_path,
        secret_key="test-secret-key",
        debug=True,
    )
    app = create_app(config)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def db(temp_db_path):
    """Create database instance."""
    database = init_database(temp_db_path)
    return database


@pytest.fixture
def tag_repo(db):
    """Create tag repository."""
    return TagRepository(db)


@pytest.fixture
def sample_tag_data():
    """Sample tag data for testing."""
    return {
        "tag": "test-tag",
        "context": "Test context",
        "category": "TestCategory",
        "sub_category": "TestSubCategory",
        "translations": {"zh_CN": "测试标签"},
        "available": True,
    }
