"""
数据服务层
"""

from models import db, District, HotpotRestaurant, Brand, Teahouse, NightEconomy, Alert
from typing import List, Dict, Any
from sqlalchemy import func, desc
import json


class DataService:
    """数据服务类"""

    def __init__(self):
        pass

    # ==================== 地图相关服务 ====================

    def get_districts(self) -> List[Dict[str, Any]]:
        """获取所有区县数据"""
        districts = District.query.all()
        return [d.to_dict() for d in districts]

    def get_district_detail(self, district_id: int) -> Dict[str, Any]:
        """获取区县详情"""
        district = District.query.get(district_id)
        if not district:
            return {}

        data = district.to_dict()
        # 添加关联数据
        data['hotpot_count'] = HotpotRestaurant.query.filter_by(district_id=district_id).count()
        data['teahouse_count'] = Teahouse.query.filter_by(district_id=district_id).count()
        return data

    def get_hotpot_points(self) -> List[Dict[str, Any]]:
        """获取火锅店点位数据"""
        # 使用 joinedload 预加载关联数据，避免 N+1 查询
        from sqlalchemy.orm import joinedload
        restaurants = HotpotRestaurant.query\
            .options(joinedload(HotpotRestaurant.brand))\
            .options(joinedload(HotpotRestaurant.district))\
            .filter_by(status=1)\
            .all()
        return [r.to_dict() for r in restaurants]

    def get_teahouse_points(self) -> List[Dict[str, Any]]:
        """获取茶馆点位数据"""
        # 使用 joinedload 预加载关联数据
        from sqlalchemy.orm import joinedload
        teahouses = Teahouse.query\
            .options(joinedload(Teahouse.district))\
            .all()
        return [t.to_dict() for t in teahouses]

    # ==================== 火锅江湖服务 ====================

    def get_density_matrix(self) -> List[Dict[str, Any]]:
        """获取火锅店密度矩阵"""
        districts = self.get_districts()
        restaurants = HotpotRestaurant.query.all()

        result = []
        for district in districts:
            count = len([r for r in restaurants if r.district_id == district['id']])
            result.append({
                'district': district['name'],
                'density': district['hotpot_density'],
                'count': count
            })

        return result

    def get_brand_distribution(self) -> List[Dict[str, Any]]:
        """获取品牌分布数据"""
        brands = Brand.query.all()
        return [b.to_dict() for b in brands]

    def get_price_distribution(self) -> List[Dict[str, Any]]:
        """获取价格分布数据"""
        restaurants = HotpotRestaurant.query.filter(
            HotpotRestaurant.price_avg.isnot(None)
        ).all()

        # 按价格区间分组
        price_ranges = {
            '50以下': {'min': 0, 'max': 50, 'count': 0},
            '50-80': {'min': 50, 'max': 80, 'count': 0},
            '80-100': {'min': 80, 'max': 100, 'count': 0},
            '100-150': {'min': 100, 'max': 150, 'count': 0},
            '150以上': {'min': 150, 'max': 9999, 'count': 0}
        }

        for r in restaurants:
            price = r.price_avg
            for range_name, range_data in price_ranges.items():
                if range_data['min'] <= price < range_data['max']:
                    range_data['count'] += 1
                    break

        return [{'range': k, 'count': v['count']} for k, v in price_ranges.items()]

    def get_shop_type_distribution(self) -> List[Dict[str, Any]]:
        """获取店铺类型分布"""
        restaurants = HotpotRestaurant.query.filter(
            HotpotRestaurant.shop_type.isnot(None)
        ).all()

        type_count = {}
        for r in restaurants:
            if r.shop_type:
                type_count[r.shop_type] = type_count.get(r.shop_type, 0) + 1

        return [{'type': k, 'count': v} for k, v in type_count.items()]

    def get_hotpot_ranking(self) -> List[Dict[str, Any]]:
        """获取火锅店排名"""
        districts = self.get_districts()
        restaurants = HotpotRestaurant.query.all()

        # 按区县统计火锅店数量
        district_stats = {}
        for district in districts:
            district_stats[district['id']] = {
                'name': district['name'],
                'count': 0
            }

        for r in restaurants:
            if r.district_id in district_stats:
                district_stats[r.district_id]['count'] += 1

        # 排序并返回
        result = list(district_stats.values())
        result.sort(key=lambda x: x['count'], reverse=True)

        # 添加排名
        for i, item in enumerate(result, 1):
            item['rank'] = i

        return result

    # ==================== 夜间经济服务 ====================

    def get_24hour_trend(self) -> List[Dict[str, Any]]:
        """获取24小时趋势数据"""
        # 按小时聚合数据
        hourly_data = db.session.query(
            NightEconomy.hour,
            func.avg(NightEconomy.population_index).label('avg_population'),
            func.avg(NightEconomy.consumption_heat).label('avg_consumption')
        ).group_by(NightEconomy.hour).all()

        result = []
        for item in hourly_data:
            result.append({
                'hour': item.hour,
                'population': round(item.avg_population or 0),
                'consumption': round(item.avg_consumption or 0)
            })

        return sorted(result, key=lambda x: x['hour'])

    def get_district_comparison(self) -> List[Dict[str, Any]]:
        """获取区县对比数据"""
        districts = self.get_districts()
        return districts

    def get_metro_passengers(self, hour: int) -> List[Dict[str, Any]]:
        """获取指定小时的地铁客流数据"""
        data = NightEconomy.query.filter_by(hour=hour).all()
        return [d.to_dict() for d in data]

    def get_city_operation(self) -> Dict[str, Any]:
        """获取城市运行数据"""
        return {
            'total_districts': District.query.count(),
            'total_hotpots': HotpotRestaurant.query.filter_by(status=1).count(),
            'total_teahouses': Teahouse.query.count(),
            'timestamp': db.session.query(func.max(NightEconomy.timestamp)).scalar()
        }

    # ==================== 茶馆岁月服务 ====================

    def get_teahouse_time_series(self) -> List[Dict[str, Any]]:
        """获取茶馆时间序列数据"""
        teahouses = Teahouse.query.filter(
            Teahouse.founding_year.isnot(None)
        ).all()

        # 按年代分组
        decades = {}
        for t in teahouses:
            decade = (t.founding_year // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1

        result = [{'decade': k, 'count': v} for k, v in sorted(decades.items())]
        return result

    def get_teahouse_district_distribution(self) -> List[Dict[str, Any]]:
        """获取茶馆区域分布"""
        teahouses = Teahouse.query.all()
        districts = {d.id: d.name for d in District.query.all()}

        dist_count = {}
        for t in teahouses:
            district_name = districts.get(t.district_id, '未知')
            dist_count[district_name] = dist_count.get(district_name, 0) + 1

        return [{'district': k, 'count': v} for k, v in sorted(dist_count.items(), key=lambda x: x[1], reverse=True)]

    def get_teahouse_cultural_tags(self) -> List[Dict[str, Any]]:
        """获取文化标签"""
        teahouses = Teahouse.query.all()
        tag_count = {}

        for t in teahouses:
            if t.cultural_tags:
                try:
                    tags = json.loads(t.cultural_tags)
                    for tag in tags:
                        tag_count[tag] = tag_count.get(tag, 0) + 1
                except:
                    pass

        return [{'tag': k, 'count': v} for k, v in sorted(tag_count.items(), key=lambda x: x[1], reverse=True)]

    def get_teahouse_timeline(self) -> List[Dict[str, Any]]:
        """获取茶馆时间线数据"""
        teahouses = Teahouse.query.filter(
            Teahouse.founding_year.isnot(None)
        ).order_by(Teahouse.founding_year).all()

        return [t.to_dict() for t in teahouses]

    def get_teahouse_wordcloud(self) -> List[Dict[str, Any]]:
        """获取茶馆词云数据"""
        return self.get_teahouse_cultural_tags()

    # ==================== 数据洞察服务 ====================

    def get_city_temperature_index(self) -> Dict[str, Any]:
        """计算城市温度指数"""
        districts = District.query.all()
        restaurants = HotpotRestaurant.query.filter_by(status=1).all()
        teahouses = Teahouse.query.all()
        night_economy = NightEconomy.query.all()

        # 计算各维度得分
        if districts:
            hotpot_score = sum(d.hotpot_density or 0 for d in districts) / len(districts)
            vitality_score = sum(d.vitality_score or 0 for d in districts) / len(districts)
        else:
            hotpot_score = 0
            vitality_score = 0

        teahouse_score = min(len(teahouses) * 0.1, 30)

        if night_economy:
            night_score = sum(n.population_index or 0 for n in night_economy) / len(night_economy) / 1000
        else:
            night_score = 0

        # 归一化到0-100
        normalize = lambda x, max_val: max(0, min(100, (x / max_val) * 100)) if x > 0 else 0

        score = round(
            normalize(hotpot_score, 20) * 0.3 +
            normalize(night_score, 10) * 0.3 +
            normalize(teahouse_score, 30) * 0.2 +
            normalize(vitality_score, 100) * 0.2
        )

        return {
            'score': score,
            'date': db.session.query(func.current_date()).scalar().isoformat(),
            'factors': {
                'hotpot_density': round(normalize(hotpot_score, 20)),
                'night_economy': round(normalize(night_score, 10)),
                'teahouse_culture': round(normalize(teahouse_score, 30)),
                'vitality': round(normalize(vitality_score, 100))
            }
        }

    def get_district_vitality_ranking(self) -> List[Dict[str, Any]]:
        """获取区县活力排名"""
        districts = District.query.order_by(desc(District.vitality_score)).all()
        return [d.to_dict() for d in districts]

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """获取活跃预警"""
        alerts = Alert.query.filter_by(status=1).order_by(desc(Alert.alert_time)).all()
        return [a.to_dict() for a in alerts]

    def get_temperature_detail(self) -> Dict[str, Any]:
        """获取温度指数详情"""
        return self.get_city_temperature_index()

    def get_ranking_detail(self) -> List[Dict[str, Any]]:
        """获取排名详情"""
        return self.get_district_vitality_ranking()
