"""
预警数据模型
"""

from models import db
from datetime import datetime


class Alert(db.Model):
    """预警信息模型"""
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True, comment='预警ID')
    alert_time = db.Column(db.TIMESTAMP, nullable=False, comment='预警时间')
    alert_type = db.Column(db.String(50), nullable=False, comment='预警类型')
    content = db.Column(db.Text, comment='预警内容')
    impact_value = db.Column(db.String(100), comment='影响值')
    status = db.Column(db.SmallInteger, default=1, comment='状态：1-活跃，0-已处理')

    # 时间戳
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # 索引
    __table_args__ = (
        db.Index('idx_alert_time', 'alert_time'),
        db.Index('idx_alert_type', 'alert_type'),
        db.Index('idx_status', 'status'),
    )

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'alert_time': self.alert_time.isoformat() if self.alert_time else None,
            'alert_type': self.alert_type,
            'content': self.content,
            'impact_value': self.impact_value,
            'status': self.status
        }

    def __repr__(self):
        return f'<Alert {self.alert_type} {self.alert_time}>'
