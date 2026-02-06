# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based web admin panel for managing an image tag vocabulary stored in SQLite3. The application provides CRUD operations for tags, category management, translation management, and data export capabilities.

## Development Commands

### Running the Application

```bash
# Install dependencies (editable mode recommended for development)
pip install -e .

# Run the Flask application
python src/app_tagging.py

# Run on a custom port
PORT=5000 python src/app_tagging.py
```

Default access: `http://localhost:80/tagging/vocab`

### Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src
```

## Architecture

### Application Structure

- **Entry Point**: `src/app_tagging.py` - Creates Flask app, registers blueprints, configures paths
- **Database Layer**: `src/db.py` - `VocabDB` class wraps SQLite3 operations with context manager for connections
- **Routes**: `src/routers/tag_manager.py` - Flask blueprint with all API endpoints and export logic
- **Templates**: `src/templates/tags.html` - Single-page web interface
- **Static Assets**: `src/static/css/main.css`, `src/static/js/tags.js` - Frontend assets

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

- `GET /tagging/vocab/api/tags` - List tags with filtering, sorting, pagination
- `POST /tagging/vocab/api/tags` - Create new tag
- `PUT /tagging/vocab/api/tags/<id>` - Update tag
- `DELETE /tagging/vocab/api/tags/<id>` - Soft delete tag
- `GET /tagging/vocab/api/export/protobuf` - Export as Protobuf binary
- `GET /tagging/vocab/api/export/csv` - Export as CSV

### Configuration

- `config/categories.json` - Defines valid categories with IDs and translations
- `vocab.db` - SQLite database file (created automatically if missing)

### Protobuf Export

The application uses a generated protobuf file (`src/protobuf/tags_vocabulary_pb2.py`) for exporting vocabulary in binary format. The `.proto` definition is not in the repo - the generated file is committed directly.
