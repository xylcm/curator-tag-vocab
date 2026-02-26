"""
标签管理路由 - 处理HTTP请求
"""
import os
import tempfile
from flask import Blueprint, render_template, jsonify, request, send_file

from src.dao import TagDAO, DatabaseConnection
from src.services import TagService, CategoryService, ExportService


bp = Blueprint('tag_manager', __name__, url_prefix='/tagging/vocab')


def _get_services():
    """获取服务实例"""
    db = DatabaseConnection()
    tag_dao = TagDAO(db)
    tag_service = TagService(tag_dao)
    category_service = CategoryService()
    export_service = ExportService(tag_dao, category_service)
    return tag_service, category_service, export_service


@bp.route('/')
def index():
    """首页"""
    return render_template('tags.html')


@bp.route('/api/categories')
def get_categories():
    """获取分类列表"""
    _, category_service, _ = _get_services()
    categories = category_service.get_category_names()
    return jsonify({'categories': categories})


@bp.route('/api/categories/config')
def get_categories_config():
    """获取完整分类配置"""
    _, category_service, _ = _get_services()
    try:
        categories = category_service.to_dict_list()
        return jsonify({'categories': categories})
    except Exception as e:
        return jsonify({'error': str(e), 'categories': []}), 500


@bp.route('/api/stats')
def get_stats():
    """获取统计信息"""
    tag_service, _, _ = _get_services()
    deleted_filter = request.args.get('deleted', 'active')
    stats = tag_service.get_stats(deleted=deleted_filter)
    return jsonify(stats)


@bp.route('/api/tags')
def get_tags():
    """获取标签列表"""
    tag_service, _, _ = _get_services()

    # 解析查询参数
    available_filter = request.args.get('available', '')
    deleted_filter = request.args.get('deleted', 'active')
    category_filter = request.args.get('category', '')
    search_keyword = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))

    result = tag_service.list_tags(
        available=available_filter if available_filter else None,
        deleted=deleted_filter,
        category=category_filter if category_filter else None,
        search_keyword=search_keyword if search_keyword else None,
        sort_by=sort_by,
        order=order,
        page=page,
        limit=limit
    )

    return jsonify(result)


@bp.route('/api/tags', methods=['POST'])
def create_tag():
    """创建新标签"""
    tag_service, _, _ = _get_services()
    data = request.json

    if not data or 'tag' not in data:
        return jsonify({'error': 'Tag name is required'}), 400

    try:
        tag_id = tag_service.create_tag(
            tag=data['tag'],
            context=data.get('context', ''),
            category=data.get('category', ''),
            sub_category=data.get('sub_category', ''),
            translations=data.get('translations', {}),
            available=data.get('available', True)
        )
        return jsonify({'success': True, 'id': tag_id})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    """更新标签"""
    tag_service, _, _ = _get_services()
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # 构建更新数据
    update_fields = {}
    field_mapping = {
        'tag': 'tag',
        'context': 'context',
        'category': 'category',
        'sub_category': 'sub_category',
        'translations': 'translations',
        'available': 'available'
    }

    for api_field, service_field in field_mapping.items():
        if api_field in data:
            update_fields[service_field] = data[api_field]

    if not update_fields:
        return jsonify({'error': 'No valid fields to update'}), 400

    success = tag_service.update_tag(tag_id, **update_fields)

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Tag not found'}), 404


@bp.route('/api/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """删除标签"""
    tag_service, _, _ = _get_services()
    success = tag_service.delete_tag(tag_id)

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Tag not found'}), 404


@bp.route('/api/export/protobuf')
def export_protobuf():
    """导出 Protobuf 格式"""
    _, _, export_service = _get_services()

    try:
        data, filename = export_service.export_to_protobuf()

        # 写入临时文件
        temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pb')
        temp_file.write(data)
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/export/csv')
def export_csv():
    """导出 CSV 格式"""
    _, _, export_service = _get_services()

    try:
        content, filename = export_service.export_to_csv()

        # 写入临时文件
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
        temp_file.write(content)
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
