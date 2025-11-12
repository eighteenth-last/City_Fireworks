"""
火锅店模型
"""

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from models import db
from datetime import datetime


class HotpotRestaurant(db.Model):
    """火锅店模型"""
    __tablename__ = 'hotpot_restaurants'

    id = db.Column(db.Integer, primary_key=True, comment='店铺ID')
    name = db.Column(db.String(200), nullable=False, comment='店铺名称')
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), comment='品牌ID')
    address = db.Column(db.String(500), comment='地址')
    district_id = db.Column(
        db.Integer,
        db.ForeignKey('districts.id'),
        nullable=False,
        comment='区县ID'
    )

    # 价格信息
    price_min = db.Column(db.Integer, comment='最低价')
    price_max = db.Column(db.Integer, comment='最高价')
    price_avg = db.Column(db.Integer, comment='平均价')

    # 评价信息
    rating = db.Column(db.Numeric(3, 1), comment='评分')
    review_count = db.Column(db.Integer, comment='评价数')

    # 店铺信息
    shop_type = db.Column(db.String(50), comment='店铺类型')
    business_hours = db.Column(db.String(100), comment='营业时间')
    is_24h = db.Column(db.Boolean, default=False, comment='是否24小时营业')
    open_date = db.Column(db.Date, comment='开业日期')
    status = db.Column(db.SmallInteger, default=1, comment='营业状态：1-营业，0-停业')

    # 空间坐标（支持两种方式）
    coordinates_lng = db.Column(db.Numeric(10, 7), comment='经度')
    coordinates_lat = db.Column(db.Numeric(10, 7), comment='纬度')
    location = db.Column(Geometry('POINT', srid=4326), comment='坐标')

    # 时间戳
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.TIMESTAMP,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # 关联
    brand = db.relationship('Brand', backref=db.backref('restaurants', lazy=True))
    district = db.relationship('District', backref=db.backref('restaurants', lazy=True))

    # 索引
    __table_args__ = (
        db.Index('idx_district', 'district_id'),
        db.Index('idx_brand', 'brand_id'),
        db.Index('idx_rating', 'rating'),
        db.Index('idx_coordinates', 'coordinates_lng', 'coordinates_lat'),
    )

    def to_dict(self):
        """转换为字典格式"""
        data = {
            'id': self.id,
            'name': self.name,
            'brand_id': self.brand_id,
            'address': self.address,
            'district_id': self.district_id,
            'price_min': self.price_min,
            'price_max': self.price_max,
            'price_avg': self.price_avg,
            'rating': float(self.rating) if self.rating else None,
            'review_count': self.review_count,
            'shop_type': self.shop_type,
            'business_hours': self.business_hours,
            'is_24h': self.is_24h,
            'open_date': self.open_date.isoformat() if self.open_date else None,
            'status': self.status
        }

        # 处理空间坐标（优先使用 location）
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
        return f'<HotpotRestaurant {self.name}>'
