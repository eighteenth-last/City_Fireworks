#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV转JSON工具
将output文件夹中的CSV文件转换为JSON格式，供前端使用
"""

import csv
import json
import os
from typing import List, Dict, Any

def parse_wkt_point(wkt: str) -> Dict[str, float]:
    """
    解析POINT WKT格式为坐标对象
    例：POINT(106.551 29.563) -> {lng: 106.551, lat: 29.563}
    """
    if not wkt or not wkt.startswith('POINT'):
        return {}
    # 提取括号内的坐标
    coords = wkt.replace('POINT(', '').replace(')', '').strip()
    parts = coords.split()
    if len(parts) >= 2:
        return {
            'lng': float(parts[0]),
            'lat': float(parts[1])
        }
    return {}

def parse_wkt_polygon(wkt: str) -> List[List[float]]:
    """
    解析POLYGON WKT格式为坐标数组
    例：POLYGON((106.4 29.4 106.7 29.4 ...)) -> [[lng, lat], [lng, lat], ...]
    """
    if not wkt or not wkt.startswith('POLYGON'):
        return []
    # 提取括号内的坐标
    coords_str = wkt.replace('POLYGON((', '').replace('))', '').strip()
    coords = []
    for pair in coords_str.split():
        if ' ' in pair:
            parts = pair.split(' ')
            if len(parts) >= 2:
                coords.append([float(parts[0]), float(parts[1])])
    return coords

def csv_to_json(csv_file: str, json_file: str, transform_func=None) -> List[Dict[str, Any]]:
    """
    将CSV文件转换为JSON文件
    """
    data = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换数据类型
            for key, value in row.items():
                # 处理空字符串
                if value == '':
                    row[key] = None
                # 尝试转换为数字（排除日期格式）
                elif isinstance(value, str):
                    # 日期格式检查
                    if '-' in value and len(value) > 4:
                        # 可能是日期，保留字符串
                        pass
                    # 纯数字检查
                    elif value.replace('.', '').replace('-', '').isdigit():
                        if '.' in value:
                            row[key] = float(value)
                        else:
                            row[key] = int(value)
                    # 尝试转换为布尔值
                    elif value in ['True', 'False']:
                        row[key] = value == 'True'

            # 如果有转换函数，应用转换
            if transform_func:
                row = transform_func(row)

            data.append(row)

    # 写入JSON文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"OK {csv_file} -> {json_file} ({len(data)} records)")
    return data

def transform_district(row: Dict[str, Any]) -> Dict[str, Any]:
    """转换区县数据"""
    # 解析中心点坐标
    if row.get('center'):
        row['center_coords'] = parse_wkt_point(row['center'])
        del row['center']
    # 解析边界多边形
    if row.get('boundary'):
        row['boundary_coords'] = parse_wkt_polygon(row['boundary'])
        del row['boundary']
    return row

def transform_hotpot(row: Dict[str, Any]) -> Dict[str, Any]:
    """转换火锅店数据"""
    # 解析坐标
    if row.get('location'):
        row['coordinates'] = parse_wkt_point(row['location'])
        del row['location']
    return row

def transform_teahouse(row: Dict[str, Any]) -> Dict[str, Any]:
    """转换茶馆数据"""
    # 解析坐标
    if row.get('location'):
        row['coordinates'] = parse_wkt_point(row['location'])
        del row['location']
    # 解析文化标签JSON
    if row.get('cultural_tags'):
        try:
            row['cultural_tags'] = json.loads(row['cultural_tags'])
        except:
            row['cultural_tags'] = []
    return row

def transform_night_economy(row: Dict[str, Any]) -> Dict[str, Any]:
    """转换夜间经济数据"""
    # 转换时间戳
    if row.get('timestamp'):
        dt = row['timestamp']
        row['date'] = dt.split(' ')[0]
        row['time'] = dt.split(' ')[1]
    return row

def main():
    """主函数"""
    print("=" * 60)
    print("CSV转JSON数据处理工具")
    print("=" * 60)
    print()

    # 输入输出目录
    csv_dir = './output'
    json_dir = './city-fireworks/public/data'

    # 确保输出目录存在
    os.makedirs(json_dir, exist_ok=True)

    # 转换配置
    conversions = [
        {
            'csv': 'districts.csv',
            'json': 'districts.json',
            'transform': transform_district
        },
        {
            'csv': 'brands.csv',
            'json': 'brands.json',
            'transform': None
        },
        {
            'csv': 'hotpot_restaurants.csv',
            'json': 'hotpot_restaurants.json',
            'transform': transform_hotpot
        },
        {
            'csv': 'teahouses.csv',
            'json': 'teahouses.json',
            'transform': transform_teahouse
        },
        {
            'csv': 'night_economy_realtime.csv',
            'json': 'night_economy_realtime.json',
            'transform': transform_night_economy
        },
        {
            'csv': 'alerts.csv',
            'json': 'alerts.json',
            'transform': None
        }
    ]

    total_records = 0

    for config in conversions:
        csv_file = os.path.join(csv_dir, config['csv'])
        json_file = os.path.join(json_dir, config['json'])

        if not os.path.exists(csv_file):
            print(f"WARNING: File not found: {csv_file}")
            continue

        print(f"Converting {config['csv']}...")

        if config['transform']:
            data = csv_to_json(csv_file, json_file, config['transform'])
        else:
            data = csv_to_json(csv_file, json_file)

        total_records += len(data)
        print()

    print("=" * 60)
    print(f"Conversion complete! Processed {len(conversions)} files, {total_records} records")
    print("=" * 60)
    print()
    print("JSON files location:")
    print(f"   {json_dir}/")
    print()
    print("File list:")
    for config in conversions:
        json_file = os.path.join(json_dir, config['json'])
        if os.path.exists(json_file):
            size = os.path.getsize(json_file) / 1024  # KB
            print(f"   - {config['json']} ({size:.1f} KB)")
    print()
    print("Data is ready for frontend use!")

if __name__ == '__main__':
    main()
