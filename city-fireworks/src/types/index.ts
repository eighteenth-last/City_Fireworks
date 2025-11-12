// 区县数据类型
export interface District {
  id: number
  name: string
  area_km2: number
  hotpot_density: number
  population: number
  vitality_score: number
  center_coords?: {
    lng: number
    lat: number
  }
  boundary_coords?: number[][]
}

// 火锅品牌类型
export interface Brand {
  id: number
  name: string
  market_share: number
  avg_wait_time: number
  store_count: number
  price_position: string
  update_date: string
}

// 火锅店类型
export interface HotpotRestaurant {
  id: number
  name: string
  brand_id?: number
  address: string
  district_id: number
  price_min: number
  price_max: number
  price_avg: number
  rating: number
  review_count: number
  shop_type: string
  business_hours: string
  is_24h: boolean
  open_date: string
  status: number
  coordinates?: {
    lng: number
    lat: number
  }
}

// 茶馆类型
export interface Teahouse {
  id: number
  name: string
  address: string
  district_id: number
  founding_year: number
  tea_type: string
  avg_price: number
  popularity: number
  is_historic: boolean
  community_type: string
  cultural_tags: string[]
  update_time: string
  coordinates?: {
    lng: number
    lat: number
  }
}

// 夜间经济类型
export interface NightEconomy {
  id: number
  timestamp: string
  hour: number
  district_id: number
  population_index: number
  consumption_heat: number
  metro_passengers: number
  active_businesses: number
  weather: string
  special_event: string
  date?: string
  time?: string
}

// 预警类型
export interface Alert {
  id: number
  alert_time: string
  alert_type: string
  content: string
  impact_value: string
  status: number
}

// 城市温度指数计算结果
export interface CityTemperatureIndex {
  score: number
  date: string
  factors: {
    hotpot_density: number
    night_economy: number
    teahouse_culture: number
    vitality: number
  }
}

// 地图配置
export interface MapConfig {
  center: [number, number]
  zoom: number
  pitch: number
  bearing: number
}

// 图表配置基类
export interface ChartConfig {
  title?: string
  tooltip?: any
  legend?: any
  grid?: any
  [key: string]: any
}
