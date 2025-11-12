"""
火锅品牌模型
"""

from models import db
from datetime import datetime


class Brand(db.Model):
    """火锅品牌模型"""
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment='品牌名称')
    market_share = db.Column(db.Numeric(5, 2), comment='市场份额')
    avg_wait_time = db.Column(db.Integer, comment='平均等待时间（分钟）')
    store_count = db.Column(db.Integer, comment='门店数量')
    price_position = db.Column(
        db.Enum('大众', '中端', '高端', '奢华', name='price_position'),
        default='中端',
        comment='价位定位'
    )
    update_date = db.Column(db.Date, default=datetime.utcnow, comment='更新日期')

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
        db.Index('idx_market_share', 'market_share'),
    )

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'market_share': float(self.market_share) if self.market_share else None,
            'avg_wait_time': self.avg_wait_time,
            'store_count': self.store_count,
            'price_position': self.price_position,
            'update_date': self.update_date.isoformat() if self.update_date else None
        }

    def __repr__(self):
        return f'<Brand {self.name}>'
