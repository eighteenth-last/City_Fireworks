"""
茶馆模型
"""

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from models import db
from datetime import datetime


class Teahouse(db.Model):
    """茶馆模型"""
    __tablename__ = 'teahouses'

    id = db.Column(db.Integer, primary_key=True, comment='茶馆ID')
    name = db.Column(db.String(200), nullable=False, comment='茶馆名称')
    address = db.Column(db.String(500), comment='地址')
    district_id = db.Column(
        db.Integer,
        db.ForeignKey('districts.id'),
        nullable=False,
        comment='区县ID'
    )

    # 基础信息
    founding_year = db.Column(db.Integer, comment='创立年份')
    tea_type = db.Column(db.String(200), comment='茶馆类型（逗号分隔）')
    avg_price = db.Column(db.Numeric(8, 2), comment='平均价格')
    popularity = db.Column(db.Integer, comment='受欢迎程度')
    is_historic = db.Column(db.Boolean, default=False, comment='是否历史悠久')
    community_type = db.Column(db.String(50), comment='社区类型')

    # 文化标签（JSON）
    cultural_tags = db.Column(db.Text, comment='文化标签（JSON格式）')

    # 空间坐标
    coordinates_lng = db.Column(db.Numeric(10, 7), comment='经度')
    coordinates_lat = db.Column(db.Numeric(10, 7), comment='纬度')
    location = db.Column(Geometry('POINT', srid=4326), comment='坐标')

    # 时间戳
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    update_time = db.Column(
        db.TIMESTAMP,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # 关联
    district = db.relationship('District', backref=db.backref('teahouses', lazy=True))

    # 索引
    __table_args__ = (
        db.Index('idx_district', 'district_id'),
        db.Index('idx_founding_year', 'founding_year'),
        db.Index('idx_popularity', 'popularity'),
    )

    def to_dict(self):
        """转换为字典格式"""
        data = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'district_id': self.district_id,
            'founding_year': self.founding_year,
            'tea_type': self.tea_type,
            'avg_price': float(self.avg_price) if self.avg_price else None,
            'popularity': self.popularity,
            'is_historic': self.is_historic,
            'community_type': self.community_type,
            'cultural_tags': [],
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

        # 解析文化标签
        if self.cultural_tags:
            try:
                import json
                data['cultural_tags'] = json.loads(self.cultural_tags)
            except:
                data['cultural_tags'] = []

        # 处理空间坐标（优先使用location）
        if self.location:
            location_shape = to_shape(self.location)
            coords = mapping(location_shape)['coordinates']
            # MySQL SRID 4326 存储格式是 POINT(lat lng)，所以 coords[0] 是纬度，coords[1] 是经度
            data['coordinates'] = {'lng': coords[1], 'lat': coords[0]}
        elif self.coordinates_lng and self.coordinates_lat:
            data['coordinates'] = {
                'lng': float(self.coordinates_lng),
                'lat': float(self.coordinates_lat)
            }

        return data

    def __repr__(self):
        return f'<Teahouse {self.name}>'
