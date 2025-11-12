/**
 * Flask API 服务
 * 用于调用后端 Flask API 接口
 */

import type {
  District,
  Brand,
  HotpotRestaurant,
  Teahouse,
  NightEconomy,
  Alert,
  CityTemperatureIndex
} from '../types/index.js'

class ApiService {
  private static instance: ApiService
  private baseURL: string
  private cache: Map<string, { data: any; timestamp: number }> = new Map()
  private readonly CACHE_TTL = 5 * 60 * 1000 // 5分钟缓存

  constructor() {
    // 根据环境变量设置 API 基础 URL
    const env = import.meta.env as any
    this.baseURL = env.VITE_API_BASE_URL || 'http://localhost:5000/api'
  }

  static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService()
    }
    return ApiService.instance
  }

  /**
   * 通用 GET 请求方法
   */
  private async get<T>(endpoint: string, useCache = true): Promise<T> {
    const cacheKey = endpoint

    // 检查缓存
    if (useCache && this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey)!
      if (Date.now() - cached.timestamp < this.CACHE_TTL) {
        return cached.data
      }
    }

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`)
      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`)
      }
      const data = await response.json()

      // 更新缓存
      if (useCache) {
        this.cache.set(cacheKey, { data, timestamp: Date.now() })
      }

      return data
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error)
      throw error
    }
  }

  // ==================== 地图相关 API ====================

  async getDistricts(): Promise<District[]> {
    return this.get<District[]>('/map/districts')
  }

  async getDistrictDetail(districtId: number): Promise<District> {
    return this.get<District>(`/map/district/${districtId}`)
  }

  async getHotpotPoints(): Promise<HotpotRestaurant[]> {
    return this.get<HotpotRestaurant[]>('/map/hotpot-points')
  }

  async getTeahousePoints(): Promise<Teahouse[]> {
    return this.get<Teahouse[]>('/map/teahouse-points')
  }

  // ==================== 火锅江湖 API ====================

  async getDensityMatrix(): Promise<Array<{ district: string; density: number; count: number }>> {
    return this.get('/hotpot/density-matrix')
  }

  async getBrandDistribution(): Promise<Brand[]> {
    return this.get<Brand[]>('/hotpot/brand-distribution')
  }

  async getPriceDistribution(): Promise<Array<{ range: string; count: number }>> {
    return this.get('/hotpot/price-distribution')
  }

  async getShopTypeDistribution(): Promise<Array<{ type: string; count: number }>> {
    return this.get('/hotpot/shop-type')
  }

  async getHotpotRanking(): Promise<Array<{ name: string; count: number; rank: number }>> {
    return this.get('/hotpot/ranking')
  }

  // ==================== 夜间经济 API ====================

  async get24HourTrend(): Promise<Array<{ hour: number; population: number; consumption: number }>> {
    return this.get('/night/24hour-trend')
  }

  async getDistrictComparison(): Promise<District[]> {
    return this.get<District[]>('/night/district-comparison')
  }

  async getMetroPassengers(hour: number): Promise<NightEconomy[]> {
    return this.get<NightEconomy[]>(`/night/metro-passengers/${hour}`)
  }

  async getCityOperation(): Promise<any> {
    return this.get('/night/city-operation')
  }

  // ==================== 茶馆岁月 API ====================

  async getTeahouseTimeSeries(): Promise<Array<{ decade: number; count: number }>> {
    return this.get('/teahouse/time-series')
  }

  async getTeahouseDistrictDistribution(): Promise<Array<{ district: string; count: number }>> {
    return this.get('/teahouse/district-distribution')
  }

  async getTeahouseCulturalTags(): Promise<Array<{ tag: string; count: number }>> {
    return this.get('/teahouse/cultural-tags')
  }

  async getTeahouseTimeline(): Promise<Teahouse[]> {
    return this.get<Teahouse[]>('/teahouse/timeline')
  }

  async getTeahouseWordCloud(): Promise<Array<{ tag: string; count: number }>> {
    return this.get('/teahouse/wordcloud')
  }

  // ==================== 数据洞察 API ====================

  async getCityTemperatureIndex(): Promise<CityTemperatureIndex> {
    return this.get<CityTemperatureIndex>('/insight/city-temperature', false) // 不缓存实时数据
  }

  async getDistrictVitalityRanking(): Promise<District[]> {
    return this.get<District[]>('/insight/district-vitality')
  }

  async getActiveAlerts(): Promise<Alert[]> {
    return this.get<Alert[]>('/insight/alerts', false) // 不缓存预警数据
  }

  async getTemperatureDetail(): Promise<CityTemperatureIndex> {
    return this.get<CityTemperatureIndex>('/insight/temperature-detail', false)
  }

  async getRankingDetail(): Promise<District[]> {
    return this.get<District[]>('/insight/ranking-detail')
  }

  // ==================== 工具方法 ====================

  /**
   * 清除所有缓存
   */
  clearCache(): void {
    this.cache.clear()
  }

  /**
   * 清除指定端点的缓存
   */
  clearCacheByEndpoint(endpoint: string): void {
    this.cache.delete(endpoint)
  }

  /**
   * 设置 API 基础 URL
   */
  setBaseURL(url: string): void {
    this.baseURL = url
  }

  /**
   * 获取当前 API 基础 URL
   */
  getBaseURL(): string {
    return this.baseURL
  }
}

export default ApiService
