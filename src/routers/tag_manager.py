from flask import Blueprint, render_template, jsonify, request
from src.db import VocabDB
import json
import os

bp = Blueprint('tag_manager', __name__, url_prefix='/tagging/tags')

def get_db():
    return VocabDB()

@bp.route('/')
def index():
    return render_template('tags.html')

@bp.route('/api/categories')
def get_categories():
    db = get_db()
    with db._connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT category 
            FROM tags_vocab 
            WHERE category IS NOT NULL AND category != '' AND is_deleted = 0
            ORDER BY category
        """)
        categories = [row['category'] for row in cursor.fetchall()]
    return jsonify({'categories': categories})

@bp.route('/api/categories/config')
def get_categories_config():
    """返回完整的分类配置（包含翻译等信息）"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'categories.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            categories_config = json.load(f)
        return jsonify({'categories': categories_config})
    except Exception as e:
        return jsonify({'error': str(e), 'categories': []}), 500

@bp.route('/api/stats')
def get_stats():
    db = get_db()
    deleted_filter = request.args.get('deleted', 'active')
    
    is_deleted = None
    if deleted_filter == 'active':
        is_deleted = 0
    elif deleted_filter == 'deleted':
        is_deleted = 1
    
    total = db.count(is_deleted=is_deleted)
    available = db.count(available=1, is_deleted=is_deleted)
    unavailable = db.count(available=0, is_deleted=is_deleted)
    deleted = db.count(is_deleted=1)
    
    return jsonify({
        'total': total,
        'available': available,
        'unavailable': unavailable,
        'deleted': deleted
    })

@bp.route('/api/tags')
def get_tags():
    db = get_db()
    available_filter = request.args.get('available', '')
    deleted_filter = request.args.get('deleted', 'active')
    category_filter = request.args.get('category', '')
    search_keyword = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))
    offset = (page - 1) * limit
    
    with db._connection() as conn:
        cursor = conn.cursor()
        
        conditions = []
        params = []
        
        if available_filter == 'available':
            conditions.append('available = 1')
        elif available_filter == 'unavailable':
            conditions.append('available = 0')
        
        if deleted_filter == 'active':
            conditions.append('is_deleted = 0')
        elif deleted_filter == 'deleted':
            conditions.append('is_deleted = 1')
        
        if category_filter:
            conditions.append('category = ?')
            params.append(category_filter)
        
        if search_keyword:
            conditions.append("(tag LIKE ? OR context LIKE ? OR json_extract(translations, '$.zh_CN') LIKE ?)")
            search_pattern = f'%{search_keyword}%'
            params.extend([search_pattern, search_pattern, search_pattern])
        
        where_clause = ' AND '.join(conditions) if conditions else '1=1'
        
        count_query = f"SELECT COUNT(*) as count FROM tags_vocab WHERE {where_clause}"
        cursor.execute(count_query, tuple(params))
        total_count = cursor.fetchone()['count']
        
        if sort_by == 'tag':
            order_clause = f'tag {order.upper()}'
        elif sort_by == 'translation':
            order_clause = f"json_extract(translations, '$.zh_CN') {order.upper()}"
        elif sort_by == 'updated_at':
            order_clause = f'updated_at {order.upper()}'
        else:
            order_clause = 'tag ASC'
        
        query = f"""
            SELECT id, tag, context, category, sub_category, translations, available, created_at, updated_at
            FROM tags_vocab 
            WHERE {where_clause}
            ORDER BY {order_clause}
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        
        tags = []
        import json
        for row in rows:
            translations = json.loads(row['translations']) if row['translations'] else {}
            tags.append({
                'id': row['id'],
                'tag': row['tag'],
                'context': row['context'] or '',
                'category': row['category'] or '',
                'sub_category': row['sub_category'] or '',
                'translations': translations,
                'available': bool(row['available']),
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
    
    total_pages = (total_count + limit - 1) // limit
    
    return jsonify({
        'tags': tags,
        'page': page,
        'page_size': limit,
        'total': total_count,
        'total_pages': total_pages
    })

@bp.route('/api/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    db = get_db()
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
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
        update_fields['available'] = 1 if data['available'] else 0
    
    if not update_fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    existing_tag = db.query(record_id=tag_id, fetch_one=True)
    if not existing_tag:
        return jsonify({'error': 'Tag not found'}), 404
    
    db.update(record_id=tag_id, **update_fields)
    
    return jsonify({'success': True})

@bp.route('/api/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    db = get_db()
    rows_deleted = db.delete(record_id=tag_id)
    
    if rows_deleted > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Tag not found'}), 404

@bp.route('/api/tags', methods=['POST'])
def create_tag():
    db = get_db()
    data = request.json
    
    if not data or 'tag' not in data:
        return jsonify({'error': 'Tag name is required'}), 400
    
    tag = data['tag']
    context = data.get('context', '')
    category = data.get('category', '')
    sub_category = data.get('sub_category', '')
    translations = data.get('translations', {})
    available = 1 if data.get('available', True) else 0
    
    tag_id = db.add(tag=tag, context=context, category=category, sub_category=sub_category, 
                    translations=translations, available=available)
    
    return jsonify({
        'success': True,
        'id': tag_id
    })

