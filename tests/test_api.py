"""
API 集成测试
"""
import json


class TestIndex:
    """测试首页"""

    def test_index_page(self, client):
        response = client.get('/tagging/vocab/')
        assert response.status_code == 200
        assert b'Curator Tag Vocabulary' in response.data


class TestCategoriesAPI:
    """测试分类API"""

    def test_get_categories(self, client):
        response = client.get('/tagging/vocab/api/categories')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'categories' in data
        assert isinstance(data['categories'], list)

    def test_get_categories_config(self, client):
        response = client.get('/tagging/vocab/api/categories/config')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'categories' in data


class TestStatsAPI:
    """测试统计API"""

    def test_get_stats(self, client):
        response = client.get('/tagging/vocab/api/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total' in data
        assert 'available' in data
        assert 'unavailable' in data
        assert 'deleted' in data


class TestTagsAPI:
    """测试标签API"""

    def test_create_tag(self, client):
        response = client.post('/tagging/vocab/api/tags',
                              data=json.dumps({'tag': 'test_api_tag', 'available': True}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'id' in data

    def test_create_tag_no_name(self, client):
        response = client.post('/tagging/vocab/api/tags',
                              data=json.dumps({'available': True}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_get_tags(self, client):
        # 先创建一个标签
        client.post('/tagging/vocab/api/tags',
                   data=json.dumps({'tag': 'list_test', 'available': True}),
                   content_type='application/json')

        response = client.get('/tagging/vocab/api/tags')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tags' in data
        assert 'total' in data
        assert 'page' in data

    def test_get_tags_with_filters(self, client):
        response = client.get('/tagging/vocab/api/tags?available=available&page=1&limit=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tags' in data

    def test_update_tag(self, client):
        # 创建标签
        create_response = client.post('/tagging/vocab/api/tags',
                                     data=json.dumps({'tag': 'update_test', 'available': True}),
                                     content_type='application/json')
        tag_id = json.loads(create_response.data)['id']

        # 更新标签
        response = client.put(f'/tagging/vocab/api/tags/{tag_id}',
                             data=json.dumps({'tag': 'updated_name', 'context': 'updated context'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_update_tag_not_found(self, client):
        response = client.put('/tagging/vocab/api/tags/99999',
                             data=json.dumps({'tag': 'updated'}),
                             content_type='application/json')
        assert response.status_code == 404

    def test_update_tag_no_data(self, client):
        response = client.put('/tagging/vocab/api/tags/1',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400

    def test_delete_tag(self, client):
        # 创建标签
        create_response = client.post('/tagging/vocab/api/tags',
                                     data=json.dumps({'tag': 'delete_test', 'available': True}),
                                     content_type='application/json')
        tag_id = json.loads(create_response.data)['id']

        # 删除标签
        response = client.delete(f'/tagging/vocab/api/tags/{tag_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_delete_tag_not_found(self, client):
        response = client.delete('/tagging/vocab/api/tags/99999')
        assert response.status_code == 404


class TestExportAPI:
    """测试导出API"""

    def test_export_protobuf(self, client):
        # 先创建一些数据
        client.post('/tagging/vocab/api/tags',
                   data=json.dumps({'tag': 'export_pb_test', 'available': True}),
                   content_type='application/json')

        response = client.get('/tagging/vocab/api/export/protobuf')
        assert response.status_code == 200
        assert response.content_type == 'application/octet-stream'

    def test_export_csv(self, client):
        # 先创建一些数据
        client.post('/tagging/vocab/api/tags',
                   data=json.dumps({'tag': 'export_csv_test', 'available': True}),
                   content_type='application/json')

        response = client.get('/tagging/vocab/api/export/csv')
        assert response.status_code == 200
        assert response.content_type == 'text/csv; charset=utf-8'
