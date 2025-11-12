# 重庆城市人文市井烟火大屏

> 一个基于 Vue 3 + Vite 开发的重庆城市数据可视化大屏系统，实时展示城市经济活力、商业分布和人文市井数据。

## 📋 项目简介

本项目是一个综合性的城市数据可视化平台，聚焦重庆市的城市活力、商业分布和文化特色，通过多维度的数据展示和分析，为城市管理和商业决策提供数据支持。

## 🎯 核心功能

### 🗺️ 地图展示
- **重庆市区县分布**：展示重庆市各区县的地理位置、面积和人口信息
- **商业点位标注**：火锅店、茶楼等商业设施的精确位置展示
- **热力图分析**：基于火锅店密度的区域商业活力热力图

### 🍲 火锅江湖（左屏）
- **火锅店品牌分布**：展示各品牌市场占有率和门店数量
- **火锅店密度矩阵**：各区县火锅店密度对比
- **价格分布分析**：不同价位火锅店的空间分布
- **店铺类型分析**：老字号、连锁店等类型占比

### 🍵 茶馆岁月（左下）
- **茶馆发展时间线**：展示茶馆的历史发展脉络
- **文化标签云图**：基于川剧、麻将等文化标签的词云展示
- **区域分布分析**：茶馆在各区县的空间分布

### 🌃 24小时城市运行趋势（右上）
- **实时数据监控**：人口指数、消费热度、商圈活跃度
- **地铁客流分析**：各时段地铁乘客数量变化
- **天气影响分析**：天气对城市运行的影响

### 📊 数据洞察（右下）
- **城市活力指数**：综合评估各区县城市活力
- **区县排行榜**：按活力指数排名的区县榜单
- **实时预警信息**：交通管制、活动、天气等预警信息

## 🏗️ 技术架构

### 前端技术栈
- **框架**：Vue 3.5.22
- **构建工具**：Vite 7.1.7
- **UI 组件库**：Element Plus 2.11.7
- **图表库**：ECharts 6.0.0
- **3D 地图**：deck.gl 9.2.2
- **地图服务**：Mapbox GL JS 3.16.0
- **动画库**：GSAP 3.13.0
- **词云组件**：echarts-wordcloud 2.1.0

### 项目结构
```
city-fireworks/
├── public/                 # 静态资源
│   └── data/              # 数据文件
│       ├── alerts.json                    # 预警信息
│       ├── brands.json                     # 火锅品牌
│       ├── CQ.json                         # 重庆市区县数据
│       ├── districts.json                  # 区县详情
│       ├── hotpot_restaurants.json         # 火锅店数据
│       ├── night_economy_realtime.json     # 夜间经济实时数据
│       └── teahouses.json                  # 茶馆数据
├── src/                   # 源代码
│   ├── api/              # API 接口
│   │   └── index.ts
│   ├── components/       # Vue 组件
│   │   └── charts/       # 图表组件
│   │       ├── BrandTree.vue
│   │       ├── ChongqingMap.vue
│   │       ├── CityOperationTrend.vue
│   │       ├── DensityMatrix.vue
│   │       ├── DistrictMerchantTop10.vue
│   │       ├── DistrictRadar.vue
│   │       ├── HotpotRanking.vue
│   │       ├── HourlyTrend.vue
│   │       ├── MetroPassengers.vue
│   │       ├── ParallelAnalysis.vue
│   │       ├── PriceWaterfall.vue
│   │       ├── ShopTypePie.vue
│   │       ├── ShopTypeRatingBox.vue
│   │       ├── TeahouseDistribution.vue
│   │       ├── TeahouseTimeline.vue
│   │       ├── TeahouseWordCloud.vue
│   │       └── TemperatureIndex.vue
│   ├── services/         # 数据服务
│   │   └── DataService.ts
│   ├── types/            # TypeScript 类型定义
│   │   └── index.ts
│   ├── utils/            # 工具函数
│   │   └── dataHelpers.ts
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── .env                  # 环境变量
├── index.html            # HTML 模板
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript 配置
└── vite.config.js        # Vite 配置
```

## 📊 数据模型

### 区县数据 (District)
```typescript
{
  id: number              // 区县 ID
  name: string            // 区县名称
  area_km2: number        // 面积（平方公里）
  hotpot_density: number  // 火锅店密度
  population: number      // 人口数量
  vitality_score: number  // 活力指数
  center_coords: {        // 中心坐标
    lng: number
    lat: number
  }
}
```

### 火锅店数据 (HotpotRestaurant)
```typescript
{
  id: number              // 店铺 ID
  name: string            // 店铺名称
  brand_id: number        // 品牌 ID
  address: string         // 地址
  district_id: number     // 所属区县 ID
  price_min: number       // 最低价
  price_max: number       // 最高价
  price_avg: number       // 平均价
  rating: number          // 评分
  review_count: number    // 评价数
  shop_type: string       // 店铺类型
  business_hours: string  // 营业时间
  is_24h: boolean         // 是否 24 小时营业
  open_date: string       // 开业日期
  status: number          // 营业状态
  coordinates: {          // 坐标
    lng: number
    lat: number
  }
}
```

### 品牌数据 (Brand)
```typescript
{
  id: number              // 品牌 ID
  name: string            // 品牌名称
  market_share: number    // 市场份额
  avg_wait_time: number   // 平均等待时间（分钟）
  store_count: number     // 门店数量
  price_position: string  // 价位定位
  update_date: string     // 更新日期
}
```

### 茶馆数据 (Teahouse)
```typescript
{
  id: number              // 茶馆 ID
  name: string            // 茶馆名称
  address: string         // 地址
  district_id: number     // 所属区县 ID
  founding_year: number   // 创立年份
  tea_type: string        // 茶馆类型
  avg_price: number       // 平均价格
  popularity: number      // 受欢迎程度
  is_historic: boolean    // 是否历史悠久
  community_type: string  // 社区类型
  cultural_tags: string[] // 文化标签
  update_time: string     // 更新时间
  coordinates: {          // 坐标
    lng: number
    lat: number
  }
}
```

### 夜间经济数据 (NightEconomy)
```typescript
{
  id: number              // 数据 ID
  timestamp: string       // 时间戳
  hour: number            // 小时
  district_id: number     // 区县 ID
  population_index: number    // 人口指数
  consumption_heat: number    // 消费热度
  metro_passengers: number    // 地铁乘客数
  active_businesses: number   // 活跃商家数
  weather: string         // 天气
  special_event: string   // 特殊事件
  date: string            // 日期
  time: string            // 时间
}
```

### 预警数据 (Alert)
```typescript
{
  id: number              // 预警 ID
  alert_time: string      // 预警时间
  alert_type: string      // 预警类型
  content: string         // 预警内容
  impact_value: string    // 影响值
  status: number          // 状态
}
```

## 🚀 快速开始

### 环境要求
- Node.js >= 16
- npm >= 7

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### 预览生产版本
```bash
npm run preview
```

## ⚙️ 配置说明

### Mapbox 配置
项目使用 Mapbox 作为底图服务，需要在 `.env` 文件中配置访问令牌：

```env
VITE_MAPBOX_ACCESS_TOKEN=your_mapbox_access_token_here
```

获取访问令牌：https://account.mapbox.com/access-tokens/

## 📁 数据文件说明

所有数据文件位于 `public/data/` 目录下，以 JSON 格式存储：

1. **districts.json** - 38个区县的基础信息
2. **hotpot_restaurants.json** - 约1.6万家火锅店的详细信息
3. **brands.json** - 主要火锅品牌信息
4. **teahouses.json** - 约5000家茶馆信息
5. **night_economy_realtime.json** - 24小时城市运行数据
6. **alerts.json** - 实时预警信息
7. **CQ.json** - 重庆市区县地理边界数据

## 🎨 核心组件

### DataService
数据服务层，单例模式管理所有数据加载和缓存：
- 统一的 JSON 数据加载接口
- 智能缓存机制，避免重复加载
- 数据筛选和聚合功能
- 支持按多种维度查询数据

### 图表组件
位于 `src/components/charts/` 目录，包含20+个专业图表组件：
- 地图可视化
- 雷达图
- 排行榜
- 词云图
- 时间线
- 热力图
- 等

## 🔌 API 设计

项目采用前端直接读取 JSON 文件的方式获取数据，未来可扩展为 RESTful API：

### 地图相关
- `GET /api/map/districts` - 获取区县数据
- `GET /api/map/hotpot-points` - 获取火锅店点位
- `GET /api/map/teahouse-points` - 获取茶馆点位

### 火锅江湖
- `GET /api/hotpot/density-matrix` - 获取火锅店密度矩阵
- `GET /api/hotpot/brand-distribution` - 获取品牌分布
- `GET /api/hotpot/price-distribution` - 获取价格分布

### 茶馆岁月
- `GET /api/teahouse/time-series` - 获取时间序列数据
- `GET /api/teahouse/district-distribution` - 获取区域分布
- `GET /api/teahouse/cultural-tags` - 获取文化标签

### 夜间经济
- `GET /api/night/24-hour-trend` - 获取24小时趋势
- `GET /api/night/district-comparison` - 获取区县对比
- `GET /api/night/metro-passengers` - 获取地铁客流

## 📈 性能优化

1. **数据缓存**：DataService 使用 Map 缓存已加载的数据
2. **按需加载**：图表组件采用懒加载模式
3. **虚拟滚动**：大数据列表使用虚拟滚动优化性能
4. **图片优化**：使用 WebP 格式和懒加载
5. **代码分割**：路由级别的代码分割

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 📄 许可证

MIT License

## 👥 团队

城市数据可视化团队

## 📞 联系方式

如有问题，请通过 Issue 联系我们。

---

**注意**：本项目为演示项目，数据均为模拟数据。实际应用时需要对接真实的数据源。
