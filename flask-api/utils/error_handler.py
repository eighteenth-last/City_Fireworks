"""
统一错误处理模块
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)


class APIError(Exception):
    """API 自定义错误类"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status'] = 'error'
        return rv


def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """处理自定义 API 错误"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logger.error(f"API Error: {error.message}")
        return response
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """处理 HTTP 异常"""
        response = jsonify({
            'error': error.description,
            'status': 'error',
            'code': error.code
        })
        response.status_code = error.code
        logger.warning(f"HTTP Exception: {error.code} - {error.description}")
        return response
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """处理未预期的错误"""
        logger.exception("Unexpected error occurred")
        response = jsonify({
            'error': '服务器内部错误',
            'status': 'error',
            'message': str(error) if app.debug else '请稍后重试'
        })
        response.status_code = 500
        return response
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """处理 404 错误"""
        response = jsonify({
            'error': '资源未找到',
            'status': 'error',
            'code': 404
        })
        response.status_code = 404
        return response
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """处理方法不允许错误"""
        response = jsonify({
            'error': '请求方法不允许',
            'status': 'error',
            'code': 405
        })
        response.status_code = 405
        return response
