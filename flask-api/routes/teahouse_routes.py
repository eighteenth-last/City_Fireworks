"""
茶馆岁月API路由
"""

from flask_restx import Resource, Namespace
from services.data_service import DataService

api = Namespace('teahouse', description='茶馆岁月API')

data_service = DataService()


@api.route('/time-series')
class TimeSeries(Resource):
    @api.doc('get_time_series_data')
    def get(self):
        """获取茶馆时间序列数据"""
        return data_service.get_teahouse_time_series()


@api.route('/district-distribution')
class DistrictDistribution(Resource):
    @api.doc('get_district_distribution')
    def get(self):
        """获取茶馆区域分布"""
        return data_service.get_teahouse_district_distribution()


@api.route('/cultural-tags')
class CulturalTags(Resource):
    @api.doc('get_cultural_tags')
    def get(self):
        """获取文化标签"""
        return data_service.get_teahouse_cultural_tags()


@api.route('/timeline')
class TeahouseTimeline(Resource):
    @api.doc('get_timeline')
    def get(self):
        """获取茶馆时间线数据"""
        return data_service.get_teahouse_timeline()


@api.route('/wordcloud')
class TeahouseWordCloud(Resource):
    @api.doc('get_wordcloud')
    def get(self):
        """获取茶馆词云数据"""
        return data_service.get_teahouse_wordcloud()


def register_teahouse_routes(main_api):
    """注册茶馆岁月路由"""
    main_api.add_namespace(api, path='/teahouse')
