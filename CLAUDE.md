# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based web admin panel for managing an image tag vocabulary stored in SQLite3. The application provides CRUD operations for tags, category management, translation management, and data export capabilities.

This project has been refactored to use a clean layered architecture with Repository Pattern and Service Layer.

## Development Commands

### Running the Application

```bash
# Install dependencies (editable mode recommended for development)
pip install -e ".[dev]"

# Run the Flask application
python -m curator_tag_vocab.app

# Or use the entry script
curator-tag-vocab

# Run on a custom port
PORT=5000 python -m curator_tag_vocab.app
```

Default access: `http://localhost:80/tagging/vocab`

### Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run tests with coverage
pytest --cov=curator_tag_vocab
```

## Architecture

### Project Structure (Refactored)

```
curator_tag_vocab/
├── __init__.py
├── app.py                  # Flask application factory
├── config.py               # Configuration management
├── models/                 # Data models (Tag, Category, DTOs)
│   ├── __init__.py
│   ├── tag.py
│   └── category.py
├── repositories/           # Data access layer (Repository Pattern)
│   ├── __init__.py
│   ├── database.py         # Database connection management
│   └── tag_repository.py   # Tag data access
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── tag_service.py      # Tag business logic
│   ├── category_service.py # Category configuration
│   └── export_service.py   # Data export
├── api/                    # API layer
│   ├── __init__.py
│   └── routes.py           # API endpoints
├── utils/                  # Utilities
│   ├── __init__.py
│   ├── error_handlers.py   # Error handling
│   └── logging_config.py   # Logging setup
├── templates/              # HTML templates
├── static/                 # Static assets (CSS, JS)
└── protobuf/               # Protobuf definitions
```

### Layered Architecture

1. **Models Layer** (`models/`)
   - `Tag`: Tag entity with validation and serialization
   - `Category`: Category entity
   - `TagCreate`/`TagUpdate`/`TagFilter`: DTOs for data transfer

2. **Repository Layer** (`repositories/`)
   - `DatabaseConnection`: SQLite connection management with context manager
   - `TagRepository`: CRUD operations for tags
   - Handles database-specific logic only

3. **Service Layer** (`services/`)
   - `TagService`: Business logic for tag operations
   - `CategoryService`: Category configuration management
   - `ExportService`: Data export functionality
   - Contains business rules and orchestrates repositories

4. **API Layer** (`api/`)
   - `routes.py`: Flask blueprints and HTTP endpoints
   - Input validation and response formatting
   - Calls service layer for business logic

5. **Utils Layer** (`utils/`)
   - `error_handlers.py`: Centralized error handling
   - `logging_config.py`: Logging configuration

### Database Schema

Table: `tags_vocab`
- `id` (INTEGER PRIMARY KEY)
- `tag` (TEXT) - The tag name
- `context` (TEXT) - Description/meaning of the tag
- `category` (TEXT) - Category name
- `sub_category` (TEXT) - Sub-category
- `translations` (TEXT) - JSON string with language translations (e.g., `{"zh_CN": "..."}`)
- `available` (INTEGER 0/1) - Whether tag is active
- `is_deleted` (INTEGER 0/1) - Soft delete flag
- `created_at`, `updated_at` (TIMESTAMP)

### Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tagging/vocab/` | Main UI |
| GET | `/tagging/vocab/api/tags` | List tags (with filtering, sorting, pagination) |
| POST | `/tagging/vocab/api/tags` | Create new tag |
| PUT | `/tagging/vocab/api/tags/<id>` | Update tag |
| DELETE | `/tagging/vocab/api/tags/<id>` | Soft delete tag |
| GET | `/tagging/vocab/api/stats` | Get statistics |
| GET | `/tagging/vocab/api/categories` | Get categories from DB |
| GET | `/tagging/vocab/api/categories/config` | Get category config |
| GET | `/tagging/vocab/api/export/protobuf` | Export as Protobuf |
| GET | `/tagging/vocab/api/export/csv` | Export as CSV |

### Configuration

Configuration is managed via `config.py` and environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Environment name |
| `SECRET_KEY` | `dev-secret-key...` | Flask secret key |
| `DATABASE_PATH` | `vocab.db` | SQLite database path |
| `PORT` | `80` | Server port |
| `HOST` | `0.0.0.0` | Bind address |

- `config/categories.json` - Defines valid categories with IDs and translations
- `vocab.db` - SQLite database file (created automatically if missing)

### Protobuf Export

The application uses a generated protobuf file (`curator_tag_vocab/protobuf/tags_vocabulary_pb2.py`) for exporting vocabulary in binary format.

## Development Guidelines

### Adding New Features

1. **Model Layer**: Define data structures in `models/`
2. **Repository Layer**: Add data access methods in `repositories/`
3. **Service Layer**: Implement business logic in `services/`
4. **API Layer**: Add endpoints in `api/routes.py`
5. **Tests**: Add unit tests in `tests/unit/` and integration tests in `tests/integration/`

### Testing

- Unit tests: Test individual components in isolation (use mocks)
- Integration tests: Test API endpoints with test client
- Use unique identifiers for test data to avoid conflicts

### Code Style

- Use type hints for function signatures
- Use dataclasses for data models
- Follow PEP 8 naming conventions
- Keep functions focused on single responsibility
