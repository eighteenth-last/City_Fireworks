"""
数据库工具函数
"""

from models import db, District, Brand, HotpotRestaurant, Teahouse, NightEconomy, Alert
import json
import os
from typing import List


def init_db():
    """初始化数据库，创建所有表"""
    db.create_all()
    print("✅ 数据库表创建完成")


def load_json_data(json_file: str):
    """从JSON文件加载数据"""
    if not os.path.exists(json_file):
        print(f"⚠️  数据文件不存在: {json_file}")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def import_districts():
    """导入区县数据"""
    data = load_json_data('../public/data/districts.json')
    if not data:
        return

    for item in data:
        district = District(
            id=item['id'],
            name=item['name'],
            area_km2=item.get('area_km2'),
            hotpot_density=item.get('hotpot_density'),
            population=item.get('population'),
            vitality_score=item.get('vitality_score')
        )
        db.session.add(district)

    db.session.commit()
    print(f"✅ 导入区县数据: {len(data)} 条")


def import_brands():
    """导入品牌数据"""
    data = load_json_data('../public/data/brands.json')
    if not data:
        return

    for item in data:
        brand = Brand(
            id=item['id'],
            name=item['name'],
            market_share=item.get('market_share'),
            avg_wait_time=item.get('avg_wait_time'),
            store_count=item.get('store_count'),
            price_position=item.get('price_position', '中端'),
            update_date=item.get('update_date')
        )
        db.session.add(brand)

    db.session.commit()
    print(f"✅ 导入品牌数据: {len(data)} 条")


def import_hotpot_restaurants():
    """导入火锅店数据"""
    data = load_json_data('../public/data/hotpot_restaurants.json')
    if not data:
        return

    for item in data:
        restaurant = HotpotRestaurant(
            id=item['id'],
            name=item['name'],
            brand_id=item.get('brand_id'),
            address=item.get('address'),
            district_id=item['district_id'],
            price_min=item.get('price_min'),
            price_max=item.get('price_max'),
            price_avg=item.get('price_avg'),
            rating=item.get('rating'),
            review_count=item.get('review_count'),
            shop_type=item.get('shop_type'),
            business_hours=item.get('business_hours'),
            is_24h=item.get('is_24h', False),
            open_date=item.get('open_date'),
            status=item.get('status', 1)
        )
        db.session.add(restaurant)

    db.session.commit()
    print(f"✅ 导入火锅店数据: {len(data)} 条")


def import_teahouses():
    """导入茶馆数据"""
    data = load_json_data('../public/data/teahouses.json')
    if not data:
        return

    for item in data:
        teahouse = Teahouse(
            id=item['id'],
            name=item['name'],
            address=item.get('address'),
            district_id=item['district_id'],
            founding_year=item.get('founding_year'),
            tea_type=item.get('tea_type'),
            avg_price=item.get('avg_price'),
            popularity=item.get('popularity'),
            is_historic=item.get('is_historic', False),
            community_type=item.get('community_type'),
            cultural_tags=json.dumps(item.get('cultural_tags', [])),
            coordinates_lng=item.get('coordinates', {}).get('lng'),
            coordinates_lat=item.get('coordinates', {}).get('lat'),
            update_time=item.get('update_time')
        )
        db.session.add(teahouse)

    db.session.commit()
    print(f"✅ 导入茶馆数据: {len(data)} 条")


def import_night_economy():
    """导入夜间经济数据"""
    data = load_json_data('../public/data/night_economy_realtime.json')
    if not data:
        return

    for item in data:
        night_economy = NightEconomy(
            id=item['id'],
            timestamp=item.get('timestamp'),
            hour=item['hour'],
            district_id=item['district_id'],
            population_index=item.get('population_index'),
            consumption_heat=item.get('consumption_heat'),
            metro_passengers=item.get('metro_passengers'),
            active_businesses=item.get('active_businesses'),
            weather=item.get('weather'),
            special_event=item.get('special_event'),
            date=item.get('date'),
            time=item.get('time')
        )
        db.session.add(night_economy)

    db.session.commit()
    print(f"✅ 导入夜间经济数据: {len(data)} 条")


def import_alerts():
    """导入预警数据"""
    data = load_json_data('../public/data/alerts.json')
    if not data:
        return

    for item in data:
        alert = Alert(
            id=item['id'],
            alert_time=item.get('alert_time'),
            alert_type=item['alert_type'],
            content=item.get('content'),
            impact_value=item.get('impact_value'),
            status=item.get('status', 1)
        )
        db.session.add(alert)

    db.session.commit()
    print(f"✅ 导入预警数据: {len(data)} 条")


def import_all_data():
    """导入所有数据"""
    print("🚀 开始导入数据...")
    import_districts()
    import_brands()
    import_hotpot_restaurants()
    import_teahouses()
    import_night_economy()
    import_alerts()
    print("🎉 所有数据导入完成！")


if __name__ == '__main__':
    from app import app
    with app.app_context():
        init_db()
        import_all_data()
