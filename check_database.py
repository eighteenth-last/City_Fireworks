#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库数据
"""

import pymysql
from pymysql.cursors import DictCursor

def check_database():
    """检查数据库中的数据"""
    try:
        connection = pymysql.connect(
            host='172.31.142.67',
            port=3306,
            user='root',
            password='qwer4321',
            database='city_fireworks',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
        print("=" * 50)
        print("数据库数据统计")
        print("=" * 50)
        
        with connection.cursor() as cursor:
            tables = [
                'districts',
                'brands',
                'hotpot_restaurants',
                'teahouses',
                'night_economy',
                'alerts'
            ]
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = cursor.fetchone()
                count = result['count'] if result else 0
                print(f"{table:25} {count:>10} 条")
        
        print("=" * 50)
        
        # 检查火锅店数据样例
        print("\n火锅店数据样例（前5条）：")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, district_id, price_avg, rating, shop_type 
                FROM hotpot_restaurants 
                LIMIT 5
            """)
            results = cursor.fetchall()
            for row in results:
                print(f"  ID: {row['id']}, 名称: {row['name']}, 区县ID: {row['district_id']}, "
                      f"均价: {row['price_avg']}, 评分: {row['rating']}, 类型: {row['shop_type']}")
        
        # 检查茶馆数据样例
        print("\n茶馆数据样例（前5条）：")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, district_id, founding_year, popularity 
                FROM teahouses 
                LIMIT 5
            """)
            results = cursor.fetchall()
            for row in results:
                print(f"  ID: {row['id']}, 名称: {row['name']}, 区县ID: {row['district_id']}, "
                      f"创立年份: {row['founding_year']}, 人气: {row['popularity']}")
        
        connection.close()
        print("\n✅ 数据库检查完成")
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")

if __name__ == '__main__':
    check_database()
