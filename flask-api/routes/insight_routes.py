"""
数据洞察API路由
"""

from flask_restx import Resource, Namespace
from services.data_service import DataService

api = Namespace('insight', description='数据洞察API')

data_service = DataService()


@api.route('/city-temperature')
class CityTemperature(Resource):
    @api.doc('get_city_temperature_index')
    def get(self):
        """获取城市温度指数"""
        return data_service.get_city_temperature_index()


@api.route('/district-vitality')
class DistrictVitality(Resource):
    @api.doc('get_district_vitality_ranking')
    def get(self):
        """获取区县活力排名"""
        return data_service.get_district_vitality_ranking()


@api.route('/alerts')
class Alerts(Resource):
    @api.doc('get_active_alerts')
    def get(self):
        """获取活跃预警信息"""
        return data_service.get_active_alerts()


@api.route('/temperature-detail')
class TemperatureDetail(Resource):
    @api.doc('get_temperature_detail')
    def get(self):
        """获取温度指数详情"""
        return data_service.get_temperature_detail()


@api.route('/ranking-detail')
class RankingDetail(Resource):
    @api.doc('get_ranking_detail')
    def get(self):
        """获取排名详情"""
        return data_service.get_ranking_detail()


def register_insight_routes(main_api):
    """注册数据洞察路由"""
    main_api.add_namespace(api, path='/insight')
