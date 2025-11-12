#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《市井烟火》重庆城市人文数据生成器
基于MySQL DDL表结构生成模拟数据，支持导出SQL/CSV
"""

import json
import random
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import argparse
import os
import pymysql
from pymysql.cursors import DictCursor

# ==================== 基础配置 ====================
# 重庆地理范围
CHONGQING_BOUNDS = {
    "lat_min": 28.5,
    "lat_max": 30.5,
    "lng_min": 105.5,
    "lng_max": 107.5,
    "center_lat": 29.563,
    "center_lng": 106.551
}

# 重庆38个区县
DISTRICTS = [
    # 主城九区
    "渝中区", "江北区", "南岸区", "沙坪坝区", "九龙坡区",
    "大渡口区", "北碚区", "渝北区", "巴南区",
    # 其他区
    "万州区", "涪陵区", "黔江区", "长寿区", "永川区", 
    "合川区", "江津区", "南川区", "綦江区", "大足区", 
    "璧山区", "铜梁区", "潼南区", "荣昌区", "开州区", 
    "梁平区", "武隆区",
    # 县
    "城口县", "丰都县", "垫江县", "忠县", "云阳县",
    "奉节县", "巫山县", "巫溪县", "石柱县", "秀山县",
    "酉阳县", "彭水县"
]

# 知名火锅品牌
HOTPOT_BRANDS = [
    "佩姐老火锅", "周师兄火锅", "秦妈火锅", "德庄火锅",
    "小天鹅火锅", "刘一手火锅", "桥头火锅", "渝味晓宇",
    "大龙火锅", "巴将军火锅"
]

# 茶馆特色标签
TEA_FEATURES = ["盖碗茶", "川剧", "评书", "采耳", "麻将", "茶艺", "古筝"]

# 预警类型
ALERT_TYPES = ["暴雨预警", "高温预警", "节假日高峰", "交通管制", "演唱会活动", "体育赛事"]


@dataclass
class District:
    """区县基础数据 - 适配数据库表结构"""
    __tablename__ = 'districts'

    id: int
    name: str
    area_km2: float
    hotpot_density: float
    population: int
    vitality_score: float
    center: str  # POINT WKT 格式
    boundary: str  # MULTIPOLYGON WKT 格式
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Brand:
    """火锅品牌维度"""
    __tablename__ = 'brands'

    id: int
    name: str
    market_share: float
    avg_wait_time: int
    store_count: int
    price_position: str
    update_date: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class HotpotRestaurant:
    """火锅门店 - 适配数据库表结构"""
    __tablename__ = 'hotpot_restaurants'

    id: int
    name: str
    brand_id: Optional[int]
    address: str
    district_id: int
    price_min: int
    price_max: int
    price_avg: int
    rating: float
    review_count: int
    shop_type: str
    business_hours: str
    is_24h: bool
    open_date: str
    status: int
    coordinates_lng: float  # 经度
    coordinates_lat: float  # 纬度
    location: str  # POINT WKT 格式
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Teahouse:
    """茶馆 - 适配数据库表结构"""
    __tablename__ = 'teahouses'

    id: int
    name: str
    address: str
    district_id: int
    founding_year: int
    tea_type: str  # 逗号分隔字符串
    avg_price: float
    popularity: int
    is_historic: bool
    community_type: str
    cultural_tags: str  # JSON字符串
    coordinates_lng: float  # 经度
    coordinates_lat: float  # 纬度
    location: str  # POINT WKT 格式
    created_at: Optional[str] = None
    update_time: Optional[str] = None


@dataclass
class NightEconomyRealtime:
    """夜间经济实时数据 - 适配数据库表结构"""
    __tablename__ = 'night_economy'

    id: int
    timestamp: str
    hour: int
    district_id: int
    population_index: int
    consumption_heat: float
    metro_passengers: int
    active_businesses: int
    weather: str
    special_event: Optional[str]
    date: str
    time: str
    created_at: Optional[str] = None


@dataclass
class Alert:
    """实时预警"""
    __tablename__ = 'alerts'

    id: int
    alert_time: str
    alert_type: str
    content: str
    impact_value: str
    status: int
    created_at: Optional[str] = None


class DataGenerator:
    def __init__(self):
        self.district_centers = {}
        self.brand_ids = {}

    def generate_wkt_point(self, lng: float, lat: float) -> str:
        """生成MySQL POINT WKT格式字符串"""
        # 对于 SRID 4326（WGS84），MySQL 期望的格式是 POINT(纬度 经度)
        # 这与常规的 (经度, 纬度) 顺序相反
        # 纬度范围：-90 到 90，经度范围：-180 到 180
        return f"POINT({lat} {lng})"

    def generate_wkt_multipolygon(self, center_lng: float, center_lat: float, radius: float = 0.1) -> str:
        """生成 MULTIPOLYGON WKT 格式"""
        # 生成一个简单的矩形多边形
        # 对于 SRID 4326，MySQL 期望的格式是 (纬度 经度)
        points = [
            (center_lat - radius, center_lng - radius),
            (center_lat + radius, center_lng - radius),
            (center_lat + radius, center_lng + radius),
            (center_lat - radius, center_lng + radius),
            (center_lat - radius, center_lng - radius)  # 闭合
        ]
        coords = ", ".join([f"{lat} {lng}" for lat, lng in points])
        return f"MULTIPOLYGON((({coords})))"

    def random_location(self, district_name: str = None) -> tuple:
        """生成随机坐标"""
        if district_name and district_name in self.district_centers:
            base_lng, base_lat = self.district_centers[district_name]
            # 在区县中心点附近随机偏移（增大偏移范围）
            lng = base_lng + random.uniform(-0.15, 0.15)
            lat = base_lat + random.uniform(-0.12, 0.12)
        else:
            # 如果没有指定区县，在整个重庆范围内随机生成
            lng = random.uniform(CHONGQING_BOUNDS["lng_min"], CHONGQING_BOUNDS["lng_max"])
            lat = random.uniform(CHONGQING_BOUNDS["lat_min"], CHONGQING_BOUNDS["lat_max"])

        # 确保在边界内
        lng = max(CHONGQING_BOUNDS["lng_min"], min(CHONGQING_BOUNDS["lng_max"], lng))
        lat = max(CHONGQING_BOUNDS["lat_min"], min(CHONGQING_BOUNDS["lat_max"], lat))

        return round(lng, 7), round(lat, 7)

    def time_series_value(self, hour: int, base_value: int, peak_hour: int = 21) -> int:
        """生成基于时间节律的值"""
        # 使用正弦波模拟
        distance = abs(hour - peak_hour)
        wave = 1 + 0.8 * (1 - min(distance, 12) / 12)
        noise = random.uniform(0.7, 1.3)
        return int(base_value * wave * noise)


class TableGenerator:
    def __init__(self):
        self.gen = DataGenerator()
        self.next_id = {
            'district': 1,
            'brand': 1,
            'hotpot': 1,
            'teahouse': 1,
            'night': 1,
            'alert': 1
        }

    def generate_districts(self) -> List[District]:
        """生成区县基础数据（必须最先执行）- 适配Flask模型"""
        results = []
        main_city_ids = range(1, 10)  # 主城九区

        for i, name in enumerate(DISTRICTS, 1):
            # 生成区县中心点
            center_lng, center_lat = self.gen.random_location()
            self.gen.district_centers[name] = (center_lng, center_lat)

            # 主城九区密度更高
            is_main_city = i < 10
            density = random.uniform(15, 25) if is_main_city else random.uniform(0.5, 5)
            population = random.randint(300000, 2000000) if is_main_city else random.randint(50000, 500000)
            vitality = random.uniform(80, 95) if is_main_city else random.uniform(60, 85)

            # 生成 WKT 格式的中心点和边界
            center_wkt = self.gen.generate_wkt_point(center_lng, center_lat)
            boundary_wkt = self.gen.generate_wkt_multipolygon(center_lng, center_lat,
                                                               radius=0.15 if is_main_city else 0.3)

            results.append(District(
                id=i,
                name=name,
                area_km2=round(random.uniform(50 if is_main_city else 1000,
                                              350 if is_main_city else 4000), 2),
                hotpot_density=round(density, 2),
                population=population,
                vitality_score=round(vitality, 1),
                center=center_wkt,
                boundary=boundary_wkt,
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

        self.next_id['district'] = len(results) + 1
        return results



    def generate_brands(self) -> List[Brand]:
        """生成品牌维度数据（第二执行）"""
        results = []
        # 确保市场份额总和约100%
        remaining_share = 100.0
        brand_count = len(HOTPOT_BRANDS)

        for i, brand_name in enumerate(HOTPOT_BRANDS, 1):
            if i == brand_count:
                share = round(remaining_share, 1)
            else:
                share = round(random.uniform(5, min(20, remaining_share - (brand_count - i) * 5)), 1)
                remaining_share -= share

            self.gen.brand_ids[brand_name] = i

            results.append(Brand(
                id=i,
                name=brand_name,
                market_share=share,
                avg_wait_time=random.randint(15, 90),
                store_count=random.randint(50, 300),
                price_position=random.choice(['高端', '中端', '大众']),
                update_date=datetime.now().strftime('%Y-%m-%d'),
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

        self.next_id['brand'] = len(results) + 1
        return results

    def generate_hotpot_restaurants(self, count: int = 8000) -> List[HotpotRestaurant]:
        """生成火锅门店数据 - 适配Flask模型"""
        results = []
        # 主城九区占70%门店
        main_districts = list(range(1, 10))
        other_districts = list(range(10, len(DISTRICTS) + 1))

        for i in range(count):
            # 70%概率选择主城九区
            district_id = random.choice(main_districts) if random.random() < 0.7 else random.choice(other_districts)
            district_name = DISTRICTS[district_id - 1]

            # 随机坐标
            lng, lat = self.gen.random_location(district_name)

            # 品牌（80%使用知名品牌，20%个体经营）
            if random.random() < 0.8:
                brand_id = random.randint(1, len(HOTPOT_BRANDS))
            else:
                brand_id = None  # 个体经营

            # 价格逻辑
            shop_type = random.choice(['老字号', '网红店', '社区店', '连锁'])
            if shop_type == '社区店':
                price_avg = random.randint(60, 90)
            elif shop_type == '网红店':
                price_avg = random.randint(120, 250)
            else:
                price_avg = random.randint(80, 150)

            price_min = max(30, price_avg - random.randint(10, 30))
            price_max = price_avg + random.randint(20, 50)

            # 评分和评论数
            rating = round(random.uniform(3.5, 4.8), 1)
            review_count = random.randint(50, 5000)

            # 开业日期
            days_ago = random.randint(30, 7300)
            open_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

            # 是否24小时营业（5%概率）
            is_24h = random.random() < 0.05

            # 生成 POINT WKT
            location_wkt = self.gen.generate_wkt_point(lng, lat)

            results.append(HotpotRestaurant(
                id=self.next_id['hotpot'],
                name=f"{district_name}{random.choice(['老', '重庆', '地道'])}{random.choice(['火锅', '老火锅'])}",
                brand_id=brand_id,
                address=f"{district_name}{random.randint(1, 500)}号",
                district_id=district_id,
                price_min=price_min,
                price_max=price_max,
                price_avg=price_avg,
                rating=rating,
                review_count=review_count,
                shop_type=shop_type,
                business_hours="00:00-24:00" if is_24h else f"{random.randint(9, 11)}:00-23:00",
                is_24h=is_24h,
                open_date=open_date,
                status=1,
                coordinates_lng=lng,
                coordinates_lat=lat,
                location=location_wkt,
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            self.next_id['hotpot'] += 1

        return results

    def generate_teahouses(self, count: int = 500) -> List[Teahouse]:
        """生成茶馆数据 - 适配Flask模型"""
        results = []

        for i in range(count):
            district_id = random.randint(1, len(DISTRICTS))
            district_name = DISTRICTS[district_id - 1]
            lng, lat = self.gen.random_location(district_name)

            # 百年老店概率
            is_historic = random.random() < 0.08
            founding_year = random.randint(1900, 1950) if is_historic else random.randint(1950, 2024)

            # 特色标签
            features = random.sample(TEA_FEATURES, random.randint(1, 3))

            # 类型
            if founding_year < 1950:
                community_type = '社区型'
            elif founding_year < 2000:
                community_type = random.choice(['社区型', '景区型'])
            else:
                community_type = random.choice(['景区型', '商务型'])

            # 生成 POINT WKT
            location_wkt = self.gen.generate_wkt_point(lng, lat)

            results.append(Teahouse(
                id=self.next_id['teahouse'],
                name=f"{district_name}{random.choice(['老茶馆', '茶舍', '茶园', '茶艺馆'])}",
                address=f"{district_name}{random.randint(1, 500)}号",
                district_id=district_id,
                founding_year=founding_year,
                tea_type=','.join(features),
                avg_price=round(random.uniform(15, 80), 2),
                popularity=random.randint(10, 1000),
                is_historic=is_historic,
                community_type=community_type,
                cultural_tags=json.dumps(features),
                coordinates_lng=lng,
                coordinates_lat=lat,
                location=location_wkt,
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            self.next_id['teahouse'] += 1

        return results

    def generate_night_economy(self, days: int = 7) -> List[NightEconomyRealtime]:
        """生成夜间经济实时数据"""
        results = []
        weather_options = ['晴天', '多云', '小雨', '阴天']

        # 只为主城九区生成数据
        main_district_ids = list(range(1, 10))

        for day in range(days):
            for hour in range(24):
                for district_id in main_district_ids:
                    # 基础人流
                    base_population = random.randint(1000, 8000)
                    population = self.gen.time_series_value(hour, base_population)

                    # 特殊事件（低概率）
                    special_event = ''
                    if random.random() < 0.02:
                        special_event = random.choice(['演唱会', '体育赛事', '节日活动'])

                    # 计算日期和时间
                    current_datetime = (datetime.now() - timedelta(days=day)).replace(
                        hour=hour, minute=0, second=0
                    )
                    timestamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    date_str = current_datetime.strftime('%Y-%m-%d')
                    time_str = current_datetime.strftime('%H:%M:%S')

                    results.append(NightEconomyRealtime(
                        id=self.next_id['night'],
                        timestamp=timestamp,
                        hour=hour,
                        district_id=district_id,
                        population_index=population,
                        consumption_heat=round(population * random.uniform(0.8, 1.5), 2),
                        metro_passengers=random.randint(5000, 20000) if 6 <= hour <= 23 else random.randint(200, 2000),
                        active_businesses=random.randint(500, 3000),
                        weather=random.choice(weather_options),
                        special_event=special_event if special_event else None,
                        date=date_str,
                        time=time_str,
                        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ))
                    self.next_id['night'] += 1

        return results

    def generate_alerts(self, count: int = 50) -> List[Alert]:
        """生成预警数据"""
        results = []

        for i in range(count):
            alert_type = random.choice(ALERT_TYPES)
            district_name = random.choice(DISTRICTS)

            results.append(Alert(
                id=self.next_id['alert'],
                alert_time=(datetime.now() - timedelta(hours=random.randint(0, 168))).strftime('%Y-%m-%d %H:%M:%S'),
                alert_type=alert_type,
                content=f"{district_name} {alert_type}：{random.choice(['火锅预订率↑', '交通延误↑', '人流激增↑'])}",
                impact_value=f"+{random.randint(10, 50)}%",
                status=random.choice([0, 1]),
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            self.next_id['alert'] += 1

        return results


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, host='localhost', port=3306, user='root', password='', database='city_fireworks'):
        """初始化数据库连接"""
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(**self.config)
            print(f"✅ 成功连接到数据库: {self.config['database']}")
            return True
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("✅ 数据库连接已关闭")
    
    def check_tables_have_data(self, tables: List[str]) -> bool:
        """检查表中是否有数据"""
        try:
            with self.connection.cursor() as cursor:
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                    result = cursor.fetchone()
                    if result and result['count'] > 0:
                        return True
            return False
        except Exception as e:
            # 如果表不存在或其他错误，返回 False
            return False
    
    def clear_table(self, table_name: str):
        """清空表数据并重置自增ID"""
        try:
            with self.connection.cursor() as cursor:
                # 先删除数据
                cursor.execute(f"DELETE FROM {table_name}")
                # 重置自增ID
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")
                self.connection.commit()
                print(f"✅ 已清空表: {table_name}")
        except Exception as e:
            print(f"⚠️  清空表 {table_name} 失败: {e}")
    
    def insert_batch(self, data: List[Any], table_name: str, batch_size: int = 1000):
        """批量插入数据"""
        if not data:
            return 0
        
        fields = [f.name for f in data[0].__dataclass_fields__.values()]
        
        # 对于包含 WKT 格式的字段，使用 ST_GeomFromText
        geo_fields = ['center', 'boundary', 'location']
        placeholders = []
        for field in fields:
            if field in geo_fields:
                placeholders.append('ST_GeomFromText(%s, 4326)')
            else:
                placeholders.append('%s')
        
        sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
        
        inserted = 0
        try:
            with self.connection.cursor() as cursor:
                # 分批插入
                for i in range(0, len(data), batch_size):
                    batch = data[i:i + batch_size]
                    values = []
                    for item in batch:
                        row = []
                        for field in fields:
                            val = getattr(item, field)
                            if val is None or val == '':
                                row.append(None)
                            else:
                                row.append(val)
                        values.append(tuple(row))
                    
                    cursor.executemany(sql, values)
                    inserted += len(batch)
                    print(f"  已插入 {inserted}/{len(data)} 条数据...", end='\r')
                
                self.connection.commit()
                print(f"\n✅ 成功插入 {inserted} 条数据到 {table_name}")
                return inserted
        except Exception as e:
            self.connection.rollback()
            error_msg = str(e)
            if '1062' in error_msg and 'Duplicate entry' in error_msg:
                print(f"\n❌ 插入数据失败: 主键冲突")
                print(f"   💡 提示: 请使用 --clear 参数清空现有数据")
                print(f"   命令: python get_data_to_mysql.py --format db --clear")
            else:
                print(f"\n❌ 插入数据失败: {e}")
            return 0


class DataExporter:
    """数据导出工具"""

    @staticmethod
    def to_sql(data: List[Any], table_name: str) -> str:
        """生成SQL插入语句"""
        if not data:
            return ""

        fields = [f.name for f in data[0].__dataclass_fields__.values()]
        sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES\n"

        values = []
        for item in data:
            row = []
            for field in fields:
                val = getattr(item, field)
                if isinstance(val, str):
                    # 处理WKT格式和字符串
                    if val.startswith('POINT') or val.startswith('POLYGON'):
                        # WKT格式使用ST_GeomFromText
                        row.append(f"ST_GeomFromText('{val}', 4326)")
                    elif val == '':
                        row.append("NULL")
                    else:
                        row.append(f"'{val}'")
                elif val is None:
                    row.append("NULL")
                elif isinstance(val, bool):
                    row.append('1' if val else '0')
                else:
                    row.append(str(val))
            values.append(f"({', '.join(row)})")

        return sql + ",\n".join(values) + ";"

    @staticmethod
    def to_csv(data: List[Any], filepath: str):
        """导出CSV文件"""
        if not data:
            return

        fields = [f.name for f in data[0].__dataclass_fields__.values()]

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            for item in data:
                row = []
                for field in fields:
                    val = getattr(item, field)
                    if val is None:
                        row.append('')
                    else:
                        row.append(str(val))
                writer.writerow(row)
        print(f"CSV已保存至: {filepath}")


def main():
    """数据生成主入口"""
    parser = argparse.ArgumentParser(description='生成重庆市井烟火数据')
    parser.add_argument('--hotpot', type=int, default=5000, help='火锅门店数量（默认5000）')
    parser.add_argument('--teahouse', type=int, default=300, help='茶馆数量（默认300）')
    parser.add_argument('--days', type=int, default=7, help='夜间经济数据天数（默认7天）')
    parser.add_argument('--alerts', type=int, default=30, help='预警事件数量（默认30）')
    parser.add_argument('--format', choices=['sql', 'csv', 'both', 'db'], default='db', help='导出格式（db=直接入库）')
    parser.add_argument('--output-dir', default='./output', help='输出目录')
    
    # 数据库连接参数
    parser.add_argument('--db-host', default='172.31.142.67', help='数据库主机（默认localhost）')
    parser.add_argument('--db-port', type=int, default=3306, help='数据库端口（默认3306）')
    parser.add_argument('--db-user', default='root', help='数据库用户名（默认root）')
    parser.add_argument('--db-password', default='qwer4321', help='数据库密码（默认为空）')
    parser.add_argument('--db-name', default='city_fireworks', help='数据库名（默认city_fireworks）')
    parser.add_argument('--clear', action='store_true', help='清空现有数据后再插入')

    args = parser.parse_args()

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    # 初始化生成器
    generator = TableGenerator()
    exporter = DataExporter()

    print("=" * 50)
    print("开始生成《市井烟火》重庆数据...")
    print("=" * 50)

    # 1. 生成区县数据（必须最先）
    print("📍 生成区县基础数据...")
    districts = generator.generate_districts()
    print(f"✅ 已生成 {len(districts)} 条区县数据\n")

    # 2. 生成品牌数据（必须第二）
    print("🏪 生成火锅品牌数据...")
    brands = generator.generate_brands()
    print(f"✅ 已生成 {len(brands)} 条品牌数据\n")

    # 3. 生成其他数据
    print("🍲 生成火锅门店数据...")
    hotpots = generator.generate_hotpot_restaurants(args.hotpot)
    print(f"✅ 已生成 {len(hotpots)} 条火锅门店数据\n")

    print("🍵 生成茶馆数据...")
    teahouses = generator.generate_teahouses(args.teahouse)
    print(f"✅ 已生成 {len(teahouses)} 条茶馆数据\n")

    print("🌃 生成夜间经济数据...")
    night_data = generator.generate_night_economy(args.days)
    print(f"✅ 已生成 {len(night_data)} 条夜间经济数据\n")

    print("⚠️  生成预警数据...")
    alerts = generator.generate_alerts(args.alerts)
    print(f"✅ 已生成 {len(alerts)} 条预警数据\n")

    # 5. 导出/导入数据
    if args.format == 'db':
        print("=" * 50)
        print("💾 开始导入数据到MySQL数据库...")
        print("=" * 50)
        
        # 初始化数据库管理器
        db = DatabaseManager(
            host=args.db_host,
            port=args.db_port,
            user=args.db_user,
            password=args.db_password,
            database=args.db_name
        )
        
        if not db.connect():
            print("❌ 无法连接数据库，退出程序")
            return
        
        try:
            # 检查表中是否有数据
            if not args.clear:
                has_data = db.check_tables_have_data(['districts', 'brands', 'alerts'])
                if has_data:
                    print("\n⚠️  警告: 数据库表中已有数据！")
                    print("   建议使用 --clear 参数清空现有数据")
                    print("   命令: python get_data_to_mysql.py --format db --clear")
                    print("\n是否继续？可能会导致主键冲突...")
                    response = input("输入 'yes' 继续，或按 Enter 退出: ")
                    if response.lower() != 'yes':
                        print("已取消操作")
                        return
            
            # 如果指定清空，先清空所有表
            if args.clear:
                print("\n🗑️  清空现有数据...")
                db.clear_table('alerts')
                db.clear_table('night_economy')
                db.clear_table('teahouses')
                db.clear_table('hotpot_restaurants')
                db.clear_table('brands')
                db.clear_table('districts')
                print()
            
            # 按顺序插入数据（注意外键依赖）
            print("1️⃣  插入区县数据...")
            db.insert_batch(districts, 'districts')
            
            print("\n2️⃣  插入品牌数据...")
            db.insert_batch(brands, 'brands')
            
            print("\n3️⃣  插入火锅门店数据...")
            db.insert_batch(hotpots, 'hotpot_restaurants')
            
            print("\n4️⃣  插入茶馆数据...")
            db.insert_batch(teahouses, 'teahouses')
            
            print("\n5️⃣  插入夜间经济数据...")
            db.insert_batch(night_data, 'night_economy')
            
            print("\n6️⃣  插入预警数据...")
            db.insert_batch(alerts, 'alerts')
            
            print("\n" + "=" * 50)
            print("🎉 所有数据已成功导入数据库！")
            print("=" * 50)
            
        finally:
            db.close()
    
    elif args.format in ['sql', 'both']:
        print("💾 导出SQL文件...")
        sql_file = os.path.join(args.output_dir, 'chongqing_data.sql')
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("-- 《市井烟火》重庆城市人文数据\n")
            f.write("-- 生成时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
            f.write("-- 数据量: {}条火锅, {}条茶馆, {}条夜间经济, {}条预警\n\n".format(
                len(hotpots), len(teahouses), len(night_data), len(alerts)
            ))

            f.write("-- 1. 区县数据\n")
            f.write(exporter.to_sql(districts, 'districts') + "\n\n")

            f.write("-- 2. 品牌数据\n")
            f.write(exporter.to_sql(brands, 'brands') + "\n\n")

            f.write("-- 3. 火锅门店数据\n")
            f.write(exporter.to_sql(hotpots, 'hotpot_restaurants') + "\n\n")

            f.write("-- 4. 茶馆数据\n")
            f.write(exporter.to_sql(teahouses, 'teahouses') + "\n\n")

            f.write("-- 5. 夜间经济数据\n")
            f.write(exporter.to_sql(night_data, 'night_economy_realtime') + "\n\n")

            f.write("-- 6. 预警数据\n")
            f.write(exporter.to_sql(alerts, 'alerts') + "\n")

        print(f"✅ SQL文件已生成: {sql_file}\n")

    if args.format in ['csv', 'both']:
        print("📊 导出CSV文件...")
        csv_dir = args.output_dir
        exporter.to_csv(districts, os.path.join(csv_dir, 'districts.csv'))
        exporter.to_csv(brands, os.path.join(csv_dir, 'brands.csv'))
        exporter.to_csv(hotpots, os.path.join(csv_dir, 'hotpot_restaurants.csv'))
        exporter.to_csv(teahouses, os.path.join(csv_dir, 'teahouses.csv'))
        exporter.to_csv(night_data, os.path.join(csv_dir, 'night_economy_realtime.csv'))
        exporter.to_csv(alerts, os.path.join(csv_dir, 'alerts.csv'))
        print(f"✅ CSV文件已生成在: {csv_dir}/\n")

    if args.format != 'db':
        print("=" * 50)
        print("🎉 数据生成完成！")
        print("=" * 50)
        print("\n📌 使用说明：")
        print("1. SQL文件包含完整INSERT语句，可直接导入MySQL")
        print("2. 地理字段使用ST_GeomFromText()函数，确保MySQL支持GIS")
        print("3. 如需调整数据量，使用参数：--hotpot 10000 --teahouse 500")
        print("4. 数据已按真实重庆地理分布生成，主城九区密度更高")
    
    print("\n📌 直接导入数据库示例：")
    print("python get_data_to_mysql.py --format db --db-password your_password")
    print("python get_data_to_mysql.py --format db --db-password your_password --clear  # 清空后导入")
    print("python get_data_to_mysql.py --format db --hotpot 10000 --teahouse 500  # 自定义数据量")


if __name__ == '__main__':
    main()