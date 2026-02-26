"""
数据访问层 - 数据库操作封装
"""
from .tag_dao import TagDAO
from .base import DatabaseConnection

__all__ = ['TagDAO', 'DatabaseConnection']
