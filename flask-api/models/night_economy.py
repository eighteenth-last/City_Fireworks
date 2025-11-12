"""
夜间经济数据模型
"""

from models import db
from datetime import datetime


class NightEconomy(db.Model):
    """夜间经济数据模型"""
    __tablename__ = 'night_economy'

    id = db.Column(db.Integer, primary_key=True, comment='数据ID')
    timestamp = db.Column(db.TIMESTAMP, nullable=False, comment='时间戳')
    hour = db.Column(db.SmallInteger, nullable=False, comment='小时（0-23）')
    district_id = db.Column(
        db.Integer,
        db.ForeignKey('districts.id'),
        nullable=False,
        comment='区县ID'
    )

    # 数据指标
    population_index = db.Column(db.Integer, comment='人口指数')
    consumption_heat = db.Column(db.Numeric(10, 2), comment='消费热度')
    metro_passengers = db.Column(db.Integer, comment='地铁乘客数')
    active_businesses = db.Column(db.Integer, comment='活跃商家数')

    # 环境信息
    weather = db.Column(db.String(50), comment='天气')
    special_event = db.Column(db.String(200), comment='特殊事件')

    # 日期时间
    date = db.Column(db.DATE, nullable=False, comment='日期')
    time = db.Column(db.TIME, nullable=False, comment='时间')

    # 时间戳
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # 关联
    district = db.relationship('District', backref=db.backref('night_economy', lazy=True))

    # 索引
    __table_args__ = (
        db.Index('idx_timestamp', 'timestamp'),
        db.Index('idx_district_hour', 'district_id', 'hour'),
        db.Index('idx_date', 'date'),
    )

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'hour': self.hour,
            'district_id': self.district_id,
            'population_index': self.population_index,
            'consumption_heat': float(self.consumption_heat) if self.consumption_heat else None,
            'metro_passengers': self.metro_passengers,
            'active_businesses': self.active_businesses,
            'weather': self.weather,
            'special_event': self.special_event,
            'date': self.date.isoformat() if self.date else None,
            'time': str(self.time) if self.time else None
        }

    def __repr__(self):
        return f'<NightEconomy {self.date} {self.hour}:00>'
