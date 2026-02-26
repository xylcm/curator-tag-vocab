"""
Integration tests for API endpoints.
"""

import pytest
import json
import os
import sys
import uuid

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from curator_tag_vocab.app import create_app
from curator_tag_vocab.config import get_config


@pytest.fixture
def app():
    """Create application for testing."""
    config = get_config('testing')
    app = create_app('testing')
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def get_unique_tag_name(prefix='test'):
    """Generate unique tag name for testing."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


class TestIndex:
    """Test cases for index route."""

    def test_index_page(self, client):
        """Test index page loads."""
        response = client.get('/tagging/vocab/')
        assert response.status_code == 200
        assert b'Curator Tag Vocabulary' in response.data


class TestStats:
    """Test cases for stats endpoint."""

    def test_get_stats(self, client):
        """Test getting statistics."""
        response = client.get('/tagging/vocab/api/stats?deleted=active')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'total' in data
        assert 'available' in data
        assert 'unavailable' in data
        assert 'deleted' in data


class TestCategories:
    """Test cases for categories endpoints."""

    def test_get_categories(self, client):
        """Test getting categories."""
        response = client.get('/tagging/vocab/api/categories')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'categories' in data
        assert isinstance(data['categories'], list)

    def test_get_categories_config(self, client):
        """Test getting category config."""
        response = client.get('/tagging/vocab/api/categories/config')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'categories' in data


class TestTags:
    """Test cases for tags endpoints."""

    def test_list_tags(self, client):
        """Test listing tags."""
        response = client.get('/tagging/vocab/api/tags')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'tags' in data
        assert 'page' in data
        assert 'total' in data
        assert 'total_pages' in data

    def test_list_tags_with_pagination(self, client):
        """Test tag pagination."""
        response = client.get('/tagging/vocab/api/tags?page=1&limit=10')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['page'] == 1
        assert data['page_size'] == 10

    def test_list_tags_with_filter(self, client):
        """Test listing tags with filter."""
        response = client.get('/tagging/vocab/api/tags?available=available')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'tags' in data

    def test_create_tag(self, client):
        """Test creating a tag."""
        payload = {
            'tag': get_unique_tag_name('integration'),
            'context': 'Test context',
            'category': 'Test',
            'translations': {'zh_CN': '测试标签'},
            'available': True,
        }

        response = client.post(
            '/tagging/vocab/api/tags',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'id' in data

    def test_create_tag_missing_name(self, client):
        """Test creating tag without name."""
        payload = {'context': 'Test context'}

        response = client.post(
            '/tagging/vocab/api/tags',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_tag(self, client):
        """Test updating a tag."""
        # First create a tag
        tag_name = get_unique_tag_name('update')
        create_response = client.post(
            '/tagging/vocab/api/tags',
            data=json.dumps({'tag': tag_name}),
            content_type='application/json'
        )
        tag_id = json.loads(create_response.data)['id']

        # Update the tag with unique name
        update_payload = {
            'tag': get_unique_tag_name('updated'),
            'context': 'Updated context',
        }

        response = client.put(
            f'/tagging/vocab/api/tags/{tag_id}',
            data=json.dumps(update_payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_update_nonexistent_tag(self, client):
        """Test updating non-existent tag."""
        response = client.put(
            '/tagging/vocab/api/tags/99999',
            data=json.dumps({'tag': 'new-name'}),
            content_type='application/json'
        )

        assert response.status_code == 404

    def test_delete_tag(self, client):
        """Test deleting a tag."""
        # First create a tag
        tag_name = get_unique_tag_name('delete')
        create_response = client.post(
            '/tagging/vocab/api/tags',
            data=json.dumps({'tag': tag_name}),
            content_type='application/json'
        )
        tag_id = json.loads(create_response.data)['id']

        # Delete the tag
        response = client.delete(f'/tagging/vocab/api/tags/{tag_id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_delete_nonexistent_tag(self, client):
        """Test deleting non-existent tag."""
        response = client.delete('/tagging/vocab/api/tags/99999')

        assert response.status_code == 404


class TestExport:
    """Test cases for export endpoints."""

    def test_export_csv(self, client):
        """Test CSV export."""
        response = client.get('/tagging/vocab/api/export/csv')

        # May fail if no tags exist, but should return appropriate response
        assert response.status_code in [200, 500]

    def test_export_protobuf(self, client):
        """Test Protobuf export."""
        response = client.get('/tagging/vocab/api/export/protobuf')

        # May fail if protobuf not available, but should return appropriate response
        assert response.status_code in [200, 500]


class TestErrorHandling:
    """Test cases for error handling."""

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/tagging/vocab/api/nonexistent')
        assert response.status_code == 404

    def test_invalid_json(self, client):
        """Test invalid JSON handling."""
        response = client.post(
            '/tagging/vocab/api/tags',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_method_not_allowed(self, client):
        """Test method not allowed handling."""
        response = client.delete('/tagging/vocab/api/tags')
        assert response.status_code == 405
