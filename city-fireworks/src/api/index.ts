import ApiService from '../services/ApiService'

const apiService = ApiService.getInstance()

/**
 * 统一的 API 接口
 */
export const api = {
  // 地图相关API
  map: {
    getDistrictBoundaries: () => apiService.getDistricts(),
    getHotpotPoints: () => apiService.getHotpotPoints(),
    getTeahousePoints: () => apiService.getTeahousePoints()
  },

  // 火锅江湖（左屏）API
  hotpot: {
    getDensityMatrix: () => apiService.getDensityMatrix(),
    getBrandDistribution: () => apiService.getBrandDistribution(),
    getPriceDistribution: () => apiService.getPriceDistribution(),
    getShopTypeDistribution: () => apiService.getShopTypeDistribution(),
    getRanking: () => apiService.getHotpotRanking()
  },

  // 不夜山城（右上）API
  night: {
    get24HourTrend: () => apiService.get24HourTrend(),
    getDistrictComparison: () => apiService.getDistrictComparison(),
    getMetroPassengers: (hour: number) => apiService.getMetroPassengers(hour),
    getCityOperation: () => apiService.getCityOperation()
  },

  // 茶馆岁月（左下）API
  teahouse: {
    getTimeSeriesData: () => apiService.getTeahouseTimeSeries(),
    getDistrictDistribution: () => apiService.getTeahouseDistrictDistribution(),
    getCulturalTags: () => apiService.getTeahouseCulturalTags(),
    getTimeline: () => apiService.getTeahouseTimeline(),
    getWordCloud: () => apiService.getTeahouseWordCloud()
  },

  // 数据洞察（右下）API
  insight: {
    getCityTemperatureIndex: () => apiService.getCityTemperatureIndex(),
    getDistrictVitalityRanking: () => apiService.getDistrictVitalityRanking(),
    getActiveAlerts: () => apiService.getActiveAlerts(),
    getTemperatureDetail: () => apiService.getTemperatureDetail(),
    getRankingDetail: () => apiService.getRankingDetail()
  },

  // 弹窗详情API
  detail: {
    getRadarDimensionDetail: (dimension: string) => {
      return apiService.getDistricts()
    },
    getLineDetail: (lineId: string) => {
      // 暂时返回空数组，等待后端实现
      return Promise.resolve([])
    },
    getTempDetail: () => {
      return apiService.getTemperatureDetail()
    },
    getAreaDetail: (area: string) => {
      return apiService.getDistricts()
    }
  }
}

export default api
