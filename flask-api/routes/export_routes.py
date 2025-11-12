"""
数据导出API路由
"""

from flask import request, send_file, jsonify
from flask_restx import Resource, Namespace
from services.data_service import DataService
from services.export_service import ExportService
import os
import tempfile
from datetime import datetime

api = Namespace('export', description='数据导出API')

data_service = DataService()
export_service = ExportService()


@api.route('/all')
class ExportAll(Resource):
    @api.doc('export_all_data')
    def get(self):
        """导出所有数据为CSV"""
        try:
            file_path = export_service.export_all_data()
            return send_file(
                file_path,
                as_attachment=True,
                download_name=f'city_fireworks_all_{datetime.now().strftime("%Y%m%d")}.csv',
                mimetype='text/csv'
            )
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/table/<table_name>')
class ExportByTable(Resource):
    @api.doc('export_by_table')
    def get(self, table_name):
        """按表导出数据"""
        try:
            file_path = export_service.export_by_table(table_name)
            if not file_path:
                return {'error': 'Invalid table name'}, 400

            return send_file(
                file_path,
                as_attachment=True,
                download_name=f'{table_name}_{datetime.now().strftime("%Y%m%d")}.csv',
                mimetype='text/csv'
            )
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/districts')
class ExportDistricts(Resource):
    @api.doc('export_districts')
    def get(self):
        """导出区县数据"""
        return export_service.export_districts()


@api.route('/hotpots')
class ExportHotpots(Resource):
    @api.doc('export_hotpots')
    def get(self):
        """导出火锅店数据"""
        return export_service.export_hotpots()


@api.route('/teahouses')
class ExportTeahouses(Resource):
    @api.doc('export_teahouses')
    def get(self):
        """导出茶馆数据"""
        return export_service.export_teahouses()


@api.route('/brands')
class ExportBrands(Resource):
    @api.doc('export_brands')
    def get(self):
        """导出品牌数据"""
        return export_service.export_brands()


@api.route('/night-economy')
class ExportNightEconomy(Resource):
    @api.doc('export_night_economy')
    def get(self):
        """导出夜间经济数据"""
        return export_service.export_night_economy()


@api.route('/alerts')
class ExportAlerts(Resource):
    @api.doc('export_alerts')
    def get(self):
        """导出预警数据"""
        return export_service.export_alerts()


def register_export_routes(main_api):
    """注册数据导出路由"""
    main_api.add_namespace(api, path='/export')
