"""
数据导出服务
"""

from models import District, HotpotRestaurant, Brand, Teahouse, NightEconomy, Alert
import csv
import os
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Optional


class ExportService:
    """数据导出服务类"""

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def export_districts(self) -> str:
        """导出区县数据为CSV"""
        filename = os.path.join(self.temp_dir, f'districts_{datetime.now().strftime("%Y%m%d")}.csv')
        districts = District.query.all()

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'area_km2', 'hotpot_density', 'population', 'vitality_score'])
            writer.writeheader()
            for d in districts:
                writer.writerow(d.to_dict())

        return filename

    def export_hotpots(self) -> str:
        """导出火锅店数据为CSV"""
        filename = os.path.join(self.temp_dir, f'hotpots_{datetime.now().strftime("%Y%m%d")}.csv')
        restaurants = HotpotRestaurant.query.all()

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'name', 'brand_id', 'address', 'district_id',
                'price_min', 'price_max', 'price_avg', 'rating', 'review_count',
                'shop_type', 'business_hours', 'is_24h', 'open_date', 'status'
            ])
            writer.writeheader()
            for r in restaurants:
                writer.writerow(r.to_dict())

        return filename

    def export_teahouses(self) -> str:
        """导出茶馆数据为CSV"""
        filename = os.path.join(self.temp_dir, f'teahouses_{datetime.now().strftime("%Y%m%d")}.csv')
        teahouses = Teahouse.query.all()

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'name', 'address', 'district_id', 'founding_year',
                'tea_type', 'avg_price', 'popularity', 'is_historic',
                'community_type', 'cultural_tags', 'update_time'
            ])
            writer.writeheader()
            for t in teahouses:
                writer.writerow(t.to_dict())

        return filename

    def export_brands(self) -> str:
        """导出品牌数据为CSV"""
        filename = os.path.join(self.temp_dir, f'brands_{datetime.now().strftime("%Y%m%d")}.csv')
        brands = Brand.query.all()

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'name', 'market_share', 'avg_wait_time',
                'store_count', 'price_position', 'update_date'
            ])
            writer.writeheader()
            for b in brands:
                writer.writerow(b.to_dict())

        return filename

    def export_night_economy(self) -> str:
        """导出夜间经济数据为CSV"""
        filename = os.path.join(self.temp_dir, f'night_economy_{datetime.now().strftime("%Y%m%d")}.csv')
        data = NightEconomy.query.all()

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'timestamp', 'hour', 'district_id', 'population_index',
                'consumption_heat', 'metro_passengers', 'active_businesses',
                'weather', 'special_event', 'date', 'time'
            ])
            writer.writeheader()
            for item in data:
                writer.writerow(item.to_dict())

        return filename

    def export_alerts(self) -> str:
        """导出预警数据为CSV"""
        filename = os.path.join(self.temp_dir, f'alerts_{datetime.now().strftime("%Y%m%d")}.csv')
        alerts = Alert.query.all()

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'alert_time', 'alert_type', 'content', 'impact_value', 'status'
            ])
            writer.writeheader()
            for a in alerts:
                writer.writerow(a.to_dict())

        return filename

    def export_by_table(self, table_name: str) -> Optional[str]:
        """按表名导出数据"""
        export_map = {
            'districts': self.export_districts,
            'hotpots': self.export_hotpots,
            'teahouses': self.export_teahouses,
            'brands': self.export_brands,
            'night-economy': self.export_night_economy,
            'night_economy': self.export_night_economy,
            'alerts': self.export_alerts
        }

        if table_name in export_map:
            return export_map[table_name]()

        return None

    def export_all_data(self) -> str:
        """导出所有数据为CSV（合并所有表）"""
        filename = os.path.join(self.temp_dir, f'city_fireworks_all_{datetime.now().strftime("%Y%m%d")}.csv')

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            # 分别导出各个表到不同的临时文件
            tables = {
                'districts': District.query.all(),
                'hotpots': HotpotRestaurant.query.all(),
                'teahouses': Teahouse.query.all(),
                'brands': Brand.query.all(),
                'night_economy': NightEconomy.query.all(),
                'alerts': Alert.query.all()
            }

            # 先写入表头信息
            for table_name, data in tables.items():
                f.write(f'# {table_name}\n')
                if data:
                    # 获取字段名
                    fieldnames = list(data[0].to_dict().keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    # 写入数据
                    for item in data:
                        writer.writerow(item.to_dict())

                f.write('\n\n')  # 表之间空行分隔

        return filename
