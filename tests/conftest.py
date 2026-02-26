"""
测试配置和固件
"""
import os
import tempfile
import pytest
from src.app_tagging import create_tagging_app
from src.dao import DatabaseConnection, TagDAO


@pytest.fixture
def temp_db_path():
    """创建临时数据库文件"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    os.unlink(path)


@pytest.fixture
def db_connection(temp_db_path):
    """创建数据库连接"""
    return DatabaseConnection(temp_db_path)


@pytest.fixture
def tag_dao(db_connection):
    """创建TagDAO实例"""
    return TagDAO(db_connection)


@pytest.fixture
def app(temp_db_path):
    """创建Flask应用（测试模式）"""
    # 临时修改数据库路径
    original_init = DatabaseConnection.__init__

    def mock_init(self, db_path="vocab.db"):
        original_init(self, temp_db_path)

    DatabaseConnection.__init__ = mock_init

    app = create_tagging_app('testing')
    app.config['TESTING'] = True

    yield app

    # 恢复原始初始化
    DatabaseConnection.__init__ = original_init


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()
