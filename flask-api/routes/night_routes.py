"""
夜间经济API路由
"""

from flask_restx import Resource, Namespace
from services.data_service import DataService

api = Namespace('night', description='夜间经济API')

data_service = DataService()


@api.route('/24hour-trend')
class Hour24Trend(Resource):
    @api.doc('get_24hour_trend')
    def get(self):
        """获取24小时趋势数据"""
        return data_service.get_24hour_trend()


@api.route('/district-comparison')
class DistrictComparison(Resource):
    @api.doc('get_district_comparison')
    def get(self):
        """获取区县对比数据"""
        return data_service.get_district_comparison()


@api.route('/metro-passengers/<int:hour>')
class MetroPassengers(Resource):
    @api.doc('get_metro_passengers')
    def get(self, hour):
        """获取指定小时的地铁客流数据"""
        return data_service.get_metro_passengers(hour)


@api.route('/city-operation')
class CityOperation(Resource):
    @api.doc('get_city_operation')
    def get(self):
        """获取城市运行数据"""
        return data_service.get_city_operation()


def register_night_routes(main_api):
    """注册夜间经济路由"""
    main_api.add_namespace(api, path='/night')
