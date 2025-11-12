"""
地图相关API路由
"""

from flask_restx import Resource, Namespace
from models import District, HotpotRestaurant, Teahouse
from services.data_service import DataService

api = Namespace('map', description='地图相关API')

data_service = DataService()


@api.route('/districts')
class Districts(Resource):
    @api.doc('get_districts')
    def get(self):
        """获取所有区县数据"""
        return data_service.get_districts()


@api.route('/hotpot-points')
class HotpotPoints(Resource):
    @api.doc('get_hotpot_points')
    def get(self):
        """获取火锅店点位数据"""
        return data_service.get_hotpot_points()


@api.route('/teahouse-points')
class TeahousePoints(Resource):
    @api.doc('get_teahouse_points')
    def get(self):
        """获取茶馆点位数据"""
        return data_service.get_teahouse_points()


@api.route('/district/<int:district_id>')
class DistrictDetail(Resource):
    @api.doc('get_district_detail')
    def get(self, district_id):
        """获取指定区县详细信息"""
        return data_service.get_district_detail(district_id)


def register_map_routes(main_api):
    """注册地图路由"""
    main_api.add_namespace(api, path='/map')
