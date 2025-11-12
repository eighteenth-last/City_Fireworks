"""
统一响应格式化工具
"""

from flask import jsonify
from typing import Any, Optional


def success_response(data: Any = None, message: str = 'success', code: int = 200):
    """成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: HTTP 状态码
    
    Returns:
        JSON 响应
    """
    response = {
        'status': 'success',
        'message': message,
        'data': data
    }
    return jsonify(response), code


def error_response(message: str, code: int = 400, errors: Optional[dict] = None):
    """错误响应
    
    Args:
        message: 错误消息
        code: HTTP 状态码
        errors: 详细错误信息
    
    Returns:
        JSON 响应
    """
    response = {
        'status': 'error',
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), code


def paginated_response(items: list, page: int, per_page: int, total: int):
    """分页响应
    
    Args:
        items: 数据列表
        page: 当前页码
        per_page: 每页数量
        total: 总数量
    
    Returns:
        JSON 响应
    """
    response = {
        'status': 'success',
        'data': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }
    return jsonify(response), 200
