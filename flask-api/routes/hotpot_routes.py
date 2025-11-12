"""
火锅江湖API路由
"""

from flask_restx import Resource, Namespace
from services.data_service import DataService

api = Namespace('hotpot', description='火锅江湖API')

data_service = DataService()


@api.route('/density-matrix')
class DensityMatrix(Resource):
    @api.doc('get_density_matrix')
    def get(self):
        """获取火锅店密度矩阵"""
        return data_service.get_density_matrix()


@api.route('/brand-distribution')
class BrandDistribution(Resource):
    @api.doc('get_brand_distribution')
    def get(self):
        """获取品牌分布数据"""
        return data_service.get_brand_distribution()


@api.route('/price-distribution')
class PriceDistribution(Resource):
    @api.doc('get_price_distribution')
    def get(self):
        """获取价格分布数据"""
        return data_service.get_price_distribution()


@api.route('/shop-type')
class ShopType(Resource):
    @api.doc('get_shop_type_distribution')
    def get(self):
        """获取店铺类型分布"""
        return data_service.get_shop_type_distribution()


@api.route('/ranking')
class HotpotRanking(Resource):
    @api.doc('get_hotpot_ranking')
    def get(self):
        """获取火锅店排名"""
        return data_service.get_hotpot_ranking()


def register_hotpot_routes(main_api):
    """注册火锅江湖路由"""
    main_api.add_namespace(api, path='/hotpot')
