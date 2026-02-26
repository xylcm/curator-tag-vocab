"""
Application configuration management.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Base configuration class."""
    SECRET_KEY: str = 'dev-secret-key-change-in-production'
    DEBUG: bool = False
    TESTING: bool = False
    DATABASE_PATH: str = 'vocab.db'
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'
    PORT: int = 80
    HOST: str = '0.0.0.0'


@dataclass
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG: bool = True


@dataclass
class TestingConfig(Config):
    """Testing configuration."""
    TESTING: bool = True
    DEBUG: bool = True
    DATABASE_PATH: str = ':memory:'


@dataclass
class ProductionConfig(Config):
    """Production configuration."""
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'production-secret-key')
    DEBUG: bool = False


def get_config(config_name: Optional[str] = None) -> Config:
    """Get configuration by name."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }

    config_class = configs.get(config_name, DevelopmentConfig)
    config = config_class()

    # Override with environment variables
    config.SECRET_KEY = os.environ.get('SECRET_KEY', config.SECRET_KEY)
    config.DATABASE_PATH = os.environ.get('DATABASE_PATH', config.DATABASE_PATH)
    config.PORT = int(os.environ.get('PORT', config.PORT))
    config.HOST = os.environ.get('HOST', config.HOST)

    return config
