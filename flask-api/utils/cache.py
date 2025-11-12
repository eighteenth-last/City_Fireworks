"""
缓存工具模块
提供简单的内存缓存功能
"""

from functools import wraps
from datetime import datetime, timedelta
import json


class SimpleCache:
    """简单的内存缓存类"""
    
    def __init__(self):
        self._cache = {}
        self._expire_times = {}
    
    def get(self, key):
        """获取缓存"""
        if key not in self._cache:
            return None
        
        # 检查是否过期
        if key in self._expire_times:
            if datetime.now() > self._expire_times[key]:
                self.delete(key)
                return None
        
        return self._cache[key]
    
    def set(self, key, value, timeout=300):
        """设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            timeout: 过期时间（秒），默认5分钟
        """
        self._cache[key] = value
        if timeout:
            self._expire_times[key] = datetime.now() + timedelta(seconds=timeout)
    
    def delete(self, key):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
        if key in self._expire_times:
            del self._expire_times[key]
    
    def clear(self):
        """清空所有缓存"""
        self._cache.clear()
        self._expire_times.clear()
    
    def cleanup(self):
        """清理过期缓存"""
        now = datetime.now()
        expired_keys = [
            key for key, expire_time in self._expire_times.items()
            if now > expire_time
        ]
        for key in expired_keys:
            self.delete(key)


# 全局缓存实例
cache = SimpleCache()


def cache_response(timeout=300, key_prefix=''):
    """缓存装饰器
    
    Args:
        timeout: 缓存过期时间（秒）
        key_prefix: 缓存键前缀
    
    Example:
        @cache_response(timeout=600, key_prefix='districts')
        def get_districts():
            return District.query.all()
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{f.__name__}"
            if args:
                cache_key += f":{str(args)}"
            if kwargs:
                cache_key += f":{json.dumps(kwargs, sort_keys=True)}"
            
            # 尝试从缓存获取
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
            
            # 执行函数并缓存结果
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            
            return result
        return decorated_function
    return decorator


def clear_cache_by_prefix(prefix):
    """清除指定前缀的缓存
    
    Args:
        prefix: 缓存键前缀
    """
    keys_to_delete = [
        key for key in cache._cache.keys()
        if key.startswith(prefix)
    ]
    for key in keys_to_delete:
        cache.delete(key)
