-- 重庆城市人文市井烟火大屏 - 数据库初始化脚本
-- 创建数据库
CREATE DATABASE IF NOT EXISTS city_fireworks
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE city_fireworks;

-- 1️⃣ 区县表（必须先创建）
DROP TABLE IF EXISTS districts;
CREATE TABLE districts (
    id INT PRIMARY KEY COMMENT '区县ID',
    name VARCHAR(100) NOT NULL COMMENT '区县名称',
    area_km2 DECIMAL(10,2) COMMENT '面积（平方公里）',
    hotpot_density DECIMAL(10,2) COMMENT '火锅店密度',
    population INT COMMENT '人口数量',
    vitality_score DECIMAL(5,2) COMMENT '活力指数',
    center POINT COMMENT '中心点坐标',
    boundary MULTIPOLYGON COMMENT '边界多边形',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    SPATIAL INDEX idx_center (center),
    SPATIAL INDEX idx_boundary (boundary),
    INDEX idx_name (name),
    INDEX idx_vitality_score (vitality_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='区县表';

-- 2️⃣ 品牌表
DROP TABLE IF EXISTS brands;
CREATE TABLE brands (
    id INT PRIMARY KEY COMMENT '品牌ID',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '品牌名称',
    market_share DECIMAL(5,2) COMMENT '市场份额',
    avg_wait_time INT COMMENT '平均等待时间（分钟）',
    store_count INT COMMENT '门店数量',
    price_position ENUM('大众', '中端', '高端', '奢华') COMMENT '价位定位',
    update_date DATE COMMENT '更新日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_market_share (market_share)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='火锅品牌表';

-- 3️⃣ 火锅门店表
DROP TABLE IF EXISTS hotpot_restaurants;
CREATE TABLE hotpot_restaurants (
    id INT PRIMARY KEY COMMENT '店铺ID',
    name VARCHAR(200) NOT NULL COMMENT '店铺名称',
    brand_id INT COMMENT '品牌ID',
    address VARCHAR(500) COMMENT '地址',
    district_id INT NOT NULL COMMENT '区县ID',
    price_min INT COMMENT '最低价',
    price_max INT COMMENT '最高价',
    price_avg INT COMMENT '平均价',
    rating DECIMAL(3,1) COMMENT '评分',
    review_count INT COMMENT '评价数',
    shop_type VARCHAR(50) COMMENT '店铺类型',
    business_hours VARCHAR(100) COMMENT '营业时间',
    is_24h BOOLEAN DEFAULT FALSE COMMENT '是否24小时营业',
    open_date DATE COMMENT '开业日期',
    status TINYINT DEFAULT 1 COMMENT '营业状态：1-营业，0-停业',
    location POINT COMMENT '坐标',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL,
    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE CASCADE,
    SPATIAL INDEX idx_location (location),
    INDEX idx_district (district_id),
    INDEX idx_brand (brand_id),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='火锅店表';

-- 4️⃣ 茶馆表
DROP TABLE IF EXISTS teahouses;
CREATE TABLE teahouses (
    id INT PRIMARY KEY COMMENT '茶馆ID',
    name VARCHAR(200) NOT NULL COMMENT '茶馆名称',
    address VARCHAR(500) COMMENT '地址',
    district_id INT NOT NULL COMMENT '区县ID',
    founding_year INT COMMENT '创立年份',
    tea_type VARCHAR(200) COMMENT '茶馆类型（逗号分隔）',
    avg_price DECIMAL(8,2) COMMENT '平均价格',
    popularity INT COMMENT '受欢迎程度',
    is_historic BOOLEAN DEFAULT FALSE COMMENT '是否历史悠久',
    community_type VARCHAR(50) COMMENT '社区类型',
    cultural_tags JSON COMMENT '文化标签（JSON格式）',
    coordinates_lng DECIMAL(10,7) COMMENT '经度',
    coordinates_lat DECIMAL(10,7) COMMENT '纬度',
    location POINT COMMENT '坐标',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE CASCADE,
    SPATIAL INDEX idx_location (location),
    INDEX idx_district (district_id),
    INDEX idx_founding_year (founding_year),
    INDEX idx_popularity (popularity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='茶馆表';

-- 5️⃣ 夜间经济数据表
DROP TABLE IF EXISTS night_economy;
CREATE TABLE night_economy (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '数据ID',
    timestamp DATETIME NOT NULL COMMENT '时间戳',
    hour TINYINT NOT NULL COMMENT '小时',
    district_id INT NOT NULL COMMENT '区县ID',
    population_index INT COMMENT '人口指数',
    consumption_heat DECIMAL(10,2) COMMENT '消费热度',
    metro_passengers INT COMMENT '地铁乘客数',
    active_businesses INT COMMENT '活跃商家数',
    weather VARCHAR(50) COMMENT '天气',
    special_event VARCHAR(200) COMMENT '特殊事件',
    date DATE NOT NULL COMMENT '日期',
    time TIME NOT NULL COMMENT '时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE CASCADE,
    INDEX idx_timestamp (timestamp),
    INDEX idx_district_hour (district_id, hour),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='夜间经济数据表';

-- 6️⃣ 预警表
DROP TABLE IF EXISTS alerts;
CREATE TABLE alerts (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '预警ID',
    alert_time DATETIME NOT NULL COMMENT '预警时间',
    alert_type VARCHAR(50) NOT NULL COMMENT '预警类型',
    content TEXT COMMENT '预警内容',
    impact_value VARCHAR(100) COMMENT '影响值',
    status TINYINT DEFAULT 1 COMMENT '状态：1-活跃，0-已处理',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_alert_time (alert_time),
    INDEX idx_alert_type (alert_type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='预警信息表';
