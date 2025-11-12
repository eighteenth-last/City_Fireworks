/**
 * 项目常量配置
 */

// 茶色系配色方案
export const TEA_COLORS = {
  primary: '#8d6e63',
  light: '#a1887f',
  dark: '#6d4c41',
  deepDark: '#5d4037',
  accent: '#d32f2f',
  medium: '#795548',
  background: '#fffdf6',
  backgroundAlt: '#f8f4e9',
  border: '#d7ccc8'
}

// 图表默认配置
export const CHART_DEFAULTS = {
  textStyle: {
    color: TEA_COLORS.deepDark,
    fontFamily: 'STKaiti, KaiTi, Microsoft YaHei, sans-serif'
  },
  backgroundColor: 'transparent',
  animation: true,
  animationDuration: 800,
  animationEasing: 'cubicOut'
}

// API 配置
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 10000,
  retryTimes: 3
}

// 缓存配置
export const CACHE_CONFIG = {
  ttl: 5 * 60 * 1000, // 5分钟
  maxSize: 100 // 最多缓存100个请求
}

// 重庆地图边界
export const CHONGQING_BOUNDS = {
  center: [106.55, 29.57],
  zoom: 10,
  minLng: 105.3,
  maxLng: 110.2,
  minLat: 28.2,
  maxLat: 32.2
}

// 数据刷新间隔（毫秒）
export const REFRESH_INTERVALS = {
  realtime: 30 * 1000,    // 实时数据：30秒
  frequent: 5 * 60 * 1000, // 频繁更新：5分钟
  normal: 30 * 60 * 1000,  // 正常更新：30分钟
  rare: 60 * 60 * 1000     // 少量更新：1小时
}
