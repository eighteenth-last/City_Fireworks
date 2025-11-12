"""
Flask 配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 数据库配置
    DB_HOST = os.environ.get('DB_HOST', '172.31.142.67')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'qwer4321')
    DB_NAME = os.environ.get('DB_NAME', 'city_fireworks')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,          # 连接池大小
        'pool_recycle': 3600,     # 连接回收时间（秒）
        'pool_pre_ping': True,    # 连接前检查
        'max_overflow': 20,       # 超出pool_size后最多创建的连接数
        'pool_timeout': 30,       # 获取连接的超时时间
        'echo': False
    }

    # API 配置
    RESTX_MASK_SWAGGER = False
    JSON_AS_ASCII = False  # 支持中文显示
    JSON_SORT_KEYS = False

    # 缓存配置（可选 Redis）
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache')
    CACHE_REDIS_HOST = os.environ.get('REDIS_HOST', '172.31.142.67')
    CACHE_REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    CACHE_REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    CACHE_REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
    CACHE_DEFAULT_TIMEOUT = 300

    # 日志级别
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'echo': True  # 显示 SQL 语句
    }


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 在生产环境中必须从环境变量读取
    if not os.environ.get('DB_PASSWORD'):
        raise ValueError("生产环境必须设置 DB_PASSWORD 环境变量")


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
