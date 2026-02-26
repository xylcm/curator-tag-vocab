"""Tag API routes."""

from flask import Blueprint, jsonify, request, send_file, render_template

from src.api.dependencies import (
    get_tag_service,
    get_export_service,
    get_category_service,
    handle_exceptions,
)
from src.core.config import get_config

bp = Blueprint("tags", __name__, url_prefix="/tagging/vocab")


@bp.route("/")
def index():
    """Render main page."""
    return render_template("tags.html")


# Stats endpoints
@bp.route("/api/stats")
@handle_exceptions
def get_stats():
    """Get tag statistics."""
    deleted_filter = request.args.get("deleted", "active")
    service = get_tag_service()
    stats = service.get_stats(deleted=deleted_filter)
    return jsonify(stats.to_dict())


# Category endpoints
@bp.route("/api/categories")
@handle_exceptions
def get_categories():
    """Get distinct categories from tags."""
    service = get_tag_service()
    categories = service.get_categories()
    return jsonify({"categories": categories})


@bp.route("/api/categories/config")
@handle_exceptions
def get_categories_config():
    """Get full category configuration."""
    service = get_category_service()
    categories = service.get_all()
    return jsonify({"categories": categories})


# Tag CRUD endpoints
@bp.route("/api/tags", methods=["GET"])
@handle_exceptions
def list_tags():
    """List tags with filtering and pagination."""
    # Parse query parameters
    available_filter = request.args.get("available", "")
    deleted_filter = request.args.get("deleted", "active")
    category_filter = request.args.get("category", "")
    search_keyword = request.args.get("search", "").strip()
    sort_by = request.args.get("sort", "id")
    order = request.args.get("order", "asc")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 100))

    service = get_tag_service()
    result = service.list_tags(
        available=available_filter,
        deleted=deleted_filter,
        category=category_filter or None,
        search=search_keyword or None,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=limit,
    )

    return jsonify(result.to_dict())


@bp.route("/api/tags", methods=["POST"])
@handle_exceptions
def create_tag():
    """Create a new tag."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "No data provided"}), 400

    service = get_tag_service()
    tag = service.create_tag(data)

    return jsonify({"success": True, "id": tag.id}), 201


@bp.route("/api/tags/<int:tag_id>", methods=["GET"])
@handle_exceptions
def get_tag(tag_id: int):
    """Get a single tag by ID."""
    service = get_tag_service()
    tag = service.get_tag(tag_id)
    return jsonify(tag.to_dict())


@bp.route("/api/tags/<int:tag_id>", methods=["PUT"])
@handle_exceptions
def update_tag(tag_id: int):
    """Update a tag."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "No data provided"}), 400

    service = get_tag_service()
    tag = service.update_tag(tag_id, data)

    return jsonify({"success": True, "data": tag.to_dict()})


@bp.route("/api/tags/<int:tag_id>", methods=["DELETE"])
@handle_exceptions
def delete_tag(tag_id: int):
    """Soft delete a tag."""
    service = get_tag_service()
    service.delete_tag(tag_id)
    return jsonify({"success": True})


# Export endpoints
@bp.route("/api/export/protobuf")
@handle_exceptions
def export_protobuf():
    """Export tags as Protobuf binary."""
    service = get_export_service()
    file_path, filename = service.export_to_protobuf()

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream",
    )


@bp.route("/api/export/csv")
@handle_exceptions
def export_csv():
    """Export tags as CSV."""
    service = get_export_service()
    file_path, filename = service.export_to_csv()

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="text/csv",
    )
