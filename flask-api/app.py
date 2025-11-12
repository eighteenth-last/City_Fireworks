"""
重庆城市人文市井烟火大屏 - Flask API 应用入口
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
from models import db
from routes import register_routes
from utils.database import init_db
from utils.error_handler import register_error_handlers
import logging

def create_app(config_name=None):
    """Flask 应用工厂"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    # 注册路由
    register_routes(app)
    
    # 注册错误处理器
    register_error_handlers(app)

    # 初始化数据库
    with app.app_context():
        init_db()

    # 配置日志
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
