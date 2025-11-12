"""
数据模型模块
"""

from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

db = SQLAlchemy()

# 导入所有模型
from .district import District
from .hotpot import HotpotRestaurant
from .brand import Brand
from .teahouse import Teahouse
from .night_economy import NightEconomy
from .alert import Alert

__all__ = [
    'db',
    'District',
    'HotpotRestaurant',
    'Brand',
    'Teahouse',
    'NightEconomy',
    'Alert'
]
