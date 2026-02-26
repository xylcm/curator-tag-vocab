"""
API routes for the curator tag vocabulary application.
"""

import logging
from flask import Blueprint, jsonify, request, send_file, render_template, current_app

from ..config import get_config
from ..models.tag import TagCreate, TagUpdate, TagFilter
from ..repositories.database import DatabaseConnection
from ..repositories.tag_repository import TagRepository
from ..services.tag_service import TagService
from ..services.category_service import CategoryService
from ..services.export_service import ExportService
from ..utils.error_handlers import APIError

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/tagging/vocab')


def get_services():
    """Get service instances with proper dependency injection."""
    config = get_config()
    db_connection = DatabaseConnection(config.DATABASE_PATH)
    tag_repository = TagRepository(db_connection)
    tag_service = TagService(tag_repository)
    category_service = CategoryService()
    export_service = ExportService(tag_service, category_service)

    return {
        'tag_service': tag_service,
        'category_service': category_service,
        'export_service': export_service,
    }


@api_bp.route('/')
def index():
    """Render main page."""
    return render_template('tags.html')


@api_bp.route('/api/stats')
def get_stats():
    """Get tag statistics."""
    services = get_services()
    deleted_filter = request.args.get('deleted', 'active')

    try:
        stats = services['tag_service'].get_stats(deleted_filter)
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise APIError("Failed to get statistics", 500)


@api_bp.route('/api/categories')
def get_categories():
    """Get distinct categories from database."""
    services = get_services()

    try:
        categories = services['tag_service'].get_categories()
        return jsonify({'categories': categories})
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise APIError("Failed to get categories", 500)


@api_bp.route('/api/categories/config')
def get_categories_config():
    """Get full category configuration."""
    services = get_services()

    try:
        categories = services['category_service'].get_all_categories()
        return jsonify({
            'categories': [cat.to_dict() for cat in categories]
        })
    except Exception as e:
        logger.error(f"Error getting category config: {e}")
        raise APIError("Failed to get category configuration", 500)


@api_bp.route('/api/tags')
def get_tags():
    """Get tags with filtering and pagination."""
    services = get_services()

    # Parse filter parameters
    available_filter = request.args.get('available', '')
    deleted_filter = request.args.get('deleted', 'active')
    category_filter = request.args.get('category', '')
    search_keyword = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 100))
    except ValueError:
        raise APIError("Invalid page or limit parameter", 400)

    # Build filter
    filter_obj = TagFilter(
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search_keyword if search_keyword else None,
        category=category_filter if category_filter else None,
    )

    # Handle availability filter
    if available_filter == 'available':
        filter_obj.available = True
    elif available_filter == 'unavailable':
        filter_obj.available = False

    # Handle deleted filter
    if deleted_filter == 'active':
        filter_obj.is_deleted = False
    elif deleted_filter == 'deleted':
        filter_obj.is_deleted = True

    try:
        tags, total_count = services['tag_service'].list_tags(filter_obj)
        total_pages = (total_count + limit - 1) // limit

        return jsonify({
            'tags': [tag.to_dict() for tag in tags],
            'page': page,
            'page_size': limit,
            'total': total_count,
            'total_pages': total_pages,
        })
    except Exception as e:
        logger.error(f"Error getting tags: {e}")
        raise APIError("Failed to get tags", 500)


@api_bp.route('/api/tags', methods=['POST'])
def create_tag():
    """Create a new tag."""
    services = get_services()
    data = request.get_json()

    if not data:
        raise APIError("No data provided", 400)

    if 'tag' not in data:
        raise APIError("Tag name is required", 400)

    try:
        tag_data = TagCreate(
            tag=data['tag'],
            context=data.get('context', ''),
            category=data.get('category', ''),
            sub_category=data.get('sub_category', ''),
            translations=data.get('translations', {}),
            available=data.get('available', True),
        )

        tag_id = services['tag_service'].create_tag(tag_data)
        return jsonify({'success': True, 'id': tag_id}), 201

    except ValueError as e:
        raise APIError(str(e), 400)
    except Exception as e:
        logger.error(f"Error creating tag: {e}")
        raise APIError("Failed to create tag", 500)


@api_bp.route('/api/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    """Update an existing tag."""
    services = get_services()
    data = request.get_json()

    if not data:
        raise APIError("No data provided", 400)

    # Build update data
    update_fields = {}
    if 'tag' in data:
        update_fields['tag'] = data['tag']
    if 'context' in data:
        update_fields['context'] = data['context']
    if 'category' in data:
        update_fields['category'] = data['category']
    if 'sub_category' in data:
        update_fields['sub_category'] = data['sub_category']
    if 'translations' in data:
        update_fields['translations'] = data['translations']
    if 'available' in data:
        update_fields['available'] = bool(data['available'])

    if not update_fields:
        raise APIError("No valid fields to update", 400)

    try:
        tag_data = TagUpdate(**update_fields)
        success = services['tag_service'].update_tag(tag_id, tag_data)

        if success:
            return jsonify({'success': True})
        else:
            raise APIError("Failed to update tag", 500)

    except ValueError as e:
        raise APIError(str(e), 404)
    except Exception as e:
        logger.error(f"Error updating tag: {e}")
        raise APIError("Failed to update tag", 500)


@api_bp.route('/api/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """Soft delete a tag."""
    services = get_services()

    try:
        success = services['tag_service'].delete_tag(tag_id)
        if success:
            return jsonify({'success': True})
        else:
            raise APIError("Failed to delete tag", 500)
    except ValueError as e:
        raise APIError(str(e), 404)
    except Exception as e:
        logger.error(f"Error deleting tag: {e}")
        raise APIError("Failed to delete tag", 500)


@api_bp.route('/api/export/protobuf')
def export_protobuf():
    """Export tags to Protobuf format."""
    services = get_services()

    try:
        file_path = services['export_service'].export_to_protobuf()
        filename = services['export_service'].get_export_filename('pb')

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except ImportError:
        raise APIError("Protobuf export not available", 500)
    except Exception as e:
        logger.error(f"Error exporting protobuf: {e}")
        raise APIError("Failed to export protobuf", 500)


@api_bp.route('/api/export/csv')
def export_csv():
    """Export tags to CSV format."""
    services = get_services()

    try:
        file_path = services['export_service'].export_to_csv()
        filename = services['export_service'].get_export_filename('csv')

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        raise APIError("Failed to export CSV", 500)
