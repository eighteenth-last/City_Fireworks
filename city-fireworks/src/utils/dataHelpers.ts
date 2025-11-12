// 数值格式化工具
export const formatNumber = (num: number): string => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

// 百分比格式化
export const formatPercent = (num: number): string => {
  return num.toFixed(1) + '%'
}

// 坐标格式化
export const formatCoordinate = (coord: { lng: number, lat: number }): [number, number] => {
  return [coord.lng, coord.lat]
}

// 颜色工具
export const getColorScale = (value: number, max: number, min: number = 0): string => {
  const ratio = (value - min) / (max - min)
  const red = Math.floor(255 * ratio)
  const green = Math.floor(255 * (1 - ratio))
  return `rgb(${red}, ${green}, 100)`
}

// 火锅密度颜色映射
export const getHotpotDensityColor = (density: number): string => {
  if (density < 5) return '#ffd4d4'
  if (density < 10) return '#ff9999'
  if (density < 15) return '#ff6666'
  if (density < 20) return '#ff3333'
  return '#ff0000'
}

// 活力指数颜色映射
export const getVitalityColor = (score: number): string => {
  if (score < 60) return '#9999ff'
  if (score < 70) return '#6699ff'
  if (score < 80) return '#3399ff'
  if (score < 90) return '#0099ff'
  return '#0066cc'
}

// 时间格式化
export const formatTime = (hour: number): string => {
  return `${hour.toString().padStart(2, '0')}:00`
}

// 日期格式化
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 随机ID生成
export const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9)
}

// 数组分组
export const chunk = <T>(array: T[], size: number): T[][] => {
  const chunks: T[][] = []
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size))
  }
  return chunks
}

// 防抖
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// 节流
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}
