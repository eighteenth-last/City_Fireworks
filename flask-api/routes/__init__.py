"""
API路由模块
"""

from flask import Flask
from flask_restx import Api
from .map_routes import register_map_routes
from .hotpot_routes import register_hotpot_routes
from .night_routes import register_night_routes
from .teahouse_routes import register_teahouse_routes
from .insight_routes import register_insight_routes
from .export_routes import register_export_routes


def register_routes(app: Flask):
    """注册所有路由"""
    api = Api(
        app,
        version='1.0',
        title='重庆城市人文市井烟火大屏 API',
        description='提供城市数据可视化API服务',
        doc='/api/docs',
        prefix='/api'
    )

    # 注册各个模块路由
    register_map_routes(api)
    register_hotpot_routes(api)
    register_night_routes(api)
    register_teahouse_routes(api)
    register_insight_routes(api)
    register_export_routes(api)
