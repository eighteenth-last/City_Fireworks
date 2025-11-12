"""
区县数据模型
"""

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from models import db


class District(db.Model):
    """区县模型"""
    __tablename__ = 'districts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='区县名称')
    area_km2 = db.Column(db.Numeric(10, 2), comment='面积（平方公里）')
    hotpot_density = db.Column(db.Numeric(10, 2), comment='火锅店密度')
    population = db.Column(db.Integer, comment='人口数量')
    vitality_score = db.Column(db.Numeric(5, 2), comment='活力指数')

    # 空间数据
    center = db.Column(Geometry('POINT', srid=4326), comment='中心点坐标')
    boundary = db.Column(Geometry('MULTIPOLYGON', srid=4326), comment='边界多边形')

    # 时间戳
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.TIMESTAMP,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # 索引
    __table_args__ = (
        db.Index('idx_name', 'name'),
        db.Index('idx_vitality_score', 'vitality_score'),
    )

    def to_dict(self):
        """转换为字典格式"""
        data = {
            'id': self.id,
            'name': self.name,
            'area_km2': float(self.area_km2) if self.area_km2 else None,
            'hotpot_density': float(self.hotpot_density) if self.hotpot_density else None,
            'population': self.population,
            'vitality_score': float(self.vitality_score) if self.vitality_score else None,
        }

        # 处理空间数据
        if self.center:
            center_shape = to_shape(self.center)
            coords = mapping(center_shape)['coordinates']
            # MySQL SRID 4326 存储格式是 POINT(lat lng)，所以 coords[0] 是纬度，coords[1] 是经度
            data['center_coords'] = {'lng': coords[1], 'lat': coords[0]}

        if self.boundary:
            boundary_shape = to_shape(self.boundary)
            data['boundary_coords'] = mapping(boundary_shape)['coordinates'][0]

        return data

    def __repr__(self):
        return f'<District {self.name}>'
